import pygame
import settings
import random
import math

from powerup_manager import PowerUpManager
from sprites import Player, Score, Heart, PowerUp, Ball, Block, Scoreboard


class SpriteManager:
	def __init__(self):

		# Sprites groups
		(
			self.all_sprites_group,
			self.block_sprites_group,
			self.player_sprites_group,
			self.ball_sprites_group,
			self.scoreboard_sprites_group,
			self.heart_sprites_group,
			self.power_up_sprites_group,
			self.score_sprites_group
		) = (pygame.sprite.Group() for _ in range(8))

		self.scoreboard = None
		self.score = None
		self.hearts = []
		self.blocks = []
		self.player = None
		self.balls = []
		self.power_ups = []

		self.powerup_manager = PowerUpManager(self)
		self.heart_horizontal_gap = settings.SCOREBOARD_WIDTH // (settings.MAX_PLAYER_HEALTH + 1)

	def create_scoreboard(self):
		scoreboard_image = pygame.image.load('./assets/other/scoreboard.png').convert_alpha()
		scoreboard_image = pygame.transform.scale(
			surface=scoreboard_image,
			size=(settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT)
		)
		scoreboard_rect = scoreboard_image.get_rect(topright=(settings.WINDOW_WIDTH, 0))

		self.scoreboard = Scoreboard(
			self,
			sprite_groups=[self.all_sprites_group, self.scoreboard_sprites_group],
			image=scoreboard_image,
			rect=scoreboard_rect,
		)

	def create_score(self):
		score_color = pygame.Color('white')
		score_font = pygame.font.Font(None, size=36)
		score_image = score_font.render(f'Score: 0', True, score_color)
		score_rect = score_image.get_rect(
			center=(settings.WINDOW_WIDTH - settings.SCOREBOARD_WIDTH // 2, settings.WINDOW_HEIGHT // 4))
		self.score = Score(
			self,
			sprite_groups=[self.all_sprites_group, self.score_sprites_group],
			image=score_image,
			rect=score_rect,
			font=score_font,
			color=score_color
		)

	def create_heart(self, midtop: tuple):
		heart_image = pygame.image.load('./assets/other/heart_s.png').convert_alpha()
		heart_image = pygame.transform.scale(
			surface=heart_image,
			size=(settings.HEART_WIDTH, settings.HEART_HEIGHT)
		)
		heart_rect = heart_image.get_rect(midtop=midtop)
		heart = Heart(
			self,
			sprite_groups=[self.all_sprites_group, self.heart_sprites_group],
			image=heart_image,
			rect=heart_rect
		)
		self.hearts.append(heart)

	def create_block(self, health, x, y):
		block_image = pygame.transform.scale(
			surface=pygame.image.load(settings.COLOR_LEGEND[health]),
			size=(settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT)
		)
		block_rect = block_image.get_rect(topleft=(x, y))
		block = Block(
			self,
			sprite_groups=[self.all_sprites_group, self.block_sprites_group],
			image=block_image,
			rect=block_rect,
			health=health,
		)
		self.blocks.append(block)

	def create_player(self):
		player_image = pygame.Surface(size=(settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
		player_image.fill('white')
		player_rect = player_image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
		self.player = Player(
			self,
			sprite_groups=[self.all_sprites_group, self.player_sprites_group],
			image=player_image,
			rect=player_rect,
		)

	def create_ball(
			self,
			ball_image: [None, pygame.Surface] = None,
			midbottom: [None, bool] = None,
			angle_radians: [None, float] = math.pi / 4,
			speed: [None, int] = settings.DEFAULT_BALL_SPEED,
			**kwargs_to_ball
	):
		if not ball_image:
			ball_image = pygame.image.load('./assets/other/Ball.png').convert_alpha()
		if not midbottom:
			midbottom = self.player.rect.midtop
		ball_rect = ball_image.get_rect(midbottom=midbottom)
		new_ball = Ball(
			sprite_manager=self,
			sprite_groups=[self.all_sprites_group, self.ball_sprites_group],
			image=ball_image,
			rect=ball_rect,
			speed=speed
		)
		new_ball.set_direction_from_angle(angle_radians)

		for key in kwargs_to_ball:
			new_ball.__setattr__(key, kwargs_to_ball[key])

		self.balls.append(new_ball)

	def init_level(self):
		self.create_scoreboard()
		self.create_score()

		for i in range(settings.MAX_PLAYER_HEALTH):
			heart_midtop = (
				settings.GAME_WINDOW_WIDTH + (i + 1) * self.heart_horizontal_gap,
				settings.GAME_WINDOW_HEIGHT // 7
			)
			self.create_heart(midtop=heart_midtop)

		for row_index, row in enumerate(settings.BLOCK_MAP):
			for col_index, health in enumerate(row):
				if health != ' ':
					health = int(health)
					x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
					y = row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2
					self.create_block(health, x, y)

		self.create_player()
		self.create_ball()

	def create_powerup(self, center: tuple, power: str):
		power_up_image = pygame.image.load(random.choice(settings.POWER_UP_IMAGES))
		power_up_rect = power_up_image.get_rect(center=center)
		power_up = PowerUp(
			sprite_manager=self,
			sprite_groups=[self.all_sprites_group, self.power_up_sprites_group],
			image=power_up_image,
			rect=power_up_rect,
			powerup_manager=self.powerup_manager,
			power=power
		)
		self.power_ups.append(power_up)

	def activate_powerup(self, block: Block):
		random_number = random.random()
		potential_powers = []
		for power in settings.POWERS:
			if random_number <= power[1]:
				potential_powers.append(power)
		if len(potential_powers) > 0:
			chosen_power = random.choice(potential_powers)[0]
			self.create_powerup(block.rect.center, chosen_power)

	def update(self, delta_time: float, keys_pressed):
		# update the game
		self.powerup_manager.update()
		self.player.update(delta_time, keys_pressed)
		self.block_sprites_group.update()
		self.ball_sprites_group.update(delta_time, keys_pressed)
		self.heart_sprites_group.update()
		self.power_up_sprites_group.update(delta_time)
		self.score_sprites_group.update()

	def draw_all(self, display_surface):
		self.player_sprites_group.draw(surface=display_surface)
		self.ball_sprites_group.draw(surface=display_surface)
		self.block_sprites_group.draw(surface=display_surface)
		self.scoreboard_sprites_group.draw(surface=display_surface)
		self.heart_sprites_group.draw(surface=display_surface)
		self.power_up_sprites_group.draw(surface=display_surface)
		self.score_sprites_group.draw(surface=display_surface)