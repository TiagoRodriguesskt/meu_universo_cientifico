import sys
from pathlib import Path

import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore

# Ajuste de path para o Monorepo
raiz = Path(__file__).resolve().parents[2]
sys.path.append(str(raiz))

# Constantes Astronômicas (Unidades: kg, m, s)
MU_SOL = 1.32712440018e20  # G * M_sol
UA = 1.495978707e11  # Unidade Astronômica em metros

# Dados das Órbitas (Simplificadas como circulares para Hohmann clássico)
r_terra = 1.0 * UA
r_marte = 1.524 * UA


def calcular_hohmann():
    # 1. Semieixo maior da elipse de transferência
    a_trans = (r_terra + r_marte) / 2

    # 2. Velocidades orbitais iniciais
    v_terra = np.sqrt(MU_SOL / r_terra)
    v_marte = np.sqrt(MU_SOL / r_marte)

    # 3. Velocidades na elipse de transferência (Vis-Viva)
    # Na partida (Periélio)
    v_perihelio = np.sqrt(MU_SOL * (2 / r_terra - 1 / a_trans))
    # Na chegada (Afélio)
    v_afelio = np.sqrt(MU_SOL * (2 / r_marte - 1 / a_trans))

    # 4. Cálculo dos Delta-V
    dv1 = v_perihelio - v_terra
    dv2 = v_marte - v_afelio
    dv_total = dv1 + dv2

    # 5. Tempo de viagem (Metade do período orbital da elipse)
    periodo_segundos = 2 * np.pi * np.sqrt(a_trans**3 / MU_SOL)
    tempo_viagem_dias = (periodo_segundos / 2) / (24 * 3600)

    return {
        "dv1": dv1,
        "dv2": dv2,
        "total": dv_total,
        "dias": tempo_viagem_dias,
        "a_trans": a_trans,
    }


def plotar_sistema(res):
    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={"projection": "polar"})

    # Órbitas circulares
    theta = np.linspace(0, 2 * np.pi, 500)
    ax.plot(theta, np.full_like(theta, r_terra / UA), "b--", label="Terra", alpha=0.5)
    ax.plot(theta, np.full_like(theta, r_marte / UA), "r--", label="Marte", alpha=0.5)

    # Órbita de Transferência (Meia elipse)
    # Equação da elipse em coordenadas polares: r = a(1-e^2)/(1+e cos theta)
    e = (r_marte - r_terra) / (r_marte + r_terra)
    theta_trans = np.linspace(0, np.pi, 200)
    r_trans = (res["a_trans"] * (1 - e**2)) / (1 + e * np.cos(theta_trans))

    ax.plot(theta_trans, r_trans / UA, "g", linewidth=2, label="Trajetória de Hohmann")

    # Sol
    ax.plot(0, 0, "yo", markersize=10, label="Sol")

    ax.set_title(
        f"Transferência de Hohmann: Terra -> Marte\nTempo de Viagem: {res['dias']:.2f} dias",
        va="bottom",
    )
    ax.legend(
        loc="upper left",
        bbox_to_anchor=(0.8, 1.15),  # Coordenadas relativas ao eixo (x, y)
        title="Legenda Orbital",
        frameon=True,
        shadow=True,
    )  # mudança na parte superior direito
    plt.show()


# Execução
if __name__ == "__main__":
    resultados = calcular_hohmann()
    print("--- RESULTADOS DA MISSÃO ---")
    print(f"Δv1 (Saída da Terra): {resultados['dv1']:.2f} m/s")
    print(f"Δv2 (Inserção em Marte): {resultados['dv2']:.2f} m/s")
    print(f"Δv Total: {resultados['total']:.2f} m/s")
    print(f"Tempo de Viagem: {resultados['dias']:.2f} dias")

    plotar_sistema(resultados)
