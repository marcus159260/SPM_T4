from util.db import supabase

def authenticate_user(staff_id):
    try:
        response = supabase.table('employee').select('*').eq('Staff_ID', staff_id).maybe_single().execute()
        user_data = response.data
    except Exception as e:
        return None
    return {
        'staff_id': user_data['Staff_ID'],
        'role': user_data['Role'],
        'position': user_data['Position'],
        'department': user_data['Dept'],
        'staff_fname': user_data['Staff_FName'],
        'staff_lname': user_data['Staff_LName'],
        'reporting_manager': user_data['Reporting_Manager']
    }