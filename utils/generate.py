import discord

async def generate_leaderboard_txt(bot, leaderboard, name) -> str:
  msg = f"**{name}**\n```\n"  # Start the message with a code block for better alignment
  msg += f"{'Rank':<5} | {'Name':<45} | {'Count':>5}\n"
  msg += "-" * 65 + "\n"  # Add a separator line
  for i, user in enumerate(leaderboard):
    userData = await bot.fetch_user(user["userId"])
    rank = i + 1
    name = userData.name
    count = user["count"]
    msg += f"{rank:<5} | {name:<45} | {count:>5}\n"  # Adjust columns for alignment
  msg += "```"
  
  return msg


async def generate_leaderboard_embed(bot, leaderboard, name) -> discord.Embed:
  embed = discord.Embed(title=name, description="Leaderboard", color=discord.Color.blue())
  for i, user in enumerate(leaderboard):
    userData = await bot.fetch_user(user["userId"])
    rank = i + 1
    name = userData.name
    count = user["count"]
    if rank == 1:
      embed.set_author(name=f"{name} is the KING 👑", icon_url=userData.avatar.url)
    embed.add_field(name=f"{rank}. {name}", value=f"Count: {count}", inline=False)
  return embed