import pygame
from settings import *
from bullet import Bullet

class Spaceship:
    def __init__(self, x, y, speed, game, player_number):
        self.x = x
        self.y = y
        self.game = game  # Reference to the game object
        self.player_number = player_number  # 1 = Player 1, 2 = Player 2
        self.auto_fire = True  # Enable auto-fire by default

        # Load the spaceship image
        if player_number == 1:
            self.image = pygame.image.load("assets/spaceship.png")
        else:
            # Use a different image or tint for Player 2 if needed
            self.image = pygame.image.load("assets/spaceship.png")
            self.image = self.tint_image(self.image, GREEN)  # Tinting for player 2

        # Scale the image to desired size
        self.image = pygame.transform.scale(self.image, (PLAYER_WIDTH, PLAYER_HEIGHT))

        # Correctly define width and height after scaling
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT

        # Create a rect for positioning and collision detection
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)  # Initial position

        self.speed = speed
        self.base_fire_rate = PLAYER_FIRE_RATE  # Store the base fire rate
        self.fire_rate = self.base_fire_rate  # Current fire rate
        self.last_shot_time = 0
        
        # Fire rate boost tracking
        self.fire_rate_boosted = False
        self.boost_start_time = 0
        self.boost_duration = 8000  # 8 seconds in milliseconds

        # Movement and firing flags
        self.moving_left = False
        self.moving_right = False
        self.firing = False

    def tint_image(self, image, color):
        # Create a copy of the image
        tinted = image.copy()
        # Apply color tint
        tinted.fill(color, special_flags=pygame.BLEND_RGB_MULT)
        return tinted
    
    def draw(self, screen):
        # Draw the spaceship image
        screen.blit(self.image, self.rect.topleft)
    
    def update(self):
        # Check if boost has expired
        if self.fire_rate_boosted:
            current_time = pygame.time.get_ticks()
            if current_time - self.boost_start_time > self.boost_duration:
                self.reset_fire_rate()
        
        # Use movement flags to move the spaceship
        if self.moving_left:
            self.move_left()
        if self.moving_right:
            self.move_right()
        
        # If firing flag is set, shoot
        if self.auto_fire:
            return self.shoot()
        elif self.firing:  # Keep manual override capability
            return self.shoot()
        return []
        
    
    def handle_event(self, event):
        # Handle keyboard events based on player number
        if self.player_number == 1:
            # Player 1 uses arrow keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.moving_left = True
                if event.key == pygame.K_RIGHT:
                    self.moving_right = True
                
                
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.moving_left = False
                if event.key == pygame.K_RIGHT:
                    self.moving_right = False
                
                
        else:
            # Player 2 uses A and D keys
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    self.moving_left = True
                if event.key == pygame.K_d:
                    self.moving_right = True
                
               
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_a:
                    self.moving_left = False
                if event.key == pygame.K_d:
                    self.moving_right = False
    
    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time > self.fire_rate:
            # Create two bullets for dual guns
            left_bullet = Bullet(self.rect.centerx - self.width // 4, self.rect.top)
            right_bullet = Bullet(self.rect.centerx + self.width // 4, self.rect.top)
            self.last_shot_time = current_time
            
            # Play shooting sound if game reference exists
            if self.game and hasattr(self.game, 'shoot_sound'):
                self.game.shoot_sound.play()
                
            return [left_bullet, right_bullet]  # Return both bullets
        return []
    
    def boost_fire_rate(self):
        # Apply temporary fire rate boost
        self.fire_rate = self.base_fire_rate // 2  # Double firing speed (half the delay)
        self.fire_rate_boosted = True
        self.boost_start_time = pygame.time.get_ticks()
    
    def reset_fire_rate(self):
        # Reset fire rate to normal
        self.fire_rate = self.base_fire_rate
        self.fire_rate_boosted = False

    def get_boost_time_remaining(self):
        # Return remaining boost time in seconds
        if not self.fire_rate_boosted:
            return 0
        
        current_time = pygame.time.get_ticks()
        elapsed = current_time - self.boost_start_time
        remaining = max(0, self.boost_duration - elapsed)
        return remaining / 1000  # Convert to seconds

    def move_left(self):
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        self.x = self.rect.centerx  # Update self.x to keep them in sync

    def move_right(self):
        self.rect.x += self.speed
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        self.x = self.rect.centerx  # Update self.x to keep them in sync