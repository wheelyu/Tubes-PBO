 
import sys
import random
import glob
import os
import pygame
from pygame.locals import *
 
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

#kelas background untuk membuat sebuah titik yang bergerak di dalam game 
class Background(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
 
        self.image = pygame.Surface([x,y])
        self.image.fill('white') #pemberian warna
        self.image.set_colorkey('black') #penghilangan warna tertentu
        self.rect = self.image.get_rect() #mengambil posisi [x,y]
 
    def update(self):
        self.rect.y += 1
        self.rect.x += 1 
        if self.rect.y > s_height:
            self.rect.y = random.randrange(-10, 0)
            self.rect.x = random.randrange(-400, s_width)
            
#kelas untuk membuat sebuah garis seperti arus laut yang bergerak berlawanan
class Particle(Background):
    def __init__(self, x, y):
        super().__init__(x, y)
        self.rect.x = random.randrange(0, s_width)  #muncul secara acak pada x
        self.rect.y = random.randrange(0, s_height) #muncul secara acak pada y
        self.image.fill('grey') #pemberian warna
        self.vel = random.randint(3,8) #kecepatan tiap arus yang berbeda beda
 
    def update(self):
        self.rect.x += self.vel #posisi awal x lalu ditambah vel agar dapat bergerak
        if self.rect.x > s_width: #ketika posisi melebihi lebar layar 
            #akan memunculkan kembali dari titik di luar layar secara acak
            self.rect.x = random.randrange(-10, 0) 
            self.rect.y = random.randrange(0, s_height)
            
#kelas player yang nantinya digunakan pemain
class Player(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img) #mengambil gambar kapal
        self.rect = self.image.get_rect() #mengambil posisi [x,y]
        self.image.set_colorkey('white') #penghilangan warna tertentu
        self.alive = True #jika true maka player masih bisa bermain
        self.count_to_live = 0 #hitungan ketika player hidup kembali
        self.activate_bullet = True #untuk menembak
        self.alpha_duration = 0
 
    def update(self):
        if self.alive:
            self.image.set_alpha(80)
            self.alpha_duration += 1 
            if self.alpha_duration > 170: #agar tidak hancur tiba tiba, player dibuat kebal sampai melebihi 170
                self.image.set_alpha(255)
            mouse = pygame.mouse.get_pos() #player bergerak sesuai pergerakan mouse
            self.rect.x = mouse[0] - 130
            self.rect.y = mouse[1] - 50
        else: #ketika self.alive = false maka akan menjalankan else
            self.alpha_duration = 0 #di set ke 0 agar setelah hidup tidak bisa langsung hancur
            expl_x = self.rect.x + 70
            expl_y = self.rect.y + 40
            explosion = Explosion(expl_x, expl_y) #agar motion ledakan pas di posisi kapal player
            explosion_group.add(explosion)
            sprite_group.add(explosion)
            pygame.time.delay(20) #selama durasi tersebut game akan menjadi slow motion
            self.rect.y = s_height + 200
            self.count_to_live += 1 
            if self.count_to_live > 100: #ketika kapal player hancur, kapal tidak akan langsung muncul sampai batas yang ditentukan
                self.alive = True
                self.count_to_live = 0
                self.activate_bullet = True
 
    def shoot(self):
        if self.activate_bullet:
            bullet = PlayerBullet(player_bullet) #mengambil gambar peluru
            mouse = pygame.mouse.get_pos() #peluru dikeluarkan sesuai posisi mouse
            bullet.rect.x = mouse[0]
            bullet.rect.y = mouse[1]
            playerbullet_group.add(bullet)
            sprite_group.add(bullet)
 
    def dead(self):
        pygame.mixer.Sound.play(explosion_sound) #keluar suara ledakan ketika kapal hancur
        self.alive = False
        self.activate_bullet = False
        
#kelas pirates untuk memunculkan kapal musuh
class Pirates(Player):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(s_width+100, s_width+900) #memunculkan kapal pirates secara acak dari kanan
        self.rect.y = random.randrange(0, s_height-100) #memunculkan secara acak pada y
        screen.blit(self.image, (self.rect.x, self.rect.y)) #gambar kapal sesuai dengan posisi x dan y
 
    def update(self):
        
        self.rect.x -= 1 #agar kapal dapat bergerak dari kanan ke kiri
        if self.rect.x < -200: #ketika sudah melewati layar maka akan dimunculkan kembali dari kanan
            self.rect.x = random.randrange(s_width+100, s_width+200)
            self.rect.y = random.randrange(0, s_height-100)
        self.shoot() #memanggil atribut menembak
 
    def shoot(self): 
        if self.rect.x in (200, 500, 800, 1200, 1500, 2100): #ketika mencapai titik x tertentu maka pirates akan menembak
            PiratesShoot = piratesShoot(pirates_shoot) #mengambil gambar peluru
            PiratesShoot.rect.x = self.rect.x + 20
            PiratesShoot.rect.y = self.rect.y + 50 #agar posisi peluru tepat di depan pirates
            pirates_shoot_group.add(PiratesShoot)
            sprite_group.add(PiratesShoot)
            
#merupakan turunan dari pirates, kelas ini memunculkan monster
class Monster(Pirates):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = 2000 
        self.rect.y = s_height
        self.move = -1 #untuk menentukan kecepatan bergerak monster
 
    def update(self):
        self.rect.x += self.move
        self.rect.y += self.move 
        if self.rect.x < - 200: #ketika sudah melewati, monster kembali ke posisi awal
            self.rect.x = 2000 
            self.rect.y = s_height
            self.move = -1
        self.shoot() #memanggil atribut menembak
 
    def shoot(self):
        if self.rect.x % 200 == 0: #monster menembak setiap kelipatan 200 di titik x
            monsterbullet = piratesShoot(monster_attack) #mengambil gambar semburan api
            monsterbullet.rect.x = self.rect.x + 50
            monsterbullet.rect.y = self.rect.y + 70 #agar posisi semburan tepat di depan pirates
            monsterAttack_group.add(monsterbullet)
            sprite_group.add(monsterbullet)
#kelas koin turunan dari pirates, yang nantinya bisa dikumpulkan oleh player
class Coin(Pirates):
    def __init__(self, img):
        super().__init__(img)
        self.rect.x = random.randrange(s_width+1200,s_width+2000) #muncul pada titik x acak di luar layar
        self.rect.y = random.randrange(0, s_height) #muncul dengan range setinggi layar
        self.move = -7 #kecepatan pergerakan koin
 
    def update(self):
        self.rect.x += self.move #koin bergerak
        if self.rect.x < - 800: #ketika melebuhi batas, koin akan muncul kembali
            self.rect.x = s_width+400
            self.rect.y = random.randrange(0, s_height)
            self.move = -7  
#kelas Player Bullet untuk peluru kapal player 
class PlayerBullet(pygame.sprite.Sprite):
    def __init__(self, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect() #mengambil posisi [x,y]
        self.image.set_colorkey('black') #penghilangan warna tertentu
 
    def update(self):
        self.rect.x += 15 #kecepatan peluru
        if self.rect.x > s_width+30: 
            self.kill() #ketika peluru melebih layar maka peluru akan dimatikan
#kelas Pirates Shoot untuk peluru pirates dan serangan monster
class piratesShoot(PlayerBullet):
    def __init__(self, img):
        super().__init__(img)
        self.image.set_colorkey('white') #penghilangan warna tertentu
 
    def update(self):
        self.rect.x -= 8 #kecepatan peluru
        if self.rect.x < -20:
            self.kill() #ketika peluru melebih layar maka peluru akan dimatikan
#kelas ledakan jika kapal hancur
class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 6): #agar ledakan ada animasi singkat
            img = pygame.image.load(f'pict/exp{i}.png').convert() #mengambil gambar 
            img.set_colorkey('black') #penghilangan warna tertentu
            img = pygame.transform.scale(img, (200, 200)) #mengubah ukuran ledakan
            self.img_list.append(img) #gambar ledakan masuk ke dalam list
        self.index = 0
        self.image = self.img_list[self.index] #gambar pertama di list akan muncul
        self.rect = self.image.get_rect() #mengambil posisi [x,y]
        self.rect.center = [x, y]
        self.count_delay = 0 #kehalusan motion ledakan
 
    def update(self):
        self.count_delay += 3 #kecepatan motion ledekan
        if self.count_delay >= 12: 
            if self.index < len(self.img_list) - 1: #memunculkan gambar selanjutnya
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index] #gambar berikutnya akan muncul
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill() #gambar akan hilang
#kelas tenggelam jika monster dikalahkan
class Drown(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.img_list = []
        for i in range(1, 7):
            img = pygame.image.load(f'pict/monster{i}.png').convert()
            img.set_colorkey('black')
            img.set_colorkey('white')
            self.img_list.append(img) #gambar tenggelam masuk ke dalam list
        self.index = 0
        self.image = self.img_list[self.index] #gambar pertama di list akan muncul
        self.rect = self.image.get_rect()#mengambil posisi [x,y]
        self.rect.center = [x, y]
        self.count_delay = 0 #kehalusan motion ledakan
 
    def update(self):
        self.count_delay += 1
        if self.count_delay >= 12:
            if self.index < len(self.img_list) - 1: #memunculkan gambar selanjutnya
                self.count_delay = 0
                self.index += 1
                self.image = self.img_list[self.index] #gambar berikutnya akan muncul
        if self.index >= len(self.img_list) - 1:
            if self.count_delay >= 12:
                self.kill() #gambar akan hilang

#kelas untuk menentukan gameplay yang diinginkan                
class Game:
    def __init__(self):
        self.count_hit = 0                  #hitungan tembakan ke kapal pirates sampai hancur
        self.count_hit2 = 0                 #hitungan tembakan ke monster sampai monster dikalahkan
        self.lives = 3                      #jumlah nyawa player
        self.score = 0                      #jumlah score
        self.init_create = True             #menjalankan fungsi untuk membuat objek
        self.game_over_sound_delay = 0      #suara ketika game over
 
        self.start_screen()                 #menjalankan tampilan start
 
    def start_screen(self):                         #untuk menampilkan tampilan awal sebelum game di mulai
        pygame.mixer.Sound.stop(game_over_music)    #menghentikan sound gameover
        pygame.mixer.Sound.play(start_screen_music) #menjalankan sound start
        background_image = pygame.image.load("pict/start.jpg").convert()    #gambar tampilan start
        background_rect = background_image.get_rect() #mengambil posisi [x,y]
        background_image = pygame.transform.scale(background_image, (s_width, s_height)) #mengubah ukuran bg agar fit to screen
        screen.blit(background_image, background_rect)  #menampilkan gambar
        self.lives = 3 #jumlah nyawa player
        self.score = 0 #jumlah score player yang akan di reset ketika kembali ke menu start 
        sprite_group.empty()
        
        #loop
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:           #mengambil fungsi menekan keyboard
                    if event.key == K_ESCAPE:       #untuk keluar dari game
                        pygame.quit()
                        sys.exit()
                    if event.key == K_RETURN:       #ketika menekan enter maka akan pindah ke tampilan berikutnya
                        self.how_to_play_screen()   #menjalankan tampilan how to play
 
            pygame.display.update()
            
    def how_to_play_screen(self):                   #untuk menampilkan screen cara bermain
        pygame.mixer.Sound.play(select)             #suara efek ketika menekan enter
        background_image = pygame.image.load("pict/bg htpp.jpg").convert()  #gambar cara bermain
        background_rect = background_image.get_rect()   #mengambil posis [x,y]
        background_image = pygame.transform.scale(background_image, (s_width, s_height)) #mengubah ukuran bg agar fit to screen
        screen.blit(background_image, background_rect) #menampilkan gambar
        #loop
        while True: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #ketika di tekan akan kembali ke start screen
                        self.start_screen()
                    if event.key == K_RETURN: #ketika di tekan akan memulai game
                        self.run_game()
 
            pygame.display.update()
            
    def pause_text(self):                           #teks yang muncul ketika menghentikan permainan
        font = pygame.font.SysFont('Pirate Ship', 50)
        text = font.render('PAUSED', True, 'black')
        text_rect = text.get_rect(center=(s_width/2, s_height/2))
        screen.blit(text, text_rect)

        font2 = pygame.font.SysFont('Calibri', 50)
        text2 = font2.render('press <space> to continue', True, 'black')
        text2_rect = text2.get_rect(center=(s_width/2, s_height/2+60))
        screen.blit(text2, text2_rect)
 
    def pause_screen(self):                         #tampilan pause
        pygame.mixer.music.stop()   #backsound akan dmatikan
        self.init_create = False #agar tidak terjadi double objek
        while True:
            self.pause_text()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #tekan untuk keluar game
                        pygame.quit()
                        sys.exit()
                    if event.key == K_SPACE: #tekan untuk menjalankan game
                        self.run_game()
 
            pygame.display.update()
 
    def game_over_text(self):                       #teks yang muncul ketika game over
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
        
    def game_over_screen(self):                     #menampilkan screen game over
        pygame.mixer.music.stop()                   #backsound akan dimatikan
        pygame.mixer.Sound.play(game_over_sound)    #suara backsound gameover akan muncul
        while True: 
            screen.fill('black')                    #layar dibuat full color
            self.game_over_text()                   #memunculkan teks game over
            
            self.game_over_sound_delay += 1 #delay agar sound tidak langsung berjalan
            if self.game_over_sound_delay > 1400:
                pygame.mixer.Sound.play(game_over_music)
 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
 
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE: #untuk kembali ke start
                        self.start_screen()
 
            pygame.display.update()
 
    def create_background(self):                    #membuat titik bergerak untuk background
        for i in range(20):             #jumlah titik
            x = random.randint(1,15)    #kemunculan titik berdasarkan posisi x
            background_image = Background(x,x) #ukuran titik
            background_image.rect.x = random.randrange(0, s_width) #posisi awal x acak
            background_image.rect.y = random.randrange(0, s_height) #posisi awal y acak
            background_group.add(background_image)
            sprite_group.add(background_image)
 
    def create_particles(self):                     #membuat sebuah garis seperti arus
        for i in range(70):    #jumlah arus
            x = random.randint(1,30)    #panjang arus
            y = 5                       #lebar arus
            particle = Particle(x, y)   #ukuran arus
            particle_group.add(particle)
            sprite_group.add(particle)
 
    def create_player(self):                        #membuat kapal pemain
        self.player = Player(player_ship)           #mengambil gambar kapal
        player_group.add(self.player)
        sprite_group.add(self.player)
 
    def create_pirates(self):                       #membuat kapal pirates
        for i in range(10):                         #jumlah kapal yang muncul
            self.pirates = Pirates(pirates)         #mengambil gambar kapal pirates
            pirates_group.add(self.pirates)
            sprite_group.add(self.pirates)
 
    def create_monster(self):                       #membuat monster
        for i in range(1):                          #jumlah monster
            self.monster = Monster(monster)         #mengambil gambar mosnter
            monster_group.add(self.monster)
            sprite_group.add(self.monster)
            
    def create_coin(self):                          #membuat koin
        for i in range(2):                          #jumlah koin
            self.coin = Coin(coin)                  #mengambil gambar koin
            coin_group.add(self.coin)
            sprite_group.add(self.coin)
        
    def playerbullet_hits_pirates(self):            #ketika peluru player mengenai kapal pirates
        hits = pygame.sprite.groupcollide(pirates_group, playerbullet_group, False, True)   #jika kedua nya menyentuh
        for i in hits:
            self.count_hit += 1 #jumlah tembakan
            if self.count_hit == 3: #ketika sama dengan yang ditentukan maka kapal pirates hancur
                self.score += 10    #score bertambah 
                expl_x = i.rect.x + 70  
                expl_y = i.rect.y + 60
                explosion = Explosion(expl_x, expl_y) #mengambil posisi kapal untuk memunculkan ledakan
                explosion_group.add(explosion)
                sprite_group.add(explosion)
                i.rect.x = random.randrange(0, s_width)
                i.rect.y = random.randrange(-3000, -100)
                self.count_hit = 0 #di set 0 kembali
                pygame.mixer.Sound.play(explosion_sound) #muncul suara ledakan
 
    def playerbullet_hits_monster(self):            #ketika peluru player mengenai monster
        hits = pygame.sprite.groupcollide(monster_group, playerbullet_group, False, True) #jika kedua nya menyentuh
        for i in hits:
            self.count_hit2 += 1 #jumlah tembakan
            if self.count_hit2 == 20: #ketika sama dengan yang ditentukan maka monster mati
                self.score += 50        #score bertambah
                Dr_x = i.rect.x + 50
                Dr_y = i.rect.y + 60
                Dr = Drown(Dr_x, Dr_y) #mengambil posisi monster untuk memunculkan motion tenggelam
                drown_group.add(Dr)
                sprite_group.add(Dr)
                i.rect.x = -199
                self.count_hit2 = 0 #di set 0
                pygame.mixer.Sound.play(explosion_sound) #muncul suara ledakan
 
    def piratesShoot_hits_player(self):             #ketika peluru pirates mengenai kapal player
        if self.player.image.get_alpha() == 255: 
            hits = pygame.sprite.spritecollide(self.player, pirates_shoot_group, True) #jika kena
            if hits:
                self.lives -= 1 #nyawa akan berkurang
                self.player.dead() #kapal hancur
                if self.lives < 0:  #ketika kurang dari 0 maka gameover
                    self.game_over_screen() 
    
    def PlayerGetCoin(self):                        #ketika player mengambil koin
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, coin_group, False) #jika kena
            if hits:
                for i in hits:
                    pygame.mixer.Sound.play(get_coin) #suara koin
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.score += 20 #score bertambah
 
    def monsterAttack_hits_player(self):            #ketika serangan monster mengenai player
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, monsterAttack_group, True) #jika kena
            if hits:
                self.lives -= 1 #nyawa akan berkurang
                self.player.dead() #kapal hancur
                if self.lives < 0: #ketika kurang dari 0 maka gameover
                    self.game_over_screen()
 
    def player_pirates_crash(self):                 #ketika kapal player bertabrakan dengan pirates
        if self.player.image.get_alpha() == 255:    
            hits = pygame.sprite.spritecollide(self.player, pirates_group, False) #jika kena
            if hits:
                for i in hits:
                    i.rect.x = random.randrange(0, s_width)
                    i.rect.y = random.randrange(-3000, -100)
                    self.lives -= 1 #nyawa akan berkurang
                    self.player.dead() #kapal hancur
                    if self.lives < 0: #ketika kurang dari 0 maka gameover
                        self.game_over_screen()
 
    def player_monster_crash(self):                 #ketika kapal player bertabrakan dengan mosnter
        if self.player.image.get_alpha() == 255:
            hits = pygame.sprite.spritecollide(self.player, monster_group, False)
            if hits:
                for i in hits:
                    i.rect.x = -199
                    self.lives -= 1 #nyawa akan berkurang
                    self.player.dead()  #kapal hancur
                    if self.lives < 0: #ketika kurang dari 0 maka gameover
                        self.game_over_screen()
 
    def create_lives(self):                         #memunculkan nyawa
        self.live_img = pygame.image.load(lives)    #gambar nyawa
        self.live_img = pygame.transform.scale(self.live_img, (40,40)) #ukuran nyawa
        n = 12 #posisi gambarnyawa
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
 
 
 
 