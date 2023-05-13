 
import sys
import random

import pygame
from pygame.locals import *
from abc import ABC, abstractmethod
pygame.init()
 

''' IMAGES '''
 
player_ship = 'pict/1.png'
pirates = 'pict/2.png'
monster = 'pict/monsterr.png'
player_bullet = 'pict/pbullet.png'
pirates_shoot = 'pict/shoot.png'
monster_attack = 'pict/fireball.png'
lives = 'pict/lives.png'
coin = 'pict/coin.png'
 
 
''' SOUND '''
 
shoot_sound = pygame.mixer.Sound('sound/cnonn.mp3')
explosion_sound = pygame.mixer.Sound('sound/low_expl.wav')
game_over_sound = pygame.mixer.Sound('sound/game_over.wav')
start_screen_music = pygame.mixer.Sound('sound/wtp.mp3')
game_over_music = pygame.mixer.Sound('sound/illusoryrealm.mp3')
background_music = pygame.mixer.music.load('sound/main.mp3')
get_coin = pygame.mixer.Sound('sound/sfx coin.mp3')
select = pygame.mixer.Sound('sound/select.mp3')
pygame.mixer.init()
 
 
 
screen = pygame.display.set_mode((0,0), FULLSCREEN) 
s_width, s_height = screen.get_size()
pygame.display.set_caption("Bounty Hunter the game")
clock = pygame.time.Clock()
FPS = 60
 
background_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
pirates_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
playerbullet_group = pygame.sprite.Group()
pirates_shoot_group = pygame.sprite.Group()
monsterAttack_group = pygame.sprite.Group()
explosion_group = pygame.sprite.Group()
particle_group = pygame.sprite.Group()
drown_group = pygame.sprite.Group()
sprite_group = pygame.sprite.Group()
 
pygame.mouse.set_visible(True)

class abstract(ABC):
    @abstractmethod
    def update(self):
        pass 
    
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
 
        self.image = pygame.Surface([x,y])
        self.image.fill('white')
        self.image.set_colorkey('black')
        self.rect = self.image.get_rect()
 
    def update(self):
        self.rect.y += 1
        self.rect.x += 1 
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)
 
class Particle(Background):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect.x = random.randrange(0, s_width)
        self.rect.y = random.randrange(0, s_height)
        self.image.fill('grey')
        self.vel = random.randint(3,8)
 
    def update(self):
        self.rect.x += self.vel 
        if self.rect.x > s_width:
            self.rect.x = random.randrange(-10, 0)
            self.rect.y = random.randrange(0, s_height)
 
class Player(abstract, pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('white')
        self.alive = True
        self.count_to_live = 0 
        self.activate_bullet = True
        self.alpha_duration = 0
 
    def update(self):
        if self.alive:
            self.image.set_alpha(80)
            self.alpha_duration += 1
            if self.alpha_duration > 170:
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos()
            self.rect.x = mouse[0] - 130
            self.rect.y = mouse[1] - 50
        else:
            self.alpha_duration = 0
            expl_x = self.rect.x + 70
            expl_y = self.rect.y + 40
            explosion = Explosion(expl_x, expl_y)
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(15)
            self.rect.y = s_height + 200
            self.count_to_live += 1
            if self.count_to_live > 100:
                self.alive = True
                self.count_to_live = 0
                self.activate_bullet = True
 
    def shoot(self):
        if self.activate_bullet:
            bullet = PlayerBullet(player_bullet)
            mouse = pygame.mouse.get_pos()
            bullet.rect.x = mouse[0]
            bullet.rect.y = mouse[1]
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)
 
    def dead(self):
        pygame.mixer.Sound.play(explosion_sound)
        self.alive = False
        self.activate_bullet = False
 
class Pirates(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(s_width+100, s_width+900)
        self.rect.y = random.randrange(0, s_height-100)
        screen.blit(self.image, (self.rect.x, self.rect.y))
 
    def update(self):
        
        self.rect.x -= 1
        if self.rect.x < -200:
            self.rect.x = random.randrange(s_width+100, s_width+200)
            self.rect.y = random.randrange(0, s_height-100)
        self.shoot()
 
    def shoot(self):
        if self.rect.x in (200, 500, 800, 1200, 1500, 2100):
            PiratesShoot = piratesShoot(pirates_shoot)
            PiratesShoot.rect.x = self.rect.x + 20
            PiratesShoot.rect.y = self.rect.y + 50
            pirates_shoot_group.add(PiratesShoot)
            sprite_group.add(PiratesShoot)
 
class Monster(Pirates):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = 2000 
        self.rect.y = s_height
        self.move = -1
 
    def update(self):
        self.rect.x += self.move
        self.rect.y += self.move 
        if self.rect.x < - 200:
            self.rect.x = 2000 
            self.rect.y = s_height
            self.move = -1
        self.shoot()
 
    def shoot(self):
        if self.rect.x % 200 == 0:
            monsterbullet = piratesShoot(monster_attack)
            monsterbullet.rect.x = self.rect.x + 50
            monsterbullet.rect.y = self.rect.y + 70
            monsterAttack_group.add(monsterbullet)
            sprite_group.add(monsterbullet)

class Coin(Pirates):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(s_width+1200,s_width+2000)
        self.rect.y = random.randrange(0, s_height)
        self.move = -5
 
    def update(self):
        self.rect.x += self.move
        if self.rect.x < - 800:
            self.rect.x = s_width+400
            self.rect.y = random.randrange(0, s_height)
            self.move = -5  
 
class PlayerBullet(abstract, pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.image.set_colorkey('black')
 
    def update(self):
        self.rect.x += 15
        if self.rect.x > s_width+30:
            self.kill()
 
class piratesShoot(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('white')
 
    def update(self):
        self.rect.x -= 8
        if self.rect.x < -20:
            self.kill()
 
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 6):
            img = pygame.image.load(f'pict/exp{i}.png').convert()
            img.set_colorkey('black')
            img = pygame.transform.scale(img, (120, 120))
            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0 
 
    def update(self):
        self.count_delay += 3
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()

class Drown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 7):
            img = pygame.image.load(f'pict/monster{i}.png').convert()
            img.set_colorkey('black')
            img.set_colorkey('white')

            self.img_list.append(img)
        self.index = 0
        self.image = self.img_list[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.count_delay = 0 
 
    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1:
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index]
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill()
                
class Game:
    def __init__(self):
        self.count_hit = 0 
        self.count_hit2 = 0 
        self.lives = 3
        self.score = 0
        self.init_create = True
        self.game_over_sound_delay = 0
 
        self.start_screen()

    def start_screen(self):
        pygame.mixer.Sound.stop(game_over_music)
        pygame.mixer.Sound.play(start_screen_music)
        background_image = pygame.image.load("pict/start.jpg").convert()
        background_rect = background_image.get_rect()
        background_image = pygame.transform.scale(background_image, (s_width, s_height))
        screen.blit(background_image, background_rect)
        self.lives = 3
        self.score = 0 
        sprite_group.empty()
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:
                        self.how_to_play_screen()
 
            pygame.display.update()
            
    def how_to_play_screen(self):
        pygame.mixer.Sound.play(select)
        background_image = pygame.image.load("pict/bg htpp.jpg").convert()
        background_rect = background_image.get_rect()
        background_image = pygame.transform.scale(background_image, (s_width, s_height))
        screen.blit(background_image, background_rect)
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.start_screen()
                    if event.key == K_RETURN:
                        self.run_game()
 
            pygame.display.update()
            
    def pause_text(self):
        font = pygame.font.SysFont('Pirate Ship', 50)
        text = font.render('PAUSED', True, 'black')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

        font2 = pygame.font.SysFont('Calibri', 50)
        text2 = font2.render('press <space> to continue', True, 'black')
        text2_rect = text2.get_rect(center=(s_width/2, s_height/2+60))
        screen.blit(text2, text2_rect)
 
    def pause_screen(self):
        pygame.mixer.music.stop()
        self.init_create = False
        while True:
            self.pause_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE:
                        self.run_game()
 
            pygame.display.update()
 
 
    def game_over_text(self):
        font = pygame.font.SysFont('Pirate Ship', 50)
        text = font.render('GAME OVER', True, 'red')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)
        
        font2 = pygame.font.SysFont('Calibri', 20)
        text2 = font2.render('Score :'+str(self.score), True, 'green')
        text2_rect = text2.get_rect(center=(s_width/2, s_height/2+60))
        screen.blit(text2, text2_rect)
        
        font3 = pygame.font.SysFont('Calibri', 20)
        text3 = font3.render('press <esc> to start', True, 'green')
        text3_rect = text3.get_rect(center=(s_width/2, s_height/2+120))
        screen.blit(text3, text3_rect)
        
    def game_over_screen(self):
        pygame.mixer.music.stop()
        pygame.mixer.Sound.play(game_over_sound)
        while True: 
            screen.fill('black')
            self.game_over_text()
            
            self.game_over_sound_delay += 1
            if self.game_over_sound_delay > 1400:
                pygame.mixer.Sound.play(game_over_music)
 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        self.start_screen()
 
            pygame.display.update()
 
 
    def create_background(self):
        for i in range(20):
            x = random.randint(1,15)
            background_image = Background(x,x)
            background_image.rect.x = random.randrange(0, s_width)
            background_image.rect.y = random.randrange(0, s_height)
            background_group.add(background_image)
            sprite_group.add(background_image)
 
    def create_particles(self):
        for i in range(70):
            x = random.randint(1,30)
            y = 5
            particle = Particle(x, y)
            particle_group.add(particle)
            sprite_group.add(particle)
 
 
    def create_player(self):
        self.player = Player(player_ship)
        player_group.add(self.player)
        sprite_group.add(self.player)
 
    def create_pirates(self):
        for i in range(10):
            self.pirates = Pirates(pirates)
            pirates_group.add(self.pirates)
            sprite_group.add(self.pirates)
 
    def create_monster(self):
        for i in range(1):
            self.monster = Monster(monster)
            monster_group.add(self.monster)
            sprite_group.add(self.monster)
            
    def create_coin(self):
        for i in range(2):
            self.coin = Coin(coin)
            coin_group.add(self.coin)
            sprite_group.add(self.coin)
        
    def playerbullet_hits_pirates(self):
        hits = pygame.sprite.groupcollide(pirates_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit += 1
            if self.count_hit == 3:
                self.score += 10
                expl_x = i.rect.x + 70
                expl_y = i.rect.y + 60
                explosion = Explosion(expl_x, expl_y)
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0
                pygame.mixer.Sound.play(explosion_sound)
 
    def playerbullet_hits_monster(self):
        hits = pygame.sprite.groupcollide(monster_group, playerbullet_group, False, True)
        for i in hits:
            self.count_hit2 += 1
            if self.count_hit2 == 20:
                self.score += 50
                Dr_x = i.rect.x + 50
                Dr_y = i.rect.y + 60
                Dr = Drown(Dr_x, Dr_y)
                drown_group.add(Dr)
                sprite_group.add(Dr)
                i.rect.x = -199
                self.count_hit2 = 0
                pygame.mixer.Sound.play(explosion_sound)
 
    def piratesShoot_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, pirates_shoot_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0:
                    self.game_over_screen()
    
    def PlayerGetCoin(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, coin_group, False)
            if hits:
                for i in hits:
                    pygame.mixer.Sound.play(get_coin)
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.score += 20
 
    def monsterAttack_hits_player(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, monsterAttack_group, True)
            if hits:
                self.lives -= 1
                self.player.dead()
                if self.lives < 0:
                    self.game_over_screen()
 
    def player_pirates_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, pirates_group, False)
            if hits:
                for i in hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        self.game_over_screen()
 
    def player_monster_crash(self):
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, monster_group, False)
            if hits:
                for i in hits:
                    i.rect.x = -199
                    self.lives -= 1
                    self.player.dead()
                    if self.lives < 0:
                        self.game_over_screen()
 
    def create_lives(self):
        self.live_img = pygame.image.load(lives)
        self.live_img = pygame.transform.scale(self.live_img, (20,23))
        n = 0
        for i in range(self.lives):
            screen.blit(self.live_img, (0+n, s_height-860))
            n += 60
 
    def create_score(self):
        score = self.score 
        font = pygame.font.SysFont('Calibri', 30)
        text = font.render("Score: "+str(score), True, 'green')
        text_rect = text.get_rect(center=(s_width-150, s_height-850))
        screen.blit(text, text_rect)
 
 
    def run_update(self):
        sprite_group.draw(screen)
        sprite_group.update()
 
    def run_game(self):
        pygame.mixer.Sound.stop(start_screen_music)
        pygame.mixer.Sound.play(select)
        pygame.mixer.music.play(-10)
        if self.init_create:
            self.create_background()
            self.create_particles()
            self.create_player()
            self.create_pirates()
            self.create_monster()
            self.create_coin()
        while True:
            screen.fill('royalblue')
            self.playerbullet_hits_pirates()
            self.playerbullet_hits_monster()
            self.piratesShoot_hits_player()
            self.monsterAttack_hits_player()
            self.PlayerGetCoin()
            self.player_pirates_crash()
            self.player_monster_crash()
            self.run_update()
            pygame.draw.rect(screen, 'black', (0,0,s_width,30))
            self.create_lives()
            self.create_score()
 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
                
                if event.type == MOUSEBUTTONDOWN:
                    pygame.mixer.Sound.play(shoot_sound)
                    self.player.shoot()
                    
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        pygame.quit()
                        sys.exit()
 
                    if event.key == K_SPACE:
                        self.pause_screen()
 
            pygame.display.update()
            clock.tick(FPS)
 
def main():
    game = Game()
 
if __name__ == '__main__':
    main()
 
 
 
 