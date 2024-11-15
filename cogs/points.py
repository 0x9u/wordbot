import discord
from discord.ext import commands
import time
from db import db
from utils import detect_word
from utils import max_xp

# points system

class Points(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.coin_rate = 1
    self.xp_rate = 5
    self.last_msg_time : dict[str, int] = {}
  # TODO: Figure out if multiplier should be calculated on bot side
  # TODO: or stored on the database side
  
  @commands.Cog.listener()
  async def on_message(self, message : discord.Message):
    if message.author.bot:
      return
    
    user_id = str(message.author.id)
    
    new_count = detect_word(message.content)
    
    print(f"{message.author} said: {message.content}")
    
    if new_count > 0:
      db.verify_user(user_id)

      db.update_leaderboard(user_id, new_count)
      db.update_leaderboard_guild(user_id, message.guild.id, new_count)
  
      ratelimit = db.get_user_ratelimit(user_id)
      current_time = time.time()

      if current_time - self.last_msg_time.get(user_id, 0) >= ratelimit:
        self.last_msg_time[user_id] = current_time
        db.update_user_coins(user_id, self.coin_rate)
        if db.update_user_xp(user_id, self.xp_rate):
          await message.channel.send(f"Congrats {message.author.mention}, you leveled up!")
  
  @commands.command(name="count", help="Display the count of the user.")
  async def count(self, ctx, user: discord.User = None):
    if not user:
      user = ctx.author
    user_id = str(user.id)
    db.verify_user(user_id)
    count = db.get_user_word_count(user_id)
    await ctx.send(f"{user.mention}, you have {count}")
  
  @commands.command(name="level", help="Display the level of the user.")
  async def level(self, ctx, user: discord.User = None):
    if not user:
      user = ctx.author
    user_id = str(user.id)
    db.verify_user(user_id)
    level = db.get_user_level(user_id)
    await ctx.send(f"{user.mention}, you are level {level} with {db.get_user_xp(user_id)}/{max_xp(level)} XP.")
  
  @commands.command(name="coins", help="Display the coins of the user.")
  async def coins(self, ctx, user: discord.User = None):
    if not user:
      user = ctx.author
    user_id = str(user.id)
    db.verify_user(user_id)
    coins = db.get_user_coins(user_id)
    await ctx.send(f"{user.mention}, you have {coins} coins.")
  
  @commands.command(name="bank", help="Display the coins of the user's bank.")
  async def bank(self, ctx, user: discord.User = None):
    if not user:
      user = ctx.author
    user_id = str(user.id)
    db.verify_user(user_id)
    coins = db.get_bank_coins(user_id)
    maxCoins = db.get_max_bank_coins(user_id)
    await ctx.send(f"{user.mention}, you have {coins}/{maxCoins} coins in the bank.")
  
  @commands.command(name="balance", help="Display the coins and bank coins of the user.")
  async def balance(self, ctx, user: discord.User = None):
    if not user:
      user = ctx.author
    user_id = str(user.id)
    db.verify_user(user_id)
    coins = db.get_user_coins(user_id)
    bankCoins = db.get_bank_coins(user_id)
    maxBankCoins = db.get_max_bank_coins(user_id)
    await ctx.send(f"{user.mention}, you have {coins} coins and {bankCoins}/{maxBankCoins} coins in the bank.")
  
  @commands.command(name="deposit", help="Deposit coins to the bank.")
  async def deposit(self, ctx, amount: int):
    user_id = str(ctx.author.id)
    db.verify_user(user_id)
    coins = db.get_user_coins(user_id)
    if coins < amount:
      await ctx.send(f"You don't have enough coins to deposit {amount}.")
      return
    maxCoins = db.get_max_bank_coins(user_id)
    if amount > maxCoins:
      await ctx.send(f"You can't deposit more than {maxCoins} coins to the bank.")
      return
    db.update_user_coins(user_id, -amount)
    db.update_bank_coins(user_id, amount)
    await ctx.send(f"Deposited {amount} coins to the bank.")
  
  @commands.command(name="withdraw", help="Withdraw coins from the bank.")
  async def withdraw(self, ctx, amount: int):
    user_id = str(ctx.author.id)
    db.verify_user(user_id)
    coins = db.get_bank_coins(user_id)
    if coins < amount:
      await ctx.send(f"You don't have enough coins in the bank to withdraw {amount}.")
      return
    db.update_bank_coins(user_id, -amount)
    db.update_user_coins(user_id, amount)
    await ctx.send(f"Withdrew {amount} coins from the bank.")
  
  @commands.command(name="transfer", help="Transfer coins to another user.")
  async def transfer(self, ctx, user: discord.User, amount: int):
    user_id = str(ctx.author.id)
    targetId = str(user.id)
    db.verify_user(user_id)
    db.verify_user(targetId)
    coins = db.get_user_coins(user_id)
    if coins < amount:
      await ctx.send(f"You don't have enough coins to transfer {amount}.")
      return
    db.update_user_coins(user_id, -amount)
    db.update_user_coins(targetId, amount)
    await ctx.send(f"Transferred {amount} coins to {user.mention}.")

    
async def setup(bot):
  await bot.add_cog(Points(bot))