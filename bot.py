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
bot.remove_command('help')

@bot.event
async def on_ready():
    print("Ready!")

async def load_cogs():
  for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command(name="help", help="Display the help message.")
async def help(ctx, command_name: str = None):
  if command_name:
      command = bot.get_command(command_name)
      if not command:
          await ctx.send(f"No command named `{command_name}` found.")
          return
        
      embed = discord.Embed(
          title=f"Help for `{command.name}`",
          description=command.help or "No description provided.",
          color=discord.Color.blue()
      )
      
      embed.add_field(name="Usage", value=f"`{ctx.prefix}{command.name} {command.signature}`", inline=False)
      await ctx.send(embed=embed)
  else:
      embed = discord.Embed(
          title="SOS BOARD",
          description="This here command lets ya see all the shop items available, folks!",
          color=discord.Color.green()
      )
      
      for cog_name, cog in bot.cogs.items():
          commands_list = cog.get_commands()
          if commands_list:
              command_descriptions = "\n".join([f"`{ctx.prefix}{cmd.name}` - {cmd.help}" for cmd in commands_list])
              embed.add_field(name=cog_name, value=command_descriptions, inline=False)
              
      other_commands = [cmd for cmd in bot.commands if not cmd.cog_name]
      if other_commands:
          command_descriptions = "\n".join([f"`{ctx.prefix}{cmd.name}` - {cmd.help}" for cmd in other_commands])
          embed.add_field(name="Other Commands", value=command_descriptions, inline=False)
      await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Command not found. Please use a valid command!")
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("You are missing a required argument for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Invalid argument. Please check your input and try again.")
    else:
        # Generic error message for unexpected errors
        await ctx.send("An unexpected error occurred. Please try again later.")
        # Log the error for debugging
        print(f"Error occurred: {error}")

async def main():
  async with bot:
    await load_cogs()
    await bot.start(TOKEN)

if __name__ == "__main__":
  import asyncio
  asyncio.run(main())