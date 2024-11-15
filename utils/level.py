BASE_XP = 1000
GROWTH_RATE = 1.5

def can_level_up(xp, level):
  return xp > max_xp(level)

def max_xp(level):
  return BASE_XP * level * (GROWTH_RATE ** level)