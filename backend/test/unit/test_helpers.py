# backend/test_helpers.py

from util.helpers import (
    get_employee_level,
    group_employees_by_department,
    create_employee_node,
    build_department_hierarchy
)

def main():
    # Test get_employee_level
    print("Testing get_employee_level:")
    positions = ['MD', 'Finance Director', 'Sales Manager', 'Account Manager', 'Unknown']
    for position in positions:
        level = get_employee_level(position)
        print(f"Position: {position}, Level: {level}")

    # Test group_employees_by_department
    print("\nTesting group_employees_by_department:")
    data = [
        {'Dept': 'Sales', 'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith'},
        {'Dept': 'IT', 'Staff_ID': 2, 'Staff_FName': 'Bob', 'Staff_LName': 'Johnson'},
        {'Dept': 'Sales', 'Staff_ID': 3, 'Staff_FName': 'Carol', 'Staff_LName': 'Williams'}
    ]
    grouped = group_employees_by_department(data)
    print(grouped)

    # Test create_employee_node
    print("\nTesting create_employee_node:")
    employee = {'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith'}
    node = create_employee_node(employee)
    print(node)

    # Test build_department_hierarchy
    print("\nTesting build_department_hierarchy:")
    employees = [
        {'Position': 'MD', 'Staff_ID': 1, 'Staff_FName': 'Alice', 'Staff_LName': 'Smith'},
        {'Position': 'Sales Director', 'Staff_ID': 2, 'Staff_FName': 'Bob', 'Staff_LName': 'Johnson'},
        {'Position': 'Sales Manager', 'Staff_ID': 3, 'Staff_FName': 'Carol', 'Staff_LName': 'Williams'},
        {'Position': 'Account Manager', 'Staff_ID': 4, 'Staff_FName': 'David', 'Staff_LName': 'Brown'},
        {'Position': 'Sales Associate', 'Staff_ID': 5, 'Staff_FName': 'Eve', 'Staff_LName': 'Davis'},
    ]
    hierarchy = build_department_hierarchy(employees)
    print(hierarchy)

if __name__ == "__main__":
    main()
