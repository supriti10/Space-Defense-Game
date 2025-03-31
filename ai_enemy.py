import pygame
import random
import math
from settings import *
from enemy import Enemy

class AIEnemy(Enemy):
    def __init__(self, x, y):
        # Use parent class constructor but override some attributes
        super().__init__(x, y)
        self.radius = AI_ENEMY_RADIUS
        self.image = pygame.image.load("assets/AI_spaceship.png")
        self.image = pygame.transform.scale(self.image, (self.radius * 2, self.radius * 2))
        self.color = AI_ENEMY_COLOR
        self.rect = pygame.Rect(x - self.radius, y - self.radius, self.radius * 2, self.radius * 2)
        
        self.speed = AI_ENEMY_SPEED
        self.health = AI_ENEMY_HEALTH
        self.damage = AI_ENEMY_DAMAGE
        
        # AI attributes
        self.direction_x = 0
        self.last_decision_time = pygame.time.get_ticks()
        self.pause_time = 0
        
    def draw(self, screen):
        # Draw the AI enemy image
        screen.blit(self.image, (self.x - self.radius, self.y - self.radius))
        
        # Draw health indicator
        health_percentage = self.health / AI_ENEMY_HEALTH
        health_width = self.radius * 2 * health_percentage
        pygame.draw.rect(screen, GREEN, (self.x - self.radius, self.y - self.radius - 5, health_width, 3))

    def update(self, bullets=None):
        # AI decision making
        current_time = pygame.time.get_ticks()
        
        # If the AI is in a pause state
        if self.pause_time > 0:
            self.pause_time -= 1
            return
        
        # Make a new decision every AI_DECISION_TIME milliseconds
        if current_time - self.last_decision_time > AI_DECISION_TIME:
            # Random horizontal movement: -1 (left), 0 (stay), 1 (right)
            self.direction_x = random.randint(-1, 1)
            
            # Small chance to pause
            if random.random() < 0.1:
                self.pause_time = random.randint(10, 30)
            
            self.last_decision_time = current_time
            
            # Bullet avoidance (if bullets are provided)
            if bullets:
                nearest_bullet = self._find_nearest_bullet(bullets)
                if nearest_bullet and self._distance_to(nearest_bullet) < 100:
                    # Try to dodge the bullet
                    if nearest_bullet.x < self.x:
                        self.direction_x = 1  # Move right
                    else:
                        self.direction_x = -1  # Move left
        
        # Update position based on current direction
        self.x += self.direction_x * self.speed
        self.y += self.speed * 0.5  # Move down slower than normal enemies
        
        # Keep AI enemy within screen bounds
        if self.x - self.radius < 0:
            self.x = self.radius
            self.direction_x *= -1
        elif self.x + self.radius > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.radius
            self.direction_x *= -1
            
        # Update rect position
        self.rect.center = (self.x, self.y)
    
    def _find_nearest_bullet(self, bullets):
        nearest = None
        min_distance = float('inf')
        
        for bullet in bullets:
            if bullet is not None:  # Make sure bullet exists
                distance = self._distance_to(bullet)
                if distance < min_distance:
                    min_distance = distance
                    nearest = bullet
        
        return nearest
    
    def _distance_to(self, object):
        # Check if object exists
        if object is None:
            return float('inf')
            
        # Calculate distance to another object
        dx = self.x - object.x
        dy = self.y - object.y
        return math.sqrt(dx*dx + dy*dy)