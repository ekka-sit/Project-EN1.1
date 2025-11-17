import pygame
import random

screen_width = 576
screen_hieght = 720
FPS = 60
clock = pygame.time.Clock()
group_Meteor_A = pygame.sprite.Group()
group_Meteor_B = pygame.sprite.Group()
group_Effect = pygame.sprite.Group()
group_Bullet = pygame.sprite.Group()
group_Midsile = pygame.sprite.Group()
score = 0
Hp = 100

# start
pygame.init()

# SetName
pygame.display.set_caption("Pew Pew Game")

# Create Display
screen = pygame.display.set_mode((screen_width, screen_hieght))
screen_rect = screen.get_rect()

# backgroud
backgroud = pygame.image.load("Image/backgroud.png")
game_over = pygame.image.load("Image/GameOver.png")

# Space Image
SpaceF = pygame.image.load("Image/SpaceF.png")
SpaceF = pygame.transform.scale(SpaceF, (61, 115))

SpaceF_rect = SpaceF.get_rect()
SpaceF_rect.centerx = screen_width // 2
SpaceF_rect.centery = screen_hieght // 2 + 295

# Meteor A Image
Meteor_A = pygame.image.load("Image/Meteor_A.png")
Meteor_A = pygame.transform.scale(Meteor_A, (85, 81))

# Meteor B Image
Meteor_B = pygame.image.load("Image/Meteor_B.png")
Meteor_B = pygame.transform.scale(Meteor_B, (75, 45))

# Bullet Image
Bullet = pygame.image.load("Image/Bullet.png")
Bullet = pygame.transform.scale(Bullet, (55, 12))

Midsile = pygame.image.load("Image/Midsile.png")
Midsile = pygame.transform.scale(Midsile, (71, 23))

# Effect Image
Boom = pygame.image.load("Image/Boom.png")
Boom_A = pygame.transform.scale(Boom, (134, 106))
Boom_B = pygame.transform.scale(Boom, (101, 80))

MidsileImg = pygame.image.load("Image/MidsileImg.png")
MidsileImg = pygame.transform.scale(MidsileImg, (82, 102))

MidsileImg_rect = MidsileImg.get_rect()
MidsileImg_rect.centerx = 516
MidsileImg_rect.centery = 68

# font
font_1 = pygame.font.SysFont("pslxpassanun", 36)
font_2 = pygame.font.SysFont("pslxpassanun", 44)
font_3 = pygame.font.SysFont("pslxpassanun", 52)

# score and hp system
score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
Hp_text = font_3.render(str(Hp) + " %", True, (0 ,168, 14))


# Class Meteor
class imageMeteor(pygame.sprite.Sprite):
    def __init__(self, image, hp):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(30, screen_width - 50)
        self.rect.y = random.randint(5, 16)
        self.Hp = hp

    def update(self):
        self.rect.y += random.randint(0, 2)
        if self.rect.bottom >= screen_hieght:
            self.rect.x = random.randint(30, screen_width - 40)
            self.rect.y = random.randint(5, 16)

    def shootcollision(self):
        self.Hp -= random.randint(5, 13)
        if self.Hp <= 0:
            self.Hp = 0

    def MidsileCollision(self):
        self.Hp -= 70
        if self.Hp <= 0:
            self.Hp = 0

    def getHp(self):
        return self.Hp
    
# Class Effect
class Effect(imageMeteor):
    def __init__(self, image, x, y):
        super().__init__(Boom, 0)
        self.image = image
        self.rect = self.image.get_rect()
        posX = x
        posY = y
        self.rect.x = posX
        self.rect.y = posY

    def update(self):
        self.rect.y += random.randint(2, 5)
        for spriteEffect in group_Effect.sprites():
            if spriteEffect.rect.bottom >= screen_hieght:
                group_Effect.remove(spriteEffect)

# function create Meteor
def create_Meteor_A(num_sprites, delay):
    for _ in range(num_sprites):
        sprite_Meteor_A = imageMeteor(Meteor_A, 60)
        group_Meteor_A.add(sprite_Meteor_A)
        pygame.display.update()
        pygame.time.delay(delay)

def create_Meteor_B(num_spirtes, delay):
    for _ in range(num_spirtes):
        sprite_Meteor_B = imageMeteor(Meteor_B, 40)
        group_Meteor_B.add(sprite_Meteor_B)
        pygame.display.update()
        pygame.time.delay(delay)

# Class Bullet
class Shoot(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y

    def update(self):
        self.rect.y -= 14

# Show Display
running = True
create_Meteor_A(4, 1000)
create_Meteor_B(6, 1000)
cooldown = 15000
last_time = 0
while running:
    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False

        # click to shoot
        if events.type == pygame.MOUSEBUTTONDOWN:
            pos_x = SpaceF_rect.centerx
            pos_y = SpaceF_rect.top + 30
            sprite_Bullet = Shoot(Bullet, pos_x, pos_y)
            group_Bullet.add(sprite_Bullet)

    # Import keyboards
    keys = pygame.key.get_pressed()
    current_time = pygame.time.get_ticks()

    # Space Control
    if keys[pygame.K_a] and SpaceF_rect.left > 0:
        SpaceF_rect.centerx -= 10
    if keys[pygame.K_d] and SpaceF_rect.right < screen_width:
        SpaceF_rect.centerx += 10

    if keys[pygame.K_e] and (current_time - last_time >= cooldown):
        pos_x = SpaceF_rect.centerx
        pos_y = SpaceF_rect.top + 30
        sprite_Bullet = Shoot(Midsile, pos_x, pos_y)
        group_Midsile.add(sprite_Bullet)
        last_time = current_time

    cooldown_remaining = max(0, (cooldown - (current_time - last_time)) // 1000)
    cooldown_text = font_1.render(str(cooldown_remaining), True, (0 ,168, 14))

    screen.blit(backgroud, (0, 0))
    screen.blit(SpaceF, SpaceF_rect)
    screen.blit(MidsileImg, MidsileImg_rect)
    screen.blit(cooldown_text, (512, 100))

    for spriteMeteor_A in group_Meteor_A.sprites():
        collision_A = pygame.sprite.spritecollide(spriteMeteor_A, group_Bullet, True)
        collision_Midsile = pygame.sprite.spritecollide(spriteMeteor_A, group_Midsile, True)
        spriteEffect = Effect(Boom_A, spriteMeteor_A.rect.x, spriteMeteor_A.rect.y)
        if collision_A:
            spriteMeteor_A.shootcollision()
        if collision_A and spriteMeteor_A.getHp() == 0:
            score += random.randint(5, 8)
            group_Effect.add(spriteEffect)
            group_Meteor_A.remove(spriteMeteor_A)
            sprite_Meteor_A = imageMeteor(Meteor_A, 60)
            group_Meteor_A.add(sprite_Meteor_A)
            score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
            pygame.display.update()
        if collision_Midsile:
            spriteMeteor_A.MidsileCollision()
        if collision_Midsile and spriteMeteor_A.getHp() == 0:
            score += random.randint(5, 8)
            group_Effect.add(spriteEffect)
            group_Meteor_A.remove(spriteMeteor_A)
            sprite_Meteor_A = imageMeteor(Meteor_A, 60)
            group_Meteor_A.add(sprite_Meteor_A)
            score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
            pygame.display.update()
        if SpaceF_rect.colliderect(spriteMeteor_A.rect):
            Hp -= random.randint(3 ,6)
            Hp_text = font_3.render(str(Hp) + " %", True, (0, 168, 14))
            group_Meteor_A.remove(spriteMeteor_A)
            sprite_Meteor_A = imageMeteor(Meteor_A, 60)
            group_Meteor_A.add(sprite_Meteor_A)
            
    for spriteMeteor_B in group_Meteor_B.sprites():
        collision_B = pygame.sprite.spritecollide(spriteMeteor_B, group_Bullet, True)
        collision_Midsile = pygame.sprite.spritecollide(spriteMeteor_B, group_Midsile, True)
        spriteEffect = Effect(Boom_B, spriteMeteor_B.rect.x, spriteMeteor_B.rect.y)
        if collision_B:
            spriteMeteor_B.shootcollision()
        if collision_B and spriteMeteor_B.getHp() == 0:
            score += random.randint(3, 5)
            group_Effect.add(spriteEffect)
            group_Meteor_B.remove(spriteMeteor_B)
            sprite_Meteor_B = imageMeteor(Meteor_B, 60)
            group_Meteor_B.add(sprite_Meteor_B)
            score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
            pygame.display.update()
        if collision_Midsile:
            spriteMeteor_B.MidsileCollision()
        if collision_Midsile and spriteMeteor_B.getHp() == 0:
            score += random.randint(3, 5)
            group_Effect.add(spriteEffect)
            group_Meteor_B.remove(spriteMeteor_B)
            sprite_Meteor_B = imageMeteor(Meteor_B, 60)
            group_Meteor_B.add(sprite_Meteor_B)
            score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
            pygame.display.update()
        if SpaceF_rect.colliderect(spriteMeteor_B.rect):
            Hp -= random.randint(2 ,4)
            Hp_text = font_3.render(str(Hp) + " %", True, (0, 168, 14))
            group_Meteor_B.remove(spriteMeteor_B)
            sprite_Meteor_B = imageMeteor(Meteor_B, 60)
            group_Meteor_B.add(sprite_Meteor_B)

    for spriteEffect in group_Effect.sprites():
        if SpaceF_rect.colliderect(spriteEffect.rect):
            Hp -= random.randint(1 ,2)
            Hp_text = font_3.render(str(Hp) + " %", True, (0, 168, 14))
            group_Effect.remove(spriteEffect)

    group_Bullet.update()
    group_Meteor_A.update()
    group_Meteor_B.update()
    group_Effect.update()
    group_Midsile.update()

    # draw Meteor_A
    group_Bullet.draw(screen)
    group_Meteor_A.draw(screen)
    group_Meteor_B.draw(screen)
    group_Effect.draw(screen)
    group_Midsile.draw(screen)
    screen.blit(Hp_text, (20, 4))
    screen.blit(score_text, (20, 39))

    # GameOver
    if Hp <= 0:
        screen.blit(game_over, (0, 0))
        group_Meteor_A.remove(spriteMeteor_A)
        group_Meteor_B.remove(spriteMeteor_B)
        group_Effect.remove(spriteEffect)

    if keys[pygame.K_SPACE] and Hp <= 0:
        Hp = 100
        Hp_text = font_3.render(str(Hp) + " %", True, (0, 168, 14))
        score = 0
        score_text = font_2.render("Score : " + str(score), True, (201, 113, 4))
        create_Meteor_A(4, 0)
        create_Meteor_B(6, 0)
        screen.blit(backgroud, (0, 0))
        screen.blit(SpaceF, SpaceF_rect)
        screen.blit(MidsileImg, MidsileImg_rect)
        screen.blit(cooldown_text, (512, 232))
        screen.blit(Hp_text, (20, 4))
        screen.blit(score_text, (20, 39))

    pygame.display.update()
    # FPS define
    clock.tick(FPS)    

pygame.quit()
