import pygame
import sys
import time
import settings

from sprites import Player, Ball, Scoreboard, Block


def create_bg():
    bg_original = pygame.image.load('./assets/background/background.jpg').convert()
    scale_factor = settings.WINDOW_HEIGHT / bg_original.get_height()
    scaled_width = bg_original.get_width() * scale_factor
    scaled_height = bg_original.get_height() * scale_factor
    scaled_bg = pygame.transform.scale(bg_original, (scaled_width, scaled_height))
    return scaled_bg


class Game:
    def __init__(self):
        
        # general setup
        pygame.init()
        self.display_surface = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption('Breakout Game')

        # background
        self.bg = create_bg()

        # sprites group setup
        self.all_sprites = pygame.sprite.Group()
        self.block_sprites = pygame.sprite.Group()
        self.ball_sprites = pygame.sprite.Group()

        # initialise_game
        self.player: Player = self.player_setup()
        self.blocks: list[Block] = self.blocks_setup()
        self.balls: list[Ball] = self.balls_setup(self.player)
        self.scoreboard: Scoreboard = self.scoreboard_setup()

    def player_setup(self) -> Player:
        player_image = pygame.Surface(size=(settings.PADDLE_WIDTH, settings.PADDLE_HEIGHT))
        player_image.fill('white')
        player_rect = player_image.get_rect(midbottom=(settings.GAME_WINDOW_WIDTH // 2, settings.WINDOW_HEIGHT - 20))
        return Player(
            groups=self.all_sprites,
            image=player_image,
            rect=player_rect
        )

    def blocks_setup(self) -> list[Block]:
        # cycle through all rows and columns of BLOCK_MAP
        blocks = []
        for row_index, row in enumerate(settings.BLOCK_MAP):
            for col_index, health in enumerate(row):
                if health != ' ':
                    health = int(health)
                    # find the x and y position for each individual block
                    x = col_index * (settings.BLOCK_WIDTH + settings.GAP_SIZE) + settings.GAP_SIZE // 2
                    y = row_index * (settings.BLOCK_HEIGHT + settings.GAP_SIZE) + settings.GAP_SIZE // 2

                    block_image = pygame.Surface(size=(settings.BLOCK_WIDTH, settings.BLOCK_HEIGHT))
                    block_image.fill(color=settings.COLOR_LEGEND[health])

                    block_rect = block_image.get_rect(topleft=(x, y))
                    blocks.append(
                        Block(
                            groups=[self.all_sprites, self.block_sprites],
                            image=block_image,
                            rect=block_rect,
                            health=health
                        )
                    )
        return blocks

    def balls_setup(self, player):
        ball_image = pygame.image.load('./assets/other/Ball.png').convert_alpha()
        balls = [
            Ball(
                groups=[self.all_sprites, self.ball_sprites],
                image=ball_image,
                rect=ball_image.get_rect(midbottom=player.rect.midtop),
                player=player,
                blocks=self.block_sprites
            )
        ]
        return balls

    def scoreboard_setup(self):
        scoreboard_image = pygame.image.load('assets/other/scoreboard.jpg').convert_alpha()
        scoreboard_image = pygame.transform.scale(
            scoreboard_image,
            (settings.SCOREBOARD_WIDTH, settings.WINDOW_HEIGHT)
        )
        scoreboard_rect = scoreboard_image.get_rect(topright=(settings.WINDOW_WIDTH, 0))
        return Scoreboard(
            groups=self.all_sprites,
            image=scoreboard_image,
            rect=scoreboard_rect
        )

    def run(self):
        last_time = time.time()

        clock = pygame.time.Clock()
        while True:
            delta_time = clock.tick_busy_loop(settings.FPS) / 1000
            fps = clock.get_fps()

            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys_pressed = pygame.key.get_pressed()

            # update the game
            self.player.update(delta_time, keys_pressed)
            self.block_sprites.update()
            self.ball_sprites.update(delta_time, keys_pressed)

            # draw the frame
            self.display_surface.blit(source=self.bg, dest=(0, 0))
            self.all_sprites.draw(surface=self.display_surface)
            

            # update window
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
