import os
import sys

# Adiciona a raiz do projeto para o Python encontrar a pasta 'scripts'
sys.path.append(os.getcwd())

# O caminho correto conforme sua estrutura:
import time

from scripts.registry import physics_registry as reg


# 2. Toda a lógica do seu programa vai dentro da função main
def main():
    # --- Configurações da Simulação ---
    # Pegando unidades do dicionário para erudição visual
    u_pos = reg["mecanica"]["cinematica"]["s"]["unidade"] if reg else "m"
    u_vel = reg["mecanica"]["cinematica"]["v"]["unidade"] if reg else "m/s"
    u_acc = reg["mecanica"]["cinematica"]["a"]["unidade"] if reg else "m/s²"

    # Parâmetros Físicos
    # Altura Inicial digitada pelo usuárioP
    h_inicial = float(input("Altura Inicial: "))
    g = 9.81  # Gravidade (m/s²)
    v = 0.0  # Velocidade inicial (repouso)
    t = 0.0  # Tempo inicial
    dt = 0.1  # Passo de tempo (delta t) para a simulação

    print(f"{'='*40}")
    print("SIMULAÇÃO DE QUEDA LIVRE")
    print(f"Altura Inicial: {h_inicial} {u_pos}")
    print(f"Gravidade: {g} {u_acc}")
    print(f"{'='*40}\n")

    # --- Loop de Simulação (Lógica de Física Computacional) ---
    h_atual = h_inicial

    while h_atual > 0:
        # 1. Atualiza a velocidade: v = v0 + g * t
        # Aqui usamos v += g * dt (método de Euler)
        v += g * dt

        # 2. Atualiza a posição: s = s0 - v * dt
        # Subtraímos porque o objeto está caindo em direção ao solo (0)
        h_atual -= v * dt

        # 3. Incrementa o tempo
        t += dt

        # Garantir que a altura não seja negativa no print final
        exibir_h = max(0, h_atual)

        print(
            f"Tempo: {t:.1f}s | Altura: {exibir_h:.2f} {u_pos} | Velocidade: {v:.2f} {u_vel}"
        )

        # Pequena pausa para visualizarmos a "queda" no terminal
        time.sleep(0.5)

    print(f"\n{'='*40}")
    print("RESULTADO FINAL:")
    print(f"Altura foi de {h_inicial:.2f}.")
    print(f"Impacto em: {t:.2f} segundos.")
    print(f"Velocidade de impacto: {v:.2f} {u_vel} ({v*3.6:.2f} km/h)")
    print(f"{'='*40}")


# 3. Este bloco garante que o script funcione se você executá-lo diretamente
if __name__ == "__main__":
    main()
