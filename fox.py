import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Set up display
width, height = 611, 765
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Fox Coin Collector")

# Load icon image (replace "icon.png" with your icon image file)
icon = pygame.image.load("fox.png")
pygame.display.set_icon(icon)

# Load background image (replace "firstPic.jpeg" with your background image file)
background_image = pygame.image.load("firstPic.jpeg")
background_image = pygame.transform.scale(background_image, (width, height))  # Resize to match screen size

# Load play button image (replace "playButton.png" with your play button image file)
play_button_image = pygame.image.load("playButton.png")
play_button_image = pygame.transform.scale(play_button_image, (200, 70))  # Resize the play button
play_button_rect = play_button_image.get_rect(center=(width // 2, height - 50))  # Add this line

# Load try again and exit button images
try_again_image = pygame.image.load("replay.png")
exit_image = pygame.image.load("exit.png")

# Resize the fox image
fox_image = pygame.image.load("foxPic.png")
fox_image = pygame.transform.scale(fox_image, (100, 100))  # Resize the fox
fox_rect = fox_image.get_rect(center=(width // 2, height // 2))
fox_speed = 10  # Increase the fox speed

# Coin properties
coin_image = pygame.image.load("coin.png")
coin_image = pygame.transform.scale(coin_image, (100, 100))
coins = []
coin_spawn_timer = 0
coin_spawn_interval = 20  # Updated: faster coin spawn interval

# Score counter
score = 0
highest_score = 0  # New variable to store the highest score
font = pygame.font.Font(None, 36)

# Timer
timer_font = pygame.font.Font(None, 36)
timer_start_time = pygame.time.get_ticks()
game_duration = 7000  # 7 seconds

# Game loop
playing_game = False
game_over = False
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and play_button_rect.collidepoint(event.pos) and not playing_game:
            playing_game = True
            timer_start_time = pygame.time.get_ticks()
            score = 0  # Reset score when starting a new game

        # Check for button clicks in the game over screen
        if game_over and event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = event.pos
            if (
                width // 2 - try_again_image.get_width() // 2
                <= mouse_x
                <= width // 2 + try_again_image.get_width() // 2
                and height // 2 + 20
                <= mouse_y
                <= height // 2 + 20 + try_again_image.get_height()
            ):
                # Clicked on Try Again
                playing_game = True
                game_over = False
                score = 0
                timer_start_time = pygame.time.get_ticks()
                coins.clear()
            elif (
                width // 2 - exit_image.get_width() // 2
                <= mouse_x
                <= width // 2 + exit_image.get_width() // 2
                and height // 2 + 140
                <= mouse_y
                <= height // 2 + 140 + exit_image.get_height()
            ):
                # Clicked on Exit
                running = False

    # Draw background
    if not playing_game or game_over:
        screen.blit(background_image, (0, 0))
    else:
        # Draw a blank green background
        screen.fill((32, 112, 0))

    if not playing_game:
        # Draw play button
        screen.blit(play_button_image, play_button_rect)
    else:
        # Handle player controls
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and fox_rect.left > 0:
            fox_rect.x -= fox_speed
        if keys[pygame.K_RIGHT] and fox_rect.right < width:
            fox_rect.x += fox_speed
        if keys[pygame.K_UP] and fox_rect.top > 0:
            fox_rect.y -= fox_speed
        if keys[pygame.K_DOWN] and fox_rect.bottom < height:
            fox_rect.y += fox_speed

        # Spawn coins
        coin_spawn_timer += 1
        if coin_spawn_timer >= coin_spawn_interval:
            coin_spawn_timer = 0
            coin_rect = coin_image.get_rect(center=(random.randint(0, width), random.randint(0, height)))
            coins.append(coin_rect)

        # Check for collisions with coins
        for coin_rect in coins[:]:
            if fox_rect.colliderect(coin_rect):
                coins.remove(coin_rect)
                score += 10

        # Draw fox
        screen.blit(fox_image, fox_rect)

        # Draw coins
        for coin_rect in coins:
            screen.blit(coin_image, coin_rect)

        # Draw score
        score_text = font.render(f"Your score is: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        # Draw timer
        elapsed_time = pygame.time.get_ticks() - timer_start_time
        remaining_time = max(0, game_duration - elapsed_time)
        timer_text = timer_font.render(f"Timer: {remaining_time // 1000} s", True, (255, 255, 255))
        screen.blit(timer_text, (width - timer_text.get_width() - 10, 10))

        # Check for game over condition
        if elapsed_time >= game_duration:
            playing_game = False
            game_over = True
            if score > highest_score:
                highest_score = score  # Update the highest score

    if game_over:
        # Draw game over screen
        screen.fill((32, 112, 0))
        game_over_text = font.render(f"Your score is {score}", True, (255, 255, 255))
        screen.blit(game_over_text, (width // 2 - game_over_text.get_width() // 2, height // 4))

        try_again_rect = try_again_image.get_rect(center=(width // 2, height // 2 + 20))
        screen.blit(try_again_image, try_again_rect)

        exit_rect = exit_image.get_rect(center=(width // 2, height // 2 + try_again_rect.height + 2 * 20))
        screen.blit(exit_image, exit_rect)

        # Draw highest score
        highest_score_text = font.render(f"Highest Score: {highest_score}", True, (255, 255, 255))
        screen.blit(highest_score_text, (width // 2 - highest_score_text.get_width() // 2, height // 4 - 50))

    # Update the display
    pygame.display.flip()

    # Set frames per second
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
