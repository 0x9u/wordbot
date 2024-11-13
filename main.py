import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import detect.detector as detector
import db.db as db
import helpers.generate as generate

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

db = db.DB()

@bot.event
async def on_ready():
    print("Ready!")


@bot.event
async def on_message(message: discord.Message) -> None:
  if message.author == bot.user:
    return
 
  print(f"{message.author} said: {message.content}")
  
  newCount = detector.detect_word(message.content)
  # remove accents from the message
  if newCount > 0:
    db.verify_user(message.author.id)
    db.update_leaderboard(message.author.id, newCount)
    db.update_leaderboard_guild(message.author.id, message.guild.id, newCount)
    #await message.channel.send(f"Hey {message.author.mention}, you said a racial slur! You have been added to the leaderboard.")

  await bot.process_commands(message)

# command for leaderboard

@bot.command()
async def leaderboard(ctx):
  print("Leaderboard")
  leaderboard = db.get_leaderboard()
  await ctx.send(await generate.generate_leaderboard(bot, leaderboard, 'Global Leaderboard'))

@bot.command()
async def leaderboard_guild(ctx):
  print("Leaderboard guild")
  leaderboard = db.get_leaderboard_guild(ctx.guild.id)
  await ctx.send(await generate.generate_leaderboard(bot, leaderboard, 'Server Leaderboard'))


bot.run(TOKEN)