"""
James Bouchat
jbouchat@uvm.edu
CS021

particle.py
"""

from methods import *

class Particle(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/particle.png').convert_alpha()
        self.alpha = 255
        self.rect = self.image.get_rect()
        self.speed = 4
        self.timer = random.randint(25, 30)
        self.x_position = 0
        self.y_position = 0
        self.rotation = 0
        self.alpha_decrease = 255 / self.timer
        self.x_velocity = math.cos(degrees_to_radians(
            self.rotation)) * self.speed
        self.y_velocity = math.sin(degrees_to_radians(
            self.rotation)) * self.speed


    def decrease_timer(self):
        self.alpha -= self.alpha_decrease
        self.image.set_alpha(self.alpha)
        self.timer -= 1
        if self.timer == 0:
            return True
        return False


    def set_rect(self):
        self.rect.center = (self.x_position, self.y_position)


    def update_position(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity


    def update(self):
        self.set_rect()
        self.update_position()
        if self.decrease_timer():
            self.kill()


    def set_position(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position


    def set_rotation(self, rotation):
        self.rotation = rotation
        self.x_velocity = math.cos(degrees_to_radians(rotation)) * self.speed
        self.y_velocity = math.sin(degrees_to_radians(rotation)) * self.speed