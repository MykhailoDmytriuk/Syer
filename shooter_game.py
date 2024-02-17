from pygame import *
from random import randint

window = display.set_mode((700, 500))
display.set_caption("Шутер")
galaxy = transform.scale(image.load("dsiyn.jpg"), (700, 500))

clock = time.Clock()
FPS = 20

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()

        if keys_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed

        if keys_pressed[K_RIGHT] and self.rect.x < 595:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullets("bullet.png", self.rect.centerx, self.rect.y, -20, 40, 50)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global score
        if self.rect.y > 300:
            self.rect.y = 0
            self.rect.x = randint(80, 620)
            lost += 1
            print(lost)
        if sprite.spritecollide(self, bullets, True):
            score += 1
            self.rect.x = randint(80, 620)
            self.rect.y = 0
            print(score)

class Label():
    def set_text(self, text, fsize=12, text_color=(0, 0, 0)):
        self.image = font.SysFont(None, fsize).render(text, True, text_color)

    def draw(self, shift_x=0, shift_y=0):
        window.blit(self.image, (shift_x, shift_y))

class Bullets(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

lost = 0
score = 0

font.init()
main_font = font.SysFont(None, 50)
mixer.init()
sound_fire = mixer.Sound("auto.ogg")
mixer.music.load('space.ogg')

rocket = Player("pec_patron.jpg", 300, 400, 15, 100, 100)

enemies = sprite.Group()
for i in range(1, 6):
    enemy = Enemy("kolbasa.png", randint(80, 620), 1, randint(1, 2), 150, 100)
    enemies.add(enemy)

bullets = sprite.Group()

game = True
finish = False

while game:
    window.blit(galaxy, (0, 0))
    rocket.update()
    enemies.update()
    bullets.update()
    rocket.reset()
    enemies.draw(window)
    bullets.draw(window)
    lost_text = main_font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
    score_text = main_font.render("Рахунок: " + str(score), 1, (255, 255, 255))
    window.blit(lost_text, (10, 10))
    window.blit(score_text, (10, 40))

    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                rocket.fire()
                sound_fire.play()

    if sprite.spritecollide(rocket, enemies, False) or lost >= 1000:
        lose = Label()
        lose.set_text(" You LOSE", 100, (0, 255, 255))
        window.blit(galaxy, (0, 0))
        lose.draw(200, 200)
        finish = True

    if score >= 1000:
        win_label = Label()
        win_label.set_text(" You WIN!!", 100, (0, 255, 255))
        window.blit(galaxy, (0, 0))
        win_label.draw(200, 200)
        finish = True



    display.flip()

    
