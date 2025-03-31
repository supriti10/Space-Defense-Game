import pygame
import random
import time
import sys
from settings import *
from spaceship import Spaceship
from bullet import Bullet
from enemy import Enemy
from ai_enemy import AIEnemy

class Game:
    def toggle_sound(self):
        if pygame.mixer.music.get_volume() > 0:
            pygame.mixer.music.set_volume(0)
            self.explosion_sound.set_volume(0)
            self.damage_sound.set_volume(0)
            self.upgrade_sound.set_volume(0)
            self.shoot_sound.set_volume(0)
        else:
            pygame.mixer.music.set_volume(MUSIC_VOLUME)
            self.explosion_sound.set_volume(SOUND_VOLUME)
            self.damage_sound.set_volume(SOUND_VOLUME)
            self.upgrade_sound.set_volume(SOUND_VOLUME)
            self.shoot_sound.set_volume(SOUND_VOLUME)

    def draw_pause_menu(self):
        # Draw a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))  # Semi-transparent black
        self.screen.blit(overlay, (0, 0))
        
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 48)

        # Draw Pause Text
        pause_text = font_large.render("Game Paused", True, WHITE)
        self.screen.blit(pause_text, (SCREEN_WIDTH // 2 - pause_text.get_width() // 2, SCREEN_HEIGHT // 3))

        # Draw Resume and Exit options
        resume_color = GOLD if self.pause_selected_option == 0 else WHITE
        exit_color = GOLD if self.pause_selected_option == 1 else WHITE
        
        resume_option = font_medium.render("Resume", True, resume_color)
        exit_option = font_medium.render("Exit", True, exit_color)

        resume_y = SCREEN_HEIGHT // 2
        exit_y = SCREEN_HEIGHT // 2 + 60
        
        self.screen.blit(resume_option, (SCREEN_WIDTH // 2 - resume_option.get_width() // 2, resume_y))
        self.screen.blit(exit_option, (SCREEN_WIDTH // 2 - exit_option.get_width() // 2, exit_y))
        
        # Store button positions for mouse click detection
        self.pause_menu_rects = {
            "resume": pygame.Rect(SCREEN_WIDTH // 2 - resume_option.get_width() // 2, resume_y, 
                                resume_option.get_width(), resume_option.get_height()),
            "exit": pygame.Rect(SCREEN_WIDTH // 2 - exit_option.get_width() // 2, exit_y,
                              exit_option.get_width(), exit_option.get_height())
        }

    def __init__(self, screen, is_multiplayer=False):
        self.screen = screen
        self.game_over = False
        self.victory = False
        self.score = 0
        self.is_multiplayer = is_multiplayer
        self.paused = False
        self.pause_selected_option = 0  # Option in pause menu (0 = Resume, 1 = Exit)
        self.pause_menu_rects = {}  # Pause menu button positions


        self.show_bonus_notification = False
        self.bonus_notification_time = 0
        self.bonus_notification_duration = 2000  # 2 seconds

        # Background
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        # Castle image
        self.castle_image = pygame.image.load("assets/castle.jpg")
        self.castle_image = pygame.transform.scale(self.castle_image, (CASTLE_WIDTH, CASTLE_HEIGHT))

        # Create player spaceship(s)
        if self.is_multiplayer:
            # Two players
            self.player1 = Spaceship(SCREEN_WIDTH // 2 + 100, SCREEN_HEIGHT - CASTLE_HEIGHT - PLAYER_HEIGHT // 2, PLAYER_SPEED, self, 1)
            self.player2 = Spaceship(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - CASTLE_HEIGHT - PLAYER_HEIGHT // 2, PLAYER_SPEED, self, 2)
            self.player = self.player1  # Set player1 as default player for compatibility
        else:
            # Single player
            self.player = Spaceship(SCREEN_WIDTH // 2, SCREEN_HEIGHT - CASTLE_HEIGHT - PLAYER_HEIGHT // 2, PLAYER_SPEED, self, 1)
            self.player2 = None

        # Initialize game objects
        self.bullets = []
        self.enemies = []
        self.ai_enemies = []
        
        # Castle attributes
        self.castle_health = CASTLE_STARTING_HEALTH
        
        # Spawn control
        self.last_enemy_spawn_time = 0
        self.enemy_groups_spawned = 0
        self.enemies_in_current_group = 0
        self.ai_enemies_to_spawn = 0
        
        # Player upgrade tracking
        self.ai_enemies_killed = 0
        
        # Load sounds
        self.explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
        self.explosion_sound.set_volume(0.3)
        self.damage_sound = pygame.mixer.Sound("assets/damage.wav")
        self.damage_sound.set_volume(0.3)
        self.upgrade_sound = pygame.mixer.Sound("assets/upgrade.wav")
        self.upgrade_sound.set_volume(0.5)
        self.shoot_sound = pygame.mixer.Sound("assets/shoot.wav")
        self.shoot_sound.set_volume(0.2)
        
        # Load background music
        pygame.mixer.music.load("assets/background.wav")
        pygame.mixer.music.set_volume(0.2)
        pygame.mixer.music.play(-1)  # Loop indefinitely
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            # Toggle pause with ESC
            if event.key == pygame.K_ESCAPE:
                self.paused = not self.paused
                return True  # Event handled

            # Handle pause menu navigation
            if self.paused:
                if event.key == pygame.K_UP:
                    self.pause_selected_option = (self.pause_selected_option - 1) % 2
                    return True
                elif event.key == pygame.K_DOWN:
                    self.pause_selected_option = (self.pause_selected_option + 1) % 2
                    return True
                elif event.key == pygame.K_RETURN:
                    if self.pause_selected_option == 0:  # Resume
                        self.paused = False
                        return True
                    elif self.pause_selected_option == 1:  # Exit
                        # Return to main menu instead of quitting the game entirely
                        return "exit_to_menu"
                return True  # All pause menu events are handled
            
            # When not paused, forward events to player spaceships
            if not self.game_over:
                self.player.handle_event(event)
                if self.is_multiplayer and self.player2:
                    self.player2.handle_event(event)
        
        elif event.type == pygame.KEYUP:
            # Forward keyup events to players
            if not self.paused and not self.game_over:
                self.player.handle_event(event)
                if self.is_multiplayer and self.player2:
                    self.player2.handle_event(event)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # Handle mouse clicks in pause menu
            if self.paused and event.button == 1:  # Left mouse button
                mouse_pos = pygame.mouse.get_pos()
                if self.pause_menu_rects.get("resume") and self.pause_menu_rects["resume"].collidepoint(mouse_pos):
                    self.paused = False
                    return True
                elif self.pause_menu_rects.get("exit") and self.pause_menu_rects["exit"].collidepoint(mouse_pos):
                    # Return to main menu instead of quitting the game entirely
                    return "exit_to_menu"
        
        return False  # Event not handled
    
    def check_ai_enemy_kill_bonuses(self):
        # Check if player has killed 3 AI enemies
        if self.ai_enemies_killed >= 3:
            # Apply fire rate boost if not already boosted
            if not self.player.fire_rate_boosted:
                self.player.boost_fire_rate()
                if self.is_multiplayer and self.player2:
                    self.player2.boost_fire_rate()
                self.upgrade_sound.play()
            
            # Increase castle health by 2 units
            self.castle_health = min(self.castle_health + 2, CASTLE_STARTING_HEALTH)
            
            # Reset the counter
            self.ai_enemies_killed = 0
            
            # Display bonus notification (optional)
            font = pygame.font.SysFont(None, 36)
            # bonus_text = font.render("BONUS: Fire Rate Boost + Castle Repair!", True, GOLD)
            self.show_bonus_notification = True
            self.bonus_notification_time = pygame.time.get_ticks()
            # self.screen.blit(bonus_text, (SCREEN_WIDTH // 2 - bonus_text.get_width() // 2, 100))
            pygame.display.update()
            
            return True
        return False
    
    def update(self):
        if self.game_over or self.paused:
            return
        
        # Update player(s)
        new_bullets = self.player.update()
        if new_bullets:
            self.bullets.extend(new_bullets)
        
        if self.is_multiplayer and self.player2:
            new_bullets = self.player2.update()
            if new_bullets:
                self.bullets.extend(new_bullets)
        
        # Update bullets
        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_off_screen():
                self.bullets.remove(bullet)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update()
            
            # Check for bullet collisions
            for bullet in self.bullets[:]:
                if bullet and enemy and self._check_collision(bullet, enemy):
                    destroyed = enemy.take_damage(bullet.damage)
                    if bullet in self.bullets:  # Check if bullet is still in list
                        self.bullets.remove(bullet)
                    
                    if destroyed:
                        if enemy in self.enemies:  # Check if enemy is still in list
                            self.enemies.remove(enemy)
                            self.score += NORMAL_ENEMY_SCORE
                            self.explosion_sound.play()
                    break

            # Check if enemy hits castle
            if enemy and enemy.hit_castle():
                self.castle_health -= enemy.damage
                if enemy in self.enemies:
                    self.enemies.remove(enemy)
                self.damage_sound.play()
        
        # Update AI enemies
        for ai_enemy in self.ai_enemies[:]:
            ai_enemy.update(self.bullets)
            
            # Check for bullet collisions
            for bullet in self.bullets[:]:
                if bullet and ai_enemy and self._check_collision(bullet, ai_enemy):
                    destroyed = ai_enemy.take_damage(bullet.damage)
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)
                    
                    if destroyed:
                        if ai_enemy in self.ai_enemies:
                            self.ai_enemies.remove(ai_enemy)
                            self.score += AI_ENEMY_SCORE
                            self.ai_enemies_killed += 1
                            self.explosion_sound.play()
                            
                            # Check for bonuses after killing AI enemy
                            self.check_ai_enemy_kill_bonuses()
                    break

            # Check if AI enemy hits castle
            if ai_enemy and ai_enemy.hit_castle():
                self.castle_health -= ai_enemy.damage
                if ai_enemy in self.ai_enemies:
                    self.ai_enemies.remove(ai_enemy)
                self.damage_sound.play()
        
        # Spawn enemies
        self._handle_enemy_spawning()
        
        # Check game over condition
        if self.castle_health <= 0:
            self.castle_health = 0
            self.game_over = True
    
    def draw(self):
        # Fill background
        self.screen.blit(self.background, (0, 0))
        
        if not self.game_over:
            # Draw castle
            castle_x = (SCREEN_WIDTH - CASTLE_WIDTH) // 2
            castle_y = SCREEN_HEIGHT - CASTLE_HEIGHT
            self.screen.blit(self.castle_image, (castle_x, castle_y))

            # Draw player(s)
            self.player.draw(self.screen)
            if self.is_multiplayer and self.player2:
                self.player2.draw(self.screen)
            
            # Draw bullets
            for bullet in self.bullets:
                bullet.draw(self.screen)
            
            # Draw enemies
            for enemy in self.enemies:
                enemy.draw(self.screen)
            
            # Draw AI enemies
            for ai_enemy in self.ai_enemies:
                ai_enemy.draw(self.screen)
            
            # Draw UI elements
            self._draw_ui()
        else:
            # Draw game over screen
            self._draw_game_over()
    
    def _draw_ui(self):
        # Draw castle health bar
        health_width = 200
        health_height = 20
        health_x = 20
        health_y = 20
        
        # Draw background bar
        pygame.draw.rect(self.screen, RED, (health_x, health_y, health_width, health_height))
        
        # Draw current health
        health_percentage = max(0, self.castle_health / CASTLE_STARTING_HEALTH)
        current_health_width = int(health_width * health_percentage)
        pygame.draw.rect(self.screen, GREEN, (health_x, health_y, current_health_width, health_height))
        
        # Draw health text
        font = pygame.font.SysFont(None, 24)
        health_text = font.render(f"Castle Health: {self.castle_health}", True, WHITE)
        self.screen.blit(health_text, (health_x, health_y + health_height + 5))
        
        # Draw score
        score_text = font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))
        
        # Draw AI enemies killed counter
        ai_killed_text = font.render(f"AI Enemies Killed: {self.ai_enemies_killed}/3", True, WHITE)
        self.screen.blit(ai_killed_text, (SCREEN_WIDTH - ai_killed_text.get_width() - 20, 80))
        
        # Draw fire rate boost status
        if self.player.fire_rate_boosted:
            remaining_time = self.player.get_boost_time_remaining()
            boost_text = f"Fire Rate Boost: {remaining_time:.1f}s"
            boost_color = GOLD
        else:
            boost_text = "Fire Rate: Normal"
            boost_color = WHITE
            
        boost_render = font.render(boost_text, True, boost_color)
        self.screen.blit(boost_render, (SCREEN_WIDTH - boost_render.get_width() - 20, 50))

        # Draw bonus notification if active
        if self.show_bonus_notification:
            current_time = pygame.time.get_ticks()
            if current_time - self.bonus_notification_time < self.bonus_notification_duration:
                font = pygame.font.SysFont(None, 36)
                bonus_text = font.render("BONUS: Fire Rate Boost ~ Health Increased by 2", True, GOLD)
                self.screen.blit(bonus_text, (SCREEN_WIDTH // 2 - bonus_text.get_width() // 2, 100))
            else:
                self.show_bonus_notification = False
    
    def _draw_game_over(self):
        # Draw game over text
        font_large = pygame.font.SysFont(None, 72)
        font_medium = pygame.font.SysFont(None, 36)
        
        # Game over message
        game_over_text = font_large.render("Game Over", True, RED)
        self.screen.blit(game_over_text, 
                        (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, 
                         SCREEN_HEIGHT // 3))
        
        # Final score
        score_text = font_medium.render(f"Final Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, 
                        (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2))
        
        # Restart instructions
        restart_text = font_medium.render("Press SPACE to play again", True, WHITE)
        self.screen.blit(restart_text, 
                        (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, 
                         SCREEN_HEIGHT // 2 + 50))
    
    def _handle_enemy_spawning(self):
        current_time = pygame.time.get_ticks()
        
        # Handle AI enemy spawning
        if (self.ai_enemies_to_spawn > 0 and len(self.ai_enemies) == 0 and 
            current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY):
            # Spawn a new AI enemy at a random x position
            x = random.randint(AI_ENEMY_RADIUS, SCREEN_WIDTH - AI_ENEMY_RADIUS)
            self.ai_enemies.append(AIEnemy(x, AI_ENEMY_RADIUS))
            self.ai_enemies_to_spawn -= 1
            self.last_enemy_spawn_time = current_time
            return  # Don't spawn normal enemies at the same time
        
        # Handle normal enemy spawning
        if (self.ai_enemies_to_spawn == 0 and 
            current_time - self.last_enemy_spawn_time > ENEMY_SPAWN_DELAY):
            
            # If all enemies in current group have been spawned, prepare for next group
            if self.enemies_in_current_group >= ENEMY_GROUP_SIZE:
                self.enemies_in_current_group = 0
                self.enemy_groups_spawned += 1
                
                # Check if it's time to spawn AI enemies
                if self.enemy_groups_spawned % AI_SPAWN_AFTER_GROUPS == 0:
                    self.ai_enemies_to_spawn = 2  # Spawn two AI enemies
                    return
            
            # Spawn a new enemy at a random x position
            if self.enemies_in_current_group < ENEMY_GROUP_SIZE:
                x = random.randint(ENEMY_RADIUS, SCREEN_WIDTH - ENEMY_RADIUS)
                self.enemies.append(Enemy(x, ENEMY_RADIUS))
                self.enemies_in_current_group += 1
                self.last_enemy_spawn_time = current_time
    
    def _check_collision(self, obj1, obj2):
        # Check if objects are valid before checking collision
        if not obj1 or not obj2:
            return False
        
        # Use rect collision if available
        if hasattr(obj1, 'rect') and hasattr(obj2, 'rect'):
            return obj1.rect.colliderect(obj2.rect)
        else:
            # Fall back to circular collision detection
            distance = ((obj1.x - obj2.x) ** 2 + (obj1.y - obj2.y) ** 2) ** 0.5
            return distance < (obj1.radius + obj2.radius)