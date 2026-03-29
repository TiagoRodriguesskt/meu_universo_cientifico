import customtkinter as ctk
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore  # noqa: F401
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class SimuladorFoguete(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Simulador de Foguete - Fís. Computacional")
        self.geometry("1100x700")

        # --- CORREÇÃO: FECHAMENTO SEGURO ---
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PAINEL LATERAL ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=15)
        self.sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.titulo = ctk.CTkLabel(
            self.sidebar, text="Parâmetros de Voo", font=("Arial", 18, "bold")
        )
        self.titulo.pack(pady=15)

        # Sliders
        self.m_seca_var = ctk.StringVar(value="500 kg")
        ctk.CTkLabel(self.sidebar, text="Massa da Estrutura:").pack()
        ctk.CTkLabel(
            self.sidebar, textvariable=self.m_seca_var, text_color="#3498db"
        ).pack()
        self.slider_seca = ctk.CTkSlider(
            self.sidebar,
            from_=100,
            to=2000,
            command=lambda v: self.m_seca_var.set(f"{int(v)} kg"),
        )
        self.slider_seca.set(500)
        self.slider_seca.pack(pady=(0, 15), padx=20)

        self.m_fuel_var = ctk.StringVar(value="1000 kg")
        ctk.CTkLabel(self.sidebar, text="Massa do Combustível:").pack()
        ctk.CTkLabel(
            self.sidebar, textvariable=self.m_fuel_var, text_color="#3498db"
        ).pack()
        self.slider_fuel = ctk.CTkSlider(
            self.sidebar,
            from_=100,
            to=5000,
            command=lambda v: self.m_fuel_var.set(f"{int(v)} kg"),
        )
        self.slider_fuel.set(1000)
        self.slider_fuel.pack(pady=(0, 15), padx=20)

        self.burn_var = ctk.StringVar(value="20 kg/s")
        ctk.CTkLabel(self.sidebar, text="Taxa de Queima:").pack()
        ctk.CTkLabel(
            self.sidebar, textvariable=self.burn_var, text_color="#3498db"
        ).pack()
        self.slider_queima = ctk.CTkSlider(
            self.sidebar,
            from_=5,
            to=100,
            command=lambda v: self.burn_var.set(f"{int(v)} kg/s"),
        )
        self.slider_queima.set(20)
        self.slider_queima.pack(pady=(0, 15), padx=20)

        self.ve_var = ctk.StringVar(value="2500 m/s")
        ctk.CTkLabel(self.sidebar, text="Velocidade de Exaustão:").pack()
        ctk.CTkLabel(
            self.sidebar, textvariable=self.ve_var, text_color="#3498db"
        ).pack()
        self.slider_ve = ctk.CTkSlider(
            self.sidebar,
            from_=1000,
            to=4000,
            command=lambda v: self.ve_var.set(f"{int(v)} m/s"),
        )
        self.slider_ve.set(2500)
        self.slider_ve.pack(pady=(0, 15), padx=20)

        self.btn_lancar = ctk.CTkButton(
            self.sidebar,
            text="🚀 LANÇAR",
            fg_color="green",
            command=self.calcular_e_plotar,
        )
        self.btn_lancar.pack(pady=30, padx=20)

        self.lbl_apogeu = ctk.CTkLabel(
            self.sidebar, text="Apogeu: ---", font=("Arial", 14, "bold")
        )
        self.lbl_apogeu.pack(pady=10)

        # --- ÁREA DO GRÁFICO (CORRIGIDA) ---
        self.fig, self.ax = plt.subplots(figsize=(5, 4), facecolor="#242424")
        self.estilizar_eixo()  # Aplica as cores logo no início

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(
            row=0, column=1, padx=20, pady=20, sticky="nsew"
        )

    def estilizar_eixo(self):
        """Define as cores do gráfico para não bugar"""
        self.ax.set_facecolor("#1a1a1a")
        self.ax.tick_params(colors="white")
        self.ax.xaxis.label.set_color("white")
        self.ax.yaxis.label.set_color("white")
        self.ax.title.set_color("white")
        for spine in self.ax.spines.values():
            spine.set_color("white")
        self.ax.grid(True, alpha=0.2, linestyle="--")

    def on_closing(self):
        """Fecha tudo e devolve o controle ao terminal"""
        plt.close("all")
        self.quit()
        self.destroy()

    def calcular_e_plotar(self):
        m_seca = self.slider_seca.get()
        m_total = m_seca + self.slider_fuel.get()
        taxa_queima = self.slider_queima.get()
        v_ex = self.slider_ve.get()

        g = 9.81
        dt = 0.1
        t, h, v = 0, 0, 0
        tempos, alturas = [], []

        while h >= 0:
            empuxo = (taxa_queima * v_ex) if (m_total > m_seca) else 0
            aceleracao = (empuxo - (m_total * g)) / m_total
            v += aceleracao * dt
            h += v * dt
            if m_total > m_seca:
                m_total -= taxa_queima * dt
            t += dt
            alturas.append(h)
            tempos.append(t)
            if t > 1500:
                break

        self.lbl_apogeu.configure(text=f"Apogeu: {max(alturas):.2f} m")

        # --- ATUALIZAÇÃO DO GRÁFICO ---
        self.ax.clear()
        self.estilizar_eixo()  # Reaplica as cores após o clear
        self.ax.plot(tempos, alturas, color="#E63946", linewidth=2)
        self.ax.set_title("Trajetória do Foguete")
        self.ax.set_xlabel("Tempo (s)")
        self.ax.set_ylabel("Altitude (m)")
        self.canvas.draw()


if __name__ == "__main__":
    app = SimuladorFoguete()
    app.mainloop()
