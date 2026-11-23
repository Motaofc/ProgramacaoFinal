import customtkinter as ctk
from tkinter import messagebox

from logica_robos import LogicaRobo


# Tema visual da aplicação
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG = "#0B1220"
SIDEBAR = "#111C2E"
PANEL = "#172338"
PANEL_ALT = "#1D2B42"
BORDER = "#2B3B55"
TEXT = "#F1F5F9"
MUTED = "#94A3B8"
BLUE = "#38BDF8"
GREEN = "#34D399"
ORANGE = "#FBBF24"
RED = "#FB7185"


class ParteGrafica(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("RoboFleet | Gestão de Robôs")
        self.geometry("1240x780")
        self.minsize(1050, 700)
        self.configure(fg_color=BG)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._criar_barra_lateral()
        self._criar_conteudo()
        self._criar_logica()
        self._atualizar_resumo()

    def _criar_barra_lateral(self):
        sidebar = ctk.CTkFrame(self, width=245, corner_radius=0, fg_color=SIDEBAR)
        sidebar.grid(row=0, column=0, sticky="nsew")
        sidebar.grid_propagate(False)
        sidebar.grid_rowconfigure(5, weight=1)

        marca = ctk.CTkFrame(sidebar, fg_color="transparent")
        marca.pack(fill="x", padx=24, pady=(28, 36))
        ctk.CTkLabel(marca, text="◈", text_color=BLUE,
                     font=ctk.CTkFont(size=34, weight="bold")).pack(side="left")
        nome = ctk.CTkFrame(marca, fg_color="transparent")
        nome.pack(side="left", padx=10)
        ctk.CTkLabel(nome, text="ROBOFLEET", text_color=TEXT,
                     font=ctk.CTkFont(size=18, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(nome, text="GESTÃO INTELIGENTE", text_color=MUTED,
                     font=ctk.CTkFont(size=9, weight="bold")).pack(anchor="w")

        ctk.CTkLabel(sidebar, text="MENU PRINCIPAL", text_color="#64748B",
                     font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=25, pady=(0, 12))
        self._nav_item(sidebar, "▦", "Painel geral", active=True)
        self._nav_item(sidebar, "⌖", "Mapa das instalações")
        self._nav_item(sidebar, "▤", "Gestão de robôs")

        info = ctk.CTkFrame(sidebar, fg_color=PANEL, corner_radius=14)
        info.pack(side="bottom", fill="x", padx=16, pady=20)
        ctk.CTkLabel(info, text="SISTEMA", text_color=MUTED,
                     font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=14, pady=(13, 3))
        ctk.CTkLabel(info, text="●  Interface operacional", text_color=GREEN,
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=14, pady=(0, 13))

    def _nav_item(self, parent, icon, label, active=False):
        frame = ctk.CTkFrame(parent, fg_color=(PANEL_ALT if active else "transparent"), corner_radius=10)
        frame.pack(fill="x", padx=13, pady=4)
        ctk.CTkLabel(frame, text=icon, width=38, text_color=(BLUE if active else MUTED),
                     font=ctk.CTkFont(size=18)).pack(side="left", padx=(7, 0), pady=10)
        ctk.CTkLabel(frame, text=label, text_color=(TEXT if active else MUTED),
                     font=ctk.CTkFont(size=13, weight=("bold" if active else "normal"))).pack(side="left", pady=10)

    def _criar_conteudo(self):
        main = ctk.CTkFrame(self, fg_color="transparent")
        main.grid(row=0, column=1, sticky="nsew", padx=30, pady=26)
        main.grid_columnconfigure((0, 1), weight=1)
        main.grid_rowconfigure(3, weight=1)

        topo = ctk.CTkFrame(main, fg_color="transparent")
        topo.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(0, 22))
        titulo = ctk.CTkFrame(topo, fg_color="transparent")
        titulo.pack(side="left")
        ctk.CTkLabel(titulo, text="Painel de controlo", text_color=TEXT,
                     font=ctk.CTkFont(size=27, weight="bold")).pack(anchor="w")
        ctk.CTkLabel(titulo, text="Acompanha e gere os robôs das tuas instalações.",
                     text_color=MUTED, font=ctk.CTkFont(size=13)).pack(anchor="w", pady=(4, 0))
        ctk.CTkLabel(topo, text="●  SISTEMA ONLINE", text_color=GREEN,
                     fg_color=PANEL, corner_radius=20,
                     font=ctk.CTkFont(size=11, weight="bold"), padx=14, pady=9).pack(side="right", pady=6)

        resumo = ctk.CTkFrame(main, fg_color="transparent")
        resumo.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 20))
        resumo.grid_columnconfigure((0, 1, 2), weight=1)
        self.valor_total = self._cartao_resumo(resumo, 0, "ROBÔS REGISTADOS", "3", BLUE, "Frota configurada")
        self.valor_ativos = self._cartao_resumo(resumo, 1, "ROBÔS ATIVOS", "0", GREEN, "Em funcionamento")
        self.valor_inativos = self._cartao_resumo(resumo, 2, "ROBÔS INATIVOS", "3", ORANGE, "Em espera")

        ctk.CTkLabel(main, text="MONITORIZAÇÃO", text_color=MUTED,
                     font=ctk.CTkFont(size=11, weight="bold")).grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 10))

        mapa_card = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=18, border_width=1, border_color=BORDER)
        mapa_card.grid(row=3, column=0, sticky="nsew", padx=(0, 10))
        mapa_card.grid_rowconfigure(1, weight=1)
        mapa_card.grid_columnconfigure(0, weight=1)
        cab = ctk.CTkFrame(mapa_card, fg_color="transparent")
        cab.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))
        ctk.CTkLabel(cab, text="Mapa das instalações", text_color=TEXT,
                     font=ctk.CTkFont(size=16, weight="bold")).pack(side="left")
        ctk.CTkLabel(cab, text="PLANTA 01", text_color=BLUE, fg_color=PANEL_ALT,
                     corner_radius=8, font=ctk.CTkFont(size=10, weight="bold"), padx=9, pady=5).pack(side="right")

        self.mapa = ctk.CTkFrame(mapa_card, fg_color="#101B2C", corner_radius=13)
        self.mapa.grid(row=1, column=0, sticky="nsew", padx=18, pady=(8, 18))
        self.mapa.grid_columnconfigure((0, 1, 2), weight=1)
        self.mapa.grid_rowconfigure((0, 1), weight=1)
        self._criar_zona("SALA DE ESTAR", "Zona de convívio", 0, 0, 2, 1)
        self._criar_zona("COZINHA", "Área de refeições", 0, 2, 1, 1)
        self._criar_zona("QUARTO", "Zona privada", 1, 0, 1, 1)
        self._criar_zona("SALA DE LAZER", "Área de lazer", 1, 1, 1, 1)
        self._criar_zona("GARAGEM", "Estacionamento", 1, 2, 1, 1)
        base = ctk.CTkFrame(self.mapa, fg_color="#203B55", corner_radius=9, border_width=1, border_color=BLUE)
        base.place(relx=0.70, rely=0.06, relwidth=0.25, relheight=0.16)
        ctk.CTkLabel(base, text="⚡ BASE", text_color=BLUE,
                     font=ctk.CTkFont(size=11, weight="bold")).place(relx=0.5, rely=0.5, anchor="center")

        lado = ctk.CTkFrame(main, fg_color=PANEL, corner_radius=18, border_width=1, border_color=BORDER)
        lado.grid(row=3, column=1, sticky="nsew", padx=(10, 0))
        lado.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(lado, text="Estado da frota", text_color=TEXT,
                     font=ctk.CTkFont(size=16, weight="bold")).grid(row=0, column=0, sticky="w", padx=20, pady=(18, 3))
        ctk.CTkLabel(lado, text="Estado atual de cada unidade", text_color=MUTED,
                     font=ctk.CTkFont(size=11)).grid(row=1, column=0, sticky="w", padx=20, pady=(0, 12))

        self.status_labels = {}
        self._cartao_robo(lado, 2, "Robô Aspirador", "Limpeza de superfícies", "#38BDF8", "aspirador")
        self._cartao_robo(lado, 3, "Robô Lavador", "Lavagem do chão", "#A78BFA", "lavador")
        self._cartao_robo(lado, 4, "Robô Híbrido", "Limpeza multifunções", "#FB7185", "hibrido")

        ctk.CTkLabel(lado, text="AÇÕES RÁPIDAS", text_color=MUTED,
                     font=ctk.CTkFont(size=10, weight="bold")).grid(row=5, column=0, sticky="w", padx=20, pady=(18, 8))
        acoes = ctk.CTkFrame(lado, fg_color="transparent")
        acoes.grid(row=6, column=0, sticky="ew", padx=16, pady=(0, 18))
        acoes.grid_columnconfigure((0, 1), weight=1)
        ctk.CTkButton(acoes, text="＋  Adicionar", height=39, corner_radius=10,
                      fg_color=BLUE, hover_color="#0EA5E9", text_color="#071321",
                      font=ctk.CTkFont(size=12, weight="bold"), command=self.abrir_janela_adicionar).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ctk.CTkButton(acoes, text="－  Remover", height=39, corner_radius=10,
                      fg_color=PANEL_ALT, hover_color="#344761", text_color=TEXT,
                      font=ctk.CTkFont(size=12, weight="bold"), command=self.abrir_janela_remover).grid(row=0, column=1, sticky="ew", padx=(5, 0))

    def _cartao_resumo(self, parent, coluna, titulo, valor, cor, descricao):
        card = ctk.CTkFrame(parent, fg_color=PANEL, corner_radius=15, border_width=1, border_color=BORDER)
        card.grid(row=0, column=coluna, sticky="ew", padx=(0 if coluna == 0 else 7, 0 if coluna == 2 else 7))
        ctk.CTkLabel(card, text=titulo, text_color=MUTED,
                     font=ctk.CTkFont(size=10, weight="bold")).pack(anchor="w", padx=17, pady=(14, 2))
        linha = ctk.CTkFrame(card, fg_color="transparent")
        linha.pack(fill="x", padx=17)
        valor_label = ctk.CTkLabel(linha, text=valor, text_color=cor,
                                   font=ctk.CTkFont(size=27, weight="bold"))
        valor_label.pack(side="left")
        ctk.CTkLabel(card, text=descricao, text_color=MUTED,
                     font=ctk.CTkFont(size=11)).pack(anchor="w", padx=17, pady=(0, 14))
        return valor_label

    def _criar_zona(self, nome, detalhe, linha, coluna, colspan=1, rowspan=1):
        zona = ctk.CTkFrame(self.mapa, fg_color="#1A2A40", corner_radius=10,
                            border_width=1, border_color="#2B405C")
        zona.grid(row=linha, column=coluna, columnspan=colspan, rowspan=rowspan,
                  sticky="nsew", padx=6, pady=6)
        ctk.CTkLabel(zona, text=nome, text_color="#DCE7F5",
                     font=ctk.CTkFont(size=11, weight="bold")).place(relx=0.08, rely=0.40, anchor="w")
        ctk.CTkLabel(zona, text=detalhe, text_color=MUTED,
                     font=ctk.CTkFont(size=9)).place(relx=0.08, rely=0.62, anchor="w")

    def _cartao_robo(self, parent, linha, nome, descricao, cor, chave):
        card = ctk.CTkFrame(parent, fg_color=PANEL_ALT, corner_radius=12)
        card.grid(row=linha, column=0, sticky="ew", padx=15, pady=5)
        card.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(card, text="▣", text_color=cor,
                     font=ctk.CTkFont(size=22)).grid(row=0, column=0, rowspan=2, padx=(13, 10), pady=11)
        ctk.CTkLabel(card, text=nome, text_color=TEXT,
                     font=ctk.CTkFont(size=12, weight="bold")).grid(row=0, column=1, sticky="w", pady=(10, 0))
        ctk.CTkLabel(card, text=descricao, text_color=MUTED,
                     font=ctk.CTkFont(size=10)).grid(row=1, column=1, sticky="w", pady=(0, 10))
        status = ctk.CTkLabel(card, text="INATIVO", text_color=MUTED,
                              fg_color="#29384D", corner_radius=8,
                              font=ctk.CTkFont(size=9, weight="bold"), padx=9, pady=5)
        status.grid(row=0, column=2, rowspan=2, padx=12)
        self.status_labels[chave] = status

    def _criar_logica(self):
        # Coordenadas dos marcadores no mapa (relativas ao canto superior esquerdo).
        self.logicas = {
            "aspirador": LogicaRobo(self.mapa, self.status_labels["aspirador"], 75, 72, "#38BDF8"),
            "lavador": LogicaRobo(self.mapa, self.status_labels["lavador"], 245, 165, "#A78BFA"),
            "hibrido": LogicaRobo(self.mapa, self.status_labels["hibrido"], 390, 265, "#FB7185"),
        }

    def _atualizar_resumo(self):
        ativos = sum(1 for robo in self.logicas.values() if robo.robo is not None)
        self.valor_ativos.configure(text=str(ativos))
        self.valor_inativos.configure(text=str(3 - ativos))

    def _abrir_selecao(self, titulo, adicionar):
        janela = ctk.CTkToplevel(self)
        janela.title(titulo)
        janela.geometry("380x330")
        janela.resizable(False, False)
        janela.configure(fg_color=BG)
        janela.transient(self)
        janela.grab_set()

        ctk.CTkLabel(janela, text=titulo, text_color=TEXT,
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=24, pady=(24, 5))
        ctk.CTkLabel(janela, text="Seleciona a unidade que pretendes gerir.", text_color=MUTED,
                     font=ctk.CTkFont(size=12)).pack(anchor="w", padx=24, pady=(0, 16))

        nomes = [("Robô Aspirador", "aspirador"), ("Robô Lavador de Chão", "lavador"), ("Robô Híbrido", "hibrido")]
        for nome, chave in nomes:
            robo = self.logicas[chave]
            ja_ativo = robo.robo is not None
            indisponivel = (adicionar and ja_ativo) or (not adicionar and not ja_ativo)
            texto = nome + ("  ·  já ativo" if adicionar and ja_ativo else "  ·  inativo" if not adicionar and not ja_ativo else "")
            ctk.CTkButton(
                janela, text=texto, height=42, corner_radius=10,
                fg_color=PANEL_ALT, hover_color="#344761", text_color=(MUTED if indisponivel else TEXT),
                state=("disabled" if indisponivel else "normal"),
                command=lambda k=chave: self._executar_acao(k, adicionar, janela),
            ).pack(fill="x", padx=24, pady=5)

    def _executar_acao(self, chave, adicionar, janela):
        robo = self.logicas[chave]
        if adicionar:
            robo.adicionarAgente()
        else:
            robo.removerAgente()
        self._atualizar_resumo()
        janela.destroy()

    def abrir_janela_adicionar(self):
        self._abrir_selecao("Adicionar robô", True)

    def abrir_janela_remover(self):
        self._abrir_selecao("Remover robô", False)


if __name__ == "__main__":
    app = ParteGrafica()
    app.mainloop()
