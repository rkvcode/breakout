# GRAPHICS

RESOLUTIONS = {
	'800x600': {
		'window-width': 800,
		'window-height': 600,
	},
	'1024x768': {
		'window-width': 1024,
		'window-height': 768,
	},
	'1280x720': {
		'window-width': 1280,
		'window-height': 720,
	},
	'1366x768': {
		'window-width': 1366,
		'window-height': 768,
	},
	'1600x900': {
		'window-width': 1600,
		'window-height': 900,
	},
	'1920x1080': {
		'window-width': 1920,
		'window-height': 1080,
	},
	'2560x1440': {
		'window-width': 2560,
		'window-height': 1440,
	},
}

SELECTED_RESOLUTION = RESOLUTIONS['1280x720']

WINDOW_WIDTH = SELECTED_RESOLUTION['window-width']
WINDOW_HEIGHT = SELECTED_RESOLUTION['window-height']
NUM_PIXELS = WINDOW_WIDTH * WINDOW_HEIGHT

SCOREBOARD_WIDTH = WINDOW_WIDTH // 5

GAME_WINDOW_WIDTH = WINDOW_WIDTH - SCOREBOARD_WIDTH
GAME_WINDOW_HEIGHT = WINDOW_HEIGHT

PADDLE_WIDTH = GAME_WINDOW_WIDTH // 5
PADDLE_HEIGHT = WINDOW_HEIGHT // 40

FPS = 60

# Speeds of objects
PADDLE_SPEED_PER_PIXEL = 0.001
BALL_SPEED_PER_PIXEL = 0.0002
POWERUP_SPEED_PER_PIXEL = 0.0005

DEFAULT_PADDLE_SPEED = PADDLE_SPEED_PER_PIXEL * NUM_PIXELS
DEFAULT_BALL_SPEED = BALL_SPEED_PER_PIXEL * NUM_PIXELS
DEFAULT_POWERUP_SPEED = POWERUP_SPEED_PER_PIXEL * NUM_PIXELS

# Levels
BLOCK_MAP = [
	'666666666666',
	'444557755444',
	'333333333333',
	'222222222222',
	'111111111111',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            ',
	'            '
]

COLOR_LEGEND = {
	1: './assets/blocks/1.png',
	2: './assets/blocks/2.png',
	3: './assets/blocks/3.png',
	4: './assets/blocks/4.png',
	5: './assets/blocks/5.png',
	6: './assets/blocks/6.png',
	7: './assets/blocks/7.png'
}

POWER_UP_IMAGES = [
	'./assets/other/heart.png',
	'./assets/other/laser.png',
	'./assets/other/size.png',
	'./assets/other/speed.png'
]

POWERS = [
	('multiply-balls', 1),
	# ('add-life', 0.005),
	# ('big-ball', 0.05),
	# ('small-ball', 0.05),
	# ('fast-ball', 0.03),
	# ('slow-ball', 0.03),
	# ('multiply-balls', 0.05),
	# ('super-ball', 0.05),
	# ('big-paddle', 0.05),
	# ('small-paddle', 0.05)
]

GAP_SIZE = 2
BLOCK_HEIGHT = WINDOW_HEIGHT / len(BLOCK_MAP) - GAP_SIZE
BLOCK_WIDTH = GAME_WINDOW_WIDTH / len(BLOCK_MAP[0]) - GAP_SIZE

MAX_PLAYER_HEALTH = 3
