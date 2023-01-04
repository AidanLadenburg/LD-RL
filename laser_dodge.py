import pygame
import random
import sys

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
        
    def move(self, direction=None):
        if direction == 'left':
            self.left = -7
        elif direction == 'sleft':
            self.left = 0
        if direction == 'right':
            self.right = 7
        elif direction == 'sright':
            self.right = 0
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
                for l in lasers:
                    l.reset()
                self.reset()
    def draw(self, screen, lasers):
        self.score += 1
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.w, self.h))
        if self.y < screen_h - self.h:
            self.vel -= 1
            self.y -= self.vel
        elif self.y > screen_h - self.h:
            self.y = screen_h - self.h
            self.vel = 0
        else:
            self.db = True
            self.vel = 0
        if self.x < 0:
            self.x = 0
        if self.x > screen_w - self.w:
            self.x = screen_w - self.w
        self.collision(lasers)
    def reset(self):
        self.x = (screen_w/2) - (self.w/2)
        self.y = screen_h - self.h
        self.left = 0
        self.right = 0
        print("Score:", self.score)
        self.score = 0
        self.vel = 0
    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move('left')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move('right')
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    if self.y == screen_h - self.h: 
                        self.jump()
                    else:
                        if self.db == True:
                            self.jump(True)
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    self.move('sleft')
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    self.move('sright')
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE:
                    pass#self.jump()

class laser():
    def __init__(self, y, side):
        self.w = 70
        self.h = 13
        if side == 'left':
            self.x = -self.w
        if side == 'right':
            self.x = screen_w
        self.y = y
        self.side = side
        self.ystart = y
        self.shoot_num = random.randint(0,200)
        self.shooting = False
    def shoot(self):
        self.shooting = True
    def draw(self, screen):
        rand = random.randint(0,200)
        if rand == self.shoot_num:
            self.shoot()
        if self.shooting:
            if self.side == 'left':
                self.x += 8 
            if self.side == 'right':
                self.x -= 8
        if self.side == 'left':
            if self.x > screen_w + self.w:
                self.reset()
        if self.side == 'right':
            if self.x < -self.w:
                self.reset()
        pygame.draw.rect(screen, (0,0,0), (self.x, self.y, self.w, self.h))
    def reset(self):
        if self.side == 'left':
            self.x = -self.w
        if self.side == 'right':
            self.x = screen_w
        self.y = self.ystart
        self.shooting = False

screen_w = 900
screen_h = 500

laser_ys = [460, 350, 240]
    

def main():
    pygame.init()
    
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((screen_w, screen_h), 0, 32)

    char = ninja()
    lasers = []
    for y in laser_ys:
        lasers.append(laser(y, 'left'))
        lasers.append(laser(y, 'right'))
    
    font = pygame.font.SysFont('didot.ttc', 50)
    

    while True:
        clock.tick(60)
        char.handle_keys()
        

        char.x += char.right+char.left
        screen.fill((255,255,255))
        text = font.render("Score: " + str(char.score), True, (0,0,0))
        screen.blit(text, (screen_w - 230,0))
        char.draw(screen, lasers)
        for l in lasers:
            l.draw(screen)
        pygame.display.update()

main()