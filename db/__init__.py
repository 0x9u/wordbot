import os
from dotenv import load_dotenv
from supabase import create_client, Client
from utils import canLevelUp

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")

print(SUPABASE_URL, SUPABASE_KEY)


class DB:
    def __init__(self):
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.ratelimit: dict[str, int] = {}

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

    def get_user_ratelimit(self, userId: str) -> int:
        """
        Gets the ratelimit for the given user.

        This function caches the result to avoid repeated database queries.

        Parameters
        ----------
        userId : str
            The id of the user to get the ratelimit for

        Returns
        -------
        int
            The ratelimit for the given user
        """
        
        if userId in self.ratelimit:
            return self.ratelimit[userId]
        
        self.ratelimit[userId] = self.supabase.table("users").select("ratelimit").eq("id", userId).execute().data[0].get("ratelimit")
        return self.ratelimit[userId]

    def invalidate_user_ratelimit(self, userId: str):
        
        """
        Invalidates the cached ratelimit for the given user.

        This function removes the user's ratelimit from the cache,
        forcing the next retrieval to query the database.

        Parameters
        ----------
        userId : str
            The id of the user whose ratelimit cache is to be invalidated
        """
        del self.ratelimit[userId]
    
    def update_user_ratelimit(self, userId: str, ratelimit: int):
        """
        Updates the ratelimit for the given user in the database and caches the result.

        Parameters
        ----------
        userId : str
            The id of the user to update the ratelimit for
        ratelimit : int
            The new ratelimit for the user
        """
        self.supabase.table("users").upsert({"id": userId, "ratelimit": ratelimit}).execute()
        self.ratelimit[userId] = ratelimit
    
    def update_user_coins(self, userId: str, amount: int):
        """
        Updates the coins for the given user in the database.

        Parameters
        ----------
        userId : str
            The id of the user to update the coins for
        coins : int
            The new coins for the user
        """
        coinsData = self.supabase.table("users").select("coins").eq("id", userId).execute()
        coins = coinsData.data[0].get("coins")
        self.supabase.table("users").upsert({"id": userId, "coins": coins + amount }).execute()
    
    def get_user_coins(self, userId: str) -> int:
        """
        Gets the coins for the given user.

        Parameters
        ----------
        userId : str
            The id of the user to get the coins for

        Returns
        -------
        int
            The coins for the given user
        """
        coinsData = self.supabase.table("users").select("coins").eq("id", userId).execute()
        coins = coinsData.data[0].get("coins")
        return coins
    
    def get_user_coins_leaderboard(self) -> list:
        return self.supabase.table("users").select("*").order("coins", desc=True).execute().data

    def get_user_level(self, userId: str) -> int:
        """
        Gets the level for the given user.

        Parameters
        ----------
        userId : str
            The id of the user to get the level for

        Returns
        -------
        int
            The level for the given user
        """
        levelData = self.supabase.table("users").select("level").eq("id", userId).execute()
        level = levelData.data[0].get("level")
        return level
    
    def update_user_xp(self, userId: str, amount: int) -> bool:
        """
        Updates the XP for the given user in the database and checks if they leveled up.

        If the user leveled up, the user's level is incremented and the user's XP is reset to 0.

        Parameters
        ----------
        userId : str
            The id of the user to update the XP for
        amount : int
            The amount of XP to add to the user

        Returns
        -------
        bool
            True if the user leveled up, False if they didn't
        """
        
        xpData = self.supabase.table("users").select("xp").eq("id", userId).execute()
        xp = xpData.data[0].get("xp")
        self.supabase.table("users").upsert({"id": userId, "xp": xp + amount }).execute()
        
        # check if leveled up
        level = self.get_user_level(userId)
        ableToLevelUp = canLevelUp(xp + amount, level)
        if ableToLevelUp:
            self.supabase.table("users").upsert({"id": userId, "level": level + 1}).execute()
            self.supabase.table("users").upsert({"id": userId, "xp": 0}).execute()
        return ableToLevelUp
    
    def get_user_xp(self, userId: str) -> int:
        """
        Gets the current XP for the given user.

        Parameters
        ----------
        userId : str
            The id of the user to get the XP for

        Returns
        -------
        int
            The current XP for the given user
        """
        
        xpData = self.supabase.table("users").select("xp").eq("id", userId).execute()
        xp = xpData.data[0].get("xp")
        return xp
    
        
        
        
        
    

# Global instance baby

db = DB()

__all__ = ["db"]