import pygame
import sys
import math

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 40
CAMERA_BUFFER = 100
PLAYER_START_X = 50
LEFT_BOUNDARY = CAMERA_BUFFER
WHITE = (255, 255, 255)

# Create the window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mario Platformer")

# Define the player
player = pygame.Rect(PLAYER_START_X, 500, PLAYER_SIZE, PLAYER_SIZE)
vel_x = 0  # Initial speed
acceleration = 0.2  # Acceleration factor
max_speed = 6.6  # Maximum speed
player_jump_power = -13.5
vel_y = 0.5

# Initialize camera
camera_x = 0

# Initialize clock
clock = pygame.time.Clock()
FPS = 60

# Player state variables
is_jumping = False
player_dir = 0 # 0 is right, 1 is left
player_anim_frame = 1 
player_state = "normal"

level_complete = False # Set to True once sequence is done

# Load level image
level_image = pygame.image.load("assets/level.png") 
level_image = pygame.transform.scale(level_image, (int(level_image.get_width() * 2.5), int(level_image.get_height() * 2.5)))

# Load player image
player_image = pygame.image.load("assets/player/idle.png")
player_image = pygame.transform.scale(player_image, (player_image.get_width() * 1.25, player_image.get_height() * 1.25))

# Load Font
font = pygame.font.Font(None, 60)

# Load well done text
welldone_text = font.render("Well done!", True, (255, 255, 255))
welldone_rect = welldone_text.get_rect()
welldone_rect.topleft = (WIDTH // 2 - 80, 100)

# Method to set current player's image
def set_player_image(image_name):
    global player_image

    player_image = pygame.image.load(f'assets/player/{image_name}.png')
    player_image = pygame.transform.scale(player_image, (player_image.get_width() * 1.25, player_image.get_height() * 1.25))

# Load well done message
welldone = pygame.image.load("assets/welldone.svg")
welldone = pygame.transform.scale(welldone, (welldone.get_width() * 1.5, welldone.get_height() * 1.5))

# Load sounds
death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
jump_sound = pygame.mixer.Sound("assets/sounds/jump.wav")
stomp_sound = pygame.mixer.Sound("assets/sounds/stomp.wav")
goal_sound = pygame.mixer.Sound("assets/sounds/goal.wav")
music = pygame.mixer.Sound("assets/sounds/level.wav")

# List to store platforms
platforms = [
    # Side wall
    {"rect": pygame.Rect(-40, 0, 40, HEIGHT), "vertical_wall": True},
    # Ground platforms
    {"rect": pygame.Rect(0, HEIGHT - 40, 3180, 32), "vertical_wall": False},
    {"rect": pygame.Rect(3260, HEIGHT - 40, 400, 32), "vertical_wall": False},
    {"rect": pygame.Rect(3740, HEIGHT - 40, 5000, 32), "vertical_wall": False}, 
    # First 2 floating platforms
    {"rect": pygame.Rect(440, 520, 1, 80), "vertical_wall": True},
    {"rect": pygame.Rect(600, 520, 1, 80), "vertical_wall": True},
    {"rect": pygame.Rect(440, 480, 160, 20), "vertical_wall": False},
    
    {"rect": pygame.Rect(560, 360, 1, 40), "vertical_wall": True},
    {"rect": pygame.Rect(720, 360, 1, 40), "vertical_wall": True},
    {"rect": pygame.Rect(560, 320, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(560, 380, 160, 20), "vertical_wall": False},
    # Brick structure
    {"rect": pygame.Rect(1200, 440, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1280, 360, 40, 200), "vertical_wall": True},
    {"rect": pygame.Rect(1280, 320, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1360, 400, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1320, 400, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1480, 440, 40, 40), "vertical_wall": True},
    {"rect": pygame.Rect(1480, 360, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1400, 440, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1440, 440, 40, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1440, 360, 200, 40), "vertical_wall": False},
    {"rect": pygame.Rect(1600, 360, 40, 200), "vertical_wall": True},
    # Hard Blocks
    {"rect": pygame.Rect(1800, 400, 160, 40), "vertical_wall": False, "vert_top": True},
    {"rect": pygame.Rect(2080, 480, 40, 80), "vertical_wall": True},
    {"rect": pygame.Rect(2080, 440, 40, 40), "vertical_wall": False, "vert_top": True},
    {"rect": pygame.Rect(2400, 480, 40, 80), "vertical_wall": True},
    {"rect": pygame.Rect(2400, 440, 40, 40), "vertical_wall": False, "vert_top": True},
    {"rect": pygame.Rect(2720, 480, 40, 80), "vertical_wall": True},
    {"rect": pygame.Rect(2720, 440, 40, 40), "vertical_wall": False, "vert_top": True},
    {"rect": pygame.Rect(3040, 480, 40, 80), "vertical_wall": True},
    {"rect": pygame.Rect(3040, 440, 40, 40), "vertical_wall": False, "vert_top": True},
    {"rect": pygame.Rect(3760, 480, 40, 80), "vertical_wall": True},
    {"rect": pygame.Rect(3760, 440, 40, 40), "vertical_wall": False, "vert_top": True},

    # Final floating platforms section
    {"rect": pygame.Rect(3880, 480, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4080, 480, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(3880, 440, 200, 20), "vertical_wall": False},
    {"rect": pygame.Rect(3880, 500, 200, 20), "vertical_wall": False},

    {"rect": pygame.Rect(4400, 440, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4600, 440, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4400, 400, 200, 20), "vertical_wall": False},
    {"rect": pygame.Rect(4400, 460, 200, 20), "vertical_wall": False},

    {"rect": pygame.Rect(3920, 240, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4080, 240, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(3920, 200, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(3920, 260, 160, 20), "vertical_wall": False},

    {"rect": pygame.Rect(4120, 400, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4280, 400, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4120, 360, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(4120, 420, 160, 20), "vertical_wall": False},

    {"rect": pygame.Rect(4320, 320, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4480, 320, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4320, 280, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(4320, 340, 160, 20), "vertical_wall": False},

    {"rect": pygame.Rect(4640, 360, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4800, 360, 1, 20), "vertical_wall": True},
    {"rect": pygame.Rect(4640, 320, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(4640, 380, 160, 20), "vertical_wall": False},

    {"rect": pygame.Rect(4840, 260, 1, 320), "vertical_wall": True},
    {"rect": pygame.Rect(5000, 260, 1, 320), "vertical_wall": True},
    {"rect": pygame.Rect(4840, 240, 160, 20), "vertical_wall": False},
    {"rect": pygame.Rect(4840, 540, 160, 20), "vertical_wall": False},
]

# Enemies data
enemies = [
    {"rect": pygame.Rect(600, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": True},
    {"rect": pygame.Rect(840, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(2000, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(2320, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(2640, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(2960, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(4120, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(4240, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
    {"rect": pygame.Rect(4360, 520, 40, 40), "type": "goomba", "vel_x": -2, "vel_y":0, "image": "move1", "state": 0, "destroy_tick": 0, "spawned": False},
]

# Keep a copy to reset to when player is respawned
enemies_orig = enemies.copy()

frame = 0

# Play level music (-1 means forever until it is forcefully stopped)
music.play(-1)

# Game loop
while True:
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

    keys = pygame.key.get_pressed()

    if player_state == "normal":
        # Accelerate player
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            vel_x -= acceleration
            player_dir = 1

            if frame % 20 == 0:
                player_anim_frame = 1
            elif frame % 20 == 10:
                player_anim_frame = 2
                
            set_player_image(f'move{player_anim_frame}')
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            vel_x += acceleration
            player_dir = 0

            if frame % 14 == 0:
                player_anim_frame = 1
            elif frame % 14 == 7:
                player_anim_frame = 2
                
            set_player_image(f'move{player_anim_frame}')
        else:
            # Decelerate when no movement keys are pressed
            if vel_x > 0:
                vel_x -= acceleration
            elif vel_x < 0:
                vel_x += acceleration

        # Ensure vel_x is exactly 0 to avoid drifting
        if math.isclose(vel_x, 0, abs_tol=0.01):
            vel_x = 0

        # Limit player speed
        vel_x = max(-max_speed, min(max_speed, vel_x))

        # Update player position
        player.x += vel_x

        # Jumping
        if not is_jumping:
            if keys[pygame.K_SPACE] or keys[pygame.K_UP]:
                is_jumping = True
                vel_y = player_jump_power
                jump_sound.play()

        if is_jumping:
            set_player_image("jump")
        else:
            if vel_x == 0: # The player is not moving
                set_player_image("idle")

        if vel_y > 1.5: # The player is in the air but aren't jumping.
            set_player_image("fall")

        # Apply gravity
        player.y += vel_y
        vel_y += 0.6

        # Collision with platforms
        for platform_data in platforms:
            platform = platform_data["rect"]

            distance = 8

            if (platform_data["vertical_wall"]):

                platform.x -= distance if player_dir == 0 else -distance

                if player.colliderect(platform): # If the player collides with the platform
                    
                    if platform.colliderect(player.x + vel_x, player.y, player.width, player.height): # Checking whether the collision was indeed horizontal
                        # Moves the player out the way by the x axis and sets their velocity to 0.
                        if vel_x > 0:
                            player.x = platform.left - player.width
                        elif vel_x < 0:
                            player.x = platform.right
                        vel_x = 0

                    # If it wasn't horizontal, collision should be handled as normal.
                    elif vel_y > 0:
                        player.y = platform.y - player.height
                        vel_y = 0
                        is_jumping = False
                    elif vel_y < 0:
                        player.y = platform.y + platform.height
                        vel_y = 0
                
                platform.x += distance if player_dir == 0 else -distance
                
            else:
                if player.colliderect(platform):

                    if platform_data.get('vert_top'): # If the platform is a `vert_top` (explanation below) then make sure it is in line with the vertical platform
                        platform.x -= distance if player_dir == 0 else -distance
                
                    if vel_y > 0:
                        player.y = platform.y - player.height
                        vel_y = 0
                        is_jumping = False
                    elif vel_y < 0:
                        player.y = platform.y + platform.height
                        vel_y = 0

                    if platform_data.get('vert_top'):
                        platform.x += distance if player_dir == 0 else -distance

        # HOW COLLISIONS WORK
        # Normal platforms have normal collisions, but if you touch the side you'll be launched up until you are on the top of the platform.
        # With vertical platforms, the player is stopped in their tracks but cannot stand on them so there is a block at the top (called `vert_top`) to let the player stand normally.


        # Enemies
        for i, enemy_data in enumerate(enemies):
            enemy = enemy_data['rect']

            if enemy_data["spawned"]:
                # Enemy movement

                enemy_data['vel_y'] -= 0.2
                enemy.y -= enemy_data['vel_y']

                enemy.x += enemy_data['vel_x']

                # Enemy platform collisions
                for platform_data in platforms:
                    platform = platform_data["rect"]

                    if (platform_data["vertical_wall"]):

                        distance = 8

                        platform.x -= distance

                        if enemy.colliderect(platform):
                            
                            if platform.colliderect(enemy.x + enemy_data["vel_x"], enemy.y, enemy.width, enemy.height):
                                enemy_data["vel_x"] *= -1

                        
                        platform.x += distance
                        
                    else:
                        if enemy.colliderect(platform):
                        
                            if enemy_data["vel_y"] > 0:
                                enemy.y = platform.y + enemy.height
                                enemy_data["vel_y"] = 0

                                while enemy.colliderect(platform): # To make sure the enemy is fully out of the platform
                                    enemy.y += 1

                            elif enemy_data["vel_y"] < 0:
                                enemy.y = platform.y - platform.height
                                enemy_data["vel_y"] = 0

                                while enemy.colliderect(platform):
                                    enemy.y -= 1
                
                if enemy.colliderect(player) and enemy_data['state'] == 0:
                    if vel_y > 3: # The player was falling so the Goomba should be stomped
                        enemy_data['image'] = "stomp"
                        enemy_data['vel_x'] = 0
                        enemy_data['state'] = 1
                        vel_y = -11
                        stomp_sound.play()
                    else: # The Goomba touched the player so the player should deal damage.
                        frame = 0
                        player_state = "death"
                        pygame.mixer.stop()
                        death_sound.play()

                if enemy_data['state'] == 1: # Stomped state
                    enemy_data['destroy_tick'] += 1

                    if enemy_data['destroy_tick'] >= 30: # After half a second the enemy will disappear so as not to clutter the screen.
                        enemy_data['image'] = 'empty'
                        enemy_data['state'] = 2

                elif enemy_data['state'] == 0: # Default state
                    if frame % 20 == 0:
                        enemy_data['image'] = 'move1'
                    elif frame % 20 == 10:
                        enemy_data['image'] = 'move2'
            else:
                if enemy.x - camera_x < WIDTH + 20: # By default an enemy won't move until it is revealing by scrolling the screen far enough
                    enemy_data['spawned'] = True

        if camera_x > 5550 and player.x > 6021 and player.x < 6133 and player.y < 360: # These coordinates are where the goal box is.
            pygame.mixer.stop()
            goal_sound.play()
            player_state = "goal"

        if player.y > HEIGHT: # If the player falls through a gap in the ground
            frame = 0
            pygame.mixer.stop()
            death_sound.play()
            player_state = "death"
            
        # Calculate the camera's threshold for scrolling
        camera_threshold_left = WIDTH // 4
        camera_threshold_right = 3 * WIDTH // 4 - CAMERA_BUFFER

        # Camera scrolling
        if not camera_x + player.x < camera_threshold_left:
            if player.x > camera_x + camera_threshold_right:
                camera_x = player.x - camera_threshold_right
            elif player.x < camera_x + camera_threshold_left:
                camera_x = player.x - camera_threshold_left
        else:
            camera_x = 0

        if camera_x > 5600: # Make sure the camera doesn't scroll too far.
            camera_x = 5600
            
    elif player_state == "death": # Death animation
        set_player_image('death')

        if frame == 30: # Have a delay for about half a second before sending the player up.
            vel_y = -12

        if frame > 30:
            player.y += vel_y
            vel_y += 0.5

        if frame >= 205:
            enemies = enemies_orig.copy()
            frame = 0

            vel_x = 0
            vel_y = 0

            player.x = PLAYER_START_X
            player.y = 500

            music.play(-1)

            player_state = "normal"

    elif player_state == 'goal': # Goal collect animation

        # Making sure the  player is facing right
        player_dir = 0

        player.y += vel_y

        vel_y += 1
        if vel_y > 7:
            vel_y = 7

        if player.y >= HEIGHT - 80:
            player.y = HEIGHT - 80

            if frame % 20 == 0:
                player_anim_frame = 1
            elif frame % 20 == 10:
                player_anim_frame = 2
                
            set_player_image(f'move{player_anim_frame}')

        player.x += 3

        if player.x - camera_x > WIDTH:
            level_complete = True
    
    # Drawing everything
    screen.fill((156, 252, 240))  # Fill the screen with cyan (to mimic the background)


    for platform in platforms:
        pygame.draw.rect(screen, (255, 0, 0), platform["rect"].move(-camera_x, 0)) # Draw red rectangles to show platform hitboxes (we used this for testing)

    screen.blit(level_image, (0 - camera_x, -3)) # Draw the level image

    # Basically, we have a level image that has all the graphics and then we used the `platforms` list to map out which platforms are solid.

    for enemy in enemies: # Drawing the enemies
        img = pygame.image.load(f'assets/enemies/{enemy["type"]}/{enemy["image"]}.png')
        img = pygame.transform.scale(img, (img.get_width() * 1.25, img.get_height() * 1.25))

        screen.blit(img, (enemy["rect"].x - camera_x, enemy["rect"].y + 3))
    

    screen.blit(pygame.transform.flip(player_image, bool(player_dir), False), (player.x - camera_x, player.y + 3)) # Drawing the player and flipping it based on the direction it is facing.

    if level_complete:
        screen.blit(welldone_text, welldone_rect) # Draw the well done message


    pygame.display.flip()

    frame += 1 # Keep track of frame number for animations.

    # Limit the frame rate
    clock.tick(FPS)

    

# Quit the game
pygame.quit()
sys.exit()
