import pygame as pg
import random


# Блок констант
WIDTH = 480
HIGH = 600
FPS = 60

# Цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Настройки игры
difficulty = 1
test = 0
PlayerHealth = 100 - 60 * test
EnemyHealth = 200 - 180 * test
MeteorsCount = 4 * difficulty
EnemyShootDelay = 300 / difficulty
EnemyBulletSpeed = 7 * difficulty

# Создаем игру и окно
pg.init()
pg.mixer.init() #звук
screen = pg.display.set_mode((WIDTH, HIGH))
pg.display.set_caption("Пиу-Пиу!") # подпись экрана
clock = pg.time.Clock()
font_name = pg.font.match_font('arial') #шрифт

# Функция вывода текста (взята из Грантовика)
def draw_text(surf, text, size, x, y):
    font = pg.font.Font(font_name, size)
    textsurface = font.render(text, True, WHITE)
    textrect = textsurface.get_rect()
    textrect.midtop = (x, y)
    surf.blit(textsurface, textrect)

# Экран запуска
def show_go_screen():
    screen.blit(pg.transform.scale(background, (WIDTH, HIGH)), background_rect)# добавляем картинку, растягиваем на экран
    draw_text(screen, "Пиу-Пиу!", 64, WIDTH / 2, HIGH / 4)
    draw_text(screen, "WASD движение, пробел огонь", 22,
              WIDTH / 2, HIGH / 2)
    draw_text(screen, "Жми любую кнопку", 18, WIDTH / 2, HIGH * 3 / 4)
    pg.display.update() 
    WaitKey = True 
    while WaitKey:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            if event.type == pg.KEYUP:
                WaitKey = False
# Победный экран. Он срабатывает, если win истина, lose ложь         
def show_win_screen():
    screen.blit(pg.transform.scale(background, (WIDTH, HIGH)), background_rect)
    draw_text(screen, "Победа!", 64, WIDTH / 2, HIGH / 4)
    draw_text(screen, "Ты храбро сражался!", 22,
              WIDTH / 2, HIGH / 2)
    draw_text(screen, "Жми на клавишу F и продолжай бой!", 18, WIDTH / 2, HIGH * 3 / 4)
    pg.display.update()
    WaitKey = True
    while WaitKey:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            keystate = pg.key.get_pressed()
            # Удобный способ определять нажатие клавиши (в отличии от Грантовика мы тут избавляемся от лишнего цикла)
            if keystate[pg.K_f]: 
                WaitKey = False
# Экран лузеров, срабатывает в обратной от победного ситуации
def show_lose_screen():
    screen.blit(pg.transform.scale(background, (WIDTH, HIGH)), background_rect)
    draw_text(screen, "Поражение", 64, WIDTH / 2, HIGH / 4)
    draw_text(screen, "Ты разбил истребитель", 22,
              WIDTH / 2, HIGH / 2)
    draw_text(screen, "Жми на клавишу F и возвращайся в бой!", 18, WIDTH / 2, HIGH * 3 / 4)
    pg.display.update()
    WaitKey = True
    while WaitKey:
        clock.tick(FPS)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            keystate = pg.key.get_pressed()
            if keystate[pg.K_f]:
                WaitKey = False
                
# Рисуем зеленую полоску здоровья игрока                
def draw_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HIGH = 10
    fill = (health / PlayerHealth) * BAR_LENGTH # Заполнение полоски
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HIGH)
    fill_rect = pg.Rect(x, y, fill, BAR_HIGH)
    pg.draw.rect(surf, GREEN, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
# Рисуем красную полоску здоровья врага  
def draw_enemy_health_bar(surf, x, y, health):
    if health < 0:
        health = 0
    BAR_LENGTH = 100
    BAR_HIGH = 10
    fill = (health / EnemyHealth) * BAR_LENGTH
    outline_rect = pg.Rect(x, y, BAR_LENGTH, BAR_HIGH)
    fill_rect = pg.Rect(x, y, fill, BAR_HIGH)
    pg.draw.rect(surf, RED, fill_rect)
    pg.draw.rect(surf, WHITE, outline_rect, 2)
# Определяем класс игрока
class Player(pg.sprite.Sprite):
    def __init__(self): #Инициируем
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(player_img, (50, 40)) # Определяем иконку и сжимаем под нужный размер
        self.image.set_colorkey(BLACK) #Эта строка делает поле вокруг иконки прозрачным
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2 # Положение иконки
        self.rect.bottom = HIGH - 10 # Положение иконки
        self.speedx = 0 # Скорость перемещения по х
        self.speedy = 0 # Скорость перемещения по у
        self.health = PlayerHealth # Здоровье игрока
    
    # Задаем обновления для объектов класса
    def update(self): 
        self.speedx = 0 
        self.speedy = 0
        keystate = pg.key.get_pressed() # Проверяем на нажатия клавиши и двигаем игрока
        if keystate[pg.K_a]:
            self.speedx = -8
        if keystate[pg.K_d]:
            self.speedx = 8
        if keystate[pg.K_w]:
            self.speedy = -4
        if keystate[pg.K_s]:
            self.speedy = 4
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH: # Ограничиваем поле для игрока
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HIGH:
            self.rect.bottom = HIGH
        if self.rect.top < 0:
            self.rect.top = 0
    def shoot(self): # Определяем выстрел
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
            
            
class Bullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = -10
        PlayersLaserSound.play()

    def update(self):
        self.rect.y += self.speedy
        # убираем, если он заходит за верхнюю часть экрана
        if self.rect.bottom < 0:
            self.kill()       

            
class Meteor(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = meteor_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HIGH + 10 or self.rect.left < -25 or self.rect.right > WIDTH + 20:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 3)
            self.speedx = random.randrange(-3, 3)

class Enemy(pg.sprite.Sprite):
    def __init__(self):
        pg.sprite.Sprite.__init__(self)
        self.image = pg.transform.scale(enemy_img, (100, 80))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.bottom = 50
        self.speedx = 0
        self.speedy = 0
        self.health = EnemyHealth
        self.shoot_delay = EnemyShootDelay
        self.last_shot = pg.time.get_ticks()
        
    def update(self):
        self.speedx = 0
        self.speedy = 0
        #keystate = pg.key.get_pressed()
        if self.rect.centerx <= player.rect.centerx - 10:
            self.speedx = 1
        if self.rect.centerx >= player.rect.centerx + 10:
            self.speedx = -1
        if self.rect.centerx >= player.rect.left and self.rect.centerx <= player.rect.right:
            self.Enemy_shoot()
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.bottom > HIGH:
            self.rect.bottom = HIGH
        if self.rect.top < 0:
            self.rect.top = 0
    def Enemy_shoot(self):
        now = pg.time.get_ticks()
        if now - self.last_shot > self.shoot_delay:
            self.last_shot = now
            en_bullet = EnemyBullet(self.rect.centerx, self.rect.bottom)
            all_sprites.add(en_bullet)
            en_bullets.add(en_bullet)
class EnemyBullet(pg.sprite.Sprite):
    def __init__(self, x, y):
        pg.sprite.Sprite.__init__(self)
        self.image = en_bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.bottom = y
        self.rect.centerx = x
        self.speedy = EnemyBulletSpeed
        EnemiesLaserSound.play()
        
    def update(self):
        self.rect.y += self.speedy
        # убить, если он заходит за верхнюю часть экрана
        if self.rect.bottom > HIGH:
            self.kill()       

# картинки, используется репозиторий с картинками https://opengameart.org/
background = pg.image.load("back.png") # конвертируем пиксели, чтобы соотв главной поверхности
background_rect = background.get_rect()
player_img = pg.image.load("Ship.png").convert()
enemy_img = pg.image.load("enemy.png").convert()
meteor_img = pg.image.load("meteor.png").convert()
bullet_img = pg.image.load("laser.png").convert()
en_bullet_img = pg.image.load("laser2.png").convert()

PlayersLaserSound = pg.mixer.Sound('sfx_laser1.ogg') 
EnemiesLaserSound = pg.mixer.Sound('sfx_laser2.ogg')
PlayersHitSound = pg.mixer.Sound('sfx_shieldDown.ogg')
EnemiesHitSound = pg.mixer.Sound('sfx_shieldUp.ogg') 
MeteorsHitSound = pg.mixer.Sound('sfx_zap.ogg') 
LoseSound = pg.mixer.Sound('sfx_lose.ogg') 

all_sprites = pg.sprite.Group()
Meteors = pg.sprite.Group()
bullets = pg.sprite.Group()
en_bullets = pg.sprite.Group()
player = Player()
enemy = Enemy()
all_sprites.add(player)
all_sprites.add(enemy)
for i in range(MeteorsCount):
    m = Meteor()
    all_sprites.add(m)
    Meteors.add(m)

# Цикл игры
game_over = True
running = True
win = False
lose = False
while running:
    if game_over:
        if win == False and lose == False:
            show_go_screen()
        if win == True and lose == False:
            show_win_screen()
            win = False
            lose = False
        if win == False and lose == True:
            show_lose_screen()
            win = False
            lose = False
        game_over = False
        all_sprites = pg.sprite.Group()
        Meteors = pg.sprite.Group()
        bullets = pg.sprite.Group()
        #powerups = pg.sprite.Group()
        player = Player()
        all_sprites.add(player)
        enemy = Enemy()
        all_sprites.add(enemy)
        for i in range(MeteorsCount):
            m = Meteor()
            all_sprites.add(m)
            Meteors.add(m)
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pg.event.get():
        # проверка для закрытия окна
        if event.type == pg.QUIT:
            running = False
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                player.shoot()

    # Обновление
    all_sprites.update()
    # Проверка, не ударил ли метеорит игрока
    hits = pg.sprite.spritecollide(player, Meteors, True)
    for hit in hits:
        player.health -= 20
        PlayersHitSound.play()
        m = Meteor()
        all_sprites.add(m)
        Meteors.add(m)
        if player.health <= 0:
            LoseSound.play()
            win = False
            lose = True
            game_over = True
    hits = pg.sprite.groupcollide(Meteors, bullets, True, True)
    for hit in hits:
        MeteorsHitSound.play()
        m = Meteor()
        all_sprites.add(m)
        Meteors.add(m)
    hits = pg.sprite.spritecollide(player, en_bullets, True)
    for hit in hits:
        PlayersHitSound.play()
        player.health -= 10
        if player.health <= 0:
            LoseSound.play()
            win = False
            lose = True
            game_over = True

    hits = pg.sprite.groupcollide(en_bullets, bullets, True, True)
    hits = pg.sprite.spritecollide(enemy, bullets, True)
    for hit in hits:
        EnemiesHitSound.play()
        enemy.health -= 10
        if enemy.health <= 0:
            win = True
            lose = False
            game_over = True
        
    
    # Рендеринг
    screen.fill(BLACK)
    screen.blit(pg.transform.scale(background, (WIDTH, HIGH)), background_rect)
    all_sprites.draw(screen)
    draw_health_bar(screen, 5, 5, player.health)
    draw_enemy_health_bar(screen, WIDTH-105, 5, enemy.health)
    pg.display.update()

pg.quit()