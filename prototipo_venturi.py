"""
PROTÓTIPO - Simulador de Medidor de Venturi
Versão simplificada para demonstração ao professor

Execute com: streamlit run prototipo_venturi.py
"""

import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')

# Configuração da página
st.set_page_config(
    page_title="Protótipo - Simulador de Venturi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

class VenturiSimulator:
    """Simulador simplificado do medidor de Venturi"""
    
    def __init__(self):
        self.g = 9.81  # m/s²
        self.D1 = 0.0
        self.D2 = 0.0
        self.rho = 1000.0
        self.rho_m = 13600.0
        self.Q = 0.0
        self.delta_h = 0.0
        self.v1 = 0.0
        self.v2 = 0.0
        self.P1 = 0.0
        self.P2 = 0.0
        self.delta_P = 0.0
        self.A1 = 0.0
        self.A2 = 0.0
        
    def calcular(self, D1, D2, rho, rho_m, Q, delta_h, mode='Simulacao'):
        """Calcula os parâmetros do medidor de Venturi"""
        self.D1 = D1
        self.D2 = D2
        self.rho = rho
        self.rho_m = rho_m
        
        # Áreas
        self.A1 = np.pi * (D1/2)**2
        self.A2 = np.pi * (D2/2)**2
        
        if mode == 'Simulacao':
            # Modo simulação: Q conhecido, calcular delta_h
            self.Q = Q
            self.v1 = Q / self.A1
            self.v2 = Q / self.A2
            
            # Equação de Bernoulli simplificada
            self.delta_P = 0.5 * self.rho * (self.v2**2 - self.v1**2)
            self.delta_h = self.delta_P / ((self.rho_m - self.rho) * self.g)
            
        elif mode == 'Medidor':
            # Modo medidor: delta_h conhecido, calcular Q
            self.delta_h = delta_h
            self.delta_P = (self.rho_m - self.rho) * self.g * self.delta_h
            
            # Velocidade na garganta (simplificado)
            v2_squared = 2 * self.delta_P / self.rho
            self.v2 = np.sqrt(v2_squared)
            self.v1 = self.v2 * (self.A2 / self.A1)
            self.Q = self.v1 * self.A1
        
        # Pressões (simplificado)
        self.P1 = 101325  # Pressão atmosférica
        self.P2 = self.P1 - self.delta_P

def plotar_diagrama_venturi(sim):
    """Cria diagrama esquemático do medidor de Venturi"""
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')
    ax.set_facecolor('white')
    
    # Dimensões do diagrama
    L_total = 8
    H_entrada = 2
    H_garganta = 1
    
    # Coordenadas do Venturi
    x = np.array([0, 2, 4, 6, 8])
    y_superior = np.array([H_entrada/2, H_entrada/2, H_garganta/2, H_entrada/2, H_entrada/2])
    y_inferior = -y_superior
    
    # Desenhar o Venturi
    ax.plot(x, y_superior, 'b-', linewidth=3, label='Parede do Venturi')
    ax.plot(x, y_inferior, 'b-', linewidth=3)
    
    # Preencher área do Venturi
    ax.fill_between(x, y_superior, y_inferior, alpha=0.1, color='blue')
    
    # Pontos de medição
    ax.plot([2, 2], [-1.5, 1.5], 'r-', linewidth=2, label='Ponto 1 (Entrada)')
    ax.plot([4, 4], [-0.8, 0.8], 'r-', linewidth=2, label='Ponto 2 (Garganta)')
    
    # Manômetro
    ax.plot([2, 2, 4, 4], [2.5, 3, 3, 2.5], 'g-', linewidth=2, label='Manômetro')
    ax.plot([2, 4], [3, 3], 'g-', linewidth=2)
    
    # Anotações
    ax.annotate('D₁', xy=(2, 0), xytext=(2, 1.2), ha='center', fontsize=12, fontweight='bold')
    ax.annotate('D₂', xy=(4, 0), xytext=(4, 0.6), ha='center', fontsize=12, fontweight='bold')
    ax.annotate('Δh', xy=(3, 3), xytext=(3, 3.3), ha='center', fontsize=10, fontweight='bold')
    
    # Configurações do gráfico
    ax.set_xlim(-0.5, 8.5)
    ax.set_ylim(-3, 4)
    ax.set_xlabel('Comprimento (m)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Altura (m)', fontsize=12, fontweight='bold')
    ax.set_title('Diagrama Esquemático do Medidor de Venturi', fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    ax.legend(loc='upper right')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    plt.tight_layout()
    return fig

def main():
    # Título principal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h1 style="color: white; margin: 0; font-size: 2.5rem; font-weight: 700; text-align: center;">🔬 PROTÓTIPO - Simulador de Medidor de Venturi</h1>
        <p style="color: rgba(255, 255, 255, 0.9); margin: 0.5rem 0 0 0; font-size: 1.2rem; text-align: center;">Demonstração para aprovação do trabalho</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar com controles
    st.sidebar.header("⚙️ Parâmetros de Controle")
    
    # Modo de operação
    mode = st.sidebar.radio(
        "Modo de operação:",
        options=['Simulação', 'Medidor'],
        help="Simulação: calcular Δh a partir de Q | Medidor: calcular Q a partir de Δh"
    )
    
    st.sidebar.markdown("---")
    
    # Parâmetros geométricos
    st.sidebar.subheader("📐 Geometria")
    D1 = st.sidebar.slider("D₁ - Diâmetro de entrada (cm)", 5, 30, 10, 1)
    D2 = st.sidebar.slider("D₂ - Diâmetro da garganta (cm)", 2, 15, 5, 1)
    
    # Converter para metros
    D1 = D1 / 100
    D2 = D2 / 100
    
    # Validação
    if D2 >= D1:
        st.error("⚠️ ERRO: D₂ deve ser menor que D₁!")
        return
    
    st.sidebar.markdown("---")
    
    # Propriedades dos fluidos
    st.sidebar.subheader("💧 Propriedades dos Fluidos")
    rho = st.sidebar.slider("ρ - Densidade do fluido (kg/m³)", 500, 2000, 1000, 50)
    rho_m = st.sidebar.slider("ρₘ - Densidade manométrica (kg/m³)", 10000, 15000, 13600, 100)
    
    st.sidebar.markdown("---")
    
    # Condições de escoamento
    st.sidebar.subheader("🌊 Condições de Escoamento")
    
    if mode == 'Medidor':
        delta_h = st.sidebar.slider("Δh - Desnível manométrico (cm)", 1, 50, 10, 1)
        delta_h = delta_h / 100  # Converter para metros
        Q = None
    else:
        Q = st.sidebar.slider("Q - Vazão volumétrica (L/s)", 1, 50, 10, 1)
        Q = Q / 1000  # Converter para m³/s
        delta_h = None
    
    # Criar simulador e calcular
    sim = VenturiSimulator()
    
    if mode == 'Simulação':
        sim.calcular(D1, D2, rho, rho_m, Q, 0, 'Simulacao')
    else:
        sim.calcular(D1, D2, rho, rho_m, 0, delta_h, 'Medidor')
    
    # ========== RESULTADOS PRINCIPAIS ==========
    
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Resultados Principais</div>', unsafe_allow_html=True)
    
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
    
    # Layout em duas colunas
    col_left, col_right = st.columns([1, 1])
    
    with col_left:
        st.subheader("📐 Diagrama do Venturi")
        fig = plotar_diagrama_venturi(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with col_right:
        st.subheader("📋 Resultados Detalhados")
        
        st.markdown("**GEOMETRIA:**")
        st.write(f"• D₁ = {sim.D1*100:.1f} cm")
        st.write(f"• D₂ = {sim.D2*100:.1f} cm")
        st.write(f"• β = D₂/D₁ = {sim.D2/sim.D1:.3f}")
        
        st.markdown("")
        st.markdown("**PROPRIEDADES:**")
        st.write(f"• ρ (fluido) = {sim.rho:.0f} kg/m³")
        st.write(f"• ρₘ (manométrico) = {sim.rho_m:.0f} kg/m³")
        
        st.markdown("")
        st.markdown("**RESULTADOS:**")
        st.write(f"• Vazão Q = {sim.Q*1000:.2f} L/s")
        st.write(f"• Δh = {sim.delta_h*100:.2f} cm")
        st.write(f"• v₁ = {sim.v1:.3f} m/s")
        st.write(f"• v₂ = {sim.v2:.3f} m/s")
        st.write(f"• ΔP = {sim.delta_P/1000:.3f} kPa")
    
    # Informações sobre o protótipo
    st.markdown("---")
    st.markdown("""
    <div style="background: #f0fdf4; color: #000000; border-left: 4px solid #10b981; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    <strong>📝 Sobre este Protótipo:</strong><br><br>
    • <strong>Objetivo:</strong> Demonstrar o conceito do simulador de medidor de Venturi<br>
    • <strong>Funcionalidades:</strong> Cálculo de vazão e desnível manométrico<br>
    • <strong>Modos:</strong> Simulação (Q → Δh) e Medidor (Δh → Q)<br>
    • <strong>Visualização:</strong> Diagrama esquemático do Venturi<br><br>
    <strong>Versão completa incluirá:</strong> Gráficos avançados, exemplos práticos, análise de sensibilidade, e muito mais!
    </div>
    """, unsafe_allow_html=True)
    
    # Rodapé
    st.markdown("""
    <div style="text-align: center; padding: 2rem; color: #64748b; border-top: 1px solid #e2e8f0; margin-top: 3rem;">
        <p><strong>🔬 Protótipo - Simulador de Medidor de Venturi</strong></p>
        <p>Desenvolvido com Streamlit + Python | Modo: {}</p>
    </div>
    """.format(mode), unsafe_allow_html=True)

if __name__ == "__main__":
    main()
