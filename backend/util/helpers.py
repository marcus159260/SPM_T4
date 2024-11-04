def get_employee_level(position):
    position = position.lower()
    if 'md' in position:
        return 1
    elif 'director' in position:
        return 1
    elif 'sales manager' in position:
        return 3
    elif 'finance manager' in position:
        return 3
    else:
        return 2


def group_employees_by_department(data):
    departments = {}
    for employee in data:
        dept_name = employee['Dept']
        if dept_name not in departments:
            departments[dept_name] = []
        departments[dept_name].append(employee)
    return departments

def create_employee_node(employee):
    staff_id = employee['Staff_ID']
    staff_name = f"{employee['Staff_FName']} {employee['Staff_LName']}"
    return {
        'name': staff_name,
        'id': f"E_{staff_id}",
        'expanded': True
    }

def build_department_hierarchy(employees):
    # Map employees by their Staff_ID
    employees_by_id = {emp['Staff_ID']: emp for emp in employees}

    # Identify top-level manager(s) in the department
    top_managers = [emp for emp in employees if get_employee_level(emp['Position']) in [1]]

    if not top_managers:
        print(f"No director or MD found in department {employees[0]['Dept']}")
        return []

    nodes = []
    for top_manager in top_managers:
        def build_level(manager_id):
            nodes = []
            # Get subordinates of the current manager
            subordinates = [
                emp for emp in employees
                if emp.get('Reporting_Manager') == manager_id and emp['Staff_ID'] != emp['Reporting_Manager']
            ]

            # Separate managers and staff
            managers = [emp for emp in subordinates if get_employee_level(emp['Position']) == 3]
            staff_members = [emp for emp in subordinates if get_employee_level(emp['Position']) == 2]

            # Process managers
            for manager in managers:
                node = create_employee_node(manager)
                node['children'] = build_level(manager['Staff_ID'])
                nodes.append(node)

            # Group staff members by Position (team)
            if staff_members:
                teams = {}
                for staff_member in staff_members:
                    position = staff_member['Position']
                    teams.setdefault(position, []).append(staff_member)
                for team_name, team_members in teams.items():
                    team_node = {
                        'name': team_name,
                        'id': f"Team_{team_name}_{manager_id}",
                        'expanded': True,
                        'children': []
                    }
                    for member in team_members:
                        member_node = create_employee_node(member)
                        member_node['children'] = []
                        team_node['children'].append(member_node)
                    nodes.append(team_node)

            return nodes

        top_manager_node = create_employee_node(top_manager)
        top_manager_node['children'] = build_level(top_manager['Staff_ID'])
        nodes.append(top_manager_node)

    return nodes
