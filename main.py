import pygame
import sys
from settings import *
from game import Game

def draw_menu(screen, selected_option):
    # Set up font
    font_large = pygame.font.SysFont(None, 72)
    font_medium = pygame.font.SysFont(None, 48)
    
    # Draw title
    title = font_large.render("Space Defense", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 4))
    
    # Draw options
    single_color = GOLD if selected_option == 0 else WHITE
    multi_color = GOLD if selected_option == 1 else WHITE
    exit_color = GOLD if selected_option == 2 else WHITE
    
    single_player = font_medium.render("Single Player", True, single_color)
    multi_player = font_medium.render("Multiplayer", True, multi_color)
    exit_option = font_medium.render("Exit", True, exit_color)
    
    # Y positions
    single_y = SCREEN_HEIGHT // 2
    multi_y = SCREEN_HEIGHT // 2 + 60
    exit_y = SCREEN_HEIGHT // 2 + 120
    
    screen.blit(single_player, (SCREEN_WIDTH // 2 - single_player.get_width() // 2, single_y))
    screen.blit(multi_player, (SCREEN_WIDTH // 2 - multi_player.get_width() // 2, multi_y))
    screen.blit(exit_option, (SCREEN_WIDTH // 2 - exit_option.get_width() // 2, exit_y))

    # Draw instructions below exit option
    instructions = pygame.font.SysFont(None, 24).render("Use UP/DOWN arrows or CLICK to select, ENTER to confirm", True, WHITE)
    screen.blit(instructions, (SCREEN_WIDTH // 2 - instructions.get_width() // 2, SCREEN_HEIGHT // 2 + 180))
    
    # Return rect objects for mouse click detection
    return {
        "single": pygame.Rect(SCREEN_WIDTH // 2 - single_player.get_width() // 2, single_y, 
                          single_player.get_width(), single_player.get_height()),
        "multi": pygame.Rect(SCREEN_WIDTH // 2 - multi_player.get_width() // 2, multi_y, 
                          multi_player.get_width(), multi_player.get_height()),
        "exit": pygame.Rect(SCREEN_WIDTH // 2 - exit_option.get_width() // 2, exit_y, 
                        exit_option.get_width(), exit_option.get_height())
    }

def main():
    # Initialize pygame
    pygame.init()
    pygame.mixer.init()
    
    # Set up the display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("AI-Integrated Space Defense Game")
    
    # Clock for controlling frame rate
    clock = pygame.time.Clock()
    
    # Menu state
    running = True
    in_menu = True
    selected_option = 0  # 0 = Single Player, 1 = Multiplayer, 2 = Exit
    
    # Background for menu
    background = pygame.image.load("assets/background.jpg")
    background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))
    
    # Menu button rects for mouse click detection
    menu_rects = {}
    
    # Game instance (will be initialized when starting a game)
    game = None

    # Main game loop
    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                sys.exit()

            elif in_menu:
                # Menu event handling
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % 3  # Navigate down
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % 3  # Navigate up
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Single Player
                            game = Game(screen, False)
                            in_menu = False
                        elif selected_option == 1:  # Multiplayer
                            game = Game(screen, True)
                            in_menu = False
                        elif selected_option == 2:  # Exit
                            running = False
                            pygame.quit()
                            sys.exit()
                
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left mouse button
                    mouse_pos = pygame.mouse.get_pos()
                    if menu_rects.get("single") and menu_rects["single"].collidepoint(mouse_pos):
                        game = Game(screen, False)
                        in_menu = False
                    elif menu_rects.get("multi") and menu_rects["multi"].collidepoint(mouse_pos):
                        game = Game(screen, True)
                        in_menu = False
                    elif menu_rects.get("exit") and menu_rects["exit"].collidepoint(mouse_pos):
                        running = False
                        pygame.quit()
                        sys.exit()
            
            elif game:
                # Game event handling
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and game.game_over:
                    # Restart game on space press when game over
                    game = Game(screen, game.is_multiplayer)
                else:
                    # Forward event to game and check for exit to menu
                    result = game.handle_event(event)
                    if result == "exit_to_menu":
                        in_menu = True
                        game = None  # Clear the game instance
        
        # Draw everything
        screen.fill(BLACK)
        
        if in_menu:
            # Draw menu
            screen.blit(background, (0, 0))
            menu_rects = draw_menu(screen, selected_option)
        else:
            # Draw game
            if game.paused:
                game.draw()  # Draw game first as background
                game.draw_pause_menu()  # Then draw pause menu on top
            else:
                game.update()
                game.draw()
        
        # Flip the display
        pygame.display.flip()
        
        # Cap the frame rate
        clock.tick(FPS)

if __name__ == "__main__":
    main()