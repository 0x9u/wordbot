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

    def verify_user(self, user_id: str) -> bool:
        """
        Verifies that a user exists in the database, adding them if they don't.

        Parameters
        ----------
        user_id : str
            The id of the user to verify

        Returns
        -------
        bool
            True if the user existed in the database, False if they didn't
        """
        # add user to the database if they don't exist
        user = self.supabase.table("users").select(
            "*").eq("id", user_id).execute()
        if len(user.data) == 0:
            self.supabase.table("users").insert({"id": user_id}).execute()
            return False
        return True

    def get_leaderboard(self):
        return self.supabase.table("leaderboard").select("*").order("count", desc=True).execute().data

    def update_leaderboard(self, userId: str, newCount: int):
        countData = self.supabase.table("leaderboard").select(
        """
        Updates the leaderboard with a new entry for the given user.

        If the user already has an entry in the leaderboard, the count is incremented by one.
        If the user doesn't have an entry in the leaderboard, a new entry is created with a count of 1.

        Parameters
        ----------
        userId : str
            The id of the user to update the leaderboard for
        newCount : int
            The number of new racial slurs to add to the leaderboard
        """
            "count").eq("userId", userId).execute()
        count = 0 if len(
            countData.data) == 0 else countData.data[0].get("count")
        self.supabase.table("leaderboard").upsert(
            {"userId": userId, "count": count + newCount}).execute()

    def get_leaderboard_guild(self, guildId: str) -> list:
        """
        Gets the leaderboard for the given guild.

        Parameters
        ----------
        guildId : str
            The id of the guild to get the leaderboard for

        Returns
        -------
        list
            A list of dictionaries containing the leaderboard data for the given guild
        """
        return self.supabase.table("leaderboard_guild").select("*").eq("guildId", guildId).order("count", desc=True).execute().data

    def update_leaderboard_guild(self, userId: str, guildId: str, newCount: int):
        """
        Updates the leaderboard for the given guild with a new entry for the given user.

        If the user already has an entry in the leaderboard for the given guild, the count is incremented by one.
        If the user doesn't have an entry in the leaderboard for the given guild, a new entry is created with a count of 1.

        Parameters
        ----------
        userId : str
            The id of the user to update the leaderboard for
        guildId : str
            The id of the guild to update the leaderboard for
        newCount : int
            The new count to add to the leaderboard entry
        """
        countData = self.supabase.table("leaderboard_guild").select(
            "count").eq("guildId", guildId).eq("userId", userId).execute()
        count = 0 if len(
            countData.data) == 0 else countData.data[0].get("count")
        self.supabase.table("leaderboard_guild").upsert(
            {"guildId": guildId, "userId": userId, "count": count + newCount}).execute()
