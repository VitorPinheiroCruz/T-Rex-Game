import pygame
import sys
from random import randint
import time

import setuptools

pygame.init()
width = 800
height = 300
pygame.display.set_caption('T-Rex Google - Runner')
screen = pygame.display.set_mode((width, height))
velocidade_corrida = 10
velocidade_nuvens = 5
chronos = pygame.time.Clock()
end_scores = 0


class Screen:
    def __init__(self):
        self.chao_1 = pygame.image.load('Assets/Other/Track.png')
        self.largura = self.chao_1.get_width()
        self.chao_y = height * 0.86
        self.chao_1_rect = self.chao_1.get_rect(topleft=(0, self.chao_y))
        self.chao_2_rect = self.chao_1.get_rect(topleft=(self.largura, self.chao_y))
        self.velocidade_nuvens = 5
        self.cloud = pygame.image.load('Assets/Other/Cloud.png')
        self.cloud_rect_1 = self.cloud.get_rect(topright=(randint(100, 800), randint(10, 150)))
        self.cloud_rect_2 = self.cloud.get_rect(topright=(randint(850, 1100), randint(10, 150)))
        self.scores = 0

    def desenhar_chao(self, tela):
        tela.fill((32, 32, 32))
        tela.blit(self.chao_1, self.chao_1_rect)
        tela.blit(self.chao_1, self.chao_2_rect)

    def animar_piso(self):
        self.chao_1_rect.x -= velocidade_corrida
        self.chao_2_rect.x -= velocidade_corrida
        if self.chao_1_rect.x + self.largura < 0:
            self.chao_1_rect.x = self.chao_2_rect.x + self.largura
        if self.chao_2_rect.x + self.largura < 0:
            self.chao_2_rect.x = self.chao_1_rect.x + self.largura

    def desenhar_nuvens(self, tela):
        tela.blit(self.cloud, self.cloud_rect_1)
        tela.blit(self.cloud, self.cloud_rect_2)

    def animar_nuvens(self):
        self.cloud_rect_1.x -= velocidade_nuvens
        self.cloud_rect_2.x -= velocidade_nuvens
        if self.cloud_rect_1.x < -70:
            self.cloud_rect_1.x = randint(800, 1100)
            self.cloud_rect_1.y = randint(10, 150)
        if self.cloud_rect_2.x < -70:
            self.cloud_rect_2.x = randint(1200, 1300)
            self.cloud_rect_2.y = randint(10, 150)

    def score(self, tela):  # bold=True
        fonte_score = pygame.font.SysFont('Arial', 30)

        if velocidade_corrida == 10:
            self.scores += 1
        else:
            self.scores += 3
        score_text = fonte_score.render(f'Score: {self.scores - end_scores}', 1, (119, 136, 153))
        score_text_rect = score_text.get_rect(topright=(780, 20))
        tela.blit(score_text, score_text_rect)

    def update(self):
        self.animar_piso()
        self.animar_nuvens()


class Cactus(pygame.sprite.Sprite):
    def __init__(self, index):
        super().__init__()
        self.large_cactu_s1 = pygame.image.load('Assets/Cactus/LargeCactus1.png').convert_alpha()
        self.large_cactu_s2 = pygame.image.load('Assets/Cactus/LargeCactus2.png').convert_alpha()
        self.large_cactu_s3 = pygame.image.load('Assets/Cactus/LargeCactus3.png').convert_alpha()
        self.smal_cactu_s1 = pygame.image.load('Assets/Cactus/SmallCactus1.png').convert_alpha()
        self.smal_cactu_s2 = pygame.image.load('Assets/Cactus/SmallCactus2.png').convert_alpha()
        self.smal_cactu_s3 = pygame.image.load('Assets/Cactus/SmallCactus3.png').convert_alpha()
        self.list_cactus = [self.large_cactu_s1, self.large_cactu_s2, self.large_cactu_s3, self.smal_cactu_s1,
                            self.smal_cactu_s1, self.smal_cactu_s1]
        self.index_list_cactus = index
        self.image = self.list_cactus[self.index_list_cactus]
        self.cactus_x = 900
        self.rect = self.image.get_rect(topleft=(self.cactus_x, 200))

    def desenhar(self):
        self.image = self.list_cactus[self.index_list_cactus]
        # self.index_list_cactus = randint(0, 5)

    def animar_cactus(self):
        self.rect.x -= velocidade_corrida
        if self.rect.x < -75:
            self.kill()

    def update(self):
        self.desenhar()
        self.animar_cactus()


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.dino_duck_1 = pygame.transform.scale(pygame.image.load('Assets/Dino/DinoDuck1.png').convert_alpha(), (59, 30))
        self.dino_duck_2 = pygame.transform.scale(pygame.image.load('Assets/Dino/DinoDuck2.png').convert_alpha(), (59, 30))
        self.dino_jump = pygame.transform.scale(pygame.image.load('Assets/Dino/DinoJump.png').convert_alpha(), (43.5, 47))
        self.dino_run_1 = pygame.transform.scale(pygame.image.load('Assets/Dino/DinoRun1.png').convert_alpha(), (43.5, 47))
        self.dino_run_2 = pygame.transform.scale(pygame.image.load('Assets/Dino/DinoRun2.png').convert_alpha(), (43.5, 47))

        self.dino_lista = [self.dino_run_1, self.dino_run_2]
        self.dino_lista_duck = [self.dino_duck_1, self.dino_duck_2]
        self.dino_index = 0
        self.forca = 0
        self.image = self.dino_lista[self.dino_index]
        self.rect = self.image.get_rect(bottomleft=(40, 285))

    def desenhar_animar_dino(self):
        self.dino_index += 0.3
        if self.dino_index > len(self.dino_lista):
            self.dino_index = 0
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN] and self.rect.bottom == 285:
            self.image = self.dino_lista_duck[int(self.dino_index)]
        elif self.rect.bottom == 285:
            self.image = self.dino_lista[int(self.dino_index)]


    def pular(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom == 285:
            self.forca = -27

    def gravidade(self):
        self.forca += 2
        if self.rect.bottom < 285:
            self.image = self.dino_jump
        self.rect.bottom += self.forca
        if self.rect.bottom >= 285:
            self.rect.bottom = 285

    def update(self):
        self.desenhar_animar_dino()
        self.gravidade()
        self.pular()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        bird_1 = pygame.image.load('Assets/Bird/Bird1.png').convert_alpha()
        bird_2 = pygame.image.load('Assets/Bird/Bird2.png').convert_alpha()
        self.bird_lista = [bird_1, bird_2]
        self.bird_index = 0
        self.image = self.bird_lista[self.bird_index]
        self.rect = self.image.get_rect(center=(3000, 170))

    def desenhar_bird(self):
        bird_size = 1.5
        self.image = pygame.transform.smoothscale(self.bird_lista[int(self.bird_index)], (
            (self.bird_lista[int(self.bird_index)]).get_width() / bird_size,
            (self.bird_lista[int(self.bird_index)]).get_height() / bird_size))

    def animar_passaro(self):
        self.bird_index += 0.2
        if self.bird_index > len(self.bird_lista):
            self.bird_index = 0
        # movimentar o bird no eixo X
        self.rect.x -= velocidade_corrida * 1.5
        if self.rect.x < - 40:
            self.kill()

    def update(self):
        self.desenhar_bird()
        self.animar_passaro()


class Collisions_cactus_birds:
    def collision_sprite_cactus(self):
        if pygame.sprite.spritecollide(dino.sprite, cactus, False):
            cactus.empty()
            bird.empty()
            return False
        else:
            return True

    def collision_sprite_birds(self):
        if pygame.sprite.spritecollide(dino.sprite, bird, False):
            bird.empty()
            cactus.empty()
            return False
        else:
            return True

    def call_colisions(self):
        return (self.collision_sprite_birds() and self.collision_sprite_cactus())


chao_e_nuvens = Screen()
dino = pygame.sprite.GroupSingle()
dino.add(Dino())

cactus = pygame.sprite.Group()
bird = pygame.sprite.Group()

game_active = False

collisions = Collisions_cactus_birds()

def apresentation_screen():
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        return True

# Set Timer
cactus_time = pygame.USEREVENT + 1
pygame.time.set_timer(cactus_time, randint(1500, 2000))

bird_time = pygame.USEREVENT + 2
pygame.time.set_timer(bird_time, randint(3000, 6000))

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            print('Vc clicou no X')
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYUP:
            velocidade_corrida = 10

        if game_active:
            if event.type == cactus_time:
                cactus.add(Cactus(randint(0,5)))

            if event.type == bird_time:
                bird.add(Bird())

    if game_active:
        chao_e_nuvens.desenhar_chao(screen)
        chao_e_nuvens.desenhar_nuvens(screen)

        chao_e_nuvens.score(screen)
        dino.draw(screen)
        bird.draw(screen)
        cactus.draw(screen)
        dino.update()
        bird.update()
        cactus.update()
        chao_e_nuvens.update()

        # Alterar velocidade quanto ele corre
        keys = pygame.key.get_pressed()
        if keys[pygame.K_DOWN]:
            velocidade_corrida = 30
            velocidade_nuvens = 8

        game_active = collisions.call_colisions()

    else:
        screen.fill((32, 32, 32))
        dino_start = pygame.image.load('Assets/Dino/DinoStart.png').convert_alpha()
        dino_tela_inicial = pygame.transform.scale2x(dino_start)
        dino_tela_inicial_rect = dino_tela_inicial.get_rect(center=(400, 190))
        fonte_apresentacao = pygame.font.Font('Assets/font/Pixeltype.ttf', 75)
        apresentacao = fonte_apresentacao.render('Press Space to Play!', 1, (119, 136, 153))
        apresentacao_rect = apresentacao.get_rect(center=(400, 60))
        end_scores = chao_e_nuvens.scores

        screen.blit(apresentacao, apresentacao_rect)
        screen.blit(dino_tela_inicial, dino_tela_inicial_rect)
        game_active = apresentation_screen()

    pygame.display.update()
    chronos.tick(30)
