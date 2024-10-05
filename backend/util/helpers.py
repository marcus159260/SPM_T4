
POSITION_LEVELS = {
    "md": 1,
    "finance director": 2,
    "sales director": 2,
    "finance manager": 3,
    "sales manager": 3,
}

def get_employee_level(position):
    position = position.lower()
    return POSITION_LEVELS.get(position, 4)  # Default to Staff level

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
    employees_by_level = {
        1: [],  # MDs
        2: [],  # Directors
        3: [],  # Managers
        4: []   # Staff
    }

    for employee in employees:
        level = get_employee_level(employee['Position'])
        employees_by_level[level].append(employee)

    # Build the hierarchy recursively
    def build_level(level):
        nodes = []
        for employee in employees_by_level.get(level, []):
            node = create_employee_node(employee)
            # Build subordinates at the next level
            if level < 4:
                subordinates = build_level(level + 1)
                node['children'] = subordinates
            else:
                node['children'] = []
            nodes.append(node)
        return nodes

    # Start building from the highest level present
    for level in range(1, 5):
        if employees_by_level.get(level):
            return build_level(level)

    return []
