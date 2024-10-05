from util.db import supabase
def get_staff_requests_data(user_id):
    response = supabase.table('request').select('*').eq('Staff_ID', user_id).execute()
    if response.data:
        return response.data
    else:
        return None