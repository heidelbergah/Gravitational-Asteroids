"""
James Bouchat
jbouchat@uvm.edu
CS021

missile.py
"""

from methods import *

class Missile(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('sprites/missile.png')
        self.rect = self.image.get_rect()
        self.speed = 10
        self.x_position = 0
        self.y_position = 0
        self.rotation = 0
        self.radius = 1
        self.x_velocity = math.cos(degrees_to_radians(
            self.rotation)) * self.speed
        self.y_velocity = math.sin(degrees_to_radians(
            self.rotation)) * self.speed


    def set_rect(self):
        self.rect.center = (self.x_position, self.y_position)


    def update_position(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity


    def delete(self):
        """
        If missile goes off screen, remove from group
        """
        if self.x_position > WIDTH:
            self.kill()
        elif self.x_position < 0:
            self.kill()

        if self.y_position > HEIGHT:
            self.kill()
        elif self.y_position < 0:
            self.kill()


    def collision(self):
        self.kill()


    def update(self):
        self.delete()
        self.set_rect()
        self.update_position()


    def set_position(self, x_position, y_position):
        self.x_position = x_position
        self.y_position = y_position


    def set_rotation(self, rotation):
        self.rotation = rotation
        self.x_velocity = math.cos(degrees_to_radians(rotation)) * self.speed
        self.y_velocity = math.sin(degrees_to_radians(rotation)) * self.speed