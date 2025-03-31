import pygame
import random
from settings import *

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = ENEMY_RADIUS
        self.image = pygame.image.load("assets/enemyShip.png")
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.speed = ENEMY_SPEED
        self.color = ENEMY_COLOR
        self.health = ENEMY_HEALTH
        self.damage = NORMAL_ENEMY_DAMAGE
        # Create a rect for more accurate collision detection
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
    
    def draw(self, screen):
        # Draw the enemy image
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
        # Draw health indicator
        health_percentage = self.health / ENEMY_HEALTH
        health_width = self.radius * 2 * health_percentage
        pygame.draw.rect(screen, GREEN, (self.x - self.radius, self.y - self.radius - 5, health_width, 3))
    
    def update(self):
        # Move enemy downwards
        self.y += self.speed
        # Update rect position to match the enemy's position
        self.rect.center = (self.x, self.y)
    
    def is_off_screen(self):
        # Check if enemy is off the screen (bottom)
        return self.y > SCREEN_HEIGHT + self.radius
    
    def hit_castle(self):
        castle_x = (SCREEN_WIDTH - CASTLE_WIDTH) // 2
        castle_rect = pygame.Rect(castle_x, SCREEN_HEIGHT - CASTLE_HEIGHT, CASTLE_WIDTH, CASTLE_HEIGHT)
        
        # Check if enemy rect overlaps with castle rect
        return self.rect.colliderect(castle_rect)
    
    def take_damage(self, damage):
        self.health -= damage
        return self.health <= 0  # Return True if enemy is destroyed