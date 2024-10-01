# user_controller.py is to fetch data

from config import supabase

# Function to get data from Supabase
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

def get_employees_by_dept_data():
    # Step 1: Query employees from Engineering department
    employee_response = (
        supabase.table('employee')
        .select('*')
        .eq('Dept', 'Engineering')
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

#-----