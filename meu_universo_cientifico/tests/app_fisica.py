import customtkinter as ctk
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

# Configurações de aparência
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class AppFisica(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuração da Janela Principal
        self.title("Simulador de Física Computacional - Projéteis")
        self.geometry("1100x650")

        ### NOVO: Intercepta o botão de fechar (X) para encerrar o processo corretamente
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Configuração de Grid
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- PAINEL LATERAL (CONTROLES) ---
        self.sidebar = ctk.CTkFrame(self, width=300, corner_radius=15)
        self.sidebar.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.titulo = ctk.CTkLabel(
            self.sidebar, text="Parâmetros", font=("Arial", 20, "bold")
        )
        self.titulo.pack(pady=20)

        # Slider de Velocidade
        self.v0_var = ctk.StringVar(value="20 m/s")
        self.label_v_txt = ctk.CTkLabel(self.sidebar, text="Velocidade Inicial:")
        self.label_v_txt.pack()
        self.label_v_num = ctk.CTkLabel(
            self.sidebar,
            textvariable=self.v0_var,
            text_color="#1f77b4",
            font=("Arial", 14, "bold"),
        )
        self.label_v_num.pack()
        self.slider_v0 = ctk.CTkSlider(
            self.sidebar, from_=0, to=100, command=self.atualizar_labels
        )
        self.slider_v0.set(20)
        self.slider_v0.pack(pady=(0, 20), padx=20)

        # Slider de Ângulo
        self.ang_var = ctk.StringVar(value="45°")
        self.label_a_txt = ctk.CTkLabel(self.sidebar, text="Ângulo de Lançamento:")
        self.label_a_txt.pack()
        self.label_a_num = ctk.CTkLabel(
            self.sidebar,
            textvariable=self.ang_var,
            text_color="#1f77b4",
            font=("Arial", 14, "bold"),
        )
        self.label_a_num.pack()
        self.slider_ang = ctk.CTkSlider(
            self.sidebar, from_=0, to=90, command=self.atualizar_labels
        )
        self.slider_ang.set(45)
        self.slider_ang.pack(pady=(0, 20), padx=20)

        # Botão Gerar Gráfico
        self.btn_plot = ctk.CTkButton(
            self.sidebar,
            text="GERAR GRÁFICO",
            fg_color="green",
            hover_color="darkgreen",
            font=("Arial", 14, "bold"),
            command=self.calcular_e_plotar,
        )
        self.btn_plot.pack(pady=20, padx=20)

        # --- ÁREA DE RESULTADOS MATEMÁTICOS ---
        self.res_frame = ctk.CTkFrame(self.sidebar, fg_color="#2b2b2b")
        self.res_frame.pack(pady=10, padx=20, fill="x")

        self.res_alcance = ctk.CTkLabel(
            self.res_frame, text="Alcance: ---", font=("Arial", 12)
        )
        self.res_alcance.pack(pady=5)
        self.res_altura = ctk.CTkLabel(
            self.res_frame, text="Altura Máx: ---", font=("Arial", 12)
        )
        self.res_altura.pack(pady=5)

        # --- ÁREA DO GRÁFICO ---
        self.fig, self.ax = plt.subplots(figsize=(6, 5), facecolor="#242424")
        self.estilizar_grafico()

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(
            row=0, column=1, padx=20, pady=20, sticky="nsew"
        )

    ### NOVO: Função para fechar sem erros no terminal
    def on_closing(self):
        plt.close("all")  # Fecha o Matplotlib
        self.quit()  # Para o mainloop
        self.destroy()  # Destrói a janela

    def atualizar_labels(self, _):
        self.v0_var.set(f"{int(self.slider_v0.get())} m/s")
        self.ang_var.set(f"{int(self.slider_ang.get())}°")

    def estilizar_grafico(self):
        self.ax.set_facecolor("#1a1a1a")
        self.ax.spines["bottom"].set_color("white")
        self.ax.spines["left"].set_color("white")
        self.ax.tick_params(axis="x", colors="white")
        self.ax.tick_params(axis="y", colors="white")
        self.ax.yaxis.label.set_color("white")
        self.ax.xaxis.label.set_color("white")
        self.ax.title.set_color("white")  # type: ignore
        self.ax.grid(True, linestyle="--", alpha=0.2)

    def calcular_e_plotar(self):
        v0 = self.slider_v0.get()
        theta = np.radians(self.slider_ang.get())
        g = 9.81

        if v0 > 0:
            t_voo = (2 * v0 * np.sin(theta)) / g
            t = np.linspace(0, t_voo, 100)
            x = v0 * np.cos(theta) * t
            y = v0 * np.sin(theta) * t - 0.5 * g * t**2
            alcance = (v0**2 * np.sin(2 * theta)) / g
            h_max = (v0**2 * (np.sin(theta) ** 2)) / (2 * g)
        else:
            x, y, alcance, h_max = [0], [0], 0, 0

        self.res_alcance.configure(text=f"Alcance: {alcance:.2f} m")
        self.res_altura.configure(text=f"Altura Máx: {h_max:.2f} m")

        self.ax.clear()
        self.estilizar_grafico()
        self.ax.plot(x, y, color="#1f77b4", linewidth=3)
        self.ax.set_title("Trajetória do Projétil")
        self.ax.set_xlabel("Distância (m)")
        self.ax.set_ylabel("Altura (m)")
        self.canvas.draw()


if __name__ == "__main__":
    app = AppFisica()
    try:
        app.mainloop()
    except KeyboardInterrupt:
        ### NOVO: Permite fechar com Ctrl+C no terminal sem erro
        pass
