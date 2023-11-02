"""
James Bouchat
jbouchat@uvm.edu
CS021

methods.py
"""

import math
import random
import pygame

WIDTH = 1920
HEIGHT = 1080
FPS = 60
GRAVITATIONAL_CONSTANT = 6.6743e-11
SPEED_MULTIPLIER = 10000000000

WHITE = (255, 255, 255)
YELLOW = (255, 206, 11)
RED = (232, 63, 104)
PURPLE = (171, 62, 143)
BLUE = (0, 146, 214)
GREEN = (0, 169, 137)


def degrees_to_radians(degrees):
    """
    Converts degrees to radians
    """
    return degrees * math.pi / 180


def radians_to_degrees(radians):
    """
    Converts radians to degrees
    """
    return radians * 180 / math.pi


def calculate_gravitational_pull(mass1, mass2, distance_):
    """
    Newtons law of universal gravitation. This is used for
    applying a force on the asteroids and player.
    """
    return (GRAVITATIONAL_CONSTANT * (
        (mass1 * mass2) / (distance_ ** 2))) * SPEED_MULTIPLIER


def pythagorean(a, b):
    """
    Pythagoreans theorem used to calculate the hypotenuse of
    a triangle. This is used to find the distance between two
    object positions.
    """
    return math.sqrt(a ** 2 + b ** 2)


def adjust_rotation(rotation):
    """
    Keep the rotational value on the interval [0, 360).
    """
    if rotation < 0:
            temp = 360
            temp += rotation
            rotation = temp
    elif rotation >= 360:
        rotation = rotation - 360
    return rotation


def split_asteroid(image, x_pos, y_pos, group, rotation, radius, force):
    """
    When an asteroids whose split flag is false is hit by a missile,
    create 2 new asteroids whose velocities are opposite of eachother.
    The asteroids will also spawn with their split flag as true, and
    their radii is half that of the parent asteroid.
    """
    from asteroid import Asteroid

    adjusted_radius = radius // 2
    scale = adjusted_radius / 16
    adjusted_image = pygame.transform.scale(image, (32 * scale, 32 * scale))

    a1 = Asteroid(adjusted_image)
    a2 = Asteroid(adjusted_image)
    
    x_pos_offset = random.choice([-12, -16, -20, 12, 16, 20])
    y_pos_offset = random.choice([-12, -16, -20, 12, 16, 20])
    a1.set_position(x_pos, y_pos)
    a2.set_position(x_pos + x_pos_offset, y_pos + y_pos_offset)
    
    opposing_rotation_1 = adjust_rotation((rotation + 90))
    opposing_rotation_2 = adjust_rotation((opposing_rotation_1 + 180))
    
    # Update opposite velocities
    a1.update_velocity(opposing_rotation_1, force)
    a2.update_velocity(opposing_rotation_2, force)
    
    a1.set_radius(adjusted_radius)
    a2.set_radius(adjusted_radius)
    
    a1.update_split(True)
    a2.update_split(True)
    
    group.add(a1)
    group.add(a2)


def create_text(screen, x_pos, y_pos, font, display_text):
    """
    Display text with a specified x and y position, font, and text.
    """
    text = font.render(display_text, True, (255, 255, 255), (0, 0, 0))
    textRect = text.get_rect()
    textRect.center = (x_pos, y_pos)
    screen.blit(text, textRect)


def change_button_selection(increment, buttons):
    """
    In a list of boolean values, either move the boolean with the
    value True up one index or down one index. If the True boolean 
    is of index 0, move it to the last index, and vice versa.
    """
    if increment:
        for i in range(len(buttons)):
            if buttons[0] == True:
                buttons[0] = False
                buttons[-1] = True
                break
            elif buttons[i] == True:
                buttons[i] = False
                buttons[i-1] = True
                break
    else:
        for i in range(len(buttons)):
            if buttons[-1] == True:
                buttons[-1] = False
                buttons[0] = True
                break
            elif buttons[i] == True:
                buttons[i] = False
                buttons[i+1] = True
                break


def update_highscore(new_score):
    """
    Update the text file which holds 5 high scores.
    If the most recently played games high score is
    higher than that of one or more scores in the text
    file, add the score to the file, sort it, reverse it
    to keep the scores descending, and remove the lowest score.
    This places the new high score in its correct position
    and removes the lowest score from the text file.
    """
    scores = []
    with open("highscores.txt", "r") as f:
        for i in f:
            scores.append(int(i))
        f.close()

    scores.append(new_score)
    scores.sort()
    scores.reverse()
    scores.pop()

    with open("highscores.txt", "w") as f:
        for score in scores:
            f.write(f'{str(score)}\n')
        f.close()



def get_joystick_input(joysticks, back = 0, select = 0, up = 0, down = 0):
    """
    Get input from any connected controller and update the
    variables associated with back, select, up, and down in
    their respected loop.
    """
    for i in range(len(joysticks)):
        back = joysticks[i].get_button(10)
        select = joysticks[i].get_button(11)
        up = joysticks[i].get_button(7)
        down = joysticks[i].get_button(6)

    return (back, select, up, down)


def create_particles(x_position, y_position, group):
    from particle import Particle
    particles = random.randint(8, 20)

    for _ in range(particles):
        particle = Particle()
        particle.set_position(x_position, y_position)
        particle.set_rotation(random.randint(0, 359))
        group.add(particle)
