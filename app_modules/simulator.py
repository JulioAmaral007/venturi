import numpy as np


class VenturiSimulator:
    """Classe para cálculos do medidor de Venturi."""
    
    def __init__(self):
        """Inicializa o simulador com valores padrão."""
        self.g = 9.81  # Aceleração da gravidade (m/s²)
        
    def calcular(self, D1, D2, L, rho, rho_m, Q, delta_h, f, Cd, mode):
        """Realiza os cálculos baseados no modo selecionado."""
        self.D1 = D1
        self.D2 = D2
        self.L = L
        self.rho = rho
        self.rho_m = rho_m
        self.Q = Q
        self.delta_h = delta_h
        self.f = f
        self.Cd = Cd
        self.mode = mode
        
        # Calcular áreas
        self.A1 = np.pi * (self.D1 / 2) ** 2
        self.A2 = np.pi * (self.D2 / 2) ** 2
        
        if self.mode == 'Medidor':
            self._calcular_vazao_de_desnivel()
        else:
            self._calcular_desnivel_de_vazao()
    
    def _calcular_vazao_de_desnivel(self):
        """Calcula vazão a partir do desnível manométrico (Modo Medidor)."""
        numerator = 2 * self.g * self.delta_h * (self.rho_m - self.rho)
        denominator = self.rho * (1 - (self.A2 / self.A1) ** 2)
        
        self.Q = self.Cd * self.A2 * np.sqrt(numerator / denominator)
        
        self.v1 = self.Q / self.A1
        self.v2 = self.Q / self.A2
        
        self.delta_P = self.delta_h * (self.rho_m - self.rho) * self.g
        
        self.P1 = 101325.0
        self.P2 = self.P1 - self.delta_P
        
        self.h_L = 0 if self.Cd == 1.0 else self._calcular_perda_carga()
    
    def _calcular_desnivel_de_vazao(self):
        """Calcula desnível manométrico a partir da vazão."""
        self.v1 = self.Q / self.A1
        self.v2 = self.Q / self.A2
        
        self.P1 = 101325.0
        
        if self.mode == 'Ideal':
            self.delta_P = 0.5 * self.rho * (self.v2**2 - self.v1**2)
            self.h_L = 0.0
        else:
            self.h_L = self._calcular_perda_carga()
            self.delta_P = self.rho * (
                0.5 * (self.v2**2 - self.v1**2) + self.g * self.h_L
            )
        
        self.P2 = self.P1 - self.delta_P
        self.delta_h = self.delta_P / ((self.rho_m - self.rho) * self.g)
    
    def _calcular_perda_carga(self):
        """Calcula a perda de carga usando Darcy-Weisbach."""
        v_avg = (self.v1 + self.v2) / 2
        D_avg = (self.D1 + self.D2) / 2
        h_L = self.f * (self.L / D_avg) * (v_avg**2 / (2 * self.g))
        return h_L
    
    def calcular_reynolds(self):
        """Calcula número de Reynolds aproximado."""
        nu = 1e-6  # m²/s (água a 20°C)
        Re = (self.v1 * self.D1) / nu
        return Re


