import pygame
import random

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERMELHO = (255, 0, 0)

# Dimensões da tela
largura_tela = 800
altura_tela = 600

# Inicialização do Pygame
pygame.init()
tela = pygame.display.set_mode((largura_tela, altura_tela))
pygame.display.set_caption("Donkey Kong")

# Classe do jogador
class Jogador(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((50, 50))
        self.image.fill(VERMELHO)
        self.rect = self.image.get_rect()
        self.rect.center = (largura_tela // 2, altura_tela - 50)

    def update(self):
        # Movimentação do jogador
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT]:
            self.rect.x += 5

        # Restringir o jogador dentro da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > largura_tela:
            self.rect.right = largura_tela

    def draw(self, tela):
        tela.blit(self.image, self.rect)

# Classe do inimigo (barril)
class Inimigo(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((30, 30))
        self.image.fill(BRANCO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(50, largura_tela - 50)
        self.rect.y = 0
        self.velocidade = random.randint(1, 3)

    def update(self):
        self.rect.y += self.velocidade

        # Reiniciar a posição do inimigo quando ele sair da tela
        if self.rect.top > altura_tela:
            self.rect.x = random.randint(50, largura_tela - 50)
            self.rect.y = 0
            self.velocidade = random.randint(1, 3)

    def draw(self, tela):
        tela.blit(self.image, self.rect)

# Classe da IA controlando o jogador
class IA:
    def __init__(self, jogador):
        self.jogador = jogador

    def update(self):
        # Lógica da IA para controlar o jogador
        inimigo_mais_proximo = None
        menor_distancia = float('inf')
        for inimigo in inimigos:
            distancia = abs(inimigo.rect.x - self.jogador.rect.x)
            if distancia < menor_distancia:
                menor_distancia = distancia
                inimigo_mais_proximo = inimigo

        if inimigo_mais_proximo is not None:
            if self.jogador.rect.x < inimigo_mais_proximo.rect.x:
                self.jogador.rect.x -= 5
            else:
                self.jogador.rect.x += 5

# Criação dos grupos de sprites
todos_sprites = pygame.sprite.Group()
jogador = Jogador()
todos_sprites.add(jogador)

inimigos = pygame.sprite.Group()
for _ in range(5):
    inimigo = Inimigo()
    todos_sprites.add(inimigo)
    inimigos.add(inimigo)

ia = IA(jogador)

# Loop principal do jogo
executando = True
clock = pygame.time.Clock()

while executando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            executando = False

    # Atualizar os sprites
    todos_sprites.update()
    ia.update()

    # Verificar colisões entre jogador e inimigos
    if pygame.sprite.spritecollide(jogador, inimigos, False):
        print("Game Over")
        executando = False

    # Desenhar na tela
    tela.fill(PRETO)
    todos_sprites.draw(tela)
    pygame.display.flip()
    clock.tick(60)

# Encerrando o Pygame
pygame.quit()
