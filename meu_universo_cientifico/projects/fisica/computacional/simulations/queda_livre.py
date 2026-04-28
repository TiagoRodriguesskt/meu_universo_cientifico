"""
Busca o script registry.py na raiz do meu_universo_cientifico
"""

import os
import sys
import time


# --- Bloco de Importação do Registry ---
def importar_registry():
    caminho_base = os.path.abspath(os.path.dirname(__file__))
    enquanto = caminho_base
    while os.path.basename(enquanto) != "meu_universo_cientifico":
        parent = os.path.dirname(enquanto)
        if parent == enquanto:
            break
        enquanto = parent
    for raiz, diretorios, arquivos in os.walk(enquanto):
        if "scripts" in diretorios:
            sys.path.append(os.path.join(raiz, "scripts"))
            try:
                from registry import physics_registry

                return physics_registry
            except ImportError:
                continue
    return None


reg = importar_registry()

# --- Configurações da Simulação ---
# Pegando unidades do dicionário para erudição visual
u_pos = reg["mecanica"]["cinematica"]["s"]["unidade"] if reg else "m"
u_vel = reg["mecanica"]["cinematica"]["v"]["unidade"] if reg else "m/s"
u_acc = reg["mecanica"]["cinematica"]["a"]["unidade"] if reg else "m/s²"

# Parâmetros Físicos
# h_inicial = 55.0  # Altura (m) - Exemplo do seu vaso
h_inicial = float(input("Altura Inicial: "))  # Usuário digita a altura inicial
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
