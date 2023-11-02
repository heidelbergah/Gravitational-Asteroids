"""
James Bouchat
jbouchat@uvm.edu
CS021

spaceship.py
"""

from methods import *

##########  SPACESHIP CLASS  ##########
class Spaceship(pygame.sprite.Sprite):
    def __init__(self, imagepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagepath
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.lives = 5
        self.x_position = WIDTH / 2
        self.y_position = HEIGHT / 2
        self.x_velocity = 0
        self.y_velocity = 0
        self.radius = 75
        self.acceleration = 0.1
        self.drag = 0.1
        self.max_speed = 3
        self.rotation = 0
        self.rotation_speed = 4
        self.max_force = 4


    def reset(self):
        self.x_position = WIDTH / 2
        self.y_position = HEIGHT / 2
        self.x_velocity = 0
        self.y_velocity = 0
        self.rotation = 0


    def reset_lives(self):
        self.lives = 5


    def set_rect(self):
        self.rect.center = (self.x_position, self.y_position)


    def rotate(self, keys, axis):
        if keys[pygame.K_a]:
            self.rotation -= self.rotation_speed
        if keys[pygame.K_d]:
            self.rotation += self.rotation_speed

        if axis < 0:
            self.rotation += self.rotation_speed * axis
        if axis > 0:
            self.rotation += self.rotation_speed * axis

        if self.rotation < 0:
            temp = 360
            temp += self.rotation
            self.rotation = temp
        elif self.rotation > 360:
            self.rotation = self.rotation - 360


    def thrust(self, keys, thrust):
        if keys[pygame.K_w] or thrust == 1:
            self.x_velocity += math.cos(degrees_to_radians(
                self.rotation)) * self.acceleration
            self.y_velocity += math.sin(degrees_to_radians(
                self.rotation)) * self.acceleration
            return True
        else:
            self.x_velocity *= 0.99
            self.y_velocity *= 0.99
            return False


    def fire(self, keys, fire):
        if keys[pygame.K_SPACE] or fire == 1:
            return True
        else:
            return False


    def keep_on_screen(self):
        if self.x_position > WIDTH:
            self.x_position = 0
        elif self.x_position < 0:
            self.x_position = WIDTH

        if self.y_position > HEIGHT:
            self.y_position = 0
        elif self.y_position < 0:
            self.y_position = HEIGHT


    def update_position(self):
        self.x_position += self.x_velocity
        self.y_position += self.y_velocity
        self.keep_on_screen()


    def update_gravitational_pull(self, angle_, force_):
        if force_ < self.max_force:
            self.x_velocity += math.cos(angle_) * force_
            self.y_velocity += math.sin(angle_) * force_
        else:
            self.x_velocity += math.cos(angle_) * self.max_force
            self.y_velocity += math.sin(angle_) * self.max_force


    def update(self, keys, axis, imagepath):
        self.rotate(keys, axis)   
        self.update_position()
        self.keep_on_screen()
        self.set_rect()
        self.set_sprite(imagepath)


    def decrease_lives(self):
        self.lives -= 1
        if self.lives <= 0:
            self.lives = 0
            return True
        return False


    def set_sprite(self, imagepath):
        self.image = imagepath


##########  INDICATOR CLASS  ##########
class Indicator(pygame.sprite.Sprite):
    def __init__(self, imagepath):
        pygame.sprite.Sprite.__init__(self)
        self.image = imagepath
        self.rect = self.image.get_rect()
        self.x_position = 0
        self.y_position = 0
        self.rotation = 0
        self.x_vel = 0
        self.y_vel = 0
        self.alpha = 0


    def set_rect(self):
        self.rect.center = (self.x_position, self.y_position)


    def update_position(self, x_pos, y_pos):
        self.x_position = x_pos
        self.y_position = y_pos


    def update_rotation(self):
        """
        Use the x and y velocities being applied to the player
        to find the angle the player is being pulled due to gravity
        """
        angle = math.atan2(self.y_vel, self.x_vel)
        self.rotation = radians_to_degrees(angle)


    def update_gravitational_pull(self, angle_, force_):
        self.x_vel += math.cos(angle_) * force_
        self.y_vel += math.sin(angle_) * force_


    def update(self, x_pos, y_pos):
        self.update_position(x_pos, y_pos)
        self.update_rotation()
        self.set_rect()


    def clear_vel(self):
        self.x_vel = 0
        self.y_vel = 0