"""
James Bouchat
jbouchat@uvm.edu
CS021

main.py
"""
from methods import *
from asteroid import Asteroid
from missile import Missile
from spaceship import *

##########  START OF MAIN  ##########

if __name__ == "__main__":
    pygame.init()
    # Frames it takes to fire one missile
    time_between_missiles = 30
    # Frames it takes to start a new round
    time_between_rounds = 240
    # Game clock. Used to measure the time between rounds
    iteration_clock = time_between_missiles
    # Players clock. Used to measure the time between 
    # respawning and firing missiles 
    player_clock = 60

    # Font sizes used throughout the game
    font_14 = pygame.font.Font("fonts/arial.ttf", 14)
    font_28 = pygame.font.Font("fonts/arial.ttf", 28)
    font_52 = pygame.font.Font("fonts/arial.ttf", 52)

    # Player and indicator sprites
    player_idle_sprite = pygame.image.load(
        "sprites/spaceship_idle.png")
    player_thrust_sprite = pygame.image.load(
        "sprites/spaceship_thrust.png")
    player_gravity_indicator = pygame.image.load(
        "sprites/spaceship_gravity_indicator.png")

    # Create screen, set width and height to constants
    screen = pygame.display.set_mode([WIDTH, HEIGHT])
    # Set window name
    pygame.display.set_caption("Gravitational Asteroids")
    # Set window icon
    pygame.display.set_icon(player_thrust_sprite)
    clock = pygame.time.Clock()

    # Overall program loop. Program terminates when False
    program_loop = True
    main_menu_loop = True
    # Each value is used to determine which button is selected
    main_menu_buttons = [True, False, False]

    customize_loop = False
    # Each value is used to determine which button is selected
    customize_buttons = [True, False]
    # Used to select the players color
    player_colors = [True, False, False, False, False, False]
    # Used to select the indicators color
    indicator_colors = [True, False, False, False, False, False]
    # All colors available 
    colors = [WHITE, YELLOW, RED, PURPLE, BLUE, GREEN]
    # Used to display what color is selected
    color_strings = ["White", "Yellow", "Red", "Purple", "Blue", "Green"]

    highscore_loop = False

    game_loop = False
    round_started = True
    round_number = 1
    game_over = False

    # Initialize joystick to allow controllers to connect
    pygame.joystick.init()
    # For loop is used to detect how many joysticks 
    # are connected when the game is launched
    joysticks = [pygame.joystick.Joystick(x) 
        for x in range(pygame.joystick.get_count())]

    # PLAYER
    player = Spaceship(player_idle_sprite)
    indicator = Indicator(player_gravity_indicator)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    score = 0
    respawn_clock = 0
    immunity_time = 120
    player_color = WHITE
    indicator_color = WHITE

    # MISSILES
    missile_group = pygame.sprite.Group()

    # ASTEROIDS
    asteroid_1_sprite = pygame.image.load("sprites/asteroid_1.png")
    asteroid_2_sprite = pygame.image.load("sprites/asteroid_2.png")
    asteroid_3_sprite = pygame.image.load("sprites/asteroid_3.png")
    spawn_radius = 100
    number_of_asteroids = 3
    asteroid_group = pygame.sprite.Group()

    # PARTICLES
    particle_group = pygame.sprite.Group()

    ##########  PROGRAM LOOP  ##########
    while program_loop:

        ##########  START OF MENU LOOP  ##########
        while main_menu_loop:
            back = 0
            select = 0
            up = 0
            down = 0
            back, select, up, down = get_joystick_input(joysticks, back,
                select, up, down)

            clock.tick(FPS)
            # Get all key presses per frame
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_loop = False
                    
                if keys[pygame.K_ESCAPE] or back == 1:
                    main_menu_loop = False
                    program_loop = False
                
                if keys[pygame.K_UP] or up == 1:
                    # Move selector up
                    change_button_selection(True, main_menu_buttons)

                if keys[pygame.K_DOWN] or down == 1:
                    # Move selector down
                    change_button_selection(False, main_menu_buttons)

                if keys[pygame.K_RETURN] or select == 1:
                    if main_menu_buttons[0]:
                        game_loop = True
                        main_menu_loop = False

                    elif main_menu_buttons[1]:
                        customize_loop = True
                        main_menu_loop = False

                    elif main_menu_buttons[2]:
                        highscore_loop = True
                        main_menu_loop = False

            screen.fill([0, 0, 0])
            
            create_text(screen, WIDTH // 2, 100, font_52, 
                "Gravitational Asteroids")

            ##### Display all menu text. If the current text is selected,
            ##### add arrows around the text.
            if main_menu_buttons[0]:
                create_text(screen, WIDTH // 2, 300, font_28,
                    ">> Play <<")

            else:
                create_text(screen, WIDTH // 2, 300, font_28,
                    "Play")

            if main_menu_buttons[1]:
                create_text(screen, WIDTH // 2, 500, font_28,
                    ">> Customize <<")

            else:
                create_text(screen, WIDTH // 2, 500, font_28,
                    "Customize")

            if main_menu_buttons[2]:
                create_text(screen, WIDTH // 2, 700, font_28,
                    ">> High Scores <<")

            else:
                create_text(screen, WIDTH // 2, 700, font_28,
                    "High Scores")

            pygame.display.flip()
        ##########  END OF MENU LOOP  ##########


        ##########  START OF CUSTOMIZE LOOP  ##########
        while customize_loop:
            back = 0
            select = 0
            up = 0
            down = 0
            back, select, up, down = get_joystick_input(joysticks, back,
                select, up, down)

            clock.tick(FPS)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_loop = False

                # Exit to main menu
                if keys[pygame.K_ESCAPE] or back == 1:
                    """
                    Update the player and indicator sprites by replacing
                    their current colors with the new selected colors
                    in the customize menu
                    """
                    new_player_color = colors[player_color_index]
                    new_indicator_color = colors[indicator_color_index]
                    var = pygame.PixelArray(player_idle_sprite)
                    var.replace(player_color, new_player_color)
                    var = pygame.PixelArray(player_thrust_sprite)
                    var.replace(player_color, new_player_color)
                    var = pygame.PixelArray(player_gravity_indicator)
                    var.replace(indicator_color, new_indicator_color)

                    player_color = new_player_color
                    indicator_color = new_indicator_color
                    
                    main_menu_loop = True
                    customize_loop = False
                if keys[pygame.K_UP] or up == 1:
                    change_button_selection(True, customize_buttons)

                if keys[pygame.K_DOWN] or down == 1:
                    change_button_selection(False, customize_buttons)

                if keys[pygame.K_RETURN] or select == 1:
                    if customize_buttons[0]:
                        change_button_selection(False, player_colors)

                    if customize_buttons[1]:
                        change_button_selection(False, indicator_colors)


            screen.fill([0, 0, 0])
            
            create_text(screen, WIDTH // 2, 100, font_52, "Customize")

            ##### Display all customize text. If the current text is selected,
            ##### add arrows around the text.
            player_color_index = player_colors.index(True)
            player_color_string = "Player Color: " + str(
                color_strings[player_color_index])
            indicator_color_index = indicator_colors.index(True)
            indicator_color_string = "Indicator Color: " + str(
                color_strings[indicator_color_index])
            
            if customize_buttons[0]:
                create_text(screen, WIDTH // 2, 400, font_28, 
                    ">> " + player_color_string + " <<")

            else:
                create_text(screen, WIDTH // 2, 400, font_28,
                    player_color_string)

            if customize_buttons[1]:
                create_text(screen, WIDTH // 2, 700, font_28,
                    ">> " + indicator_color_string + " <<")

            else:
                create_text(screen, WIDTH // 2, 700, font_28,
                    indicator_color_string)

            pygame.display.flip()
        ##########  END OF CUSTOMIZE LOOP  ##########


        ##########  START OF HIGH SCORE LOOP  ##########
        while highscore_loop:
            back = 0
            select = 0
            up = 0
            down = 0
            back, select, up, down = get_joystick_input(joysticks, back,
                select, up, down)

            clock.tick(FPS)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_loop = False

                # Exit to main menu
                if keys[pygame.K_ESCAPE] or back == 1:
                    main_menu_loop = True
                    highscore_loop = False

            screen.fill([0, 0, 0])

            create_text(screen, WIDTH // 2, 100, font_52, "High Scores")

            with open("highscores.txt", "r") as f:
                """
                Display each high score value in the highscores
                text file.
                """
                score_rank = 1
                y_pos = 250
                for line in f:
                    create_text(screen, WIDTH // 2, y_pos,
                        font_28, str(score_rank) + ":  " + line.strip())
                    y_pos += 150
                    score_rank += 1

                f.close()

            pygame.display.flip()
        ##########  END OF HIGH SCORE LOOP  ##########


        ##########  START OF GAME LOOP  ##########
        while game_loop:
            back = 0
            select = 0
            up = 0
            down = 0
            back, select, up, down = get_joystick_input(joysticks, back,
                select, up, down)

            clock.tick(FPS)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    program_loop = False

                # Exit game loop and enter main menu
                if (keys[pygame.K_RETURN] or
                    keys[pygame.K_ESCAPE] or back == 1):
                    main_menu_loop = True
                    game_loop = False

                    #####  UPDATE HIGH SCORE  #####
                    update_highscore(score)

                    #####  RESET GAME  #####
                    asteroid_group.empty()
                    missile_group.empty()
                    player_group.add(player)
                    number_of_asteroids = 3
                    round_number = 1
                    game_over = False
                    iteration_clock = 0
                    player_clock = 0
                    score = 0

                    player.reset_lives()
                    player.reset()

            screen.fill([0, 0, 0])

            ##########  ASTEROID FUNCTIONS  ##########
            if (len(asteroid_group) == 0 and
                iteration_clock > time_between_rounds):
                iteration_clock = 0

            """
            When a new round starts, spawn in the number of asteroids
            correlated to the variable number_of_asteroids. Asteroids
            won't spawn directly next to the player or other asteroids
            """
            if iteration_clock == time_between_rounds:
                for _ in range(number_of_asteroids):
                    radius = random.randint(30, 35)
                    png = random.choice([
                        asteroid_1_sprite, 
                        asteroid_2_sprite, 
                        asteroid_3_sprite])

                    scale = radius / 16
                    scaled_png = pygame.transform.scale(png, 
                        (32 * scale, 32 * scale))
                    ast = Asteroid(scaled_png)
                    ast.set_radius(radius)
            
                    # Make sure asteroids don't spawn too close to player
                    # or to other asteroids
                    while True:
                        far_enough = True
                        ast.set_position(int(random.random()*WIDTH), 
                                         int(random.random()*HEIGHT))
                        x_distance = ast.x_position - player.x_position
                        y_distance = ast.y_position - player.y_position
                        distance = pythagorean(abs(x_distance),
                                               abs(y_distance))
                        if distance < player.radius * 3:
                            far_enough = False

                        for asteroid1 in asteroid_group:
                            x_distance = ast.x_position - asteroid1.x_position
                            y_distance = ast.y_position - asteroid1.y_position
                            distance = pythagorean(abs(x_distance),
                                                   abs(y_distance))
                            if distance < spawn_radius:
                                far_enough = False
                        
                        if far_enough:
                            break
                    
                    asteroid_group.add(ast)
                number_of_asteroids += 1
                round_number += 1

            """
            Outer for loop makes sure each asteroid:
            1) Checks for collision with the player
                If hit, decrement the players lives and destroy the spaceship
            2) Is affected by gravity from all other asteroids
            3) Checks for collision with all missiles
                If hit, destroy missile and asteroid
            """
            for asteroid1 in asteroid_group:
                # Check for player collision
                if asteroid1.check_spaceship_collision(player_group):
                    """if asteroid1.split == False:
                        score += 10
                        create_particles(asteroid1.x_position, asteroid1.y_position, particle_group)
                        split_asteroid(asteroid1.image, asteroid1.x_position,
                                       asteroid1.y_position, asteroid_group,
                                       player.rotation, asteroid1.radius,
                                       player.acceleration)
                    else:
                        score += 15
                        create_particles(asteroid1.x_position, asteroid1.y_position, particle_group)"""

                    if respawn_clock > immunity_time:
                        respawn_clock = 0
                        player.reset()
                        player_clock = 0
                        if player.decrease_lives():
                            game_over = True
                    player_group.add(player)

                # Update asteroid velocity due to gravitational force
                for asteroid2 in asteroid_group:
                    if asteroid1 != asteroid2:
                        x_distance = asteroid2.x_position - asteroid1.x_position
                        y_distance = asteroid2.y_position - asteroid1.y_position
                        distance = pythagorean(abs(x_distance), abs(y_distance))
                        angle = math.atan2(y_distance, x_distance)
                        force = calculate_gravitational_pull(asteroid1.radius,
                            asteroid2.radius, distance)
                        asteroid1.update_velocity(angle, force)
                
                # Check for collision with missiles
                for missile1 in missile_group:
                    x_distance = missile1.x_position - asteroid1.x_position
                    y_distance = missile1.y_position - asteroid1.y_position
                    distance = pythagorean(abs(x_distance), abs(y_distance))
                    if (asteroid1.check_missile_collision(
                        missile1.radius, distance) and
                        asteroid1.split == False):
                        score += 10
                        create_particles(asteroid1.x_position, asteroid1.y_position, particle_group)
                        split_asteroid(asteroid1.image, asteroid1.x_position,
                                       asteroid1.y_position, asteroid_group,
                                       missile1.rotation, asteroid1.radius,
                                       missile1.speed)
                        asteroid1.destroy_asteroid()
                        missile1.collision()

                    elif (asteroid1.check_missile_collision(
                          missile1.radius, distance) and
                          asteroid1.split == True):
                        create_particles(asteroid1.x_position, asteroid1.y_position, particle_group)
                        score += 15
                        asteroid1.destroy_asteroid()
                        missile1.collision()


            asteroid_group.update() # General update call
            asteroid_group.draw(screen) # Draw asteroids to screen

            ##########  PLAYER FUNCTIONS  ##########
            if not game_over:
                axis_0 = 0
                thrust = 0
                fire = 0
                for i in range(len(joysticks)):
                    axis_0 = round(joysticks[i].get_axis(0), 1)
                    thrust = joysticks[i].get_button(0)
                    fire = joysticks[i].get_button(1)

                # Rotate the player sprite, and change the player sprite
                # if the player is thrusting
                adjusted_player_rotation = 360 - player.rotation
                player_sprite_transformed = pygame.transform.rotate(
                    player_idle_sprite, adjusted_player_rotation)

                if player.thrust(keys, thrust):
                    player_sprite_transformed = pygame.transform.rotate(
                        player_thrust_sprite, adjusted_player_rotation)

                # General update call
                player_group.update(keys, axis_0, player_sprite_transformed)

                # Create and fire a missile
                if (player.fire(keys, fire) and
                    player_clock > time_between_missiles):
                    m = Missile()
                    m.set_position(player.x_position, player.y_position)
                    m.set_rotation(player.rotation)
                    missile_group.add(m)
                    player_clock = 0

                # Change the angle the gravity indicator is pointing to
                # show what direction the player is currently being
                # pulled due to gravity
                for asteroid in asteroid_group:
                    x_distance =  asteroid.x_position - player.x_position
                    y_distance =  asteroid.y_position - player.y_position
                    distance = pythagorean(abs(x_distance), abs(y_distance))
                    angle = math.atan2(y_distance, x_distance)
                    force = calculate_gravitational_pull(asteroid.radius,
                        player.radius, distance)
                    player.update_gravitational_pull(angle, force)
                    indicator.update_gravitational_pull(angle, force)

                indicator.update(player.x_position, player.y_position)
                indicator.clear_vel() # Clear stored velocity

                # Rotate indicator sprite
                adjusted_indicator_rotation = 360 - indicator.rotation
                player_gravity_indicator_transformed = pygame.transform.rotate(
                    player_gravity_indicator, adjusted_indicator_rotation)

                # Draw indicator sprite to screen
                # If there's no asteroids, don't show indicator
                if len(asteroid_group) > 0:
                    screen.blit(player_gravity_indicator_transformed, 
                        (indicator.x_position -
                        player_gravity_indicator_transformed.get_width() / 2,
                        indicator.y_position -
                        player_gravity_indicator_transformed.get_height() / 2))

                # Draw player sprite to screen
                screen.blit(player_sprite_transformed,
                    (player.x_position -
                    player_sprite_transformed.get_width() / 2,
                    player.y_position -
                    player_sprite_transformed.get_height() / 2))

            ##########  MISSILE FUNCTIONS  ##########

            missile_group.update()
            missile_group.draw(screen)

            ##########  PARTICLE FUNCTIONS  ##########

            particle_group.update()
            particle_group.draw(screen)

            ##########  FONT FUNCTIONS  ##########
            display_text = "Lives: "
            create_text(screen, 100, 100, font_28, display_text +
                str(player.lives))
            display_text = "Score: "
            create_text(screen, 100, 150, font_28, display_text +
                str(score))

            if iteration_clock < time_between_rounds and round_started:
                display_text = 'Round ' + str(round_number)
                create_text(screen, WIDTH // 2, HEIGHT // 2,
                    font_28, display_text)

            if game_over:
                create_text(screen, WIDTH // 2, HEIGHT // 2, font_28,
                    "Game Over")
                create_text(screen, WIDTH // 2, HEIGHT // 2 + 50, font_14,
                    "Press Enter or Select to Return to Menu")

            ##########  CLOCK FUNCTIONS  ##########
            player_clock += 1
            respawn_clock += 1

            # Don't let iteration_clock become too big
            if iteration_clock < 10000:
                iteration_clock += 1
            else:
                iteration_clock = 0 

            pygame.display.flip()
        ##########  END OF GAME LOOP  ##########
    ##########  END OF PROGRAM LOOP  ##########
########## END OF MAIN ##########
