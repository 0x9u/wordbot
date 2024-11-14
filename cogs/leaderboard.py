import discord
from discord.ext import commands
import time
from db import db
from utils.generate import generate_leaderboard_embed

class Leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
  
  @commands.command(name="leaderboard")
  async def leaderboard(self, ctx):
    print("Leaderboard")
    leaderboard = db.get_leaderboard()
    await ctx.send(embed=await generate_leaderboard_embed(self.bot, leaderboard, 'Global Leaderboard'))
  
  @commands.command(name="leaderboard_guild")
  async def leaderboard_guild(self, ctx):
    print("Leaderboard guild")
    leaderboard = db.get_leaderboard_guild(ctx.guild.id)
    await ctx.send(embed=await generate_leaderboard_embed(self.bot, leaderboard, 'Server Leaderboard'))
  
async def setup(bot):
  await bot.add_cog(Leaderboard(bot))