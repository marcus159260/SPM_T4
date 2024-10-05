from util.db import supabase

# Get all the requests from a specific user id (staff)
def get_staff_requests_data(user_id):
    response = (supabase.table('request').select('*').eq('Staff_ID', user_id).execute())
    if response.data:
        return response.data
        return result
    else:
        return None
    

