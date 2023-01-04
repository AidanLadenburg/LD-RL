from distutils.log import info
from turtle import speed
import pygame
from pygame.surfarray import array3d, array2d
import random
import sys
import numpy as np
import time
import gym
from gym import spaces
import math
import cv2

class ld_env(gym.Env):
    def __init__(self):
        super(ld_env, self).__init__()
        global fspeed
        global challenge
        self.games_played = -1
        self.lasers_dodged = 0
        fspeed = 60
        challenge = 250 #higher the easier
        self.highscore = 0
        self.last_10 = []
        self.last_10_jumped = []
        self.last_10_dodged = []
        self.save_num = 30
        self.reward = 0
        self.lasers_jumped = 0
        self.history = []
        for i in range(0, 6):
            self.history.append(np.zeros((128, 128)))
        self.action_space = spaces.Discrete(4)
        #self.prev_move1 = 4
        #self.prev_move2 = 4
        self.add_reward = 10
        self.draw_stuff = True
        self.prints = False
        self.shoot_list =  [True, True, True, True, True, True] #[True, False, False, False, False, False]
        self.observation_space = spaces.Box(low=0, high=1,
                                            shape=(15,), dtype=np.float32)
    
    def step(self, action):
        #print(action)
        #self.prev_move2 = self.prev_move1
        #self.prev_move1 = action
        #action = random.randint(0,3)
        #action = 0
        global fspeed
        global challenge
        self.clock.tick(fspeed)
        self.char.handle_keys(action)

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_g:
                    fspeed = 60
                if event.key == pygame.K_s:
                    if fspeed > 10:
                        fspeed -= 10
                if event.key == pygame.K_d:
                    fspeed += 10
                if event.key == pygame.K_UP:
                    fspeed += 60
                if event.key == pygame.K_DOWN:
                    if fspeed > 60:
                        fspeed -= 60
                if event.key == pygame.K_w:
                    fspeed = 1
                if event.key == pygame.K_j:
                    if challenge > 10:
                        challenge -= 10
                if event.key == pygame.K_l:
                    challenge += 10
                if event.key == pygame.K_q:
                    fspeed = 0     
                if event.key == pygame.K_KP1:
                    self.shoot_list[0] = False if self.shoot_list[0] == True else True
                if event.key == pygame.K_KP3:
                    self.shoot_list[1] = False if self.shoot_list[1] == True else True  
                if event.key == pygame.K_KP4:
                    self.shoot_list[2] = False if self.shoot_list[2] == True else True  
                if event.key == pygame.K_KP6:
                    self.shoot_list[3] = False if self.shoot_list[3] == True else True  
                if event.key == pygame.K_KP7:
                    self.shoot_list[4] = False if self.shoot_list[4] == True else True  
                if event.key == pygame.K_KP9:
                    self.shoot_list[5] = False if self.shoot_list[5] == True else True
                if event.key == pygame.K_KP5:
                    if all(self.shoot_list):
                        self.shoot_list = [False, False, False, False, False, False]
                    else:
                        self.shoot_list = [True, True, True, True, True, True]
                if event.key == pygame.K_t:
                    if self.draw_stuff == True:
                        self.draw_stuff = False  
                    else: 
                        self.draw_stuff = True
                if event.key == pygame.K_p:
                    self.prints = True if self.prints == False else False
        self.screen.fill((255,255,255))
        self.char.draw(self.lasers)
        for l in self.lasers:
            l.draw(self.shoot_list)

        if self.draw_stuff:
            pygame.draw.rect(self.screen, (0,0,0), (self.char.x, self.char.y, self.char.w, self.char.h))
            for l in self.lasers:
                pygame.draw.rect(self.screen, (0,0,0), (l.x, l.y, l.w, l.h))
            
            #cvimage = self.pre_processing(array3d(pygame.display.get_surface()))

            cscore = self.font.render("Score: " + str(self.char.score), True, (0,0,0))
            hscore = self.font.render("High Score: " + str(self.highscore), True, (0,0,0))
            fps = self.font_small.render("FPS: " + str(fspeed), True, (0,0,0))
            avg_10 = self.font.render(f"Last {self.save_num} AVG: " + str(int(sum(self.last_10)/max(len(self.last_10), 1))), True, (0,0,0))
            creward = self.font_small.render("Reward: " + str(self.reward), True, (0,0,0))
            minmax = self.font_small.render("    Min: " + str(min(self.last_10) if len(self.last_10) > 0 else 0) + "   Max: " + str(max(self.last_10) if len(self.last_10) > 0 else 0), True, (0,0,0))
            dif = self.font_small.render("Difficulty: " + str(challenge), True, (0,0,0))
            laser_jumps = self.font_small.render("Lasers Jumped: " + str(self.lasers_jumped), True, (0,0,0))
            laser_dodges = self.font_small.render("Lasers Dodged: " + str(self.lasers_dodged), True, (0,0,0))
            avg_10_jumped = self.font_small.render(f"Last {self.save_num} AVG Jumped: " + str(int((sum(self.last_10_jumped)/max(len(self.last_10_jumped), 1)*100))/100), True, (0,0,0))
            avg_10_dodged = self.font_small.render(f"Last {self.save_num} AVG Dodged: " + str(int((sum(self.last_10_dodged)/max(len(self.last_10_dodged), 1)*100))/100), True, (0,0,0))
            g_played = self.font_small.render("Games Played: " + str(self.games_played), True, (0,0,0))
            
            self.screen.blit(hscore, (20, 0))
            self.screen.blit(avg_10, ((screen_w/2) - 90, 0))
            self.screen.blit(cscore, (screen_w - 190,0))
            
            self.screen.blit(creward, (20, 35))
            self.screen.blit(minmax, ((screen_w/2) - 90, 35))
            self.screen.blit(fps, (screen_w - 190, 35))
            
            self.screen.blit(laser_jumps, (20, 60))
            self.screen.blit(avg_10_jumped, ((screen_w/2) - 90, 60))
            self.screen.blit(dif, (screen_w - 190, 60))

            self.screen.blit(laser_dodges, (20, 85))
            self.screen.blit(avg_10_dodged, ((screen_w/2) - 90, 85))
            self.screen.blit(g_played, (screen_w - 190, 85))
        
        #old obs
        self.laser_xs = []
        self.laser_dists = []
        self.laser_deltas = []
        for l in self.lasers:
            dist = 0      
            if l.shooting and not l.passed:
                self.laser_xs.append(l.x)
                if ((self.char.y + self.char.h) <= l.y) and (((self.char.x >= l.x) and (self.char.x <= (l.x + l.w))) or ((((self.char.x + self.char.w) >= (l.x)) and ((self.char.x + self.char.w) <= (l.x + l.w))))): #above
                    #print('above above')
                    dist = l.y - (self.char.y + self.char.h)
                    self.laser_deltas.append(0)
                    self.laser_deltas.append((self.char.y + self.char.h) - l.y)
                elif ((self.char.y) >= l.y) and (((self.char.x >= l.x) and (self.char.x <= (l.x + l.w))) or ((((self.char.x + self.char.w) >= (l.x)) and ((self.char.x + self.char.w) <= (l.x + l.w))))): #under
                    #print('under under')
                    dist = self.char.y - (l.y + l.h)
                    self.laser_deltas.append(0)
                    self.laser_deltas.append(dist)
                elif (self.char.x >= (l.x + l.w)) and (self.char.y <= (l.y + l.h)) and ((self.char.y + self.char.h) >= l.y): #Right
                    #print('right right')
                    dist = self.char.x - (l.x + l.w)
                    self.laser_deltas.append((l.x + l.w) - self.char.x)
                    self.laser_deltas.append(0)
                elif ((self.char.x + self.char.w) <= l.x) and (self.char.y <= (l.y + l.h)) and ((self.char.y + self.char.h) >= l.y): #left
                    #print('left left')
                    dist = l.x - (self.char.x + self.char.w)
                    self.laser_deltas.append(dist)
                    self.laser_deltas.append(0)   
                elif ((self.char.y + self.char.h) <= l.y) and (self.char.x >= (l.x + l.w)):
                    #print('top right')
                    self.laser_deltas.append((l.x + l.w) - self.char.x)
                    self.laser_deltas.append((self.char.y + self.char.h) - l.y)
                    dist = int(math.sqrt((((l.x + l.w) - self.char.x)**2) + (((self.char.y + self.char.h) - l.y)**2)))
                elif ((self.char.y + self.char.h) <= l.y) and ((self.char.x + self.char.w) <= l.x):
                    #print('top left')
                    self.laser_deltas.append(l. x - (self.char.x + self.char.w))
                    self.laser_deltas.append((self.char.y + self.char.h) - l.y)
                    dist = int(math.sqrt(((l. x - (self.char.x + self.char.w))**2) + (((self.char.y + self.char.h) - l.y)**2)))
                elif (self.char.y >= (l.y + l.h)) and (self.char.x >= (l.x + l.w)):
                    #print('bottom right')
                    self.laser_deltas.append((l.x + l.w) - self.char.x)
                    self.laser_deltas.append(self.char.y - (l.y + l.h))
                    dist = int(math.sqrt((((l.x + l.w) - self.char.x)**2) + ((self.char.y - (l.y + l.h))**2)))
                elif (self.char.y >= (l.y + l.h)) and ((self.char.x + self.char.w) <= l.x):
                    #print('bottom left')
                    self.laser_deltas.append(l.x - (self.char.x + self.char.w))
                    self.laser_deltas.append(self.char.y - (l.y + l.h))
                    dist = int(math.sqrt(((l.x - (self.char.x + self.char.w))**2) + ((self.char.y - (l.y + l.h))**2)))
                else:
                    #print('oh no')
                    self.laser_deltas.append(0)
                    self.laser_deltas.append(0)
                    dist = 0
            else:
                #print('Not Active')
                self.laser_deltas.append(10000)
                self.laser_deltas.append(10000)
                dist = 10000
                self.laser_xs.append(10000)
            for i in range(len(self.laser_deltas)):
                self.laser_deltas[i] = int(self.laser_deltas[i])
            
            dist = max(0, dist)
            self.laser_dists.append(int(dist))
        
        
        if self.char.score > self.highscore:
            self.highscore = self.char.score
        
        self.reward = 0
        #self.total_reward = self.char.score
        #self.reward = self.total_reward - self.prev_reward + 1
        #self.prev_reward = self.total_reward
        if action == 0:
            self.reward -= 1

        if self.char.dead:
            if len(self.last_10) < self.save_num:
                self.last_10.append(self.char.score)
            if len(self.last_10_jumped) < self.save_num:
                self.last_10_jumped.append(self.lasers_jumped)
            if len(self.last_10_dodged) < self.save_num:
                self.last_10_dodged.append(self.lasers_dodged)
            else:
                del self.last_10[0]
                del self.last_10_jumped[0]
                del self.last_10_dodged[0]
                self.last_10.append(self.char.score)
                self.last_10_jumped.append(self.lasers_jumped)
                self.last_10_dodged.append(self.lasers_dodged)
            self.done = True
        

        #Handle Rewards
        for l in self.lasers:
            if self.shoot_list[l.num]:
                if l.side == 'left':
                    if ((l.x > (self.char.x + self.char.w)) and (l.y > (self.char.y + self.char.h)) and l.passed == False) and l.shooting:
                        #print('above left')
                        self.reward += self.add_reward * 5
                        self.lasers_jumped += 1
                        self.lasers_dodged += 1
                        self.add_reward += 2
                        l.passed = True
                    elif ((l.x > (self.char.x + self.char.w)) and (l.y < (self.char.y + self.char.h)) and l.passed == False) and l.shooting:
                        #print('below left')
                        self.reward += self.add_reward
                        self.lasers_dodged += 1
                        l.passed = True
                if l.side == 'right':
                    if ((l.x + l.w) < self.char.x) and (l.y > (self.char.y + self.char.h)) and (l.passed == False) and l.shooting:
                        #print('above right')
                        self.reward += self.add_reward * 5
                        self.lasers_jumped += 1
                        self.lasers_dodged += 1
                        self.add_reward += 2
                        l.passed = True
                    elif ((l.x + l.w) < self.char.x) and (l.y < (self.char.y + self.char.h)) and (l.passed == False) and l.shooting:
                        #print('below right')
                        self.reward += self.add_reward
                        self.lasers_dodged += 1
                        l.passed = True
        
        for l in self.lasers:    
            if l.shooting and not l.passed and not l.leaped:
                if ((self.char.y + self.char.h) <= l.y) and (((self.char.x >= l.x) and (self.char.x <= (l.x + l.w))) or ((((self.char.x + self.char.w) >= (l.x)) and ((self.char.x + self.char.w) <= (l.x + l.w))))):
                    self.reward += 3
                    print('OVER!!!!!')
                    l.leaped = True


        if self.done:
            self.reward = -500
        
        info = {}

        """for i in range(len(self.laser_dists)):
            self.laser_dists[i] **= 3
            self.laser_dists[i] /= 100
        for i in range(len(self.laser_deltas)):
            self.laser_deltas[i] **= 3
            self.laser_deltas[i] /= 100"""

        """for i in range(len(self.laser_dists)):
            if self.laser_dists[i] >= 0:
                self.laser_dists[i] = self.laser_dists[i]**(1/2)
            else:
                self.laser_dists[i] = -1*((self.laser_dists[i]*-1)**(1/4))
            self.laser_dists[i] *= 500
        for i in range(len(self.laser_deltas)):
            if self.laser_deltas[i] >= 0:
                self.laser_deltas[i] = self.laser_deltas[i]**(1/3)
            else:
                self.laser_deltas[i] = -1*((self.laser_deltas[i]*-1)**(1/4))
            self.laser_deltas[i] *= 500"""
        
        observation = [int(self.char.db), int(self.char.x+30), int(self.char.y+60)] + self.laser_deltas #+ self.laser_xs  + self.laser_dists    self.prev_move2,
        #observation = self.laser_deltas
        #print(action) 
        #if self.prints:
        #    print(observation)
        observation = np.array(observation)

        pygame.display.update()
        #self.reward *= -1

        ###cvimage = self.pre_processing(array3d(pygame.display.get_surface()))
        """if self.prints:
            cv2.imshow('obs space', cvimage)
            print(cvimage)"""
        
        return observation, self.reward, self.done, info
    
    def reset(self):
        self.games_played += 1
        global screen_w
        global screen_h
        global laser_ys
        screen_w = 900
        screen_h = 570
        laser_ys = [540, 420, 310]
        self.lasers_jumped = 0
        self.lasers_dodged = 0
        self.add_reward = 10

        pygame.init()
    
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)
        pygame.display.set_caption('Laser Dodge')

        self.char = ninja()
        self.char.reset()
        self.lasers = []
        i = -1
        for y in laser_ys:
            i+=1
            self.lasers.append(laser(y, 'left', i))
            i+=1
            self.lasers.append(laser(y, 'right', i))
        
        self.font = pygame.font.SysFont('didot.ttc', 45)
        self.font_small = pygame.font.SysFont('didot.ttc', 27)

        #self.prev_reward = 0
        self.done = False
        
        #old obs
        self.laser_xs = []
        self.laser_dists = []
        self.laser_deltas = []
        for l in self.lasers:
            l.draw(self.shoot_list)
            dist = 0      
            self.laser_deltas.append(10000)
            self.laser_deltas.append(10000)
            dist = 10000
            self.laser_xs.append(10000)
            for i in range(len(self.laser_deltas)):
                self.laser_deltas[i] = int(self.laser_deltas[i])
            
            self.laser_dists.append(int(dist))

        """for i in range(len(self.laser_dists)):
           self.laser_dists[i] **= 3
           self.laser_dists[i] /= 100
        for i in range(len(self.laser_deltas)):
            self.laser_deltas[i] **= 3
            self.laser_deltas[i] /= 100"""
        
        """for i in range(len(self.laser_dists)):
            if self.laser_dists[i] >= 0:
                self.laser_dists[i] = self.laser_dists[i]**(1/2)
            else:
                self.laser_dists[i] = -1*((self.laser_dists[i]*-1)**(1/4))
            self.laser_dists[i] *= 500
        for i in range(len(self.laser_deltas)):
            if self.laser_deltas[i] >= 0:
                self.laser_deltas[i] = self.laser_deltas[i]**(1/3)
            else:
                self.laser_deltas[i] = -1*((self.laser_deltas[i]*-1)**(1/4))
            self.laser_deltas[i] *= 500"""

        
        observation = [int(self.char.db), int(self.char.x+30), int(self.char.y+60)] + self.laser_deltas #+ self.laser_xs  + self.laser_dists    self.prev_move2,
        #observation = self.laser_deltas
        #print(observation, 'RESET')
        observation = np.array(observation)

        #cvimage = self.pre_processing(array3d(pygame.display.get_surface()))
        return observation
    
    def pre_processing(self, image):
        image = cv2.cvtColor(cv2.resize(image, (128, 128)), cv2.COLOR_BGR2GRAY)
        _, image = cv2.threshold(image, 1, 255, cv2.THRESH_BINARY)
        image = image / 255
        del self.history[0]
        self.history.append(image)
        image = np.concatenate((self.history[-5], self.history[-3], image), axis=0)
        image = np.expand_dims(image, axis=-1)
        return image

class ninja():
    def __init__(self):
        self.h = 120
        self.w = 60
        self.x = (screen_w/2) - (self.w/2)
        self.y = screen_h - self.h
        self.left = 0
        self.right = 0
        self.db = True
        self.vel = 0
        self.score = 0
        self.dead = False
        
    def move(self, direction=None):
        if direction == 'left':
            self.x -= 5
        if direction == 'right':
            self.x += 5
    def jump(self, d=False):
        if not d:
            self.vel = 15
        else:
            self.db = False
            self.vel = 19
        self.y -= self.vel
    def collision(self, lasers):
        for l in lasers:
            if (l.x < self.x + self.w) and (l.x + l.w > self.x) and (l.y < self.y + self.h) and (l.h + l.y > self.y):
                print('COLLISION')
                self.dead = True
    def draw(self, lasers):
        self.score += 1
        
        if self.y - self.vel < screen_h - self.h:
            self.vel -= 1
            self.y -= self.vel
        elif self.y - self.vel > screen_h - self.h:
            self.y = screen_h - self.h
            self.vel = 0
        else:
            self.db = True
            self.vel = 0
        
        if ((self.x + self.right+self.left) < 0):
            self.x = 0
        elif (self.x + self.right+self.left) > (screen_w - self.w):
            self.x = screen_w - self.w
        else:
            self.x += self.right+self.left
        self.collision(lasers)
    def reset(self):
        self.x = (screen_w/2) - (self.w/2)
        self.y = screen_h - self.h
        self.left = 0
        self.right = 0
        self.score = 0
        self.vel = 0
    def handle_keys(self, action):
        if action == 0:
            if self.y == screen_h - self.h: 
                self.jump()
            else:
                if self.db == True:
                    self.jump(True)
        if action == 1:
            self.move('right')
        if action == 2:
            self.move('left')


class laser():
    def __init__(self, y, side, i):
        self.w = 70
        self.h = 13
        self.side = side
        if self.side == 'left':
            self.x = 10000
        if self.side == 'right':
            self.x = 10000
        self.y = y
        self.ystart = y
        self.shoot_num = i+1
        self.shooting = False
        self.passed = False
        self.num = i
        self.leaped = False
        self.q = 0
    def draw(self, shoot_list):
        if shoot_list[self.num]:
            self.q+=1
            random.seed(self.q)
            rand = random.randint(0,challenge)
            if rand == self.shoot_num:
                if self.side == 'left' and (not self.shooting):
                    self.x = -self.w -100
                    self.y = self.ystart
                if self.side == 'right' and (not self.shooting):
                    self.x = screen_w +100
                    self.y = self.ystart
                self.shooting = True
            if self.shooting:
                if self.side == 'left':
                    self.x += 8 
                if self.side == 'right':
                    self.x -= 8  
            if self.side == 'left':
                if self.x > screen_w + self.w + 50:
                    self.reset()
            if self.side == 'right':
                if self.x < -self.w - 50:
                    self.reset()
        else:
            self.reset()
    def reset(self):
        if self.side == 'left':
            self.x = 10000
        if self.side == 'right':
            self.x = 10000
        self.y = self.ystart
        self.shooting = False
        self.passed = False