"""
Simulador de Medidor de Venturi
Aplicação web interativa desenvolvida com Streamlit

Execute com: streamlit run app.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configurar matplotlib para tema escuro
plt.style.use('dark_background')

# Configuração da página
st.set_page_config(
    page_title="Simulador de Venturi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Classe do simulador (adaptada para Streamlit)
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


def plotar_diagrama_venturi(sim):
    """Plota o diagrama esquemático do Venturi."""
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.set_xlim(0, sim.L)
    ax.set_ylim(-sim.D1, sim.D1)
    ax.set_aspect('equal')
    
    x_points = np.linspace(0, sim.L, 100)
    
    def radius_at_x(x):
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        r1 = sim.D1 / 2
        r2 = sim.D2 / 2
        
        if x < L_conv:
            t = x / L_conv
            r = r1 - (r1 - r2) * t
        elif x < L_conv + L_throat:
            r = r2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            r = r2 + (r1 - r2) * t
        return r
    
    y_upper = [radius_at_x(x) for x in x_points]
    y_lower = [-radius_at_x(x) for x in x_points]
    
    ax.fill_between(x_points, y_lower, y_upper, color='lightblue', 
                    alpha=0.3, edgecolor='blue', linewidth=2)
    ax.plot(x_points, y_upper, 'b-', linewidth=2)
    ax.plot(x_points, y_lower, 'b-', linewidth=2)
    
    x1 = sim.L * 0.15
    x2 = sim.L * 0.5
    ax.plot(x1, 0, 'ro', markersize=10, label='Ponto 1')
    ax.plot(x2, 0, 'go', markersize=10, label='Ponto 2')
    
    ax.text(x1, -sim.D1 * 0.7, f'v₁={sim.v1:.2f} m/s', 
           ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='wheat'))
    ax.text(x2, -sim.D1 * 0.7, f'v₂={sim.v2:.2f} m/s', 
           ha='center', fontsize=10, bbox=dict(boxstyle='round', facecolor='lightgreen'))
    
    ax.set_xlabel('Posição (m)', fontsize=11)
    ax.set_ylabel('Raio (m)', fontsize=11)
    ax.set_title(f'Diagrama do Medidor de Venturi - Modo {sim.mode}', 
                fontsize=13, fontweight='bold')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3)
    
    return fig


def plotar_manometro(sim):
    """Plota o manômetro em U."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.05, 0.8)
    ax.set_aspect('equal')
    
    tube_width = 0.2
    base_height = 0.08
    
    left_x = 0.5
    left_height = base_height + sim.delta_h / 2
    
    right_x = 1.3
    right_height = base_height + sim.delta_h / 2 + sim.delta_h
    
    # Base
    base = Rectangle((left_x, 0), right_x - left_x + tube_width, base_height,
                    facecolor='gray', edgecolor='black', linewidth=2)
    ax.add_patch(base)
    
    # Tubos
    left_tube = Rectangle((left_x, base_height), tube_width, left_height,
                         facecolor='lightcoral', edgecolor='black', linewidth=2, alpha=0.7)
    ax.add_patch(left_tube)
    
    right_tube = Rectangle((right_x, base_height), tube_width, right_height,
                          facecolor='lightgreen', edgecolor='black', linewidth=2, alpha=0.7)
    ax.add_patch(right_tube)
    
    # Mercúrio
    mercury = Rectangle((left_x, 0), right_x - left_x + tube_width, base_height - 0.01,
                       facecolor='silver', edgecolor='darkgray', linewidth=1)
    ax.add_patch(mercury)
    
    # Indicação de Δh
    y_left = base_height + left_height
    y_right = base_height + right_height
    mid_x = (left_x + right_x) / 2 + tube_width / 2 + 0.15
    
    ax.plot([mid_x, mid_x], [y_left, y_right], 'r-', linewidth=2)
    ax.plot([mid_x - 0.05, mid_x + 0.05], [y_left, y_left], 'r-', linewidth=2)
    ax.plot([mid_x - 0.05, mid_x + 0.05], [y_right, y_right], 'r-', linewidth=2)
    
    ax.text(mid_x + 0.2, (y_left + y_right) / 2, f'Δh={sim.delta_h*100:.1f} cm',
           fontsize=11, color='red', fontweight='bold', rotation=90, va='center')
    
    ax.text(left_x + tube_width / 2, -0.03, 'P₁', ha='center', fontsize=11, fontweight='bold')
    ax.text(right_x + tube_width / 2, -0.03, 'P₂', ha='center', fontsize=11, fontweight='bold')
    
    ax.set_title('Manômetro Diferencial em U', fontsize=12, fontweight='bold')
    ax.axis('off')
    
    return fig


def plotar_perfil_pressao(sim):
    """Plota o perfil de pressão ao longo do tubo."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x_points = np.linspace(0, sim.L, 100)
    pressures = []
    
    for x in x_points:
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        
        if x < L_conv:
            t = x / L_conv
            P = sim.P1 - sim.delta_P * t
        elif x < L_conv + L_throat:
            P = sim.P2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            if sim.mode == 'Realista':
                P_recovery = sim.P2 + sim.delta_P * t * (1 - sim.h_L / (sim.delta_P / (sim.rho * sim.g)))
            else:
                P_recovery = sim.P2 + sim.delta_P * t
            P = P_recovery
        
        pressures.append(P / 1000)
    
    ax.plot(x_points, pressures, 'b-', linewidth=2.5, label='Pressão')
    ax.axhline(y=sim.P1/1000, color='r', linestyle='--', alpha=0.5, 
              label=f'P₁ = {sim.P1/1000:.2f} kPa')
    ax.axhline(y=sim.P2/1000, color='g', linestyle='--', alpha=0.5, 
              label=f'P₂ = {sim.P2/1000:.2f} kPa')
    
    ax.fill_between(x_points, 0, pressures, alpha=0.2, color='blue')
    
    ax.set_xlabel('Posição ao longo do tubo (m)', fontsize=11)
    ax.set_ylabel('Pressão (kPa)', fontsize=11)
    ax.set_title('Perfil de Pressão ao Longo do Medidor', fontsize=12, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    return fig


def plotar_linhas_energia(sim):
    """Plota Linha de Energia (LE) e Linha Piezométrica (LP)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x_points = np.linspace(0, sim.L, 100)
    LP = []
    LE = []
    
    for x in x_points:
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        
        if x < L_conv:
            t = x / L_conv
            P = sim.P1 - sim.delta_P * t
            v = sim.v1 + (sim.v2 - sim.v1) * t
        elif x < L_conv + L_throat:
            P = sim.P2
            v = sim.v2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            if sim.mode == 'Realista':
                P_recovery = sim.P2 + sim.delta_P * t * (1 - sim.h_L / (sim.delta_P / (sim.rho * sim.g)))
            else:
                P_recovery = sim.P2 + sim.delta_P * t
            P = P_recovery
            v = sim.v2 - (sim.v2 - sim.v1) * t
        
        lp = P / (sim.rho * sim.g)
        LP.append(lp)
        
        le = lp + v**2 / (2 * sim.g)
        LE.append(le)
    
    ax.plot(x_points, LE, 'r-', linewidth=2.5, label='Linha de Energia (LE)')
    ax.plot(x_points, LP, 'b-', linewidth=2.5, label='Linha Piezométrica (LP)')
    ax.fill_between(x_points, LP, LE, alpha=0.2, color='orange', label='Energia Cinética')
    
    if sim.mode == 'Realista' and sim.h_L > 0:
        LE_initial = LE[0]
        LE_final = LE[-1]
        ax.annotate(f'Perda: hₗ = {sim.h_L:.4f} m', 
                   xy=(sim.L * 0.85, LE_final),
                   fontsize=10, color='red', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='yellow', alpha=0.7))
    
    ax.set_xlabel('Posição ao longo do tubo (m)', fontsize=11)
    ax.set_ylabel('Carga (m)', fontsize=11)
    ax.set_title('Linha de Energia e Linha Piezométrica', fontsize=12, fontweight='bold')
    ax.legend(loc='best')
    ax.grid(True, alpha=0.3)
    
    return fig


# ========== EXEMPLOS PRÁTICOS ==========

def executar_exemplos():
    """Interface para executar os exemplos práticos do simulador."""
    st.header("📚 Exemplos Práticos")
    st.markdown("Explore diferentes casos de uso do medidor de Venturi através de exemplos pré-configurados.")
    
    # Sidebar - Seleção de exemplo
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Selecione o Exemplo")
    
    exemplo = st.sidebar.selectbox(
        "Escolha um exemplo:",
        [
            "1. Comparação: Ideal vs Realista",
            "2. Curva de Calibração",
            "3. Modo Medidor (Δh → Q)",
            "4. Sensibilidade ao Cd",
            "5. Efeito da Razão Beta (β)"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Dica:** Cada exemplo demonstra um aspecto importante do funcionamento do medidor de Venturi.")
    
    # Executar o exemplo selecionado
    if "1." in exemplo:
        exemplo_1_comparacao_modos()
    elif "2." in exemplo:
        exemplo_2_curva_calibracao()
    elif "3." in exemplo:
        exemplo_3_modo_medidor()
    elif "4." in exemplo:
        exemplo_4_sensibilidade_cd()
    elif "5." in exemplo:
        exemplo_5_efeito_beta()


def exemplo_1_comparacao_modos():
    """Exemplo 1: Comparação entre Modo Ideal e Modo Realista"""
    st.subheader("🔵🔴 Exemplo 1: Comparação Modo Ideal vs Modo Realista")
    st.markdown("---")
    
    st.markdown("""
    Este exemplo compara o comportamento do medidor de Venturi em duas condições:
    - **Modo Ideal**: Escoamento sem perdas (Cd = 1.0, sem atrito)
    - **Modo Realista**: Escoamento com perdas por atrito e coeficiente de descarga real
    """)
    
    # Parâmetros comuns
    D1 = 0.10  # m
    D2 = 0.05  # m
    Q = 0.015  # m³/s
    
    # Modo Ideal
    sim_ideal = VenturiSimulator()
    sim_ideal.calcular(D1, D2, 1.0, 1000, 13600, Q, 0, 0.02, 1.0, 'Ideal')
    
    # Modo Realista
    sim_real = VenturiSimulator()
    sim_real.calcular(D1, D2, 1.0, 1000, 13600, Q, 0, 0.025, 0.96, 'Realista')
    
    # Mostrar resultados lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 🔵 Modo Ideal")
        st.metric("Velocidade v₁", f"{sim_ideal.v1:.3f} m/s")
        st.metric("Velocidade v₂", f"{sim_ideal.v2:.3f} m/s")
        st.metric("Queda de Pressão ΔP", f"{sim_ideal.delta_P/1000:.3f} kPa")
        st.metric("Desnível Δh", f"{sim_ideal.delta_h*100:.2f} cm")
        st.metric("Perda de Carga hₗ", f"{sim_ideal.h_L:.6f} m", "zero")
    
    with col2:
        st.markdown("### 🔴 Modo Realista")
        st.metric("Velocidade v₁", f"{sim_real.v1:.3f} m/s")
        st.metric("Velocidade v₂", f"{sim_real.v2:.3f} m/s")
        st.metric("Queda de Pressão ΔP", f"{sim_real.delta_P/1000:.3f} kPa")
        st.metric("Desnível Δh", f"{sim_real.delta_h*100:.2f} cm")
        st.metric("Perda de Carga hₗ", f"{sim_real.h_L:.6f} m", "com perdas")
    
    # Análise das diferenças
    st.markdown("---")
    st.markdown("### 📊 Análise das Diferenças")
    
    diff_p = ((sim_real.delta_P - sim_ideal.delta_P) / sim_ideal.delta_P) * 100
    diff_h = ((sim_real.delta_h - sim_ideal.delta_h) / sim_ideal.delta_h) * 100
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Aumento em ΔP", f"{diff_p:.2f}%")
    with col2:
        st.metric("Aumento em Δh", f"{diff_h:.2f}%")
    with col3:
        st.metric("Perda de Energia", f"{sim_real.h_L:.6f} m")
    
    # Gráficos comparativos
    st.markdown("---")
    st.markdown("### 📈 Visualizações Comparativas")
    
    tab1, tab2 = st.tabs(["Perfil de Pressão", "Linhas de Energia"])
    
    with tab1:
        fig = plotar_perfil_pressao(sim_real)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab2:
        fig = plotar_linhas_energia(sim_real)
        st.pyplot(fig)
        plt.close(fig)


def exemplo_2_curva_calibracao():
    """Exemplo 2: Geração de Curva de Calibração"""
    st.subheader("📈 Exemplo 2: Curva de Calibração do Medidor")
    st.markdown("---")
    
    st.markdown("""
    Este exemplo gera uma **curva de calibração** relacionando a vazão volumétrica (Q) 
    com o desnível manométrico (Δh) para um medidor de Venturi específico.
    """)
    
    # Criar simulador
    sim = VenturiSimulator()
    
    # Faixa de vazões
    vazoes = np.linspace(0.005, 0.030, 20)  # m³/s
    desniveis = []
    pressoes = []
    reynolds = []
    
    # Calcular pontos da curva
    with st.spinner('Gerando curva de calibração...'):
        for q in vazoes:
            sim.calcular(0.10, 0.05, 1.0, 1000, 13600, q, 0, 0.02, 0.97, 'Realista')
            desniveis.append(sim.delta_h * 100)  # cm
            pressoes.append(sim.delta_P / 1000)   # kPa
            reynolds.append(sim.calcular_reynolds())
    
    # Resumo da calibração
    st.markdown("### 📊 Resumo da Calibração")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Faixa de Vazão", f"{vazoes[0]*1000:.1f} - {vazoes[-1]*1000:.1f} L/s")
    with col2:
        st.metric("Faixa de Desnível", f"{desniveis[0]:.2f} - {desniveis[-1]:.2f} cm")
    with col3:
        st.metric("Faixa de ΔP", f"{pressoes[0]:.2f} - {pressoes[-1]:.2f} kPa")
    
    # Tabela de dados
    st.markdown("---")
    st.markdown("### 📋 Tabela de Calibração")
    
    import pandas as pd
    df = pd.DataFrame({
        'Q (L/s)': [q*1000 for q in vazoes],
        'Q (m³/h)': [q*3600 for q in vazoes],
        'Δh (cm)': desniveis,
        'ΔP (kPa)': pressoes,
        'Reynolds': [int(re) for re in reynolds]
    })
    
    st.dataframe(df.style.format({
        'Q (L/s)': '{:.2f}',
        'Q (m³/h)': '{:.2f}',
        'Δh (cm)': '{:.2f}',
        'ΔP (kPa)': '{:.3f}',
        'Reynolds': '{:,.0f}'
    }), width='stretch')
    
    # Gráfico da curva de calibração
    st.markdown("---")
    st.markdown("### 📈 Curva de Calibração")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(np.array(vazoes) * 1000, desniveis, 'bo-', linewidth=2, markersize=6)
    ax.set_xlabel('Vazão (L/s)', fontsize=12)
    ax.set_ylabel('Desnível Manométrico Δh (cm)', fontsize=12)
    ax.set_title('Curva de Calibração do Medidor de Venturi', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)
    
    st.success("✅ A curva mostra a relação quadrática entre vazão e desnível: Q ∝ √(Δh)")


def exemplo_3_modo_medidor():
    """Exemplo 3: Uso do Modo Medidor (calcular vazão a partir de Δh)"""
    st.subheader("🔬 Exemplo 3: Modo Medidor - Calcular Vazão a partir de Δh")
    st.markdown("---")
    
    st.markdown("""
    Este exemplo demonstra o uso **prático** do medidor de Venturi: 
    medir o desnível manométrico (Δh) e calcular a vazão (Q) correspondente.
    """)
    
    # Criar simulador
    sim = VenturiSimulator()
    
    # Diferentes desníveis
    desniveis = [0.05, 0.10, 0.15, 0.20, 0.25]  # m
    resultados = []
    
    for dh in desniveis:
        sim.calcular(0.10, 0.05, 1.0, 1000, 13600, 0, dh, 0.02, 0.98, 'Medidor')
        resultados.append({
            'Δh (cm)': dh * 100,
            'Q (L/s)': sim.Q * 1000,
            'Q (m³/h)': sim.Q * 3600,
            'v₁ (m/s)': sim.v1,
            'v₂ (m/s)': sim.v2,
            'ΔP (kPa)': sim.delta_P / 1000
        })
    
    # Tabela de resultados
    st.markdown("### 📋 Resultados para Diferentes Desníveis")
    
    import pandas as pd
    df = pd.DataFrame(resultados)
    
    st.dataframe(df.style.format({
        'Δh (cm)': '{:.1f}',
        'Q (L/s)': '{:.2f}',
        'Q (m³/h)': '{:.2f}',
        'v₁ (m/s)': '{:.3f}',
        'v₂ (m/s)': '{:.3f}',
        'ΔP (kPa)': '{:.3f}'
    }), width='stretch')
    
    # Gráfico Q vs Δh
    st.markdown("---")
    st.markdown("### 📈 Relação Q = f(√Δh)")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Q vs Δh
    ax1.plot(df['Δh (cm)'], df['Q (L/s)'], 'ro-', linewidth=2, markersize=8)
    ax1.set_xlabel('Desnível Manométrico Δh (cm)', fontsize=11)
    ax1.set_ylabel('Vazão Q (L/s)', fontsize=11)
    ax1.set_title('Vazão vs Desnível', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    
    # Gráfico 2: Q vs √Δh (deve ser linear)
    ax2.plot(np.sqrt(df['Δh (cm)']), df['Q (L/s)'], 'bs-', linewidth=2, markersize=8)
    ax2.set_xlabel('√(Δh) [√cm]', fontsize=11)
    ax2.set_ylabel('Vazão Q (L/s)', fontsize=11)
    ax2.set_title('Vazão vs √Desnível (Relação Linear)', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Observação importante
    st.info("""
    💡 **Observação Importante:**
    - A vazão é proporcional à raiz quadrada do desnível: **Q ∝ √(Δh)**
    - Dobrando Δh, a vazão aumenta por um fator de √2 ≈ 1.41
    - O gráfico Q vs √(Δh) é aproximadamente linear
    """)


def exemplo_4_sensibilidade_cd():
    """Exemplo 4: Análise de Sensibilidade ao Coeficiente de Descarga"""
    st.subheader("⚙️ Exemplo 4: Sensibilidade ao Coeficiente de Descarga (Cd)")
    st.markdown("---")
    
    st.markdown("""
    Este exemplo analisa como o **coeficiente de descarga (Cd)** afeta as medições de vazão.
    O Cd leva em conta perdas e efeitos não ideais no escoamento.
    """)
    
    # Criar simulador
    sim = VenturiSimulator()
    
    # Diferentes valores de Cd
    cd_values = np.linspace(0.90, 1.00, 11)
    resultados = []
    
    q_referencia = None
    
    for cd in cd_values:
        sim.calcular(0.10, 0.05, 1.0, 1000, 13600, 0, 0.15, 0.02, cd, 'Medidor')
        
        if q_referencia is None:
            q_referencia = sim.Q * 1000
            variacao = 0
        else:
            variacao = ((sim.Q * 1000 - q_referencia) / q_referencia) * 100
        
        resultados.append({
            'Cd': cd,
            'Q (L/s)': sim.Q * 1000,
            'Variação (%)': variacao,
            'ΔP (kPa)': sim.delta_P / 1000
        })
    
    # Tabela de resultados
    st.markdown("### 📋 Efeito de Cd na Vazão (Δh fixo = 15 cm)")
    
    import pandas as pd
    df = pd.DataFrame(resultados)
    
    st.dataframe(df.style.format({
        'Cd': '{:.2f}',
        'Q (L/s)': '{:.3f}',
        'Variação (%)': '{:.2f}',
        'ΔP (kPa)': '{:.3f}'
    }), width='stretch')
    
    # Análise estatística
    st.markdown("---")
    st.markdown("### 📊 Análise Estatística")
    
    vazao_min = df['Q (L/s)'].min()
    vazao_max = df['Q (L/s)'].max()
    variacao_total = ((vazao_max - vazao_min) / vazao_min) * 100
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Vazão Mínima (Cd=0.90)", f"{vazao_min:.3f} L/s")
    with col2:
        st.metric("Vazão Máxima (Cd=1.00)", f"{vazao_max:.3f} L/s")
    with col3:
        st.metric("Variação Total", f"{variacao_total:.1f}%")
    
    # Gráfico
    st.markdown("---")
    st.markdown("### 📈 Visualização do Efeito de Cd")
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(df['Cd'], df['Q (L/s)'], 'go-', linewidth=2.5, markersize=8)
    ax.set_xlabel('Coeficiente de Descarga (Cd)', fontsize=12)
    ax.set_ylabel('Vazão Q (L/s)', fontsize=12)
    ax.set_title('Sensibilidade da Vazão ao Coeficiente Cd', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.axhline(y=vazao_min, color='r', linestyle='--', alpha=0.5, label=f'Q mín = {vazao_min:.3f} L/s')
    ax.axhline(y=vazao_max, color='g', linestyle='--', alpha=0.5, label=f'Q máx = {vazao_max:.3f} L/s')
    ax.legend()
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)
    
    # Alerta importante
    st.warning(f"""
    ⚠️ **IMPORTANTE:**
    - Uma variação de 10% em Cd causa **{variacao_total:.1f}%** de variação na vazão!
    - É crucial ter um Cd preciso para medições confiáveis
    - O Cd típico para Venturi varia entre 0.95 e 0.98
    - O Cd depende do número de Reynolds e da geometria do medidor
    """)


def exemplo_5_efeito_beta():
    """Exemplo 5: Efeito da Razão Beta (β = D₂/D₁)"""
    st.subheader("📐 Exemplo 5: Efeito da Razão Beta (β = D₂/D₁)")
    st.markdown("---")
    
    st.markdown("""
    Este exemplo analisa como a **razão de diâmetros β** afeta o desempenho do medidor.
    β é a razão entre o diâmetro da garganta (D₂) e o diâmetro de entrada (D₁).
    """)
    
    # Parâmetros fixos
    D1 = 0.10  # m
    Q = 0.015  # m³/s (fixo)
    
    # Diferentes valores de D2 (β)
    beta_values = np.linspace(0.3, 0.7, 9)
    resultados = []
    
    for beta in beta_values:
        D2 = beta * D1
        
        sim = VenturiSimulator()
        sim.calcular(D1, D2, 1.0, 1000, 13600, Q, 0, 0.02, 1.0, 'Ideal')
        
        resultados.append({
            'β': beta,
            'D₂ (cm)': D2 * 100,
            'Δh (cm)': sim.delta_h * 100,
            'ΔP (kPa)': sim.delta_P / 1000,
            'v₂ (m/s)': sim.v2,
            'v₂/v₁': sim.v2 / sim.v1
        })
    
    # Tabela de resultados
    st.markdown(f"### 📋 Efeito de β (D₁={D1*100:.0f} cm, Q={Q*1000:.0f} L/s fixo)")
    
    import pandas as pd
    df = pd.DataFrame(resultados)
    
    st.dataframe(df.style.format({
        'β': '{:.2f}',
        'D₂ (cm)': '{:.2f}',
        'Δh (cm)': '{:.2f}',
        'ΔP (kPa)': '{:.2f}',
        'v₂ (m/s)': '{:.2f}',
        'v₂/v₁': '{:.2f}'
    }), width='stretch')
    
    # Gráficos
    st.markdown("---")
    st.markdown("### 📈 Visualizações do Efeito de β")
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Δh vs β
    ax1.plot(df['β'], df['Δh (cm)'], 'ro-', linewidth=2.5, markersize=8)
    ax1.set_xlabel('Razão β = D₂/D₁', fontsize=11)
    ax1.set_ylabel('Desnível Δh (cm)', fontsize=11)
    ax1.set_title('Desnível vs Razão Beta', fontsize=12, fontweight='bold')
    ax1.grid(True, alpha=0.3)
    ax1.axvspan(0.4, 0.7, alpha=0.2, color='green', label='Faixa típica')
    ax1.legend()
    
    # Gráfico 2: v₂ vs β
    ax2.plot(df['β'], df['v₂ (m/s)'], 'bs-', linewidth=2.5, markersize=8)
    ax2.set_xlabel('Razão β = D₂/D₁', fontsize=11)
    ax2.set_ylabel('Velocidade na garganta v₂ (m/s)', fontsize=11)
    ax2.set_title('Velocidade vs Razão Beta', fontsize=12, fontweight='bold')
    ax2.grid(True, alpha=0.3)
    ax2.axvspan(0.4, 0.7, alpha=0.2, color='green', label='Faixa típica')
    ax2.legend()
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Observações
    st.markdown("---")
    st.markdown("### 📊 Observações Importantes")
    
    st.info("""
    **Efeitos da Razão Beta:**
    
    - **Menor β** (garganta mais estreita):
      - ✅ Maior velocidade na garganta
      - ✅ Maior queda de pressão (maior sensibilidade)
      - ❌ Maior perda de carga permanente
    
    - **Maior β** (garganta mais larga):
      - ✅ Menor perda de carga
      - ❌ Menor queda de pressão (menor sensibilidade)
      - ❌ Menor velocidade na garganta
    
    - **β típico para Venturi**: 0.4 - 0.7
    - **Compromisso**: Sensibilidade vs Perda de Carga
    """)


# ========== INTERFACE STREAMLIT ==========

def main():
    # Título principal
    st.title("🔬 Simulador Interativo de Medidor de Venturi")
    st.markdown("---")
    
    # Sidebar com controles
    st.sidebar.header("⚙️ Parâmetros de Controle")
    
    # Seletor de modo (Simulação ou Exemplos)
    st.sidebar.subheader("🎯 Modo de Operação")
    app_mode = st.sidebar.radio(
        "Escolha o modo:",
        options=['Simulação Interativa', 'Exemplos Práticos'],
        help="Simulação: configure parâmetros manualmente | Exemplos: veja casos pré-configurados"
    )
    
    # Se modo Exemplos foi selecionado
    if app_mode == 'Exemplos Práticos':
        executar_exemplos()
        return
    
    # Continuar com simulação interativa
    mode = st.sidebar.radio(
        "Tipo de simulação:",
        options=['Ideal', 'Realista', 'Medidor'],
        help="Ideal: sem perdas | Realista: com perdas | Medidor: calcula Q a partir de Δh"
    )
    
    st.sidebar.markdown("---")
    
    # Parâmetros geométricos
    st.sidebar.subheader("📐 Geometria")
    D1 = st.sidebar.slider("D₁ - Diâmetro de entrada (m)", 0.05, 0.30, 0.10, 0.01)
    D2 = st.sidebar.slider("D₂ - Diâmetro da garganta (m)", 0.02, 0.15, 0.05, 0.01)
    L = st.sidebar.slider("L - Comprimento total (m)", 0.5, 3.0, 1.0, 0.1)
    
    st.sidebar.markdown("---")
    
    # Propriedades dos fluidos
    st.sidebar.subheader("💧 Propriedades dos Fluidos")
    rho = st.sidebar.slider("ρ - Densidade do fluido (kg/m³)", 500, 2000, 1000, 50)
    rho_m = st.sidebar.slider("ρₘ - Densidade manométrica (kg/m³)", 10000, 15000, 13600, 100)
    
    st.sidebar.markdown("---")
    
    # Condições de escoamento
    st.sidebar.subheader("🌊 Condições de Escoamento")
    
    if mode == 'Medidor':
        delta_h = st.sidebar.slider("Δh - Desnível manométrico (m)", 0.01, 0.5, 0.1, 0.01)
        Q = None  # Será calculado
    else:
        Q = st.sidebar.slider("Q - Vazão volumétrica (m³/s)", 0.001, 0.05, 0.01, 0.001)
        delta_h = None  # Será calculado
    
    st.sidebar.markdown("---")
    
    # Parâmetros avançados
    st.sidebar.subheader("🔧 Parâmetros Avançados")
    f = st.sidebar.slider("f - Coeficiente de atrito", 0.01, 0.10, 0.02, 0.005)
    Cd = st.sidebar.slider("Cd - Coeficiente de descarga", 0.90, 1.00, 0.98, 0.01)
    
    # Validação
    if D2 >= D1:
        st.error("⚠️ ERRO: D₂ deve ser menor que D₁!")
        return
    
    # Criar simulador e calcular
    sim = VenturiSimulator()
    sim.calcular(D1, D2, L, rho, rho_m, Q if Q else 0, delta_h if delta_h else 0, f, Cd, mode)
    
    # ========== LAYOUT PRINCIPAL ==========
    
    # Métricas principais
    st.header("📊 Resultados Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Vazão Q", f"{sim.Q*1000:.2f} L/s", f"{sim.Q*3600:.1f} m³/h")
    
    with col2:
        st.metric("Desnível Δh", f"{sim.delta_h*100:.2f} cm", f"{sim.delta_h:.4f} m")
    
    with col3:
        st.metric("Velocidade v₁", f"{sim.v1:.3f} m/s")
    
    with col4:
        st.metric("Velocidade v₂", f"{sim.v2:.3f} m/s")
    
    st.markdown("---")
    
    # Abas para organizar visualizações
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📐 Diagrama", "🔬 Manômetro", "📈 Pressão", "⚡ Energia", "📋 Resultados Completos"
    ])
    
    with tab1:
        st.subheader("Diagrama Esquemático do Venturi")
        fig = plotar_diagrama_venturi(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab2:
        st.subheader("Manômetro Diferencial em U")
        fig = plotar_manometro(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab3:
        st.subheader("Perfil de Pressão ao Longo do Tubo")
        fig = plotar_perfil_pressao(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab4:
        st.subheader("Linhas de Energia e Piezométrica")
        fig = plotar_linhas_energia(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab5:
        st.subheader("Resultados Numéricos Completos")
        
        Re = sim.calcular_reynolds()
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.write("**GEOMETRIA:**")
            st.write(f"- D₁ = {sim.D1:.3f} m")
            st.write(f"- D₂ = {sim.D2:.3f} m")
            st.write(f"- A₁ = {sim.A1:.6f} m²")
            st.write(f"- A₂ = {sim.A2:.6f} m²")
            st.write(f"- β = D₂/D₁ = {sim.D2/sim.D1:.3f}")
            
            st.write("")
            st.write("**PROPRIEDADES:**")
            st.write(f"- ρ (fluido) = {sim.rho:.0f} kg/m³")
            st.write(f"- ρₘ (manométrico) = {sim.rho_m:.0f} kg/m³")
            
            st.write("")
            st.write("**VELOCIDADES:**")
            st.write(f"- v₁ = {sim.v1:.3f} m/s")
            st.write(f"- v₂ = {sim.v2:.3f} m/s")
            st.write(f"- Razão v₂/v₁ = {sim.v2/sim.v1:.2f}")
        
        with col_b:
            st.write("**PRESSÕES:**")
            st.write(f"- P₁ = {sim.P1/1000:.2f} kPa")
            st.write(f"- P₂ = {sim.P2/1000:.2f} kPa")
            st.write(f"- ΔP = {sim.delta_P/1000:.3f} kPa")
            
            st.write("")
            st.write("**MEDIÇÕES:**")
            st.write(f"- Vazão Q = {sim.Q*1000:.2f} L/s ({sim.Q*3600:.2f} m³/h)")
            st.write(f"- Δh (manômetro) = {sim.delta_h*100:.2f} cm")
            st.write(f"- Reynolds = {Re:.0f}")
            
            st.write("")
            st.write("**ENERGIA:**")
            st.write(f"- Carga cinética (1) = {sim.v1**2/(2*sim.g):.4f} m")
            st.write(f"- Carga cinética (2) = {sim.v2**2/(2*sim.g):.4f} m")
            st.write(f"- Perda de carga hₗ = {sim.h_L:.4f} m")
        
        # Indicador de regime
        st.markdown("---")
        if Re < 2300:
            st.warning("⚠️ Regime LAMINAR (Re < 2300)")
        elif Re < 4000:
            st.info("🔄 Regime de TRANSIÇÃO (2300 < Re < 4000)")
        else:
            st.success("✅ Regime TURBULENTO (Re > 4000)")
    
    # Rodapé
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center'>
        <p>🔬 <b>Simulador de Medidor de Venturi</b> | Desenvolvido com Streamlit + Python</p>
        <p style='font-size: 0.9em; color: gray;'>
            Modo {}: Simulação de escoamento em medidor de Venturi
        </p>
    </div>
    """.format(mode), unsafe_allow_html=True)


if __name__ == "__main__":
    main()

