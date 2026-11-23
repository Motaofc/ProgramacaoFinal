import customtkinter as ctk


class LogicaRobo:
    """Controla a presença e o estado de um robô no mapa."""

    def __init__(self, mapa, label_status, x=0, y=0, cor="#38BDF8"):
        self.mapa = mapa
        self.label_status = label_status
        self.x = x
        self.y = y
        self.cor = cor
        self.robo = None

    def adicionarAgente(self):
        if self.robo is not None:
            return False

        self.robo = ctk.CTkFrame(
            self.mapa,
            width=27,
            height=27,
            fg_color=self.cor,
            corner_radius=9,
            border_width=2,
            border_color="#E2E8F0",
        )
        self.robo.place(x=self.x, y=self.y)
        ctk.CTkLabel(
            self.robo,
            text="●",
            text_color="#FFFFFF",
            font=ctk.CTkFont(size=12, weight="bold"),
        ).place(relx=0.5, rely=0.5, anchor="center")
        self.label_status.configure(text="ATIVO", text_color=self.cor)
        return True

    def adicionarAgenteAspirador(self):
        return self.adicionarAgente()

    def adicionarAgenteID3(self):
        return self.adicionarAgente()

    def removerAgente(self):
        if self.robo is not None:
            self.robo.destroy()
            self.robo = None
            self.label_status.configure(text="INATIVO", text_color="#94A3B8")
            return True
        return False
