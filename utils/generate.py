import discord
import asyncio

async def generate_leaderboard_txt(bot, leaderboard, name) -> str:
  """
  Generates a text leaderboard message.

  Parameters
  ----------
  bot : discord.Bot
    The bot to use to fetch user data
  leaderboard : list[dict]
    The leaderboard data, where each entry is a dict with keys "userId" and "count"
  name : str
    The name of the leaderboard

  Returns
  -------
  str
    A text message representing the leaderboard
  """
  msg = f"**{name}**\n```\n"  # Start the message with a code block for better alignment
  msg += f"{'Rank':<5} | {'Name':<45} | {'Count':>5}\n"
  msg += "-" * 65 + "\n"  # Add a separator line
  for i, user in enumerate(leaderboard):
    user_data = await bot.fetch_user(user["user_id"])
    rank = i + 1
    name = user_data.name
    count = user["count"]
    msg += f"{rank:<5} | {name:<45} | {count:>5}\n"  # Adjust columns for alignment
  msg += "```"
  
  return msg


async def generate_leaderboard_embed(bot, leaderboard, name: str, description: str, count_name: str, in_users: bool) -> discord.Embed:
  """
  Generates an embed leaderboard message.

  Parameters
  ----------
  bot : discord.Bot
    The bot to use to fetch user data
  leaderboard : list[dict]
    The leaderboard data, where each entry is a dict with keys "userId" and "count"
  name : str
    The name of the leaderboard

  Returns
  -------
  discord.Embed
    An embed message representing the leaderboard
  """
  embed = discord.Embed(title=name, description=description, color=discord.Color.blue())
  user_ids = [user["id" if in_users else "user_id"] for user in leaderboard]
  users_data = await asyncio.gather(*(bot.fetch_user(user_id) for user_id in user_ids))
  for i, (user, user_data) in enumerate(zip(leaderboard, users_data)):
    rank = i + 1
    name = user_data.name
    count = user[count_name]
    if rank == 1:
      embed.set_author(name=f"{name} is the KING 👑", icon_url=user_data.avatar.url)
    embed.add_field(name=f"{rank}. {name}", value=f"{count_name.capitalize()}: {count}", inline=False)
  return embed

async def generate_global_leaderboard(bot, leaderboard) -> discord.Embed:
  return await generate_leaderboard_embed(bot, leaderboard, 'Global Leaderboard', 'Global Leaderboard', 'count', False)

async def generate_guild_leaderboard(bot, leaderboard, name) -> discord.Embed:
  return await generate_leaderboard_embed(bot, leaderboard, f'{name} Leaderboard', 'Server Leaderboard', 'count', False)

async def generate_coins_leaderboard(bot, leaderboard) -> discord.Embed:
  return await generate_leaderboard_embed(bot, leaderboard, 'Global Rich Leaderboard', 'Mirror mirror on the wall, who is the richest of them all?', 'coins', True)
