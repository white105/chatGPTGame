import pygame
import random
import time

# ...

explosion_image = pygame.image.load("./assets/explosion.png")

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((1600, 1100))
pygame.display.set_caption("Space Game")

# Load the player spaceship image
player_image = pygame.image.load("./assets/spaceship.png")

# Scale the player spaceship image to a smaller size
player_image = pygame.transform.scale(player_image, (50, 50))

player_x = 400
player_y = 500



# Create a list to store the asteroids
asteroids = []

# Load the asteroid image
asteroid_image = pygame.image.load("./assets/asteroid.png")

# Scale the asteroid image to a smaller size
asteroid_image = pygame.transform.scale(asteroid_image, (50, 50))
asteroid_x = 80
asteroid_y = 50
asteroids.append([asteroid_image, asteroid_x, asteroid_y])



running = True

clock = pygame.time.Clock()

player_speed = 10
player_x_change = 0
player_y_change = 0

screen_width = 1600
screen_height = 1100

# Initialize the level variable
level = 0

# Load the gem image
gem_image = pygame.image.load("./assets/gem.png")
gem_image = pygame.transform.scale(gem_image, (40, 40))
# Set the initial position of the gem
gem_x = screen_width // 2
gem_y = screen_height // 2
# Set the speed of the gem
gem_speed = 5
# Set the direction of the gem
gem_x_change = gem_speed
gem_y_change = gem_speed


# Main game loop
while running:

    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                player_x_change = -player_speed
            elif event.key == pygame.K_RIGHT:
                player_x_change = player_speed
            elif event.key == pygame.K_UP:
                player_y_change = -player_speed
            elif event.key == pygame.K_DOWN:
                player_y_change = player_speed
        elif event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                player_x_change = 0
            if event.key in (pygame.K_UP, pygame.K_DOWN):
                player_y_change = 0

    player_x += player_x_change
    player_y += player_y_change

    if player_x > screen_width:
        player_x = 0
    elif player_x < 0:
        player_x = screen_width
    if player_y > screen_height:
        player_y = 0
    elif player_y < 0:
        player_y = screen_height

    # Clear the screen
    screen.fill((0, 0, 0))
    # Draw the player spaceship
    screen.blit(player_image, (player_x, player_y))

    # Move the gem
    gem_x += gem_x_change
    gem_y += gem_y_change
    # Check if the gem is outside the screen boundaries and reverse its direction
    if gem_x > screen_width or gem_x < 0:
        gem_x_change = -gem_x_change
    if gem_y > screen_height or gem_y < 0:
        gem_y_change = -gem_y_change


    # Move the asteroid and check for collisions with the walls
    asteroid = asteroids[0]
    # Check if the asteroid is outside the screen boundaries and reverse its direction
    if asteroid[1] > screen_width or asteroid[1] < 0:
        asteroid[1] = screen_width - asteroid[1] 
    if asteroid[2] > screen_height or asteroid[2] < 0:
        asteroid[2] = screen_height - asteroid[2]

        
    # Check if the asteroid and the player collide
    asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid_image.get_width(), asteroid_image.get_height())
    player_rect = pygame.Rect(player_x, player_y, player_image.get_width(), player_image.get_height())


    # collision 

    gem_rect = pygame.Rect(gem_x, gem_y, gem_image.get_width(), gem_image.get_height())
    if gem_rect.colliderect(player_rect):
        # Create a new asteroid
        asteroid = [asteroid_image,random.randint(0, screen_width - asteroid_image.get_width()),random.randint(0, screen_height - asteroid_image.get_height())]
        asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid_image.get_width(), asteroid_image.get_height())
        while pygame.math.Vector2(asteroid_rect.center).distance_to(pygame.math.Vector2(player_rect.center)) < 200:
            asteroid[1] = random.randint(0, screen_width - asteroid_image.get_width())
            asteroid[2] = random.randint(0, screen_height - asteroid_image.get_height())
            asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid_image.get_width(), asteroid_image.get_height())
        asteroids.append(asteroid)
    # Move the asteroid and check for 

        level += 1
         # Generate random new position for the gem
        gem_x = random.randint(0, screen_width - gem_image.get_width())
        gem_y = random.randint(0, screen_height - gem_image.get_height())



    if asteroid_rect.colliderect(player_rect):
        font = pygame.font.Font(None, 30)
        text = font.render("Player Died!", True, (255,255,255))
        textRect = text.get_rect()
        textRect.center = (screen_width//2, screen_height//2)
        screen.blit(text, textRect)
        level = 0
        
        asteroids.clear()
        asteroid = [asteroid_image,random.randint(0, screen_width - asteroid_image.get_width()),random.randint(0, screen_height - asteroid_image.get_height())]
        asteroids.append(asteroid)

        screen.blit(explosion_image, (player_x, player_y))
        pygame.display.update()
        time.sleep(1)
        
    else:
        screen.blit(player_image, (player_x, player_y))

        # Draw the asteroid
    screen.blit(asteroid[0], (asteroid[1], asteroid[2]))
    # Update the display

    # Create a font object
    font = pygame.font.Font(None, 40)
    # Create a text surface object for the level
    level_text = font.render("Level: " + str(level), True, (255, 255, 255))
    # Create a rectangular object for the text surface
    level_rect = level_text.get_rect()
    # Position the rectangular object on the top left corner of the screen
    level_rect.topleft = (10, 10)
    # Draw the level text on the screen
    screen.blit(level_text, level_rect)

    # Draw the gem
    screen.blit(gem_image, (gem_x, gem_y))

    # Move the asteroid and check for collisions with the walls
    for asteroid in asteroids:
        asteroid[1] += 5
        asteroid[2] += 5
        # Check if the asteroid is outside the screen boundaries and reverse its direction
        if asteroid[1] > screen_width or asteroid[1] < 0:
            asteroid[1] = screen_width - asteroid[1] 
        if asteroid[2] > screen_height or asteroid[2] < 0:
            asteroid[2] = screen_height - asteroid[2]
        # Check if the asteroid collides with the player
        asteroid_rect = pygame.Rect(asteroid[1], asteroid[2], asteroid_image.get_width(), asteroid_image.get_height())
        if asteroid_rect.colliderect(player_rect):
            level = 0
            asteroids.clear()
            asteroid = [asteroid_image,random.randint(0, screen_width - asteroid_image.get_width()),random.randint(0, screen_height - asteroid_image.get_height())]
            asteroids.append(asteroid)
    # Draw the asteroids
    for asteroid in asteroids:
        screen.blit(asteroid[0], (asteroid[1], asteroid[2]))
    # Update the display

    pygame.display.update()
    clock.tick(60)

# Cleanup and exit
pygame.quit()
