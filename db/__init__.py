import os
from dotenv import load_dotenv
from supabase import create_client, Client
from utils import can_level_up

load_dotenv()

SUPABASE_URL: str = os.getenv("SUPABASE_URL")
SUPABASE_KEY: str = os.getenv("SUPABASE_KEY")


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

    def update_leaderboard(self, user_id: str, new_count: int):
        countData = self.supabase.table("leaderboard").select(
            """
        Updates the leaderboard with a new entry for the given user.

        If the user already has an entry in the leaderboard, the count is incremented by one.
        If the user doesn't have an entry in the leaderboard, a new entry is created with a count of 1.

        Parameters
        ----------
        user_id : str
            The id of the user to update the leaderboard for
        new_count : int
            The number of new racial slurs to add to the leaderboard
        """
            "count").eq("user_id", user_id).execute()
        count = 0 if len(
            countData.data) == 0 else countData.data[0].get("count")
        self.supabase.table("leaderboard").upsert(
            {"user_id": user_id, "count": count + new_count}).execute()

    def get_leaderboard_guild(self, guild_id: str) -> list:
        """
        Gets the leaderboard for the given guild.

        Parameters
        ----------
        guild_id : str
            The id of the guild to get the leaderboard for

        Returns
        -------
        list
            A list of dictionaries containing the leaderboard data for the given guild
        """
        return self.supabase.table("leaderboard_guild").select("*").eq("guild_id", guild_id).order("count", desc=True).execute().data

    def update_leaderboard_guild(self, user_id: str, guild_id: str, new_count: int):
        """
        Updates the leaderboard for the given guild with a new entry for the given user.

        If the user already has an entry in the leaderboard for the given guild, the count is incremented by one.
        If the user doesn't have an entry in the leaderboard for the given guild, a new entry is created with a count of 1.

        Parameters
        ----------
        user_id : str
            The id of the user to update the leaderboard for
        guild_id : str
            The id of the guild to update the leaderboard for
        new_count : int
            The new count to add to the leaderboard entry
        """
        countData = self.supabase.table("leaderboard_guild").select(
            "count").eq("guild_id", guild_id).eq("user_id", user_id).execute()
        count = 0 if len(
            countData.data) == 0 else countData.data[0].get("count")
        self.supabase.table("leaderboard_guild").upsert(
            {"guild_id": guild_id, "user_id": user_id, "count": count + new_count}).execute()
    
    def get_user_word_count(self, user_id: str) -> int:
        return self.supabase.table("leaderboard").select("count").eq("user_id", user_id).execute().data[0].get("count")

    def get_user_ratelimit(self, user_id: str) -> int:
        """
        Gets the ratelimit for the given user.

        This function caches the result to avoid repeated database queries.

        Parameters
        ----------
        user_id : str
            The id of the user to get the ratelimit for

        Returns
        -------
        int
            The ratelimit for the given user
        """

        if user_id in self.ratelimit:
            return self.ratelimit[user_id]

        self.ratelimit[user_id] = self.supabase.table("users").select(
            "ratelimit").eq("id", user_id).execute().data[0].get("ratelimit")
        return self.ratelimit[user_id]

    def invalidate_user_ratelimit(self, user_id: str):
        """
        Invalidates the cached ratelimit for the given user.

        This function removes the user's ratelimit from the cache,
        forcing the next retrieval to query the database.

        Parameters
        ----------
        user_id : str
            The id of the user whose ratelimit cache is to be invalidated
        """
        del self.ratelimit[user_id]

    def update_user_ratelimit(self, user_id: str, ratelimit: int):
        """
        Updates the ratelimit for the given user in the database and caches the result.

        Parameters
        ----------
        user_id : str
            The id of the user to update the ratelimit for
        ratelimit : int
            The new ratelimit for the user
        """
        self.supabase.table("users").upsert(
            {"id": user_id, "ratelimit": ratelimit}).execute()
        self.ratelimit[user_id] = ratelimit

    def update_user_coins(self, user_id: str, amount: int):
        """
        Updates the coins for the given user in the database.

        Parameters
        ----------
        user_id : str
            The id of the user to update the coins for
        coins : int
            The new coins for the user
        """
        coins_data = self.supabase.table("users").select(
            "coins").eq("id", user_id).execute()
        coins = coins_data.data[0].get("coins")
        self.supabase.table("users").upsert(
            {"id": user_id, "coins": coins + amount}).execute()

    def get_user_coins(self, user_id: str) -> int:
        """
        Gets the coins for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the coins for

        Returns
        -------
        int
            The coins for the given user
        """
        coins_data = self.supabase.table("users").select(
            "coins").eq("id", user_id).execute()
        coins = coins_data.data[0].get("coins")
        return coins

    def get_user_coins_leaderboard(self) -> list:
        return self.supabase.table("users").select("*").order("coins", desc=True).execute().data

    def get_user_level(self, user_id: str) -> int:
        """
        Gets the level for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the level for

        Returns
        -------
        int
            The level for the given user
        """
        levelData = self.supabase.table("users").select(
            "level").eq("id", user_id).execute()
        level = levelData.data[0].get("level")
        return level

    def update_user_xp(self, user_id: str, amount: int) -> bool:
        """
        Updates the XP for the given user in the database and checks if they leveled up.

        If the user leveled up, the user's level is incremented and the user's XP is reset to 0.

        Parameters
        ----------
        user_id : str
            The id of the user to update the XP for
        amount : int
            The amount of XP to add to the user

        Returns
        -------
        bool
            True if the user leveled up, False if they didn't
        """

        xp_data = self.supabase.table("users").select(
            "xp").eq("id", user_id).execute()
        xp = xp_data.data[0].get("xp")
        self.supabase.table("users").upsert(
            {"id": user_id, "xp": xp + amount}).execute()

        # check if leveled up
        level = self.get_user_level(user_id)
        able_to_level_up = can_level_up(xp + amount, level)
        if able_to_level_up:
            self.supabase.table("users").upsert(
                {"id": user_id, "level": level + 1}).execute()
            self.supabase.table("users").upsert(
                {"id": user_id, "xp": 0}).execute()
        return able_to_level_up

    def get_user_xp(self, user_id: str) -> int:
        """
        Gets the current XP for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the XP for

        Returns
        -------
        int
            The current XP for the given user
        """

        xp_data = self.supabase.table("users").select(
            "xp").eq("id", user_id).execute()
        return xp_data.data[0].get("xp")

    def get_bank_coins(self, user_id: str) -> int:
        """
        Gets the bank coins for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the bank coins for

        Returns
        -------
        int
            The bank coins for the given user
        """
        coins_data = self.supabase.table("users").select(
            "banked_coins").eq("id", user_id).execute()
        return coins_data.data[0].get("banked_coins")

    def update_bank_coins(self, user_id: str, amount: int):
        """
        Updates the bank coins for the given user in the database.

        Parameters
        ----------
        user_id : str
            The id of the user to update the bank coins for
        amount : int
            The new bank coins for the user
        """
        coins_data = self.supabase.table("users").select(
            "banked_coins").eq("id", user_id).execute()
        coins = coins_data.data[0].get("banked_coins")
        self.supabase.table("users").upsert(
            {"id": user_id, "banked_coins": coins + amount}).execute()

    def get_max_bank_coins(self, user_id: str) -> int:
        """
        Gets the max bank coins for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the max bank coins for

        Returns
        -------
        int
            The max bank coins for the given user
        """
        coins_data = self.supabase.table("users").select(
            "max_banked_coins").eq("id", user_id).execute()
        return coins_data.data[0].get("max_banked_coins")

    def update_max_bank_coins(self, user_id: str, amount: int):
        """
        Updates the max bank coins for the given user in the database.

        Parameters
        ----------
        user_id : str
            The id of the user to update the max bank coins for
        amount : int
            The new max bank coins for the user
        """
        coins_data = self.supabase.table("users").select(
            "max_banked_coins").eq("id", user_id).execute()
        coins = coins_data.data[0].get("max_banked_coins")
        self.supabase.table("users").upsert(
            {"id": user_id, "max_banked_coins": coins + amount}).execute()

    def get_items_shop(self):
        """
        Retrieves all items from the items table in the database that have a non-null price.

        Returns
        -------
        list
            A list of dictionaries containing the data for items with a non-null price.
        """
        return self.supabase.table("items").select("*").not_.is_("price", "null").execute().data

    def get_all_items(self):
        """
        Retrieves all items from the items table in the database.

        Returns
        -------
        list
            A list of dictionaries containing the data for all items.
        """
        return self.supabase.table("items").select("*").execute().data
    
    def get_item_shop(self, name : str):
        """
        Retrieves the item from the items table in the database with the given name that has a non-null price.

        Parameters
        ----------
        name : str
            The name of the item to retrieve

        Returns
        -------
        dict
            A dictionary containing the data for the item with the given name and a non-null price
        """
        return self.supabase.table("items").select("*").not_.is_("price", "null").eq("name", name).execute().data

    def get_item(self, name : str):
        """
        Retrieves the item from the items table in the database with the given name.

        Parameters
        ----------
        name : str
            The name of the item to retrieve

        Returns
        -------
        dict
            A dictionary containing the data for the item with the given name
        """
        return self.supabase.table("items").select("*").eq("name", name).execute().data[0]
    
    def get_inventory(self, user_id: str):
        """
        Retrieves the inventory for the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to get the inventory for

        Returns
        -------
        list
            A list of dictionaries containing the inventory data for the given user
        """
        return self.supabase.table("inventory").select("*, items ( name )").eq("user_id", user_id).execute().data

    def add_item_to_inventory(self, user_id: str, item_id: int):
        """
        Adds the given item to the inventory of the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to add the item to
        item_id : int
            The id of the item to add
        """

        self.supabase.table("inventory").insert({"user_id": user_id, "item_id": item_id}).execute()
    
    def remove_item_from_inventory(self, user_id: str, id: int):
        """
        Removes the given item from the inventory of the given user.

        Parameters
        ----------
        user_id : str
            The id of the user to remove the item from
        item_id : int
            The id of the item to remove
        """

        self.supabase.table("inventory").delete().eq("user_id", user_id).eq("id", id).execute()
    
    def get_item_inventory(self, user_id: str, item_name: str):
        return self.supabase.table("inventory_count").select("*, items ( name )").eq("user_id", user_id).eq("name", item_name).execute().data

    def update_item_inventory(self, user_id: str, inventory_id: int, uses_left: int):
        """
        Updates the inventory for a given item of the user with the new number of uses left.

        Parameters
        ----------
        user_id : str
            The id of the user whose inventory is to be updated
        inventory_id : int
            The id of the inventory entry to be updated
        uses_left : int
            The updated number of uses left for the item
        """
        self.supabase.table("inventory_count").update({"user_id": user_id,  "id" : inventory_id, "uses_left": uses_left}).execute()
    
    
# Global instance baby
db = DB()

__all__ = ["db"]
