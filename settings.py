# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GOLD = (255, 215, 0)

# Player settings
PLAYER_SPEED = 9
PLAYER_WIDTH = 80  # Adjusted for the spaceship image
PLAYER_HEIGHT = 100  # Adjusted for the spaceship image
PLAYER_COLOR = BLUE
PLAYER_BULLET_SPEED = 10
PLAYER_FIRE_RATE = 300  # milliseconds between shots
PLAYER_AUTO_FIRE_RATE = 450
PLAYER_FIRE_RATE_UPGRADE = 50  # decrease by this amount for upgrade
PLAYER_POWER_UP_DURATION = 8000 # milliseconds

# Enemy settings
ENEMY_RADIUS = 15
ENEMY_COLOR = RED
ENEMY_SPEED = 3
ENEMY_SPAWN_DELAY = 1000  # milliseconds between enemy spawns
ENEMY_GROUP_SIZE = 5
ENEMY_HEALTH = 3

# AI enemy settings
AI_ENEMY_RADIUS = 20
AI_ENEMY_COLOR = PURPLE
AI_ENEMY_SPEED = 2
AI_ENEMY_HEALTH = 5  # Increased health to make them more challenging
AI_DECISION_TIME = 500  # milliseconds between AI decisions
AI_SPAWN_AFTER_GROUPS = 3  # Spawn AI after this many normal enemy groups

# Castle settings
CASTLE_WIDTH = 600
CASTLE_HEIGHT = 30
CASTLE_COLOR = GOLD
CASTLE_STARTING_HEALTH = 30

# Bullet settings
BULLET_RADIUS = 5
BULLET_COLOR = GREEN
BULLET_DAMAGE = 1

# Game settings
AI_KILLS_FOR_UPGRADE = 3  # Number of AI kills needed for player upgrade
NORMAL_ENEMY_SCORE = 5
AI_ENEMY_SCORE = 10
NORMAL_ENEMY_DAMAGE = 1
AI_ENEMY_DAMAGE = 3

# Sound settings
SOUND_ENABLED = True
MUSIC_VOLUME = 0.2
SOUND_VOLUME = 0.3