import pygame
import random

# Dimensiones de la pantalla
WIDTH, HEIGHT = 800, 600

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Inicialización de Pygame
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space War")
clock = pygame.time.Clock()

# Función para dibujar texto en la pantalla
def draw_text(surface, text, size, x, y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

# Función para dibujar la barra de escudo
def draw_shield_bar(surface, x, y, percentage):
    bar_length, bar_height = 100, 10
    fill = (percentage / 100) * bar_length
    border = pygame.Rect(x, y, bar_length, bar_height)
    fill = pygame.Rect(x, y, fill, bar_height)
    pygame.draw.rect(surface, GREEN, fill)
    pygame.draw.rect(surface, WHITE, border, 2)

# Clase del jugador
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.shield = 100
    
    # Actualización del movimiento del jugador
    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    # Método para disparar una bala
    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)
        laser_sound.play()

# Clase para los meteoros
class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-140, -100)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)
    
    # Actualización de la posición del meteoro
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT + 10 or self.rect.left < -20 or self.rect.right > WIDTH + 40:
            self.reset_position()
    
    # Restablece la posición del meteoro cuando sale de la pantalla
    def reset_position(self):
        self.rect.x = random.randrange(WIDTH - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)

# Método para crear y agregar un meteoro
def create_meteor():
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

# Clase para las balas
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png")
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10
    
    # Actualiza la posición de la bala
    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

# Clase para las explosiones
class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    
    # Controla la animación de la explosión
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

# Pantalla de inicio
def show_go_screen():
    screen.blit(background, [0, 0])
    draw_text(screen, "Space War", 65, WIDTH // 2, HEIGHT // 4)
    draw_text(screen, "Press any key to start", 20, WIDTH // 2, HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:
                waiting = False

# Carga de imágenes y sonidos
meteor_images = [pygame.image.load(img).convert() for img in [
    "assets/meteorGrey_big1.png", "assets/meteorGrey_big2.png", 
    "assets/meteorGrey_big3.png", "assets/meteorGrey_big4.png",
    "assets/meteorGrey_med1.png", "assets/meteorGrey_med2.png",
    "assets/meteorGrey_small1.png", "assets/meteorGrey_small2.png",
    "assets/meteorGrey_tiny1.png", "assets/meteorGrey_tiny2.png"
]]
for img in meteor_images:
    img.set_colorkey(BLACK)

explosion_anim = []
for i in range(9):
    file = f"assets/regularExplosion0{i}.png"
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img, (70, 70))
    explosion_anim.append(img_scale)

background = pygame.image.load("assets/background.png").convert()
laser_sound = pygame.mixer.Sound("assets/laser5.ogg")
explosion_sound = pygame.mixer.Sound("assets/explosion.wav")
pygame.mixer.music.load("assets/music.ogg")
pygame.mixer.music.set_volume(0.2)

# Inicialización de variables del juego
pygame.mixer.music.play(loops=-1)
game_over = True
running = True
while running:
    if game_over:
        show_go_screen()
        game_over = False
        all_sprites = pygame.sprite.Group()
        meteor_list = pygame.sprite.Group()
        bullets = pygame.sprite.Group()
        player = Player()
        all_sprites.add(player)
        for _ in range(8):
            create_meteor()
        score = 0 

    # Control de velocidad del juego
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            player.shoot()

    # Actualización de sprites
    all_sprites.update()

    # Verificación de colisiones entre meteoros y balas
    hits = pygame.sprite.groupcollide(meteor_list, bullets, True, True)
    for hit in hits:
        score += 10
        explosion_sound.play()
        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        create_meteor()

    # Verificación de colisiones entre meteoros y el jugador
    hits = pygame.sprite.spritecollide(player, meteor_list, True)
    for hit in hits:
        player.shield -= 10
        create_meteor()
        if player.shield <= 0:
            game_over = True

    # Renderizado de la pantalla
    screen.blit(background, [0, 0])
    all_sprites.draw(screen)
    draw_text(screen, str(score), 25, WIDTH // 2, 10)
    draw_shield_bar(screen, 5, 5, player.shield)
    pygame.display.flip()

pygame.quit()