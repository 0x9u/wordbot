import discord
from discord.ext import commands
from db import db
from enum import Enum

class Item(Enum):
  pass  


class Shop(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name="shop", help="Display the shop.")
  async def shop(self, ctx):
    embed = discord.Embed(
      title ="Shop",
      description="Get ya stuff here!",
    )
    for item in db.get_items_shop():
      level_require_string = f"\nRequires level {item['level_require']}" if item["level_require"] and item["level_require"] > 0 else ""
      embed.add_field(name=f"{item["name"]} - {item['price']} coins", value=f"Description: {item['description']}{ level_require_string }", inline=False)
      
    await ctx.send(embed=embed)
  
  @commands.command(name="buy", help="Buy an item from the shop.")
  async def buy(self, ctx, item_name: str):
    try:
      item_name = item_name.capitalize()
      item = db.get_item_shop(item_name)
      if not item:
        await ctx.send(f"Item {item_name} not found in the shop.")
        return
      
      item = item[0]

      user_id = str(ctx.author.id)
      user_coins = db.get_user_coins(user_id)
      if user_coins < item["price"]:
        await ctx.send(f"You don't have enough coins to buy {item_name}.")
        return

      db.update_user_coins(user_id, -item["price"])
      print('bought')
      db.add_item_to_inventory(user_id, item["id"])
      await ctx.send(f"You bought {item_name}.")
    except Exception as e:
      print(e)
  
  @commands.command(name="inventory", help="Display the user's inventory.")
  async def inventory(self, ctx):
    try:
      user_id = str(ctx.author.id)
      inventory = db.get_inventory(user_id)
      if not inventory:
        await ctx.send(f"You have no items in your inventory.")
        return

      embed = discord.Embed(
        title="Inventory",
        description=f"{ctx.author.mention}'s inventory:",
      )
      
      print("WHAT")

      for item in inventory:
        print(item)
        embed.add_field(name=item["items"]["name"], value=f"Uses left: {item['uses_left']}", inline=False)
      
      print("SHIT")

      await ctx.send(embed=embed)
    except Exception as e:
      print(e)
  
  # TODO: handle use
  @commands.command(name="use", help="Use an item from the inventory.")
  async def use(self, ctx, item_name: str):
    user_id = str(ctx.author.id)
    inventory = db.get_inventory(user_id)
    if not inventory:
      await ctx.send(f"You have no items in your inventory.")
      return
    
    item = db.get_item_inventory(user_id, item_name)
    if not item:
      await ctx.send(f"Item {item_name} not found in your inventory.")
      return
    
    uses_left = item["uses_left"] - 1
    if uses_left <= 0:
      db.remove_item_from_inventory(user_id, item["id"])
    else:
      db.update_item_inventory(user_id, item["id"], uses_left)
    
    await ctx.send(f"You used {item_name}.")

# TODO: put inventory stuff in its own module

async def setup(bot):
  await bot.add_cog(Shop(bot))