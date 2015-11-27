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

    self.sprite = pygame.image.load("assets/ball.png").convert_alpha()
    self.rect = pygame.Rect((self.pos[0] - self.radius, self.pos[1] - self.radius), (self.radius*2, self.radius*2))

    self.past_pos = []
    self.past_length = 100
    self.past_interpolate = 10

    self.inc_factor = 100

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
        new_col = [30 * perc] * 3

        new_pos = (int(nextx - x_diff * i / self.past_interpolate), int(nexty - y_diff * i / self.past_interpolate))

        pygame.draw.circle(screen, new_col, new_pos, self.radius)
        # if i == 0:
        #   pygame.draw.circle(screen, (255, 0, 0), new_pos, self.radius*2)
          
    # Draw Ball
    screen.blit(pygame.transform.scale(self.sprite, (self.radius*2, self.radius*2)), (self.pos[0] - self.radius, self.pos[1] - self.radius))



class Breakout:
  def __init__(self):

    pygame.font.init()
    self.font = pygame.font.Font("assets/breakout.ttf", 14)

    self.screen_size = (800, 600)
    self.screen = pygame.display.set_mode(self.screen_size)

    self.paddle_size = (180, 10)
    self.paddle_height = self.screen_size[1] - 80
    self.paddle_pos = self.screen_size[0]/2 - self.paddle_size[0]/2
    self.paddle_rect = pygame.Rect((self.paddle_pos, self.paddle_height), self.paddle_size)
    self.paddle_col = (0, 40, 255)
    self.paddle_speed = 15

    # rand_angle = random.randrange(0, 360)
    rand_angle = -45
    velocity = 20

    rad = 10
    self.ball = Ball(
      start_pos = [self.screen_size[0]/2, self.screen_size[1]/2],
      # start_pos = [int(self.paddle_pos + self.paddle_size[0]/2), int(self.paddle_height - rad)],
      # start_vel = [100, -100],
      start_vel = [velocity * math.cos(math.radians(rand_angle)), velocity * math.sin(math.radians(rand_angle))],
      # start_vel = [5, -5],
      radius = rad,
      color = (255, 255, 255),
      screen_size = self.screen_size,
      paddle_height = self.paddle_height
    )


  def paddle_update(self):
    key = pygame.key.get_pressed()
    if key[K_RIGHT] and self.paddle_pos < self.screen_size[0] - self.paddle_size[0]:
      self.paddle_pos += self.paddle_speed
      self.paddle_rect.move_ip(self.paddle_speed, 0)
    elif key[K_LEFT] and self.paddle_pos > 0:
      self.paddle_pos -= self.paddle_speed
      self.paddle_rect.move_ip(-self.paddle_speed, 0)



  def check_ball_paddle_hit(self, newx, newy):

    new_rect = Rect(self.ball.rect)
    new_rect.x = newx - self.ball.radius
    new_rect.y = newy - self.ball.radius

    # print("{0:20s}{1:20}{2:20}".format(str(self.paddle_rect), self.paddle_pos, self.paddle_height))

    if new_rect.colliderect(self.paddle_rect):

      incx = self.ball.vel[0] / self.ball.inc_factor
      incy = self.ball.vel[1] / self.ball.inc_factor
      while new_rect.colliderect(self.paddle_rect):
        newx -= incx
        newy -= incy
        new_rect.x = newx - self.ball.radius
        new_rect.y = newy - self.ball.radius

      newx = new_rect.x + self.ball.radius
      newy = new_rect.y + self.ball.radius
     
      if new_rect.bottom == self.paddle_rect.top:
        mag = math.sqrt(self.ball.vel[0]**2 + self.ball.vel[1]**2)
        pad_perc = (newx - self.paddle_pos) / self.paddle_size[0]
        angle = -165 + pad_perc*150
        # angle = -30

        self.ball.vel[0] = mag * math.cos(math.radians(angle))
        self.ball.vel[1] = mag * math.sin(math.radians(angle))
      elif new_rect.top == self.paddle_rect.bottom:
        self.ball.vel[1] = -self.ball.vel[1]
      elif new_rect.left == self.paddle_rect.right or new_rect.right == self.paddle_rect.left:
        self.ball.vel[0] = -self.ball.vel[0]
      
    return newx, newy



  def ball_update(self):
    newx = self.ball.pos[0] + self.ball.vel[0]
    newy = self.ball.pos[1] + self.ball.vel[1]

    # self.ball.past_pos.insert(0, self.ball.pos)
    self.ball.past_pos.append([self.ball.pos[0], self.ball.pos[1]])
    if len(self.ball.past_pos) > self.ball.past_length:
      self.ball.past_pos = self.ball.past_pos[1:]

    newx, newy = self.check_ball_paddle_hit(newx, newy)

    # Check for collision with walls
    if (newx < self.ball.radius or newx > self.screen_size[0] - self.ball.radius) and (newy < self.ball.radius or newy > self.screen_size[1] - self.ball.radius):
      incx = self.ball.vel[0] / self.ball.inc_factor
      incy = self.ball.vel[1] / self.ball.inc_factor
      
      while newx < self.ball.radius or newx > self.screen_size[0] - self.ball.radius or newy < self.ball.radius or newy > self.screen_size[1] - self.ball.radius:
        newx -= incx
        newy -= incy

      self.ball.vel[0] = -self.ball.vel[0]
      self.ball.vel[1] = -self.ball.vel[1]
    elif newx < self.ball.radius or newx > self.screen_size[0] - self.ball.radius:
      # print(newx)
      incx = self.ball.vel[0] / self.ball.inc_factor
      incy = self.ball.vel[1] / self.ball.inc_factor
      
      while newx < self.ball.radius or newx > self.screen_size[0] - self.ball.radius or newy < self.ball.radius or newy > self.screen_size[1] - self.ball.radius:
        newx -= incx
        newy -= incy

      self.ball.vel[0] = -self.ball.vel[0]
    elif newy < self.ball.radius or newy > self.screen_size[1] - self.ball.radius:
      incx = self.ball.vel[0] / self.ball.inc_factor
      incy = self.ball.vel[1] / self.ball.inc_factor
      
      while newx < self.ball.radius or newx > self.screen_size[0] - self.ball.radius or newy < self.ball.radius or newy > self.screen_size[1] - self.ball.radius:
        newx -= incx
        newy -= incy

      self.ball.vel[1] = -self.ball.vel[1]

    self.ball.pos[0] = int(newx)
    self.ball.pos[1] = int(newy)

    self.ball.rect.x = int(newx - self.ball.radius)
    self.ball.rect.y = int(newy - self.ball.radius)



  def run(self):

    clock = pygame.time.Clock()

    while True:

      self.screen.fill((0, 0, 0))
      for event in pygame.event.get():
        if event.type == QUIT:
          sys.exit()

      self.paddle_update()
      self.ball_update()

      # pygame.draw.circle(self.screen, self.ball_col, self.ball_pos, self.ball_radius)
      self.ball.draw(self.screen)
      # pygame.draw.rect(self.screen, self.paddle_col, pygame.Rect(self.paddle_pos, self.paddle_height, self.paddle_size[0], self.paddle_size[1]))
      pygame.draw.rect(self.screen, self.paddle_col, self.paddle_rect)

      pygame.display.flip()

      clock.tick(60)



if __name__ == "__main__":
  Breakout().run()

