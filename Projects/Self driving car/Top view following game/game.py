import pygame
import random
import os
import numpy as np
import math

coefs = np.load("coefs.npy",allow_pickle=True)
intercepts = np.load("intercepts.npy",allow_pickle=True)

pygame.init()
pygame.mixer.init()

WIDTH = 1200
HEIGHT = 700
MaxDist = math.sqrt(WIDTH**2 + HEIGHT**2)
FPS = 30
car_acceleration = 2
handling = 0.1
speed_damping = 0.95
max_speed = 10
raycast_resolution = 5 #smaller is more accurate but slower
raycast_angle = 0.785
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()
ai_driving = True
moving_threshold = 0.2
game_folder = os.path.dirname(__file__)
#image_folder = os.path.join(game_folder,"img")

def rotateVector(vec,theta):
    rotationMatrix = [[math.cos(theta),-1*math.sin(theta)],
                    [math.sin(theta),math.cos(theta)]]
    rotationMatrix = np.array(rotationMatrix)
    np_vec = np.array(vec)
    new_vec = np.matmul(rotationMatrix,np_vec)

    return new_vec.tolist()

def rot_center_car(image, rect, angle):
    rot_image = pygame.transform.rotate(pygame.transform.scale(car_sprite,(200,100)), angle*180/(3.14))
    rot_image.set_colorkey((0,0,0))
    pos_x = rect.centerx
    pos_y = rect.centery
    rot_rect = rot_image.get_rect()
    rot_rect.centerx = pos_x
    rot_rect.centery = pos_y
    return rot_image,rot_rect

def rot_center(image, rect, angle):
    orig_img = pygame.Surface((1,MaxDist))
    orig_img.fill((255,0,0))
    orig_img.set_colorkey((0,0,0))
    rot_image = pygame.transform.rotate(orig_img, angle*180/(3.14))
    rot_image.set_colorkey((0,0,0))
    pos_x = rect.centerx
    pos_y = rect.centery
    rot_rect = rot_image.get_rect()
    rot_rect.centerx = pos_x
    rot_rect.centery = pos_y
    return rot_image,rot_rect

class Car(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(car_sprite,(200,100))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = WIDTH/2-100
        self.rect.y = HEIGHT/2-50
        self.speed = 0
        self.forward = [1,0]
        self.mask = pygame.mask.from_surface(self.image)
        self.rot = 0
        self.distTraveled = 0
        self.keys_pressed = [False,False,False,False] # left, right, up, down

    def update(self):
            self.speed *= speed_damping

            if self.keys_pressed[0]:
                self.forward = rotateVector(self.forward,-1*handling)
                self.rot += handling
                self.image,self.rect = rot_center_car(self.image,self.rect,self.rot)
                self.mask = pygame.mask.from_surface(self.image)
            if self.keys_pressed[1]:
                self.forward = rotateVector(self.forward,handling)
                self.rot -= handling
                self.image,self.rect = rot_center_car(self.image,self.rect,self.rot)
                self.mask = pygame.mask.from_surface(self.image)
            if self.keys_pressed[2]:
                self.speed += car_acceleration
            if self.keys_pressed[3]:
                self.speed -= car_acceleration

            if self.speed>max_speed:
                self.speed = max_speed

            if self.speed < -1*max_speed: #test to see if this condition isn't satisfied if cars will drive backward
                self.speed = -1*max_speed
            #self.rect.x += self.speed * self.forward[0]
            #self.rect.y += self.speed * self.forward[1]
            self.distTraveled += abs(self.speed)
            if self.rect.right > WIDTH:
                self.rect.right = WIDTH
            if self.rect.left < 0:
                self.rect.left = 0

    def update_keys(self):
        keystate = pygame.key.get_pressed()
        #self.keys_pressed = [False,False,False,False]
        if keystate[pygame.K_LEFT]:
            self.keys_pressed[0] = True
        if keystate[pygame.K_RIGHT]:
            self.keys_pressed[1] = True
        if keystate[pygame.K_UP]:
            self.keys_pressed[2] = True
        if keystate[pygame.K_DOWN]:
            self.keys_pressed[3] = True

    def get_raycast(self,type,trackGroup):
        forward_vec = None
        if type is "front":
            forward_vec = self.forward
        elif type is "right":
            forward_vec = rotateVector(self.forward,raycast_angle)
        elif type is "left":
            forward_vec = rotateVector(self.forward,-1*raycast_angle)
        totalDist = 0
        speedx = raycast_resolution*forward_vec[0]
        speedy = raycast_resolution*forward_vec[1]
        moving_point = RaycastPoint(self.rect.centerx,self.rect.centery)
        while totalDist<MaxDist:
            #check for collisions
            hits = pygame.sprite.spritecollide(moving_point,trackGroup,False,pygame.sprite.collide_mask)
            if len(hits) > 0:
                current_raycast_points.add(moving_point)
                return math.sqrt((moving_point.rect.x-self.rect.centerx)**2 + (moving_point.rect.y-self.rect.centery)**2)
            #update point position
            moving_point.update(speedx,speedy)
            totalDist += raycast_resolution


        return "no collisions"


class Track(pygame.sprite.Sprite):
    def __init__(self,player_ref):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(track_1,(4000,2000))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.player_ref = player_ref

    def update(self):
        self.rect.x -= self.player_ref.speed*self.player_ref.forward[0]
        self.rect.y -= self.player_ref.speed*self.player_ref.forward[1]

class RaycastPoint(pygame.sprite.Sprite):
    def __init__(self,x_init,y_init):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((10,10))
        self.image.fill((255,0,0))
        self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x = x_init
        self.rect.y = y_init
        self.mask = pygame.mask.from_surface(self.image)

    def update(self,speed_x,speed_y):
        self.rect.x += speed_x
        self.rect.y += speed_y
        self.mask = pygame.mask.from_surface(self.image)

all_sprites = pygame.sprite.Group()
tracks = pygame.sprite.Group()
current_raycast_points = pygame.sprite.Group()

track_1 = pygame.image.load(os.path.join(game_folder,"track_1.png")).convert()
car_sprite = pygame.image.load(os.path.join(game_folder,"car.png")).convert()

player = Car()
collision_test = Track(player)

all_sprites.add(player)
all_sprites.add(collision_test)
tracks.add(collision_test)

game_data = []

running = True
while running:
    clock.tick(FPS)


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #hits = pygame.sprite.spritecollide(player,tracks,False,pygame.sprite.collide_mask)
    #for hit in hits:
    #    print("Collision detected")
    current_raycast_points.empty()
    all_sprites.update()
    results = player.get_raycast("front",tracks)
    data_to_record = [0,0,0]
    if not (results=="no collisions"):
        data_to_record[0] = results
    results = player.get_raycast("right",tracks)
    if not (results=="no collisions"):
        data_to_record[1] = results
    results = player.get_raycast("left",tracks)
    if not (results=="no collisions"):
        data_to_record[2] = results

    player.keys_pressed = [False,False,False,False]
    if ai_driving:
        left_key = sum(np.array(coefs[0])*np.array(data_to_record[0]))+np.array(intercepts[0])
        right_key = sum(np.array(coefs[1])*np.array(data_to_record[1]))+np.array(intercepts[1])
        up_key = sum(np.array(coefs[2])*np.array(data_to_record[2]))+np.array(intercepts[2])
        print(left_key)
        if left_key>moving_threshold:
            player.keys_pressed[0] = True
        if right_key>moving_threshold:
            player.keys_pressed[1] = True
        if up_key>moving_threshold:
            player.keys_pressed[2] = True

    player.update_keys()

    data_to_record += player.keys_pressed
    game_data.append(data_to_record)
    screen.fill((0,0,0))
    all_sprites.draw(screen)
    current_raycast_points.draw(screen)
    pygame.display.flip()
    #running = False
game_data = np.array(game_data)
np.save('data_saved',game_data)
pygame.quit()
