from util.db import supabase

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

def get_user_by_id(staff_id):
    response = supabase.table('employee').select('*').eq('Staff_ID', staff_id).execute()
    
    if response.data:
        return response.data[0]
    else:
        return None
