async def generate_leaderboard(bot, leaderboard, name) -> str:
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