"""
James Bouchat
jbouchat@uvm.edu
CS021

asteroid.py
"""

from methods import *

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, imagepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagepath
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.x_position = 0
        self.y_position = 0
        self.x_velocity = 0
        self.y_velocity = 0
        self.radius = 0
        self.max_force = 4
        self.split = False


    def set_rect(self):
        self.rect.center = (self.x_position, self.y_position)


    def update_split(self, split_):
        self.split = split_


    def update_position(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity


    def update_velocity(self, angle_, force_):
        if force_ < self.max_force:
            self.x_velocity += math.cos(angle_) * force_
            self.y_velocity += math.sin(angle_) * force_
        else:
            self.x_velocity += math.cos(angle_) * self.max_force
            self.y_velocity += math.sin(angle_) * self.max_force


    def check_missile_collision(self, radius_, distance_):
        """
        Check to see if a missile is colliding with
        the asteroid
        """
        if self.radius + radius_ > distance_:
            return True
        return False


    def check_spaceship_collision(self, player_group):
        """
        This will result in checking for pixel perfect collision between
        the player and asteroid
        """
        hit = pygame.sprite.spritecollide(self, player_group, True, 
                                          pygame.sprite.collide_mask)
        if len(hit) == 1:
            return True
        return False

    def destroy_asteroid(self):
        """
        Remove asteroid from group
        """
        self.kill()

    def keep_on_screen(self):
        """
        If the player moves off screen, set the position
        to the opposite end of the screen
        """
        if self.x_position > WIDTH:
            self.x_position = 0
        elif self.x_position < 0:
            self.x_position = WIDTH

        if self.y_position > HEIGHT:
            self.y_position = 0
        elif self.y_position < 0:
            self.y_position = HEIGHT


    def update(self):
        """
        General update function called in main
        """
        self.update_position()
        self.keep_on_screen()
        self.set_rect()


    def set_radius(self, radius_):
        self.radius = radius_


    def set_position(self, x_pos, y_pos):
        self.x_position = x_pos
        self.y_position = y_pos


    def set_velocity(self, x_vel, y_vel):
        self.x_velocity = x_vel
        self.y_velocity = y_vel


    def set_color(self, r_, g_, b_):
        self.r = r_
        self.g = g_
        self.b = b_