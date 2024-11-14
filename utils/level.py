BASE_XP = 1000
GROWTH_RATE = 1.5

def canLevelUp(xp, level):
  return xp > BASE_XP * level * (GROWTH_RATE ** level)
