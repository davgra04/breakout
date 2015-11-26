# Modelling my code after https://github.com/Max00355/SpaceInvaders to jump into pygame
import pygame
from pygame.locals import *
import sys
import random
import math

class Ball:
  def __init__(self, start_pos, start_vel, radius, color, screen_size, paddle_height):

    self.screen_size = screen_size
    self.paddle_height = paddle_height

    self.pos = start_pos
    self.vel = start_vel
    self.radius = radius
    self.col = color

    self.past_pos = []
    self.past_length = 400
    self.past_interpolate = 10

  def draw(self, screen):
    # Draw Tail
    for p_idx, p in enumerate(self.past_pos):
      if p_idx == len(self.past_pos) - 1:
        nextx = self.pos[0]
        nexty = self.pos[1]
      else:
        nextx = self.past_pos[p_idx + 1][0]
        nexty = self.past_pos[p_idx + 1][1]

      x_diff = nextx - p[0]
      y_diff = nexty - p[1]

      for i in range(self.past_interpolate):
        perc = (p_idx * self.past_interpolate + (self.past_interpolate - i))/(len(self.past_pos) * self.past_interpolate)
        new_col = [90 * perc] * 3

        new_pos = (int(nextx - x_diff * i / self.past_interpolate), int(nexty - y_diff * i / self.past_interpolate))

        pygame.draw.circle(screen, new_col, new_pos, self.radius)
        # if i == 0:
        #   pygame.draw.circle(screen, (255, 0, 0), new_pos, self.radius+5)
          


      # new_col = (255, 0, 0)
      # pygame.draw.circle(screen, new_col, p, self.radius)

    # print(self.past_pos)

    # Draw Ball
    pygame.draw.circle(screen, self.col, self.pos, self.radius)

  def check_ball_hit(self, newx, newy, paddle_pos, paddle_size):

    # Let ball pass through if going up (unlikely)
    # if self.ball_vel[1] < 0:
    if self.vel[1] < 0:
      return

    # Ball is not crossing paddle this frame
    if not (self.pos[1] < self.paddle_height and newy >= self.paddle_height):
      return

    m = self.vel[1] / self.vel[0]
    b = self.pos[1] - m*self.pos[0]
    x_intersect = (self.paddle_height - b) / m

    if x_intersect > paddle_pos and x_intersect < paddle_pos + paddle_size[0]:

      incx = self.vel[0] / 10
      incy = self.vel[1] / 10

      while newy > self.paddle_height - self.radius:
        newx -= incx
        newy -= incy

      mag = math.sqrt(self.vel[0]**2 + self.vel[1]**2)
      pad_perc = (newx - paddle_pos) / paddle_size[0]
      angle = -165 + pad_perc*150
      # angle = -30

      self.vel[0] = mag * math.cos(math.radians(angle))
      self.vel[1] = mag * math.sin(math.radians(angle))

      self.pos[0] = int(newx)
      self.pos[1] = int(newy)

  def update(self, paddle_pos, paddle_size):
    newx = self.pos[0] + self.vel[0]
    newy = self.pos[1] + self.vel[1]

    # self.past_pos.insert(0, self.pos)
    self.past_pos.append([self.pos[0], self.pos[1]])
    if len(self.past_pos) > self.past_length:
      self.past_pos = self.past_pos[1:]

    self.check_ball_hit(newx, newy, paddle_pos, paddle_size)

    # Check for collision with walls
    if (newx < self.radius or newx > self.screen_size[0] - self.radius) and (newy < self.radius or newy > self.screen_size[1] - self.radius):
      incx = self.vel[0] / 10
      incy = self.vel[1] / 10
      
      while newx < self.radius or newx > self.screen_size[0] - self.radius or newy < self.radius or newy > self.screen_size[1] - self.radius:
        newx -= incx
        newy -= incy

      self.vel[0] = -self.vel[0]
      self.vel[1] = -self.vel[1]
    elif newx < self.radius or newx > self.screen_size[0] - self.radius:
      # print(newx)
      incx = self.vel[0] / 10
      incy = self.vel[1] / 10
      
      while newx < self.radius or newx > self.screen_size[0] - self.radius or newy < self.radius or newy > self.screen_size[1] - self.radius:
        newx -= incx
        newy -= incy

      self.vel[0] = -self.vel[0]
    elif newy < self.radius or newy > self.screen_size[1] - self.radius:
      incx = self.vel[0] / 10
      incy = self.vel[1] / 10
      
      while newx < self.radius or newx > self.screen_size[0] - self.radius or newy < self.radius or newy > self.screen_size[1] - self.radius:
        newx -= incx
        newy -= incy

      self.vel[1] = -self.vel[1]

    self.pos[0] = int(newx)
    self.pos[1] = int(newy)

class Breakout:
  def __init__(self):

    pygame.font.init()
    self.font = pygame.font.Font("assets/breakout.ttf", 14)

    self.screen_size = (800, 600)
    self.screen = pygame.display.set_mode(self.screen_size)

    self.paddle_size = (180, 10)
    self.paddle_height = self.screen_size[1] - 80
    self.paddle_pos = self.screen_size[0]/2 - self.paddle_size[0]/2
    self.paddle_col = (0, 40, 255)

    rad = 4
    self.ball = Ball(
      start_pos = [int(self.paddle_pos + self.paddle_size[0]/2), int(self.paddle_height - rad)],
      # start_vel = [50, -50],
      start_vel = [5, -5],
      radius = rad,
      color = (255, 255, 255),
      screen_size = self.screen_size,
      paddle_height = self.paddle_height
    )

  def paddle_update(self):
    key = pygame.key.get_pressed()
    if key[K_RIGHT] and self.paddle_pos < self.screen_size[0] - self.paddle_size[0]:
      self.paddle_pos += 5
    elif key[K_LEFT] and self.paddle_pos > 0:
      self.paddle_pos -= 5

  def run(self):

    clock = pygame.time.Clock()

    while True:

      clock.tick(60)
      self.screen.fill((0, 0, 0))
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit()

      self.paddle_update()
      self.ball.update(self.paddle_pos, self.paddle_size)

      # pygame.draw.circle(self.screen, self.ball_col, self.ball_pos, self.ball_radius)
      self.ball.draw(self.screen)
      pygame.draw.rect(self.screen, self.paddle_col, pygame.Rect(self.paddle_pos, self.paddle_height, self.paddle_size[0], self.paddle_size[1]))

      pygame.display.flip()


if __name__ == "__main__":
  Breakout().run()

