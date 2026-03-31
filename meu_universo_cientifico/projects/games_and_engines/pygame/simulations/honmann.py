import sys
from pathlib import Path

import numpy as np  # type: ignore
import pygame  # type: ignore

# --- CONFIGURAÇÃO DE AMBIENTE (MONOREPO) ---
raiz = Path(__file__).resolve().parents[5]
sys.path.append(str(raiz))

# Tenta carregar autenticação só para validar o sistema de chaves (opcional neste script)
try:
    from keys.keys import MINHA_CHAVE, validar_conexao

    if validar_conexao():
        print(f"✅ Autenticado via módulo keys. Chave: {MINHA_CHAVE[:4]}...")  # type: ignore
except:  # noqa: E722
    pass

# --- CONFIGURAÇÕES DO SIMULADOR ---
LARGURA, ALTURA = 1000, 800
FPS = 60
G_SIM = 110  # Magnitude da força gravitacional simulada

# Configurações Planetárias (Simplificadas para visualização 2D)
# Distâncias em pixels e Velocidades angulares arbitrárias
raio_terra = 200.0
vel_angular_terra = 0.005

raio_marte = 350.0  # Proporcionalmente maior que a terra (1.52x real)
vel_angular_marte = 0.0026  # Mais lento que a terra (Kepler: T^2 prop r^3)

# Cores
ESPACO = (5, 5, 10)
SOL_COR = (255, 200, 0)
TERRA_COR = (0, 100, 255)
MARTE_COR = (200, 50, 50)
FOGUETE_COR = (0, 250, 255)


def rodar_simulacao():
    pygame.init()  # type: ignore
    tela = pygame.display.set_mode((LARGURA, ALTURA))  # type: ignore
    relogio = pygame.time.Clock()  # type: ignore

    # Estado Central (Sol)
    sol_pos = np.array([LARGURA // 2, ALTURA // 2], dtype=float)

    # Estado Inicial dos Planetas (Ângulo de fase)
    theta_terra = 0.0
    theta_marte = np.radians(-0.44)  # Marte começa a 45 graus da terra

    # Estado do Foguete (Sai da Terra)
    foguete_pos = sol_pos + np.array([raio_terra, 0.0])
    # Velocidade inicial: velocidade da terra + empuxo tangencial
    vel_terra_init = np.array([0.0, raio_terra * vel_angular_terra])
    foguete_vel = vel_terra_init + np.array([0.0, -0.15])  # Empuxo extra para a elipse

    rastro_foguete = []

    # --- LOOP PRINCIPAL DA SIMULAÇÃO ---
    rodando_missao = True
    foi_capturado = False

    while rodando_missao:
        tela.fill(ESPACO)

        for evento in pygame.event.get():  # type: ignore
            if evento.type == pygame.QUIT:  # type: ignore
                pygame.quit()  # type: ignore
                sys.exit()

        # --- 1. ATUALIZAÇÃO DOS PLANETAS ---
        # Movimento circular uniforme para Terra e Marte
        theta_terra += vel_angular_terra
        terra_pos = sol_pos + np.array(
            [np.cos(theta_terra) * raio_terra, np.sin(theta_terra) * raio_terra]
        )

        theta_marte += vel_angular_marte
        marte_pos = sol_pos + np.array(
            [np.cos(theta_marte) * raio_marte, np.sin(theta_marte) * raio_marte]
        )

        # --- 2. CÁLCULO DA FÍSICA DO FOGUETE ---
        if not foi_capturado:
            # Vetor e distância Sol-Foguete
            vetor_r = sol_pos - foguete_pos
            distancia = np.linalg.norm(vetor_r)

            # Magnitude da aceleração (Lei de Newton: G*M/r^2)
            direcao = vetor_r / distancia
            acc_mag = G_SIM / max(distancia**2, 100)
            aceleracao = direcao * acc_mag

            # Atualização de Velocidade e Posição (Integração de Euler)
            foguete_vel += aceleracao
            foguete_pos += foguete_vel

            # --- 3. LÓGICA DE INSERÇÃO EM MARTE (REDEZVOUS) ---
            dist_marte = np.linalg.norm(foguete_pos - marte_pos)

            if dist_marte < 15:  # Se chegar a 15 pixels de Marte
                foi_capturado = True
                print("🚀 SUCESSO: Inserção Orbital Concluída!")

        else:
            # Se foi capturado, o foguete "trava" na posição de Marte
            # Simulando que ele agora é um satélite do planeta
            foguete_pos = (
                marte_pos + (foguete_pos - marte_pos) * 0.1
            )  # Mantém um leve offset

        # --- 4. RENDERIZAÇÃO ---
        # Desenhar Órbitas (Círculos de referência)
        pygame.draw.circle(tela, (30, 30, 50), sol_pos.astype(int), int(raio_terra), 1)  # type: ignore
        pygame.draw.circle(tela, (40, 30, 40), sol_pos.astype(int), int(raio_marte), 1)  # type: ignore

        # Desenhar Rastro do Foguete (Histórico de posições)
        if not foi_capturado:
            rastro_foguete.append(tuple(foguete_pos.astype(int)))
            if len(rastro_foguete) > 600:
                rastro_foguete.pop(0)

        if len(rastro_foguete) > 2:
            pygame.draw.lines(tela, (0, 200, 255), False, rastro_foguete, 1)  # type: ignore

        # --- Nomes e rótulos ---
        fonte_corpos = pygame.font.SysFont("Consolas", 14, bold=True)  # type: ignore
        fonte_orbitas = pygame.font.SysFont("Consolas", 12, italic=True)  # type: ignore

        # 1. Rótulo da Órbita da Terra (o círculo maior fixo)
        txt_orb_terra = fonte_orbitas.render("1.0 UA", True, (50, 50, 80))
        tela.blit(txt_orb_terra, (sol_pos[0] + raio_terra, sol_pos[1] + 5))

        # 2. Rótulo da Órbita de Marte (o círculo maior fixo)
        txt_orb_marte = fonte_orbitas.render("1.52 UA", True, (60, 40, 40))
        tela.blit(txt_orb_marte, (sol_pos[0] + raio_marte, sol_pos[1] + 5))

        # Desenhar Corpos Celestes
        pygame.draw.circle(tela, SOL_COR, sol_pos.astype(int), 30)  # type: ignore # Sol
        # 3. Nome do SOL
        txt_sol = fonte_corpos.render("SOL", True, (255, 255, 255))
        tela.blit(txt_sol, (sol_pos[0] - 15, sol_pos[1] - 50))

        pygame.draw.circle(tela, TERRA_COR, terra_pos.astype(int), 8)  # type: ignore # Terra
        # 4. Nome da TERRA (acompanha terra_pos)
        txt_terra = fonte_corpos.render("TERRA", True, (255, 255, 255))
        tela.blit(txt_terra, (terra_pos[0] - 20, terra_pos[1] - 25))

        pygame.draw.circle(tela, MARTE_COR, marte_pos.astype(int), 10)  # type: ignore # Marte
        # 5. Nome de MARTE (acompanha marte_pos)
        txt_marte = fonte_corpos.render("MARTE", True, (255, 255, 255))
        tela.blit(txt_marte, (marte_pos[0] - 20, marte_pos[1] - 25))

        # Desenhar Foguete (Destaque se capturado)
        cor_foguete = (255, 255, 255) if foi_capturado else FOGUETE_COR
        pygame.draw.circle(tela, cor_foguete, foguete_pos.astype(int), 4)  # type: ignore

        # 6. Nome do FOGUETE (apenas se não estiver acoplado)
        if not foi_capturado:
            txt_foguete = fonte_corpos.render("FOGUETE", True, (0, 255, 255))
            tela.blit(txt_foguete, (foguete_pos[0] - 25, foguete_pos[1] - 20))

        # Interface de Diagnóstico
        fonte = pygame.font.SysFont("Consolas", 16)  # type: ignore
        status = "ESTACIONADO EM MARTE" if foi_capturado else "EM TRÂNSITO"
        txt = fonte.render(
            f"STATUS: {status} | DIST MARTE: {np.linalg.norm(foguete_pos-marte_pos):.1f}",
            True,
            (255, 255, 255),
        )
        tela.blit(txt, (10, 10))

        pygame.display.flip()  # type: ignore
        relogio.tick(FPS)


if __name__ == "__main__":
    rodar_simulacao()
