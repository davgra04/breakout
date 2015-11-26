# Modelling my code after https://github.com/Max00355/SpaceInvaders to jump into pygame
import pygame
from pygame.locals import *
import sys
import random
import math

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

    self.ball_radius = 5
    self.ball_pos = [int(self.paddle_pos + self.paddle_size[0]/2), int(self.paddle_height - self.ball_radius)]
    # self.ball_pos = [self.screen_size[0] - 100, 100]
    self.ball_vel = [5, -5]
    self.ball_col = (255, 255, 255)

  def paddle_update(self):
    key = pygame.key.get_pressed()
    if key[K_RIGHT] and self.paddle_pos < self.screen_size[0] - self.paddle_size[0]:
      self.paddle_pos += 5
    elif key[K_LEFT] and self.paddle_pos > 0:
      self.paddle_pos -= 5

  def check_ball_hit(self, newx, newy):

    # Let ball pass through if going up (unlikely)
    if self.ball_vel[1] < 0:
      return

    # Ball is not crossing paddle this frame
    if not (self.ball_pos[1] < self.paddle_height and newy >= self.paddle_height):
      return

    print("BALL CROSSING")

    m = self.ball_vel[1] / self.ball_vel[0]
    b = self.ball_pos[1] - m*self.ball_pos[0]
    x_intersect = (self.paddle_height - b) / m

    if x_intersect > self.paddle_pos and x_intersect < self.paddle_pos + self.paddle_size[0]:

      print("intersect: ({0}, {1})".format(x_intersect, m*x_intersect + self.ball_pos[1] - m*self.ball_pos[0]))

      incx = self.ball_vel[0] / 10
      incy = self.ball_vel[1] / 10

      while newy > self.paddle_height - self.ball_radius:
        newx -= incx
        newy -= incy

      mag = math.sqrt(self.ball_vel[0]**2 + self.ball_vel[1]**2)
      pad_perc = (newx - self.paddle_pos) / self.paddle_size[0]
      angle = -165 + pad_perc*150
      # angle = -30

      self.ball_vel[0] = mag * math.cos(math.radians(angle))
      self.ball_vel[1] = mag * math.sin(math.radians(angle))

      self.ball_pos[0] = int(newx)
      self.ball_pos[1] = int(newy)

  def ball_update(self):
    newx = self.ball_pos[0] + self.ball_vel[0]
    newy = self.ball_pos[1] + self.ball_vel[1]

    self.check_ball_hit(newx, newy)

    # Check for collision with walls
    if (newx < self.ball_radius or newx > self.screen_size[0] - self.ball_radius) and (newy < self.ball_radius or newy > self.screen_size[1] - self.ball_radius):
      incx = self.ball_vel[0] / 10
      incy = self.ball_vel[1] / 10
      
      while newx < 0 or newx > self.screen_size[0] or newy < 0 or newy > self.screen_size[1]:
        newx -= incx
        newy -= incy

      self.ball_vel[0] = -self.ball_vel[0]
      self.ball_vel[1] = -self.ball_vel[1]
    elif newx < self.ball_radius or newx > self.screen_size[0] - self.ball_radius:
      # print(newx)
      incx = self.ball_vel[0] / 10
      incy = self.ball_vel[1] / 10
      
      while newx < 0 or newx > self.screen_size[0] or newy < 0 or newy > self.screen_size[1]:
        newx -= incx
        newy -= incy

      self.ball_vel[0] = -self.ball_vel[0]
    elif newy < self.ball_radius or newy > self.screen_size[1] - self.ball_radius:
      incx = self.ball_vel[0] / 10
      incy = self.ball_vel[1] / 10
      
      while newx < 0 or newx > self.screen_size[0] or newy < 0 or newy > self.screen_size[1]:
        newx -= incx
        newy -= incy

      self.ball_vel[1] = -self.ball_vel[1]


    self.ball_pos[0] = int(newx)
    self.ball_pos[1] = int(newy)

  def run(self):

    clock = pygame.time.Clock()

    while True:

      clock.tick(60)
      self.screen.fill((0, 0, 0))
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit()

      self.paddle_update()
      self.ball_update()

      pygame.draw.rect(self.screen, self.paddle_col, pygame.Rect(self.paddle_pos, self.paddle_height, self.paddle_size[0], self.paddle_size[1]))
      pygame.draw.circle(self.screen, self.ball_col, self.ball_pos, self.ball_radius)

      pygame.display.flip()


if __name__ == "__main__":
  Breakout().run()

