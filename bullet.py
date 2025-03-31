import pygame
from settings import *

class Bullet:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = BULLET_RADIUS
        self.speed = PLAYER_BULLET_SPEED
        self.color = BULLET_COLOR
        self.damage = BULLET_DAMAGE
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
    
    def update(self):
        # Move bullet upwards
        self.y -= self.speed
    
    def is_off_screen(self):
        # Check if bullet is off the screen
        return self.y < -self.radius
