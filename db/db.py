import os
from dotenv import load_dotenv
from supabase import create_client, Client

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

print(SUPABASE_URL, SUPABASE_KEY)


class DB:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        
    def get_leaderboard(self):
        return self.supabase.table("leaderboard").select("*").order("count", desc=True).execute().data
    
    def verify_user(self, user_id: str) -> bool:
        """ 
        Checks if the given user_id exists in the users table and adds it if it doesn't.

        If the user doesn't exist, the function will return False, otherwise it will return True.

        Parameters
        ----------
        user_id : str
            The id of the user to verify

        Returns
        -------
        bool
            True if the user exists, False if it doesn't
        """
        
        # add user to the database if they don't exist
        user = self.supabase.table("users").select("*").eq("id", user_id).execute()
        if len(user.data) == 0:
            self.supabase.table("users").insert({"id": user_id}).execute()
            return False
        return True
    
    def update_leaderboard(self, userId, newCount):
        """
        Updates the leaderboard with a new entry for the given user.

        If the user already has an entry in the leaderboard, the count is incremented by one.
        If the user doesn't have an entry in the leaderboard, a new entry is created with a count of 1.

        Parameters
        ----------
        userId : str
            The id of the user to update the leaderboard for
        """
        countData = self.supabase.table("leaderboard").select("count").eq("userId", userId).execute()
        count = 0 if len(countData.data) == 0 else countData.data[0].get("count")
        self.supabase.table("leaderboard").upsert({"userId": userId, "count": count + newCount}).execute()
        
        
