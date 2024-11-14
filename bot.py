import discord
from discord.ext import commands
from dotenv import load_dotenv
import os
import utils
import db
import utils.generate as generate

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print("Ready!")
    await load_cogs()

async def load_cogs():
  for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        await bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(TOKEN)