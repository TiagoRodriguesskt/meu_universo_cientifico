import math
import sys

import pygame

# --- Configurações de Tela ---
WIDTH, HEIGHT = 1200, 800
FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)  # Sol
BLUE = (50, 150, 255)  # Terra
RED = (255, 80, 80)  # Marte
GRAY = (200, 200, 200)  # Nave

# --- Constantes Físicas Reais (Escaladas) ---
G = 6.674e-11
M_SUN = 1.989e30
# Distâncias médias ao Sol (metros)
AU_TERRA = 1.496e11
AU_MARTE = 2.279e11

# Fator de Escala para caber na tela
SCALE = (WIDTH * 0.35) / AU_MARTE
TIMESTEP = 3600 * 24  # 1 segundo = 24 dias (para ver a viagem acontecer)


class Planet:
    def __init__(self, distance, mass, color, name, angle):
        self.dist = distance
        self.mass = mass
        self.color = color
        self.name = name
        self.angle = angle
        # Velocidade orbital circular: v = sqrt(G*M_sol / r)
        self.vel = math.sqrt(G * M_SUN / self.dist)
        self.x = self.dist * math.cos(self.angle)
        self.y = self.dist * math.sin(self.angle)

    def update(self):
        # Movimento circular uniforme simplificado para os planetas
        omega = self.vel / self.dist
        self.angle += omega * TIMESTEP
        self.x = self.dist * math.cos(self.angle)
        self.y = self.dist * math.sin(self.angle)

    def draw(self, win):
        px = int(self.x * SCALE + WIDTH / 2)
        py = int(self.y * SCALE + HEIGHT / 2)
        pygame.draw.circle(win, self.color, (px, py), 8)
        # Desenha a órbita
        pygame.draw.circle(
            win, self.color, (WIDTH // 2, HEIGHT // 2), int(self.dist * SCALE), 1
        )


class Spacecraft:
    def __init__(self, x, y, vx, vy):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.path = []

    def update(self):
        # Atração gravitacional do SOL
        dist = math.sqrt(self.x**2 + self.y**2)
        accel = G * M_SUN / dist**2
        ax = -accel * (self.x / dist)
        ay = -accel * (self.y / dist)

        self.vx += ax * TIMESTEP
        self.vy += ay * TIMESTEP
        self.x += self.vx * TIMESTEP
        self.y += self.vy * TIMESTEP
        self.path.append((self.x, self.y))

    def draw(self, win):
        if len(self.path) > 2:
            points = [
                (int(p[0] * SCALE + WIDTH / 2), int(p[1] * SCALE + HEIGHT / 2))
                for p in self.path
            ]
            pygame.draw.lines(win, WHITE, False, points, 1)
        px = int(self.x * SCALE + WIDTH / 2)
        py = int(self.y * SCALE + HEIGHT / 2)
        pygame.draw.circle(win, GRAY, (px, py), 4)


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simulação Interplanetária: Terra -> Marte (Hohmann)")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("Arial", 18)

    # 1. Criar Planetas (Ângulo inicial para o "encontro" ocorrer no apogeu)
    terra = Planet(AU_TERRA, 5.97e24, BLUE, "Terra", 0)
    marte = Planet(AU_MARTE, 6.39e23, RED, "Marte", 0.75)  # Marte começa adiantado

    # 2. Configurar a Nave no instante do TMI (Trans-Mars Injection)
    # No perigeu (órbita da Terra), a velocidade deve aumentar
    # para que o apogeu chegue em Marte.
    r1 = AU_TERRA
    r2 = AU_MARTE
    v_hohmann = math.sqrt(G * M_SUN / r1) * math.sqrt((2 * r2) / (r1 + r2))

    # Nave começa na posição da Terra, mas com a velocidade de transferência
    nave = Spacecraft(terra.x, terra.y, 0, v_hohmann)

    run = True
    while run:
        clock.tick(FPS)
        win.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Desenhar o SOL
        pygame.draw.circle(win, YELLOW, (WIDTH // 2, HEIGHT // 2), 15)

        # Atualizar e Desenhar
        terra.update()
        marte.update()
        nave.update()

        terra.draw(win)
        marte.draw(win)
        nave.draw(win)

        # Informações
        dist_marte = math.sqrt((nave.x - marte.x) ** 2 + (nave.y - marte.y) ** 2) / 1e9
        txt = font.render(
            f"Distância Nave-Marte: {dist_marte:.2f} milhões de km", True, WHITE
        )
        win.blit(txt, (20, 20))

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
