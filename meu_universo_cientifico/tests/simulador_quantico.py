import customtkinter as ctk  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import numpy as np  # type: ignore
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  # type: ignore

# Configuração para parecer com as imagens (Modo claro e tons de cinza/bege)
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")


class SimuladorQuantico(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- CONFIGURAÇÃO DA JANELA ---
        self.title("Laboratório Virtual de Mecânica Quântica")
        self.geometry("1150x750")
        self.configure(fg_color="#f5f5f5")  # Fundo da janela principal

        # Protocolo para fechar o terminal corretamente
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Layout: Esquerda (Controles) | Direita (Gráfico)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- CONTAINER DOS CONTROLES (LATERAL) ---
        self.sidebar = ctk.CTkScrollableFrame(self, width=350, fg_color="transparent")
        self.sidebar.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # 1. BLOCO: POTENCIAL (Imagem 1)
        self.frame_potencial = self.criar_container("Potencial")
        self.slider_pos = self.adicionar_slider(self.frame_potencial, "Posição", 0, 10)
        self.slider_larg = self.adicionar_slider(
            self.frame_potencial, "Largura", 0.1, 5
        )
        self.slider_amp = self.adicionar_slider(
            self.frame_potencial, "Amplitude", 0, 10
        )

        # 2. BLOCO: VISUALIZAÇÃO (Imagem 1 - RadioButtons)
        self.frame_view = self.criar_container("Visualização")
        self.view_var = ctk.StringVar(value="re")

        ctk.CTkRadioButton(
            self.frame_view,
            text="Parte Real (Reψ)",
            variable=self.view_var,
            value="re",
            command=self.atualizar_simulacao,
        ).pack(anchor="w", padx=20, pady=5)
        ctk.CTkRadioButton(
            self.frame_view,
            text="Parte Imaginária (Imψ)",
            variable=self.view_var,
            value="im",
            command=self.atualizar_simulacao,
        ).pack(anchor="w", padx=20, pady=5)
        ctk.CTkRadioButton(
            self.frame_view,
            text="Densidade de Probabilidade (|ψ|²)",
            variable=self.view_var,
            value="prob",
            command=self.atualizar_simulacao,
        ).pack(anchor="w", padx=20, pady=5)

        # 3. BLOCO: VELOCIDADE E GRID (Imagem 2)
        self.frame_config = self.criar_container("Configurações")

        self.check_grid = ctk.CTkCheckBox(
            self.frame_config, text="Mostrar grid", command=self.atualizar_simulacao
        )
        self.check_grid.pack(anchor="w", padx=20, pady=10)

        self.vel_var_txt = ctk.StringVar(value="Velocidade da simulação = 5")
        self.slider_vel = ctk.CTkSlider(
            self.frame_config,
            from_=1,
            to=10,
            number_of_steps=9,
            command=lambda v: self.vel_var_txt.set(
                f"Velocidade da simulação = {int(v)}"
            ),
        )
        self.slider_vel.set(5)
        self.slider_vel.pack(fill="x", padx=20, pady=5)

        ctk.CTkLabel(self.frame_config, textvariable=self.vel_var_txt).pack(
            anchor="w", padx=20, pady=(0, 15)
        )

        # --- ÁREA DO GRÁFICO ---
        self.fig, self.ax = plt.subplots(figsize=(6, 5), dpi=100)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().grid(
            row=0, column=1, padx=20, pady=20, sticky="nsew"
        )

        self.atualizar_simulacao()

    # --- FUNÇÕES DE CONSTRUÇÃO ---
    def criar_container(self, titulo):
        """Cria os blocos cinza-esverdeados das imagens"""
        frame = ctk.CTkFrame(
            self.sidebar,
            fg_color="#d1d5cf",
            border_color="#adb5bd",
            border_width=1,
            corner_radius=8,
        )
        frame.pack(fill="x", padx=5, pady=10)
        ctk.CTkLabel(
            frame, text=titulo, font=("Arial", 15, "bold"), text_color="#333"
        ).pack(pady=5)
        return frame

    def adicionar_slider(self, master, label, min_v, max_v):
        """Adiciona label + slider e retorna o objeto do slider"""
        ctk.CTkLabel(master, text=label, text_color="#333").pack()
        slider = ctk.CTkSlider(
            master, from_=min_v, to=max_v, command=lambda _: self.atualizar_simulacao()
        )
        slider.pack(padx=20, pady=(0, 10), fill="x")
        return slider

    def atualizar_simulacao(self):
        """Aqui entra a matemática que VOCÊ pode alterar"""
        self.ax.clear()

        # Parâmetros vindos dos Sliders
        pos = self.slider_pos.get()
        larg = self.slider_larg.get()
        amp = self.slider_amp.get()

        # Criação de um pacote de onda (exemplo de física)
        x = np.linspace(0, 10, 500)
        psi = amp * np.exp(-((x - pos) * 2) / (2 * larg * 2)) * np.exp(1j * 5 * x)

        modo = self.view_var.get()
        if modo == "re":
            self.ax.plot(x, psi.real, color="#1f77b4", label="Re(ψ)")
        elif modo == "im":
            self.ax.plot(x, psi.imag, color="#ff7f0e", label="Im(ψ)")
        else:
            self.ax.plot(x, np.abs(psi) ** 2, color="#2ca02c", label="|ψ|²")

        self.ax.set_ylim(-11, 11)
        self.ax.grid(self.check_grid.get(), linestyle="--", alpha=0.5)
        self.ax.legend(loc="upper right")
        self.canvas.draw()

    def on_closing(self):
        plt.close("all")
        self.quit()
        self.destroy()


if __name__ == "__main__":
    app = SimuladorQuantico()
    app.mainloop()
