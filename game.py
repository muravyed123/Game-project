import math
from random import choice
import random as rnd
import pygame
import time

FPS = 30
n = 2
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
GAME_COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]

WIDTH = 1280
HEIGHT = 720
GRAVITY = 1
a = 0
class Bullet:
    bullet = pygame.image.load("bullet.png")
    def __init__(self, screen: pygame.Surface, target, damage, x, y):

        global bullets, explosions
        n = 5
        self.screen = screen
        self.x = x
        self.r = 0
        self.y = y
        self.width = self.bullet.get_width() // 50
        self.height = self.bullet.get_height() // 50
        self.vx = 0
        self.vy = 0
        self.an = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        
        self.tar = target
        self.damage = damage

    def move(self):
        if self.x < WIDTH + 100:
            self.x += self.vx
        else:
            self.explode()
        if self.y < HEIGHT - 100  and self.y > 55:
            self.y -= self.vy
        else:
            self.explode()
        self.an = math.atan2(self.vy, self.vx)
        if (self.x - self.tar[0])** 2 + (self.y - self.tar[1]) ** 2 < 4 * self.r ** 2 :
            self.explode()

    def draw(self):
        p_bul = pygame.transform.scale(self.bullet, (self.width ,self.height))             
        b_rect = p_bul.get_rect()
        
        new_b = pygame.transform.rotate(p_bul , self.an *180/3.14 - 90)  
        rect = new_b.get_rect() 
        rect.center = (self.x, self.y)  
        screen.blit(new_b , rect)
        pygame.draw.circle(self.screen, BLACK, (self.x, self. y), self.r, 1)

    def hittest(self, obj):
        
        return ((obj.center[0] - self.x)**2 + (obj.center[1] - self.y)**2 < (self.r + obj.r) ** 2) and (type(obj) != Gun or self.damage != 30)
    def explode(self):
        new_exp = Explosion(self.screen, (self.x, self.y), 10, False)
        explosions.append(new_exp)
        self.die()
    def die(self):
        if self in bullets:
            del bullets[bullets.index(self)]
class Rocket:
    rocket = pygame.image.load("rocket.png")
    def __init__(self, screen: pygame.Surface, target, damage, x, y):

        global bullets, explosions
        n = 5
        self.screen = screen
        self.x = x
        self.r = 0
        self.y = y
        self.width = self.rocket.get_width() // 20
        self.height = self.rocket.get_height() // 50
        self.v = 0
        self.an = 0
        self.color = choice(GAME_COLORS)
        self.live = 30
        
        self.tar = target
        self.damage = damage

    def move(self):
        if self.x < WIDTH + 100:
            self.x += self.v * math.cos(self.an)
        else:
            self.explode()
        if self.y < HEIGHT - 100  and self.y > 20:
            self.y -= self.v * math.sin(self.an)
        else:
            self.explode()
        if self.tar:
            self.an = -math.atan2(self.tar.center[1] - self.y , self.tar.center[0] - self.x)
            if (self.x - self.tar.center[0])** 2 + (self.y - self.tar.center[1]) ** 2 < 4 *self.r ** 2  :
                self.explode()
                self.tar.hit(self.damage)

    def draw(self):
        p_roc = pygame.transform.scale(self.rocket, (self.width ,self.height))             
        b_rect = p_roc.get_rect()
        
        new_r = pygame.transform.rotate(p_roc , self.an *180/3.14 - 90)  
        rect = new_r.get_rect() 
        rect.center = (self.x, self.y)  
        screen.blit(new_r , rect)

    def hittest(self, obj):
        return ((obj.center[0] - self.x)**2 + (obj.center[1] - self.y)**2 <= (self.r + obj.r) ** 2)
    def explode(self):
        new_exp = Explosion(self.screen, (self.x, self.y), 10, False)
        explosions.append(new_exp)
        self.die()
    def die(self):
        if self in bullets:
            del bullets[bullets.index(self)]
class Bomb:
    bomb = pygame.image.load("bomb.png")
    def __init__(self, screen: pygame.Surface, target, damage, x, y):

        global bullets, explosions
        n = 5
        self.screen = screen
        self.x = x
        self.r = 0
        self.y = y
        self.width = self.bomb.get_width() // 50
        self.height = self.bomb.get_height() // 50
        self.vx = 0
        self.vy = 0
        self.an = 0
        self.live = 30
        self.tar = target
        
        self.timer = 0
        self.livetime = 10
        self.damage = damage

    def move(self):
        if self.x < WIDTH + 100:
            self.x += self.vx
        else:
            self.stop()
        if self.y < HEIGHT - 100  and self.y > 20:
            self.y -= self.vy
        else:
            self.stop()
        self.an = math.atan2(self.vy, self.vx)
        if (self.x - self.tar[0])** 2 + (self.y - self.tar[1]) ** 2 < 4*self.r ** 2 :
            self.stop()

    def draw(self):
        p_bul = pygame.transform.scale(self.bomb, (self.width ,self.height))             
        b_rect = p_bul.get_rect()
        
        new_b = pygame.transform.rotate(p_bul , self.an *180/3.14 - 90)  
        rect = new_b.get_rect() 
        rect.center = (self.x, self.y)  
        screen.blit(new_b , rect)

    def hittest(self, obj):
        return ((obj.center[0] - self.x)**2 + (obj.center[1] - self.y)**2 <= (self.r + obj.r) ** 2)
    def stop(self):
        self.vx = 0 
        self.vy = 0
        if self.timer < self.livetime:
            self.timer += 1/FPS
        else:
            self.explode()
    def explode(self):
        new_exp = Explosion(self.screen, (self.x, self.y), 7, True)
        explosions.append(new_exp)
        self.die()
        for i in bullets:
            if (self.x - i.x) ** 2 + (self.y - i.y) ** 2 <= (new_exp.width /5 + i.r)**2: 
                if type(i) == Bomb:
                    i.timer = i.livetime - 1/(0.5*FPS)
                    i.stop()
                else:
                    i.explode()
        for i in targets:
            if (self.x - i.center[0]) ** 2 + (self.y - i.center[1]) ** 2 <= (new_exp.width /5 + i.r)**2:
                i.hit(self.damage)              
    def die(self):
        if self in bullets:
            del bullets[bullets.index(self)]
class Gun:
    tank = pygame.image.load("tank1.png")
    bash = pygame.image.load('tank2.png')
    def __init__(self, screen, n):
        self.screen = screen
        self.f2_power = 20
        self.f2_on = 0
        self.an = 1
        self.angle = 0
        self.x = WIDTH//2
        self.y = HEIGHT//2
        self.speed = 8
        self.rot_speed = 4
        self.n = n
        self.basht = [self.bash.get_width() // self.n,self.bash.get_height() // self.n]
        self.width = self.tank.get_width() // self.n
        self.height = self.tank.get_height() // self.n
        self.center = [self.x +self.width/2, self.y + self.height/2]
        self.bsp = [self.center[0], self.center[1] + self.basht[1]/2]
        self.can_shoot = True
        self.timer = 0
        self.cooldown_time = 1
        self.timer2 = 0
        self.cooldown_time2 = 0
        self.now_effect = 0
        self.r = 40
        self.defense = 0
        self.attack = 0
        
        self.canshoot2 = True
        self.health = 100
        self.max_health = 100
        self.rad = 20
        self.n_tar = (0,0)
        self.btype = 1
    def fire2_start(self, event):
        self.f2_on = 1

    def fire2_end(self, event):

        if self.can_shoot and self.can_shoot2:
            global bullets
            if self.btype == 1:
                new_bullet = Bullet(self.screen, self.n_tar, 30 + self.attack, self.bsp[0], self.bsp[1])
                new_bullet.r += 5
                self.an = math.atan2((event.pos[1]-new_bullet.y), (event.pos[0]-new_bullet.x))
                new_bullet.vx = self.f2_power * math.cos(self.an)
                new_bullet.vy = - self.f2_power * math.sin(self.an)
                new_bullet.tar = (new_bullet.tar[0] + new_bullet.vx * 5, new_bullet.tar[1] - new_bullet.vy * 5)
                bullets.append(new_bullet)
            elif self.btype == 2:
                target = give_target(self.n_tar, self.rad)
                new_rocket = Rocket(self.screen, target, 10 + self.attack, self.bsp[0], self.bsp[1])
                new_rocket.r += 5
                self.an = math.atan2((event.pos[1]-new_rocket.y), (event.pos[0]-new_rocket.x))
                new_rocket.v = self.f2_power 
                new_rocket.an = -self.an
                bullets.append(new_rocket)  
            elif self.btype == 3:
                new_bomb = Bomb(self.screen, self.n_tar, 20 + self.attack, self.bsp[0], self.bsp[1])
                new_bomb.r += 5
                self.an = math.atan2((event.pos[1]-new_bomb.y), (event.pos[0]-new_bomb.x))
                new_bomb.vx = self.f2_power * math.cos(self.an)
                new_bomb.vy = - self.f2_power * math.sin(self.an)
                bullets.append(new_bomb)                
            self.can_shoot = False
            self.timer = 0

    def targetting(self, event):
        """Прицеливание. Зависит от положения мыши."""
        if event:
            if (event.pos[0] - self.center[0]) ** 2 + (event.pos[1] - self.center[1])** 2 > 4900:
                self.an = math.atan2((event.pos[1]-self.center[1]) , (event.pos[0]-self.center[0]))
                self.n_tar = tuple(event.pos)    
                self.can_shoot2 = True
            else:
                self.can_shoot2 = False
    def rot(self, t):
        self.angle += t*self.rot_speed
    def give_effect(self, number, name, time_of):
        if number == 0:
            self.defense = 0
            selth.attack = 0
        elif number == 1:
            self.health = min(self.health + 30, self.max_health)
        elif number == 2:
            self.attack = 40
        elif number == 3:
            self.defense = 20
        self.timer2 = 0
        self.now_effect = number
        self.cooldown_time2 = time_of
        scor.text = name
    def movef(self, t):
        f = True
        new_x = self.x + t*self.speed* math.sin(self.angle/180 * 3.14)
        new_y = self.y + t*self.speed* math.cos(self.angle / 180  * 3.14)
        for i in targets:
            if i != self:
                if (i.center[0]- new_x - self.width/2)** 2+ (i.center[1] - new_y - self.height/2)** 2<= (self.r + i.r)**2:
                    f = False
                    break    
        if new_x < WIDTH - 210 and new_x > 110 and f:
            self.x = new_x
        if new_y < HEIGHT - 160  and new_y > 60 and f:
            self.y = new_y
    def draw(self): 
        self.cooldown()
        if self.now_effect != 0:
            if self.cooldown2():
                self.now_effect = 0
                self.defense = 0
                self.attack = 0
                scor.text = ''
                
        self.center = [self.x +self.width/2, self.y + self.height/2]
        self.bsp = [self.center[0] + + self.basht[1]*math.cos(self.an)/2, self.center[1] + self.basht[1]*math.sin(self.an)/2]
        p_tank = pygame.transform.scale(self.tank, (self.width, self.height))        
        p_bash = pygame.transform.scale(self.bash, tuple(self.basht))      
        t_rect = p_tank.get_rect()
        b_rect = p_bash.get_rect()
        
        new_t = pygame.transform.rotate(p_tank , self.angle)
        new_b = pygame.transform.rotate(p_bash , -self.an * 180/3.14 - 90)  
        rect1 = new_t.get_rect()  
        rect2 = new_b.get_rect() 
        rect1.center = tuple(self.center)
        rect2.center = tuple(self.center)  
        screen.blit(new_t, rect1)
        screen.blit(new_b, rect2)
        
        pygame.draw.circle(self.screen, BLACK, tuple(self.bsp), 5)
        pygame.draw.circle(self.screen, BLACK, tuple(self.center), 70, 1)
        if self.btype == 2:
            pygame.draw.circle(self.screen, BLACK, tuple(self.n_tar), self.rad, 2)    
    def hit(self,damage):
        self.health -= max(damage - self.defense, 0)
        if self.health <= 0:
            self.die()
    def cooldown(self):
        #print(self.timer)
        if self.timer < self.cooldown_time:
            self.timer += 1/FPS
        else:
            self.can_shoot = True
    def cooldown2(self):
        if self.timer2 < self.cooldown_time2:
            self.timer2 += 1/FPS
            return False
        else: return True
    def die(self):
        game_over()


class Explosion:
    frames = []
    for i in range(1, 10):
        t = 'explosion\image_part_00' + str(i) +'.png'
        new_f = pygame.image.load(t)
        new_f.set_colorkey((255, 255, 255))
        frames.append(new_f)
    def __init__(self,screen, pos, size, need):
        self.screen = screen
        self.size = size
        self.x = pos[0]
        self.y = pos[1]
        self.width = self.frames[0].get_width() // self.size
        self.height = self.frames[0].get_height() // self.size
        self.timer = 0
        self.time_live = 1
        self.need = need
    def draw(self):
        if self.need:
            pygame.draw.circle(self.screen, RED, (self.x, self.y ), self.width/5, 1)        
        now_f = math.floor(self.timer * 9 // self.time_live)
        exp = pygame.transform.scale(self.frames[now_f], (self.width ,self.height))   
        r = exp.get_rect()
        r.center = (self.x, self.y)
        screen.blit(exp , r)
        if self.timer > self.time_live - 1/FPS:
            self.die()
        else:
            self.timer += 1/FPS
    def die(self):
        del explosions[explosions.index(self)]
        
class Target:
    tank = pygame.image.load("tank3.png")
    bash = pygame.image.load("tank4.png")
    tank1 = pygame.image.load('tank5.png')
    bash1 = pygame.image.load("tank6.png")
    def __init__(self, screen, typ):
        self.screen = screen
        self.points = 0
        self.live = 1
        self.f2_power = 20
        self.an = 1
        self.angle = 0
        self.need_angle = 0
        self.r = 45
        self.health = 100
        self.max_health = 100     
        self.defense = 15
        self.damage = 20
        self.cooldown_time = 1.5
        
        
        self.new_target()
        self.speed = 2
        self.rot_speed = 0.5
        self.n = 2
        if typ == 2:
            self.tank = self.tank1
            self.bash = self.bash1
            self.n = 3
            self.r = 30
            self.rot_speed = 2
            self.max_health = 50
            self.health = self.max_health
            self.speed = 8
            self.damage = 10
            self.defense = 0
            self.cooldown_time = 0.8
        self.basht = [self.bash.get_width() // self.n,self.bash.get_height() // self.n]
        self.width = self.tank.get_width() // self.n
        self.height = self.tank.get_height() // self.n
        self.center = [self.x +self.width/2, self.y + self.height/2]
        self.bsp = [self.center[0], self.center[1] + self.basht[1]/2]
        self.can_shoot = True
        self.timer = 0

        self.t = 1
        
        self.rad = 20
        self.n_tar = (0,0)
        self.btype = 1     
        self.typ = typ
    def give_coord(self):
        rnd.random()
        y = rnd.randint(200, HEIGHT - 200)
        rnd.random()
        x = WIDTH//2 + (rnd.randint(0,1)-0.5) * (WIDTH + 100)        
        return (x,y)
    def find_direction(self):
        rast = (gun.center[0] - self.center[0]) ** 2 + (gun.center[1] - self.center[1])** 2
        rot = self.rot_speed
        need_ang = 0
        if rast > 100 ** 2:
            need_ang = -(math.atan2(gun.center[1] - self.center[1], gun.center[0] - self.center[0])/3.14 * 180 + 270) % 360
            #print(need_ang, self.angle)
            if abs((self.angle - need_ang) % 360) < abs((-self.angle+need_ang)%360):
                rot *= -1
            if abs(self.need_angle - self.angle) < 120 and abs(self.need_angle - self.angle) > 60:
                rot*= 2
            if abs(self.angle - need_ang) < self.rot_speed:
                rot = 0
        #print(need_ang, ',', self.angle)   
        self.need_angle = need_ang % 360
        return (self.angle + rot) % 360
    def coord_ok(self, coord):
        t = True
        for i in targets:
            if (i.x - coord[0]) ** 2 + (i.y - coord[1])** 2 <= (self.r + i.r) ** 2:
                t = False
                break
        return t
    def new_target(self):
        """ Инициализация новой цели. """
        coord = self.give_coord()
        while not self.coord_ok(coord): coord = self.give_coord()
        self.x = coord[0]
        self.y = coord[1]
        self.angle =  90 * (self.x - 1000) /abs(self.x- 1000) +180
        self.health = self.max_health
    def targetting(self, event):
        if event:
            rast = (event.center[0] - self.center[0]) ** 2 + (event.center[1] - self.center[1])** 2
            if rast > 4900:
                self.an = math.atan2((event.center[1]-self.center[1]) , (event.center[0]-self.center[0])) 
                self.n_tar = tuple(event.center)     
                if rast < 90000:
                    self.fire(event)
            else:
                self.can_shoot = False    
    def fire(self, event):

        if self.can_shoot:
            global bullets
            new_bullet = Bullet(self.screen, self.n_tar, self.damage, self.bsp[0], self.bsp[1])
            new_bullet.r += 5
            self.an = math.atan2((event.center[1]-new_bullet.y), (event.center[0]-new_bullet.x))
            new_bullet.vx = self.f2_power * math.cos(self.an)
            new_bullet.vy = - self.f2_power * math.sin(self.an)
            new_bullet.tar = (new_bullet.tar[0] + new_bullet.vx * 5, new_bullet.tar[1] - new_bullet.vy * 5)
            bullets.append(new_bullet)            
            self.can_shoot = False
            self.timer = 0        
    def hit(self, damage):
        self.health -= max(damage - self.defense, 0)
        if self.health <= 0:
            self.health = 0
            self.die()
    def die(self):
        scor.change_score(1)
        #new_cam()
        if self in targets:
            del targets[targets.index(self)]        

    def draw(self):
        self.cooldown()
        self.center = [self.x +self.width/2, self.y + self.height/2]
        self.bsp = [self.center[0] + self.basht[1]*math.cos(self.an)/2, self.center[1] + self.basht[1]*math.sin(self.an)/2]
        p_tank = pygame.transform.scale(self.tank, (self.width ,self.height))        
        p_bash = pygame.transform.scale(self.bash, tuple(self.basht))      
        t_rect = p_tank.get_rect()
        b_rect = p_bash.get_rect()
        
        new_t = pygame.transform.rotate(p_tank , self.angle)
        new_b = pygame.transform.rotate(p_bash , -self.an *180/3.14 - 90)  
        rect1 = new_t.get_rect()  
        rect2 = new_b.get_rect() 
        rect1.center = tuple(self.center)
        rect2.center = tuple(self.center)  
        screen.blit(new_t , rect1)
        screen.blit(new_b , rect2)
        
        pygame.draw.circle(self.screen, BLACK, tuple(self.center), self.r, 1)
        pygame.draw.rect(self.screen, BLACK, (self.center[0]- 25, self.center[1]- 40,  50,  10))
        length = self.health* 50//self.max_health
        pygame.draw.rect(self.screen, GREEN, (self.center[0] - 25, self.center[1]- 40, length,  10))
    def move(self):
        self.angle = self.find_direction()
        speed = self.speed * self.t
        if abs(self.need_angle - self.angle) > 120 and self.typ == 1:  
            speed *= -1
        elif abs(self.need_angle - self.angle) > 60:  
            speed = 0 
            
        new_x = self.x + speed* math.sin(self.angle/180 * 3.14)
        new_y = self.y + speed* math.cos(self.angle / 180  * 3.14)
        t = True
        for i in targets:
            if i != self:
                if (i.center[0]- new_x - self.width/2)** 2+ (i.center[1] - new_y - self.height/2)** 2<= (self.r + i.r)**2:
                    t = False
                    break
        t = (t and (gun.center[0]- new_x - self.width/2)** 2+ (gun.center[1] - new_y - self.height/2)** 2>= (self.r + gun.r)**2)
        if new_x < WIDTH + 80 and new_x > -90 and t:
            self.x = new_x
        if new_y < HEIGHT - 160  and new_y > 60 and t:
            self.y = new_y
    def cooldown(self):
        #print(self.timer)
        if self.timer < self.cooldown_time:
            self.timer += 1/FPS
        else:
            self.can_shoot = True
class Kamikadze():
    def __init__(self,screen):
        self.screen = screen
        self.tank = pygame.image.load('kamikadz.png')
        self.health = 20
        self.center = (0, 0)
        self.n = 6
        self.angle = 45
        self.speed = 10
        self.damage = 50
        self.r = 20
        self.live = 1
        self.width = self.tank.get_width() // self.n
        self.height = self.tank.get_height() // self.n
        self.x, self.y = self.give_coord()
        self.center = [self.x +self.width/2, self.y + self.height/2]   
    def give_coord(self):
        rnd.random()
        y = rnd.randint(200, HEIGHT - 200)
        rnd.random()
        x =  WIDTH // 2+ (rnd.randint(0,1)-0.5) * (WIDTH-200)        
        return (x,y)
    def coord_ok(self, coord):
        t = True
        for i in targets:
            if (i.x - coord[0]) ** 2 + (i.y - coord[1])** 2 <= (self.r + i.r) ** 2:
                t = False
                break
        return t    
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.health = 0
            self.die()
    def die(self):
        self.explode()
    def draw(self):
        #self.angle = self.find_direction()
        #self.cooldown()
        self.center = [self.x +self.width/2, self.y + self.height/2]
        p_tank = pygame.transform.scale(self.tank, (self.width ,self.height))           
        t_rect = p_tank.get_rect()
        
        new_t = pygame.transform.rotate(p_tank , self.angle)
        rect1 = new_t.get_rect()  
        rect1.center = tuple(self.center)
        screen.blit(new_t , rect1)
    def explode(self):
        if self in targets:
            del targets[targets.index(self)]
        exp = Explosion(self.screen, (self.center[0], self.center[1]), 5, True)
        explosions.append(exp)
        for i in bullets:
            if (self.x - i.x) ** 2 + (self.y - i.y) ** 2 <= (exp.width /5 + i.r)**2: 
                if type(i) == Bomb:
                    i.timer = i.livetime - 1/(0.5*FPS)
                    i.stop()
                else:
                    i.explode()
        for i in targets:
            if self != i:
                if (self.x - i.center[0]) ** 2 + (self.y - i.center[1]) ** 2 <= (exp.width /5 + i.r)**2:
                    i.hit(self.damage)   
        if (self.x - gun.center[0]) ** 2 + (self.y - gun.center[1]) ** 2 <= (exp.width /5 + gun.r)**2:
            gun.hit(self.damage)         
    def move(self):
        
        new_x = self.x + self.speed* math.sin(self.angle/180 * 3.14)
        new_y = self.y + self.speed* math.cos(self.angle / 180  * 3.14)
        angle = self.angle
        t = True
        for i in targets:
            if i != self:
                if (i.center[0]- new_x - self.width/2)** 2+ (i.center[1] - new_y - self.height/2)** 2<= (self.r + i.r)**2:
                    t = False
                    break
        if (gun.center[0] - new_x - self.width/2)** 2 + (gun.center[1] - new_y - self.height/2)** 2 <= (self.r + gun.r)**2:
            self.die()
        if new_x < WIDTH - 100 and new_x > 100 and t:
            self.x = new_x
        else:
            angle = -self.angle 
        if new_y < HEIGHT - 100  and new_y > 60 and t:
            self.y = new_y
        else:
            if angle == -self.angle:
                angle = 180 + self.angle
            else:
                angle = 180 - self.angle
        
        self.angle = angle
class Box:
    def __init__(self, screen):
        self.screen = screen
        self.health = 50
        self.effect = 1
        self.effect_name = ['health', 'fire', 'defense']
        self.color = RED
        self.colors = [GREEN, RED, BLUE]
        self.timer = 0
        self.timespawn = 5
        self.center = (0, 0)
        self.x = 0
        self.y = 0
        self.live = True
        self.health = 100
        self.r = 25
        self.size = 30
        self.time_of = 5

        self.new_box()
    def give_coord(self):
        rnd.random()
        y = rnd.randint(100, HEIGHT - 100)
        rnd.random()
        x = rnd.randint(100, WIDTH - 100)        
        return (x,y)    
    def coord_ok(self, coord):
        t = True
        for i in targets:
            if i!= self:
                if (i.center[0] - coord[0]) ** 2 + (i.center[1] - coord[1])** 2 <= (self.r * 2 + i.r) ** 2:
                    t = False
                    break
        if (gun.center[0] - coord[0]) ** 2 + (gun.center[1] - coord[1])** 2 <= (self.r * 2 + gun.r) ** 2:
            t = False  
        return t    
    def new_box(self):
        rnd.random()
        self.effect = rnd.randint(0, 2) + 1
        self.x, self.y = self.give_coord()
        while not self.coord_ok((self.x + self.size//2, self.y + self.size//2)):
            self.x, self.y = self.give_coord()                
        self.health = rnd.randint(1, 100)
        self.time_of = rnd.randint(3, 7)
        self.color = self.colors[self.effect - 1]
    def hit(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.die()
    def die(self):
        gun.give_effect(self.effect, self.effect_name[self.effect - 1], self.time_of) 
        self.timer = 0
        self.center = [-1000, -1000]
    def wait(self):
        if self.timer <= self.timespawn:
            self.timer += 1/FPS
            return False
        else:
            if self.center[0] == -1000:
                self.new_box()
            self.center = [self.x + self.size//2,self.y + self.size//2]
            return True
    def draw(self):
        if self.wait():
            pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.size, self.size))
            pygame.draw.rect(self.screen, BLACK, (self.x, self.y, self.size, self.size), 2)
            pygame.draw.circle(self.screen, BLACK, (self.center[0], self.center[1]), 5)
class Score:
    def __init__(self, screen):
        self.score = 0
        self.screen = screen
        self.text = ''
        #self.draw()
    def change_score(self,plus):
        self.score += plus
        self.draw()
    def draw(self):
        pygame.draw.line(screen, RED, [100, 0], [100, 720 ], 3)
        pygame.draw.line(screen, RED, [WIDTH - 100, 0], [WIDTH - 100, 720 ], 3)
        pygame.draw.rect(screen, MAGENTA, (0, 0, WIDTH, 50))
        pygame.draw.rect(screen, BLACK, (0, -5, WIDTH, 55), 5)
        pygame.draw.rect(screen, CYAN, (0, HEIGHT- 50, WIDTH, HEIGHT ))
        pygame.draw.rect(screen, BLACK, (0, HEIGHT -55, WIDTH, HEIGHT + 5), 5) 
        pygame.draw.rect(screen, BLACK, (600, 10, 300, 25))
        length = gun.health * 300 //gun.max_health 
        pygame.draw.rect(screen, GREEN, (600, 12, length, 20))
        f1 = pygame.font.Font(None, size=40)
        text1 = f1.render('score: ' + str(self.score), True,
                  (1, 0, 0))
        self.screen.blit(text1, (50, 10))
        #f2 = pygame.font.Font(None, size=40)
        text2 = f1.render('Your health:', True,
                  (1, 0, 0))
        self.screen.blit(text2, (400, 10)) 
        if self.text != '':
            text3 = f1.render('effect:' + str(self.text), True,
                      (1, 0, 0))
            self.screen.blit(text3, (950, 10))         
        
class Button:
    """Create a button, then blit the surface in the while loop"""
    def __init__(self, text,  pos, font, bg, screen, typ):
        self.x, self.y = pos
        self.font = pygame.font.SysFont("Arial", font)
        self.command = self.change_type
        self.screen = screen
        if typ == 1:
            self.command = self.change_type
        elif typ == 2:
            self.command = self.pause
        elif typ == 3:
            self.command = self.reset
        self.type = 0
        self.bg = bg
        self.rect = pygame.Rect(self.x, self.y, 5, 5)
        self.sost = False
        self.command()
        self.change_colour()
    def change_type(self, bg="black"):
        self.type = (self.type) % 3 + 1
        gun.btype = self.type
        text = 'now type: '+ str(self.type)
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    def pause(self):
        text = 'pause ||'
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        stops()
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])    
    def reset(self):
        text = 'GAME OVER. Reset..?'
        self.text = self.font.render(text, 1, pygame.Color("White"))
        self.size = self.text.get_size()
        global over 
        over = not over
        stops()
        scor.score = 0
        gun.health = 100
        box = Box(screen)
        targets.append(box)
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])  
    def change_colour(self):
        if self.sost:
            fg = 'red'
        else:
            fg = self.bg
        self.surface = pygame.Surface(self.size)
        self.surface.fill(fg)
        self.surface.blit(self.text, (0, 0))        
    def show(self):
        screen.blit(self.surface, (self.x, self.y))
    def click(self, event):
        x, y = pygame.mouse.get_pos()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(x, y):
                self.sost = pygame.mouse.get_pressed()[0]
                self.command()
                self.change_colour()
        else:
            self.sost = False
            self.change_colour()
def give_target(tar, rad):
    for i in targets:
        if i.live:
            if (i.center[0] - tar[0])** 2 +(i.center[1] - tar[1]) ** 2 < (i.r + rad)**2:
                return(i)
    else: return(False)
def spawn(timer, screen):
    global time2sp
    if timer < time2sp or len(targets)>n+1:
        return timer + 1/FPS
    else:
        a = [0,0]
        for i in targets:
            if type(i) == Target:
                a[0] += 1
            elif type(i) == Kamikadze:
                a[1] += 1
        if a[0] == n :
            new_t = Kamikadze(screen)
        else:
            new_t = Target(screen, rnd.randint(1,2))
        targets.append(new_t)
        time2sp = rnd.randint(5,10)
        return(0)
def game_over():
    global targets, bullets
    targets =[]
    bullets =[]
    global over
    over = not over
    stops()
def stops():
    global stop
    stop = not stop
    
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption('Game')
bullets = []
explosions= []

clock = pygame.time.Clock()
gun = Gun(screen, 2)
scor = Score(screen)
targets = []
buttons  = []
over = True
stop = True
button1 = Button("text",
    (250, 5),
    30,
    "navy",
    screen, 1)
button2 = Button("pause",
    (1150, 5),
    30,
    "navy",
    screen, 2)
buttons.append(button1)
buttons.append(button2)
button3 = Button("again",
    (700, 300),
    30,
    "navy",
    screen, 3)
buttons.append(button3)

box = Box(screen)
kamik = Kamikadze(screen)
targets.append(box)
targets.append(kamik)
finished = False


timer_sp = 0
time2sp = 10
game_over()
while not finished:
    screen.fill(WHITE)
    gun.draw()
    for i in targets:
        i.draw()
    for b in bullets:
        b.draw()
    for e in explosions:
        e.draw()
    scor.draw()
    button1.show()
    button2.show()
    clock.tick(FPS)
    if not stop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if  event.pos[1] > 50:
                    gun.fire2_start(event)
            elif event.type == pygame.MOUSEBUTTONUP:
                if  event.pos[1] > 50:
                    gun.fire2_end(event)
            elif event.type == pygame.MOUSEMOTION:
                gun.targetting(event)
            for i in buttons[:-1]:
                i.click(event)
                
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            gun.rot(1)
        if keys[pygame.K_RIGHT]:
            gun.rot(-1)    
        if keys[pygame.K_UP]:
            gun.movef(-1)  
        if keys[pygame.K_DOWN]:
            gun.movef(1)    
        for b in bullets:
            for i in targets:
                if b.hittest(i):
                    #target.live = 0
                    i.hit(b.damage)
                    #i.new_target()
                    b.explode()
            if b.hittest(gun):
                gun.hit(b.damage)
                b.explode()
            b.move()
        for i in targets:
            if type(i) == Target:
                i.move()
                i.targetting(gun)  
            elif type(i) == Kamikadze:
                i.move()
        timer_sp = spawn(timer_sp, screen)
    else:
        if not over:
            button3.show()
        for event in pygame.event.get():
            if over:
                button2.click(event)    
            else:
                button3.click(event)
                
    pygame.display.update()
pygame.quit()
