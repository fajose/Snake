import pygame
from pygame.locals import *
import time
import random


screen_size = (1000, 600)


class Apple:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        self.int1 = screen_size[0] // 40
        self.int2 = screen_size[1] // 40
        self.image = pygame.image.load("resources/apple.jpg")
        self.x = 600
        self.y = 200

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))

    def move(self):
        self.x = random.randint(0, self.int1 - 1) * 40
        self.y = random.randint(0, self.int2 - 1) * 40


class Snake:
    def __init__(self, parent_screen, length=5):
        self.length = length

        self.parent_screen = parent_screen

        self.block = pygame.image.load("resources/block.jpg")

        self.size = 40

        self.x = [i * self.size for i in range(length)]
        self.y = [40] * length

        self.direction = "right"

    def play_song(self, song):
        sound = pygame.mixer.Sound(f"resources/{song}")
        pygame.mixer.Sound.play(sound)

    def increase_size(self):
        self.length += 1
        self.play_song("ding.mp3")
        self.walk(True)

    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))

    def move_up(self, increase=False):
        if increase:
            self.x = self.x + [self.x[-1]]
            self.y = self.y + [self.y[-1]]
        else:
            self.y[:-1] = self.y[1:]
            self.x[:-1] = self.x[1:]

        self.y[-1] -= self.size

    def move_down(self, increase=False):
        if increase:
            self.x = self.x + [self.x[-1]]
            self.y = self.y + [self.y[-1]]
        else:
            self.y[:-1] = self.y[1:]
            self.x[:-1] = self.x[1:]

        self.y[-1] += self.size

    def move_left(self, increase=False):
        if increase:
            self.x = self.x + [self.x[-1]]
            self.y = self.y + [self.y[-1]]
        else:
            self.y[:-1] = self.y[1:]
            self.x[:-1] = self.x[1:]

        self.x[-1] -= self.size

    def move_right(self, increase=False):
        if increase:
            self.x = self.x + [self.x[-1]]
            self.y = self.y + [self.y[-1]]
        else:
            self.y[:-1] = self.y[1:]
            self.x[:-1] = self.x[1:]

        self.x[-1] += self.size

    def walk(self, increase=False):
        if self.direction == "up":
            self.move_up(increase)
        elif self.direction == "down":
            self.move_down(increase)
        elif self.direction == "left":
            self.move_left(increase)
        elif self.direction == "right":
            self.move_right(increase)

        self.draw()

    def collision_with_body(self):
        if (self.x[-1], self.y[-1]) in zip(self.x[:-1], self.y[:-1]):
            return True
        else:
            return False

    def collision_with_wall(self):
        if self.x[-1] < 0 or self.x[-1] > screen_size[0] - 40:
            return True
        elif self.y[-1] < 0 or self.y[-1] > screen_size[1] - 40:
            return True
        else:
            return False


class Game:
    def __init__(self):
        pygame.init()
        self.surface = pygame.display.set_mode(screen_size)
        self.bg = pygame.image.load("resources/background.jpg").convert()

        self.score = 0
        self.font = pygame.font.SysFont("arial", 30)

        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)

        self.running = True
        self.game_over_state = False

        pygame.mixer.init()
        self.play_background_music()

    def play_background_music(self):
        pygame.mixer.music.load("resources/bg_music_1.mp3")
        pygame.mixer.music.play()

    def play(self):
        self.surface.blit(self.bg, (0, 0))
        self.snake.walk()

        if self.snake.x[-1] == self.apple.x and self.snake.y[-1] == self.apple.y:
            self.snake.increase_size()
            self.score += 1
            self.apple.move()

            while (self.apple.x, self.apple.y) in zip(self.snake.x, self.snake.y):
                self.apple.move()

        self.apple.draw()
        self.display_score()
        pygame.display.flip()

    def display_score(self):
        score_text = self.font.render(f"Score: {self.score}", True, (200, 200, 200))
        self.surface.blit(score_text, (860, 10))

    def game_over(self):
        if not self.game_over_state:
            self.snake.play_song("crash.mp3")

        self.surface.blit(self.bg, (0, 0))

        game_over_font = pygame.font.SysFont("arial", 72)
        text1 = game_over_font.render("GAME OVER!", True, (255, 255, 255))

        text2 = self.font.render(f"FINAL SCORE: {self.score}", True, (255, 255, 255))
        text3 = self.font.render("Press Enter to play again or Escape to Exit", True, (255, 255, 255))

        self.surface.blit(text1, (325, 200))
        self.surface.blit(text2, (410, 350))
        self.surface.blit(text3, (300, 400))

        pygame.display.flip()

        self.game_over_state = True

    def reset(self):
        self.score = 0
        self.snake = Snake(self.surface)
        self.apple = Apple(self.surface)
        self.game_over_state = False

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if self.game_over_state and event.key == K_RETURN:
                        self.reset()
                        break

                    if event.key == K_ESCAPE:
                        self.running = False

                    if not self.game_over_state:
                        if event.key == K_UP:
                            if self.snake.direction != "down":
                                self.snake.direction = "up"
                                break

                        if event.key == K_DOWN:
                            if self.snake.direction != "up":
                                self.snake.direction = "down"
                                break

                        if event.key == K_LEFT:
                            if self.snake.direction != "right":
                                self.snake.direction = "left"
                                break

                        if event.key == K_RIGHT:
                            if self.snake.direction != "left":
                                self.snake.direction = "right"
                                break

                elif event.type == QUIT:
                    self.running = False

            if self.snake.collision_with_body():
                self.game_over()
            elif self.snake.collision_with_wall():
                self.game_over()

            if not self.game_over_state:
                self.play()

            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
