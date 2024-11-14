import discord
from discord.ext import commands
import time
from db import db
from utils import detect_word

# points system

class Points(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    self.coinRate = 1
    self.xpRate = 5
    self.lastMsgTime : dict[str, int] = {}
  # TODO: Figure out if multiplier should be calculated on bot side
  # TODO: or stored on the database side
  
  @commands.Cog.listener()
  async def on_message(self, message : discord.Message):
    if message.author.bot:
      return
    
    userId = str(message.author.id)
    
    newCount = detect_word(message.content)
    
    print(f"{message.author} said: {message.content}")
    
    if newCount > 0:
      db.verify_user(userId)

      db.update_leaderboard(userId, newCount)
      db.update_leaderboard_guild(userId, message.guild.id, newCount)
  
      ratelimit = db.get_user_ratelimit(userId)
      currentTime = time.time()

      if currentTime - self.lastMsgTime.get(userId, 0) >= ratelimit:
        self.lastMsgTime[userId] = currentTime
        db.update_user_coins(userId, self.coinRate)
        if db.update_user_xp(userId, self.xpRate):
          await message.channel.send(f"Congrats {message.author.mention}, you leveled up!")

  @commands.command(name="level")
  async def level(self, ctx):
    userId = str(ctx.author.id)
    level = db.get_user_level(userId)
    await ctx.send(f"{ctx.author.mention}, you are level {level} with {db.get_user_xp(userId)} XP.")
  
  @commands.command(name="coins")
  async def coins(self, ctx):
    userId = str(ctx.author.id)
    coins = db.get_user_coins(userId)
    await ctx.send(f"{ctx.author.mention}, you have {coins} coins.")
    
    
async def setup(bot):
  await bot.add_cog(Points(bot))