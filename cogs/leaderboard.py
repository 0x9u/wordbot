from discord.ext import commands
from db import db
from utils.generate import generate_global_leaderboard, generate_guild_leaderboard, generate_coins_leaderboard


class Leaderboard(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name="leaderboard", help="Display the global leaderboard.")
  async def leaderboard(self, ctx):
    print("Leaderboard")
    leaderboard = db.get_leaderboard()
    await ctx.send(embed=await generate_global_leaderboard(self.bot, leaderboard))

  @commands.command(name="leaderboard_guild", help="Display the guild leaderboard.")
  async def leaderboard_guild(self, ctx):
    print("Leaderboard guild")
    leaderboard = db.get_leaderboard_guild(ctx.guild.id)
    await ctx.send(embed=await generate_guild_leaderboard(self.bot, leaderboard, ctx.guild.name))
  
  @commands.command(name="rich", help="Display the coins leaderboard.")
  async def rich(self, ctx):
    print("Rich")
    leaderboard = db.get_user_coins_leaderboard()
    await ctx.send(embed=await generate_coins_leaderboard(self.bot, leaderboard))
    print("Rich done")
  
async def setup(bot):
  await bot.add_cog(Leaderboard(bot))