"""
DocString: Queda Visual

# Documentação Física do Simulador

Abaixo estão as fórmulas utilizadas para calcular o impacto do objeto ao atingir o solo.

### 1. Energia Cinética ($E_c$)
Calcula a energia total acumulada pelo objeto devido ao seu movimento e massa.
$$E_c = \frac{1}{2} m v^2$$

### 2. Força de Impacto ($F$)
Utiliza o **Teorema do Trabalho-Energia** para determinar a força média baseada na distância de parada ($d$) do material.
$$F = \frac{E_c}{d}$$

### 3. Impacto em Toneladas ($T$)
Converte a força de Newtons para Tonelada-força ($tf$) usando a constante gravitacional padrão.
$$T = \frac{F}{9806,65}$$

---

### Fórmula Unificada
Para implementação direta no código:
$$T = \frac{m \cdot v^2}{2 \cdot d \cdot 9806,65}$$


"""

import sys

import pygame

# --- CONFIGURAÇÃO E ENTRADA DE DADOS ---
print("=" * 30)
print(" CONFIGURAÇÃO DA SIMULAÇÃO")
print("=" * 30)

massa_kg = float(input("Digite o peso do objeto (kg): "))
h_inicial_m = float(input("Digite a altura inicial (metros): "))

# --- SISTEMA DE VALIDAÇÃO DO SOLO ---
while True:
    print("\nEscolha o solo para o impacto:")
    print("1 - Concreto (Parada: 0.1m)")
    print("2 - Água (Parada: 5.0m)")
    print("3 - Grama (Parada: 1.0m)")

    solo_opt = input("Opção escolhida: ")

    if solo_opt in ["1", "2", "3"]:
        break
    else:
        print("\n[ERRO] Opção inválida! Digite 1, 2 ou 3.")

# --- PARÂMETROS DE FÍSICA E SOLO ---
g = 9.81
if solo_opt == "1":
    distancia_parada = 0.1
    nome_solo = "Concreto"
    cor_solo = (120, 120, 120)
elif solo_opt == "2":
    distancia_parada = 5.0
    nome_solo = "Água"
    cor_solo = (0, 100, 200)
else:
    distancia_parada = 1.0
    nome_solo = "Grama"
    cor_solo = (34, 139, 34)

# --- CONFIGURAÇÕES GRÁFICAS ---
LARGURA, ALTURA = 500, 700
pygame.init()
tela = pygame.display.set_mode((LARGURA, ALTURA))
relogio = pygame.time.Clock()
fonte = pygame.font.SysFont("Consolas", 18)

escala = (ALTURA - 150) / h_inicial_m if h_inicial_m > 0 else 1


def main():
    y_pos_m = 0
    velocidade = 0
    tempo_decorrido = 0
    caindo = True
    tonelada_impacto = 0
    camera_lenta = 0.5

    while True:
        # Controle de tempo e FPS
        dt = (relogio.tick(30) / 1000) * camera_lenta

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # --- LÓGICA DE FÍSICA (AQUI ESTAVA O ERRO) ---
        if caindo:
            # 1. Atualiza a física enquanto cai
            velocidade += g * dt
            y_pos_m += velocidade * dt
            tempo_decorrido += dt / camera_lenta

            # 2. Verifica se atingiu o solo
            if y_pos_m >= h_inicial_m:
                y_pos_m = h_inicial_m
                caindo = False  # Para a queda

                # 3. Cálculo do Impacto (Executa apenas uma vez agora)
                energia_cinetica = 0.5 * massa_kg * (velocidade**2)
                forca_n = energia_cinetica / distancia_parada
                tonelada_impacto = forca_n / 9806.65

        # --- RENDERIZAÇÃO ---
        tela.fill((25, 25, 30))

        # Desenhar Solo
        pygame.draw.rect(tela, cor_solo, (0, ALTURA - 50, LARGURA, 50))

        # Desenhar Objeto
        y_pixel = 50 + (y_pos_m * escala)
        pygame.draw.circle(tela, (0, 255, 200), (LARGURA // 2, int(y_pixel)), 15)

        # Painel de Dados
        dados = [
            f"Solo: {nome_solo}",
            f"Massa: {massa_kg} kg",
            f"Velocidade: {velocidade:.2f} m/s",
            f"Tempo: {tempo_decorrido:.2f} s",
            f"Dist. Parada: {distancia_parada} m",
        ]

        if not caindo:
            dados.append(f"IMPACTO: {tonelada_impacto:.4f} Toneladas")

        for i, texto in enumerate(dados):
            img = fonte.render(texto, True, (255, 255, 255))
            tela.blit(img, (20, 20 + (i * 25)))

        pygame.display.flip()


if __name__ == "__main__":
    main()
