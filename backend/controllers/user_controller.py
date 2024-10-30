from util.db import supabase
from util.helpers import (
    group_employees_by_department,
    build_department_hierarchy,
)
from datetime import datetime, timedelta

def get_all_users_names():
    response = supabase.table('employee').select('Staff_ID, Staff_FName, Staff_LName').execute()
    full_names = [
        {
            'Staff_ID': row['Staff_ID'],
            'Full_Name': f"{row['Staff_FName']} {row['Staff_LName']}"
        }
        for row in response.data
    ]
    return full_names

def get_all_users_data():
    response = supabase.table('employee').select('*').execute()
    return response.data

# Function to get a specific user by ID
def get_user_data_by_id(user_id):
    response = supabase.table('employee').select('*').eq('Staff_ID', user_id).execute() #eq is filter
    if response.data:
        return response.data[0]
    else:
        return None
    
  
def get_manager_details_data(manager_id: int):
    # Query to get manager details by Staff_ID (which is manager_id)
    response = (
        supabase.table('employee')
        .select('Staff_ID, Staff_FName, Staff_LName, Dept, Position, Country')
        .eq('Staff_ID', manager_id)
        .execute()
    )
    
    if response.data:
        # Return the first result (since Staff_ID is unique)
        manager_data = response.data[0]
        
        # Query to get all employees reporting to this manager
        reporting_response = (
            supabase.table('employee')
            .select('Dept, Position, Country')
            .eq('Reporting_Manager', manager_id)  # Assuming 'Reporting_Manager' is the correct column
            .execute()
        )
        
        # Prepare in-charge-of details as a set to ensure uniqueness
        in_charge_of_combinations = set()  # Use a set to avoid duplicates
        if reporting_response.data:
            for employee in reporting_response.data:
                combination = f"{employee['Dept']} - {employee['Position']} - {employee['Country']}"
                in_charge_of_combinations.add(combination)  # Add combination to set
        
        # Convert the set to a list of lists
        in_charge_of_list = [[combination] for combination in in_charge_of_combinations]

        return {
            'Staff_ID': manager_data['Staff_ID'],
            'Full_Name': f"{manager_data['Staff_FName']} {manager_data['Staff_LName']}",
            'Department': manager_data['Dept'],
            'Position': manager_data['Position'],
            'Country': manager_data['Country'],
            'In_Charge_Of': in_charge_of_list  # Store as a list of lists
        }
    else:
        return None


def get_employees_by_dept_data():
    # Step 1: Query employees from Engineering department and Call Centre Position
    employee_response = (
        supabase.table('employee')
        .select('*')
        .eq('Dept', 'Engineering')
        .eq('Position', 'Call Centre')
        .execute()
    )
    
    employees = employee_response.data if employee_response.data else []
    
    # Step 2: Get all managers for the reporting manager ID
    # Extract unique Reporting_Manager IDs from employee list
    reporting_manager_ids = list(set(emp['Reporting_Manager'] for emp in employees))
    
    if reporting_manager_ids:
        # Query to get all reporting managers by their Staff_ID
        managers_response = (
            supabase.table('employee')
            .select('Staff_ID, Staff_FName, Staff_LName')
            .in_('Staff_ID', reporting_manager_ids)
            .execute()
        )
        
        managers = managers_response.data if managers_response.data else []
        
        # Step 3: Merge employees and managers by Reporting_Manager ID
        manager_dict = {manager['Staff_ID']: f"{manager['Staff_FName']} {manager['Staff_LName']}" for manager in managers}
        
        # Add manager name to each employee
        for employee in employees:
            manager_id = employee.get('Reporting_Manager')
            employee['Manager_Name'] = manager_dict.get(manager_id, 'No Manager')

    return employees

def get_resources():
    try:
        response = supabase.table('employee').select(
            'Dept',
            'Position',
            'Staff_ID',
            'Staff_FName',
            'Staff_LName',
            'Reporting_Manager'
        ).execute()
        data = response.data
    except Exception as e:
        print(f"Error fetching employee data: {e}")
        return None

    resources = build_resource_tree(data)
    return resources

def build_resource_tree(data):
    departments = group_employees_by_department(data)
    resources = []
    
    for dept_name, employees in departments.items():
        dept_node = {
            'name': dept_name,
            'id': f"D_{dept_name}",
            'expanded': True,
            'children': build_department_hierarchy(employees)
        }
        resources.append(dept_node)
    return resources

# get team members (same reporting manager)
def get_employees_by_reporting_manager(reporting_manager_id:int):
    # reporting_manager_id = 140894

    # Query the employee table for employees with the specified Reporting_Manager
    team_response = (
        supabase.table('employee')
        .select('*')
        .eq('Reporting_Manager', reporting_manager_id)
        .execute()
    )

    manager_response = (supabase.table("employee").select("*").eq("Staff_ID", reporting_manager_id).execute())

   
    # Return the list of employees
    # print(str(team_response.data))
    return team_response.data+ manager_response.data

def get_department_wfh_wfo_counts(start_date=None, end_date=None):
    try:
        start_date, end_date = set_default_date_range(start_date, end_date)

        employees = fetch_all_employees()

        departments = build_departments_mapping(employees)

        requests = fetch_approved_wfh_requests(start_date, end_date)

        process_wfh_requests(requests, employees, departments, start_date, end_date)

        result = calculate_department_counts(departments)

        return result

    except Exception as e:
        print(f"Error calculating department counts: {e}")
        return None

def set_default_date_range(start_date, end_date):
    """
    Sets the default date range to the current week if not provided.
    """
    if not start_date:
        today = datetime.today()
        start_date = today - timedelta(days=today.weekday())  # Start of the week (Monday)
    else:
        start_date = datetime.strptime(start_date, '%Y-%m-%d')

    if not end_date:
        end_date = start_date + timedelta(days=6)  # End of the week (Sunday)
    else:
        end_date = datetime.strptime(end_date, '%Y-%m-%d')

    return start_date, end_date

def fetch_all_employees():
    """
    Fetches all employees from the 'employee' table.
    """
    employee_response = supabase.table('employee').select(
        'Dept',
        'Staff_ID'
    ).execute()
    employees = employee_response.data
    return employees

def build_departments_mapping(employees):
    """
    Builds a mapping of departments to their total employee count and initializes WFH sets.
    """
    departments = {}
    for employee in employees:
        dept_name = employee['Dept']
        staff_id = employee['Staff_ID']
        departments.setdefault(dept_name, {'total': 0, 'wfh': set()})
        departments[dept_name]['total'] += 1
    return departments

def fetch_approved_wfh_requests(start_date, end_date):
    """
    Fetches approved WFH requests within the specified date range.
    """
    # Convert dates to strings for the query
    start_date_str = start_date.strftime('%Y-%m-%d')
    end_date_str = end_date.strftime('%Y-%m-%d')

    request_response = supabase.table('request').select(
        'Staff_ID',
        'Start_Date',
        'End_Date',
        'Status'
    ).eq('Status', 'Approved').execute()
    requests = request_response.data
    return requests

def process_wfh_requests(requests, employees, departments, start_date, end_date):
    """
    Processes WFH requests and updates the departments' WFH staff sets.
    """
    for request in requests:
        req_start_date = datetime.strptime(request['Start_Date'], '%Y-%m-%d')
        req_end_date = datetime.strptime(request['End_Date'], '%Y-%m-%d')

        # Check if the request overlaps with the specified date range
        if req_end_date >= start_date and req_start_date <= end_date:
            staff_id = request['Staff_ID']
            # Find the department of the staff member
            staff_dept = next((emp['Dept'] for emp in employees if emp['Staff_ID'] == staff_id), None)
            if staff_dept and staff_dept in departments:
                departments[staff_dept]['wfh'].add(staff_id)

def calculate_department_counts(departments):
    """
    Calculates WFO counts and prepares the result list.
    """
    result = []
    for dept_name, data in departments.items():
        wfh_count = len(data['wfh'])
        total_count = data['total']
        wfo_count = total_count - wfh_count
        result.append({
            'department': dept_name,
            'wfh_count': wfh_count,
            'wfo_count': wfo_count
        })
    return result
