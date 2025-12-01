import numpy as np


class VenturiSimulator:
    
    def __init__(self):
        self.g = 9.81  
        
    def calcular(self, D1, D2, L_garganta, rho, rho_m, Q, delta_h, f, mode, mu, P1):
        self.D1 = D1
        self.D2 = D2
        self.L_garganta = L_garganta
        self.rho = rho
        self.rho_m = rho_m
        self.Q = Q
        self.delta_h = delta_h
        self.f = f
        self.mode = mode
        self.mu=mu
        self.P1 = P1
        
        self.A1 = np.pi * (self.D1 / 2) ** 2
        self.A2 = np.pi * (self.D2 / 2) ** 2

        self._calcular_geometria_automatica()
        
        self._calcular_desnivel_de_vazao()
     
    def _calcular_desnivel_de_vazao(self):
        self.v1 = self.Q / self.A1
        self.v2 = self.Q / self.A2

        if self.mode == 'Ideal':
            k_entrada = 0.0
        else:
            k_entrada = 0.04

        self.P2 = self.P1 - 0.5 * self.rho * ((self.v2**2 * (1 + k_entrada)) - self.v1**2)

        if self.mode == 'Ideal':
            perda_garganta_Pa = 0.0
        else:
            h_f_garganta = self._calcular_perda_carga_garganta()
            perda_garganta_Pa = h_f_garganta * self.rho * self.g

        self.P2_fim = self.P2 - perda_garganta_Pa

        self.delta_P = self.P1 - self.P2

        if self.mode == 'Ideal':
            self.P3 = self.P1 
            self.h_L = 0.0
        else:
            recuperacao_dinamica = 0.5 * self.rho * (self.v2**2 - self.v1**2)
            K_difusor = self._obter_k_difusor_15_graus()
            perda_difusor_Pa = K_difusor * (0.5 * self.rho * self.v2**2)
            self.P3 = self.P2_fim + recuperacao_dinamica - perda_difusor_Pa
            perda_entrada_Pa = k_entrada * (0.5 * self.rho * self.v2**2)
            perda_total_Pa = perda_entrada_Pa + perda_garganta_Pa + perda_difusor_Pa
            self.h_L = perda_total_Pa / (self.rho * self.g)

        self.delta_h = self.delta_P / ((self.rho_m - self.rho) * self.g)
    
    def _calcular_perda_carga_garganta(self):
        h_f_garganta = self.f * (self.L_garganta / self.D2) * (self.v2**2 / (2 * self.g))
        
        return h_f_garganta
    
    def calcular_reynolds(self):
        Re = (self.rho * self.v2 * self.D2) / self.mu
        return Re

    def _calcular_geometria_automatica(self):
        angulo_graus = 15.0
        angulo_rad = np.radians(angulo_graus)
        
        delta_raio = (self.D1 - self.D2) / 2
        
        if delta_raio <= 0:
            self.L_entrada = 0
            self.L_saida = 0
        else:
            comprimento_cone = delta_raio / np.tan(angulo_rad / 2)
            
            self.L_entrada = comprimento_cone
            self.L_saida = comprimento_cone
        
        self.L = self.L_entrada + self.L_garganta + self.L_saida

    def _obter_k_difusor_15_graus(self):

        AR = (self.D1 / self.D2) ** 2
 
        cp_ideal = 1.0 - (1.0 / AR**2)

        if AR < 1.2:
            cp_real = 1.4 * (AR - 1.0)
        elif AR > 4.0:
            cp_real = 0.64
        else:
            cp_real = (0.0394 * AR**3) - (0.3954 * AR**2) + (1.3095 * AR) - 0.7897
            
        cp_real = max(0.0, min(cp_real, cp_ideal))
        
        k_difusor = cp_ideal - cp_real
        
        return max(0.0, k_difusor)