import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import detect.detector as detector
import db.db as db

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
    await message.channel.send(f"Hey {message.author.mention}, you said a racial slur! You have been added to the leaderboard.")

  await bot.process_commands(message)

# command for leaderboard

@bot.command()
async def leaderboard(ctx):
  print("Leaderboard")
  leaderboard = db.get_leaderboard()
  msg = "```\n"  # Start the message with a code block for better alignment
  msg += f"{'Rank':<5} | {'Name':<20} | {'Count':>5}\n"
  msg += "-" * 40 + "\n"  # Add a separator line
  # Loop through each user and format their rank, name, and count
  for i, user in enumerate(leaderboard):
    userData = await bot.fetch_user(user["userId"])
    rank = i + 1
    name = userData.name
    count = user["count"]
    msg += f"{rank:<5} | {name:<20} | {count:>5}\n"  # Adjust columns for alignment

  msg += "```"  # End the message with a code block

  await ctx.send(f"**Leaderboard**\n{msg}")


bot.run(TOKEN)