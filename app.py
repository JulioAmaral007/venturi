"""
Simulador de Medidor de Venturi
Aplicação web interativa desenvolvida com Streamlit

Execute com: streamlit run app.py
"""

from pathlib import Path
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import warnings
warnings.filterwarnings('ignore')
from app_modules.simulator import VenturiSimulator
from app_modules.plots import (
    plotar_diagrama_venturi,
    plotar_manometro,
    plotar_perfil_pressao,
    plotar_linhas_energia,
)
from app_modules.examples import executar_exemplos

# Configuração da página
st.set_page_config(
    page_title="Simulador de Venturi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# (Definições de simulador, plots e exemplos foram movidas para app_modules)


def exemplo_1_comparacao_modos():
    """Exemplo 1: Comparação entre Modo Ideal e Modo Realista"""
    st.markdown('<div style="color: white; padding: 1rem 1.5rem; margin: 0; font-weight: 600;">🔵🔴 Exemplo 1: Comparação Modo Ideal vs Modo Realista</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo compara o comportamento do medidor de Venturi em duas condições:<br>
    • <strong>Modo Ideal</strong>: Escoamento sem perdas (Cd = 1.0, sem atrito)<br>
    • <strong>Modo Realista</strong>: Escoamento com perdas por atrito e coeficiente de descarga real
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Análise das Diferenças</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div style="color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Exemplo 2: Curva de Calibração do Medidor</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo gera uma <strong>curva de calibração</strong> relacionando a vazão volumétrica (Q) 
    com o desnível manométrico (Δh) para um medidor de Venturi específico.
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 1.5rem 0 1rem 0; font-weight: 600;">📊 Resumo da Calibração</div>', unsafe_allow_html=True)
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Curva de Calibração</div>', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.set_facecolor('white')
    ax.plot(np.array(vazoes) * 1000, desniveis, 'o-', color='#2563eb', 
            linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax.set_xlabel('Vazão (L/s)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_ylabel('Desnível Manométrico Δh (cm)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_title('Curva de Calibração do Medidor de Venturi', fontsize=14, 
                 fontweight='bold', color='#000000', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)
    
    st.markdown('<div style="background: #f0fdf4; color: #000000; border-left: 4px solid #10b981; padding: 1rem; border-radius: 8px; margin: 1rem 0;">✅ A curva mostra a relação quadrática entre vazão e desnível: <strong>Q ∝ √(Δh)</strong></div>', unsafe_allow_html=True)


def exemplo_3_modo_medidor():
    """Exemplo 3: Uso do Modo Medidor (calcular vazão a partir de Δh)"""
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">🔬 Exemplo 3: Modo Medidor - Calcular Vazão a partir de Δh</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo demonstra o uso <strong>prático</strong> do medidor de Venturi: 
    medir o desnível manométrico (Δh) e calcular a vazão (Q) correspondente.
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Relação Q = f(√Δh)</div>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Q vs Δh
    ax1.set_facecolor('white')
    ax1.plot(df['Δh (cm)'], df['Q (L/s)'], 'o-', color='#ef4444', 
             linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax1.set_xlabel('Desnível Manométrico Δh (cm)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_ylabel('Vazão Q (L/s)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_title('Vazão vs Desnível', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Gráfico 2: Q vs √Δh (deve ser linear)
    ax2.set_facecolor('white')
    ax2.plot(np.sqrt(df['Δh (cm)']), df['Q (L/s)'], 'o-', color='#2563eb', 
             linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax2.set_xlabel('√(Δh) [√cm]', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_ylabel('Vazão Q (L/s)', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_title('Vazão vs √Desnível (Relação Linear)', fontsize=12, fontweight='bold', 
                  color='#000000', pad=15)
    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Observação importante
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    💡 <strong>Observação Importante:</strong><br>
    • A vazão é proporcional à raiz quadrada do desnível: <strong>Q ∝ √(Δh)</strong><br>
    • Dobrando Δh, a vazão aumenta por um fator de √2 ≈ 1.41<br>
    • O gráfico Q vs √(Δh) é aproximadamente linear
    </div>
    """, unsafe_allow_html=True)


def exemplo_4_sensibilidade_cd():
    """Exemplo 4: Análise de Sensibilidade ao Coeficiente de Descarga"""
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">⚙️ Exemplo 4: Sensibilidade ao Coeficiente de Descarga (Cd)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo analisa como o <strong>coeficiente de descarga (Cd)</strong> afeta as medições de vazão.
    O Cd leva em conta perdas e efeitos não ideais no escoamento.
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Análise Estatística</div>', unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Visualização do Efeito de Cd</div>', unsafe_allow_html=True)
    
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.set_facecolor('white')
    ax.plot(df['Cd'], df['Q (L/s)'], 'o-', color='#10b981', 
            linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax.set_xlabel('Coeficiente de Descarga (Cd)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_ylabel('Vazão Q (L/s)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_title('Sensibilidade da Vazão ao Coeficiente Cd', fontsize=14, fontweight='bold', 
                 color='#000000', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.axhline(y=vazao_min, color='#ef4444', linestyle='--', alpha=0.5, linewidth=1.5,
               label=f'Q mín = {vazao_min:.3f} L/s')
    ax.axhline(y=vazao_max, color='#10b981', linestyle='--', alpha=0.5, linewidth=1.5,
               label=f'Q máx = {vazao_max:.3f} L/s')
    ax.legend(frameon=True, fancybox=True, shadow=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    
    st.pyplot(fig)
    plt.close(fig)
    
    # Alerta importante
    st.markdown(f"""
    <div style="background: #fffbeb; color: #000000; border-left: 4px solid #f59e0b; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    ⚠️ <strong>IMPORTANTE:</strong><br>
    • Uma variação de 10% em Cd causa <strong>{variacao_total:.1f}%</strong> de variação na vazão!<br>
    • É crucial ter um Cd preciso para medições confiáveis<br>
    • O Cd típico para Venturi varia entre 0.95 e 0.98<br>
    • O Cd depende do número de Reynolds e da geometria do medidor
    </div>
    """, unsafe_allow_html=True)


def exemplo_5_efeito_beta():
    """Exemplo 5: Efeito da Razão Beta (β = D₂/D₁)"""
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📐 Exemplo 5: Efeito da Razão Beta (β = D₂/D₁)</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo analisa como a <strong>razão de diâmetros β</strong> afeta o desempenho do medidor.
    β é a razão entre o diâmetro da garganta (D₂) e o diâmetro de entrada (D₁).
    </div>
    """, unsafe_allow_html=True)
    
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Visualizações do Efeito de β</div>', unsafe_allow_html=True)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    
    # Gráfico 1: Δh vs β
    ax1.set_facecolor('white')
    ax1.plot(df['β'], df['Δh (cm)'], 'o-', color='#ef4444', 
             linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax1.set_xlabel('Razão β = D₂/D₁', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_ylabel('Desnível Δh (cm)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_title('Desnível vs Razão Beta', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax1.axvspan(0.4, 0.7, alpha=0.2, color='#10b981', label='Faixa típica')
    ax1.legend(frameon=True, fancybox=True, shadow=True)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Gráfico 2: v₂ vs β
    ax2.set_facecolor('white')
    ax2.plot(df['β'], df['v₂ (m/s)'], 'o-', color='#2563eb', 
             linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax2.set_xlabel('Razão β = D₂/D₁', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_ylabel('Velocidade na garganta v₂ (m/s)', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_title('Velocidade vs Razão Beta', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax2.axvspan(0.4, 0.7, alpha=0.2, color='#10b981', label='Faixa típica')
    ax2.legend(frameon=True, fancybox=True, shadow=True)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Observações
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Observações Importantes</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    <strong>Efeitos da Razão Beta:</strong><br><br>
    
    • <strong>Menor β</strong> (garganta mais estreita):<br>
      &nbsp;&nbsp;✅ Maior velocidade na garganta<br>
      &nbsp;&nbsp;✅ Maior queda de pressão (maior sensibilidade)<br>
      &nbsp;&nbsp;❌ Maior perda de carga permanente<br><br>
    
    • <strong>Maior β</strong> (garganta mais larga):<br>
      &nbsp;&nbsp;✅ Menor perda de carga<br>
      &nbsp;&nbsp;❌ Menor queda de pressão (menor sensibilidade)<br>
      &nbsp;&nbsp;❌ Menor velocidade na garganta<br><br>
    
    • <strong>β típico para Venturi</strong>: 0.4 - 0.7<br>
    • <strong>Compromisso</strong>: Sensibilidade vs Perda de Carga
    </div>
    """, unsafe_allow_html=True)


def render_sistema_tubulacoes():
    # Seção de Teoria e Metodologia
    with st.expander("📚 Fundamentos Teóricos e Metodologia de Cálculo", expanded=False):
        try:
            project_root = Path(__file__).parent
            venturi_image = project_root / "assets" / "venturi.jpeg"

            if venturi_image.exists():
                st.image(
                    str(venturi_image),
                    caption="Geometria típica de um tubo de Venturi",
                    use_container_width=True
                )
            else:
                st.info("Esquema do Venturi não disponível. Consulte a documentação interna.")
        except Exception:
            st.info("Esquema do Venturi não disponível. Consulte a documentação interna.")

        st.markdown("""
        ### 📐 Conceito do Tubo de Venturi
        O Venturi é um duto convergente-divergente projetado para converter energia de pressão em energia cinética
        na garganta e, em seguida, recuperar parte dessa energia na seção divergente. A medição de pressão entre as
        seções de entrada e garganta permite estimar a vazão com alta precisão, especialmente quando a razão β = D₂/D₁
        está dentro dos limites recomendados.

        ### 🎯 Metodologia de Resolução Passo a Passo

        Esta simulação resolve problemas de escoamento interno em dutos seguindo uma sequência lógica 
        baseada nas leis fundamentais da Mecânica dos Fluidos.
        """)

        # Passo 1
        st.markdown("""
        ---
        #### **Passo 1: Propriedades do Fluido** 🧪

        As propriedades mais relevantes são:
        - **Massa Específica (ρ)**: Relacionada com as forças de inércia do fluido
        - **Viscosidade Dinâmica (μ)**: Mede a resistência ao cisalhamento (fonte do atrito)

        Ambas variam com a temperatura e são obtidas de banco de dados interno.

        *Exemplo para Água a 20°C:*
        ```
        ρ = 998 kg/m³
        μ = 1.002×10⁻³ Pa·s
        ```
        """)

        # Passo 2
        st.markdown("""
        ---
        #### **Passo 2: Velocidade Média do Escoamento** 💨

        Baseado no **Princípio da Conservação da Massa** (Equação da Continuidade):
        """)

        st.latex(r"A = \frac{\pi D^2}{4}")
        st.latex(r"V = \frac{Q}{A}")

        st.markdown("""
        Onde:
        - **Q**: Vazão volumétrica (m³/s)
        - **D**: Diâmetro interno (m)
        - **A**: Área da seção transversal (m²)
        - **V**: Velocidade média (m/s)
        """)

        # Passo 3
        st.markdown("""
        ---
        #### **Passo 3: Número de Reynolds** 🌀

        O **Número de Reynolds (Re)** é o parâmetro mais importante em mecânica dos fluidos. 
        Ele representa a razão entre as **forças de inércia** e as **forças viscosas**.
        """)

        st.latex(r"Re = \frac{\rho V D}{\mu}")

        st.markdown("""
        **Classificação do Regime:**
        - 🟢 **Laminar** (Re < 2.300): Movimento suave em camadas
        - 🟡 **Transição** (2.300 ≤ Re ≤ 4.000): Zona intermediária
        - 🔴 **Turbulento** (Re > 4.000): Movimento caótico com redemoinhos

        O regime determina como calculamos o fator de atrito!
        """)

        # Passo 4
        st.markdown("""
        ---
        #### **Passo 4: Fator de Atrito de Darcy (f)** ⚙️

        O fator de atrito quantifica a resistência ao escoamento causada pelo atrito com as paredes.

        **Para Escoamento Laminar:**
        """)
        st.latex(r"f = \frac{64}{Re}")

        st.markdown("""
        **Para Escoamento Turbulento:**

        Usamos a **Equação de Colebrook-White** (implícita):
        """)
        st.latex(r"\frac{1}{\sqrt{f}} = -2 \log_{10} \left( \frac{\epsilon/D}{3.7} + \frac{2.51}{Re \sqrt{f}} \right)")

        st.markdown("""
        Onde:
        - **ε**: Rugosidade absoluta da parede (m)
        - **ε/D**: Rugosidade relativa (adimensional)

        Esta equação é resolvida numericamente pelo programa.
        """)

        # Passo 5
        st.markdown("""
        ---
        #### **Passo 5: Perdas de Carga (hₗ)** 📉

        A "perda de carga" é a **dissipação de energia mecânica** convertida em calor devido ao atrito.

        **5.1) Perda Distribuída (ao longo do tubo):**

        Calculada pela **Equação de Darcy-Weisbach**:
        """)
        st.latex(r"h_f = f \frac{L}{D} \frac{V^2}{2g}")

        st.markdown("""
        **5.2) Perda Localizada (em acessórios):**

        Cada acessório causa turbulência adicional:
        """)
        st.latex(r"h_s = K \frac{V^2}{2g}")

        st.markdown("""
        **Coeficientes K típicos:**
        - Contração: K = 0.5(1-β²)
        - Expansão: K = (1-β²)²
        - Curva 90°: K = 0.3
        - Válvula gaveta: K = 0.15
        - Válvula globo: K = 10.0
        - Válvula esfera: K = 0.05
        - Válvula retenção: K = 2.5
        - Tê passagem: K = 0.6
        - Tê lateral: K = 1.8

        **Perda Total:**
        """)
        st.latex(r"h_L = h_f + \sum h_s")

        # Passo 6
        st.markdown("""
        ---
        #### **Passo 6: Variação de Pressão** 📊

        Baseado no **Princípio da Conservação de Energia** (Equação de Bernoulli Estendida):
        """)
        st.latex(r"\frac{P_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{P_2}{\rho g} + \frac{V_2^2}{2g} + z_2 + h_L")

        st.markdown("""
        Para diâmetro constante (V₁ = V₂), a pressão em qualquer ponto é:
        """)
        st.latex(r"P_i = P_1 - \rho g \left( \Delta z + h_L^{1 \to i} \right)")

        st.markdown("""
        Onde:
        - **Δz**: Variação de elevação (m)
        - **h_L**: Perda de carga acumulada até o ponto i (m)
        - **g**: Aceleração da gravidade (9.81 m/s²)
        """)

        st.markdown("---")
        st.markdown("**📐 Diagrama do Princípio de Bernoulli**")

        try:
            project_root = Path(__file__).parent
            image_path = project_root / "assets" / "principio-bernoulli.webp"

            if image_path.exists():
                st.image(
                    str(image_path),
                    caption="Princípio de Bernoulli - Conservação de Energia em Escoamentos",
                    use_container_width=True
                )
            else:
                st.info("Diagrama não disponível. Equações mostradas acima ilustram o princípio.")

        except Exception:
            st.info("Diagrama não disponível. Equações mostradas acima ilustram o princípio.")

        st.markdown("""
        **Legenda das Variáveis:**
        - **P₁, P₂**: Pressões nos pontos 1 e 2 (Pa)
        - **V₁, V₂**: Velocidades nos pontos 1 e 2 (m/s)
        - **h₁, h₂**: Alturas (cota) dos pontos 1 e 2 (m)
        - **A₁, A₂**: Áreas das seções transversais 1 e 2 (m²)
        - **Q**: Vazão volumétrica (m³/s)
        - **ρ**: Densidade do fluido (kg/m³)
        - **g**: Aceleração da gravidade (9.81 m/s²)

        **Equação de Bernoulli Estendida:**
        """)
        st.latex(r"\frac{P_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{P_2}{\rho g} + \frac{V_2^2}{2g} + z_2 + h_L")

        st.markdown("""
        ---

        ### 💡 Como Usar Esta Simulação

        1. **Escolha o modo de operação** (Ideal, Realista ou Medidor) e selecione o fluido na barra lateral.
        2. **Defina os parâmetros geométricos** (D₁, D₂ e L) e ajuste os controles de vazão ou Δh conforme o modo selecionado.
        3. **Refine parâmetros avançados** (f e Cd) quando quiser estudar efeitos de atrito ou calibração.
        4. **Analise as métricas principais** exibidas no topo e utilize as abas para visualizar diagramas, linhas de energia e dados completos.
        5. **Compare com os exemplos práticos** na aba “Exemplos Práticos” da barra lateral para validar cenários típicos.
        """)


def render_sobre_projeto():
    """Renderiza o conteúdo da aba Sobre o Projeto"""
    st.header("Sobre o Projeto")

    try:
        project_root = Path(__file__).parent
        venturi_image = project_root / "assets" / "tubo-venturi.webp"

        if venturi_image.exists():
            st.image(
                str(venturi_image),
                caption="Visualização esquemática do Venturi utilizado na simulação",
                use_container_width=True
            )
        else:
            st.info("Imagem esquemática do Venturi não encontrada no diretório de assets.")
    except Exception:
        st.info("Imagem esquemática do Venturi não pôde ser carregada.")

    st.markdown("""
    O Venturi funciona ao acelerar o fluido na garganta e medir a diferença de pressão entre as seções de
    entrada e estrangulamento. Essa diferença, combinada com a razão geométrica β, permite calcular a vazão
    com precisão superior à de orifícios simples, com menores perdas de carga permanentes.
    """)

    st.markdown("""
    ### 📋 Descrição
    Este simulador interativo foi criado para estudar o comportamento de medidores de Venturi,
    permitindo comparar diferentes modos de operação, ajustar parâmetros geométricos e visualizar
    resultados numéricos e gráficos em tempo real.

    ### 🎯 Funcionalidades

    #### Configuração de Fluidos e Modos
    - Presets de fluidos com propriedades prontas (água em diferentes temperaturas, óleos, etc.).
    - Modo **Ideal**, **Realista** e **Medidor**, com seleção direta na barra lateral.
    - Ajuste manual ou automático de densidade do fluido e fluido manométrico fixo (Hg).

    #### Simulação do Venturi
    - Sliders para definir D₁, D₂ e comprimento total.
    - Controle de vazão ou desnível conforme o modo ativo.
    - Parâmetros avançados: coeficiente de atrito (f) e coeficiente de descarga (Cd).
    - Indicadores automáticos de β, número de Reynolds e regime de escoamento.
    - Visualizações: diagrama esquemático, manômetro em U, perfil de pressão e linhas de energia.

    #### Exemplos Práticos
    - Conjunto de cenários prontos para comparação entre modos ideal/real, curvas de calibração,
      uso como medidor, sensibilidade ao Cd e efeito da razão β.

    ### 📊 Métodos de Cálculo
    """)

    st.markdown("#### Continuidade e equações principais")
    st.latex(r"A = \pi D^2 / 4")
    st.latex(r"V = \frac{Q}{A}")

    st.markdown("#### Número de Reynolds")
    st.latex(r"Re = \frac{\rho V D}{\mu}")

    st.markdown("#### Equação de energia para o Venturi")
    st.latex(r"\frac{P_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{P_2}{\rho g} + \frac{V_2^2}{2g} + z_2 + h_L")

    st.markdown("#### Relação manométrica")
    st.latex(r"\Delta P = (\rho_m - \rho) g \Delta h")

    st.markdown("#### Vazão corrigida (modo Realista)")
    st.latex(r"Q = C_d A_2 \sqrt{\frac{2 (P_1 - P_2)}{\rho (1 - \beta^4)}}")

    st.markdown("""
    ### 🛠️ Tecnologias
    - **Streamlit** para a interface.
    - **NumPy/Pandas** no processamento numérico.
    - **Matplotlib** nas visualizações customizadas.

    ### 💡 Dicas de Uso
    1. Ajuste β dentro da faixa recomendada (0.4 a 0.7) para manter boa sensibilidade.
    2. Utilize o modo Realista para avaliar efeitos de atrito e Cd.
    3. No modo Medidor, varie Δh para gerar rapidamente curvas Q versus Δh.
    4. Teste os exemplos prontos para validar interpretações ou preparar aulas/demonstrações.
    """)

    st.info("""
    **💡 Dica:** Personalize os slides da barra lateral e utilize os gráficos da aba “Visão Geral”
    para identificar rapidamente impactos em pressão, energia e vazão.
    """)


def render_graph_explanation(description: str):
    """Renderiza expander com diretrizes de interpretação do gráfico atual."""
    st.markdown("##### Explicação do gráfico")
    with st.expander("ℹ️ Como interpretar este gráfico", expanded=False):
        st.markdown(description)


# ========== INTERFACE STREAMLIT ==========

def main():
    from app_modules.components import (
        parameter_slider, fluid_preset_selector, manometric_fluid_selector,
        validate_geometry, display_beta_ratio, create_expander, error_box,
        warning_box, info_box
    )
    from app_modules.utils import get_fluid_properties, get_manometric_density
    from app_modules.constants import ICONS, TOOLTIPS
    
    # Sidebar com controles
    st.sidebar.header(f"{ICONS['settings']} Configuração do Simulador")
    
    # Seletor de modo (Simulação ou Exemplos)
    st.sidebar.subheader(f"{ICONS['mode']} Modo de Operação")
    app_mode = st.sidebar.radio(
        "Escolha o modo:",
        options=['Simulação Interativa', 'Exemplos Práticos'],
        help="Simulação: configure parâmetros manualmente | Exemplos: veja casos pré-configurados"
    )
    
    # Se modo Exemplos foi selecionado
    if app_mode == 'Exemplos Práticos':
        executar_exemplos()
        return
    
    # Título principal (apenas no modo Simulação Interativa)
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">🔬 Simulador Interativo de Medidor de Venturi</h1>
        <p style="color: rgba(255, 255, 0, 1); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Ferramenta avançada para análise de escoamento em medidores de Venturi</p>
    </div>
    """, unsafe_allow_html=True)

    # Tipo de simulação
    mode = st.sidebar.radio(
        f"{ICONS['science']} Tipo de Simulação:",
        options=['Ideal', 'Realista', 'Medidor'],
        help=f"Ideal: {TOOLTIPS['modo_ideal']}\nRealista: {TOOLTIPS['modo_realista']}\nMedidor: {TOOLTIPS['modo_medidor']}"
    )
    
    st.sidebar.markdown("---")
    
    # Seção teórica antes dos parâmetros
    render_sistema_tubulacoes()

    # Parâmetros geométricos (com expander)
    with create_expander(f"{ICONS['geometry']} Geometria", expanded=True):
        D1 = parameter_slider(
            "D₁ - Diâmetro de entrada (m)",
            min_value=0.05,
            max_value=0.30,
            default_value=0.10,
            step=0.01,
            tooltip_key='D1',
            key='D1_slider'
        )
        
        D2 = parameter_slider(
            "D₂ - Diâmetro da garganta (m)",
            min_value=0.02,
            max_value=0.15,
            default_value=0.05,
            step=0.01,
            tooltip_key='D2',
            key='D2_slider'
        )
        
        # Mostrar razão beta
        display_beta_ratio(D1, D2)
        
        L = parameter_slider(
            "L - Comprimento total (m)",
            min_value=0.5,
            max_value=3.0,
            default_value=1.0,
            step=0.1,
            tooltip_key='L',
            key='L_slider'
        )
    
    # Propriedades dos fluidos (com expander e presets)
    with create_expander(f"{ICONS['fluid']} Fluido", expanded=True):
        # Seletor de preset
        fluid_name = fluid_preset_selector(key='fluid_preset')
        fluid_props = get_fluid_properties(fluid_name)
        
        if fluid_name == 'Personalizado':
            rho = st.slider(
                "ρ - Densidade do fluido (kg/m³)",
                min_value=500,
                max_value=2000,
                value=1000,
                step=50,
                help=TOOLTIPS.get('rho', ''),
                key='rho_custom'
            )
            nu_value = st.number_input(
                "ν - Viscosidade cinemática (m²/s)",
                min_value=2e-7,
                max_value=2e-3,
                value=1e-6,
                step=1e-7,
                format="%.2e",
                help=TOOLTIPS.get('nu', ''),
                key='nu_custom'
            )
            st.caption(f"ν selecionado: {nu_value:.2e} m²/s")
        else:
            rho = fluid_props['rho']
            nu_value = fluid_props.get('nu', 1e-6)
            st.metric(
                "Densidade ρ",
                f"{rho} kg/m³",
                help=TOOLTIPS.get('rho', '')
            )
            st.metric(
                "Viscosidade cinemática ν",
                f"{nu_value:.2e} m²/s",
                help=TOOLTIPS.get('nu', '')
            )
        
        # Fluido manométrico fixo (Mercúrio)
        st.markdown("**Fluido Manométrico**")
        st.caption("Mercúrio (Hg)")
        rho_m = 13600  # kg/m³ (densidade do mercúrio)
        st.metric("Densidade ρₘ", f"{rho_m} kg/m³")
    
    # Condições de escoamento (com expander)
    with create_expander(f"{ICONS['flow']} Condições de Escoamento", expanded=True):
        if mode == 'Medidor':
            delta_h = parameter_slider(
                "Δh - Desnível manométrico (m)",
                min_value=0.01,
                max_value=0.5,
                default_value=0.1,
                step=0.01,
                tooltip_key='delta_h',
                key='delta_h_slider'
            )
            Q = None  # Será calculado
        else:
            flow_input_mode = st.radio(
                "Variável de entrada",
                options=[
                    "Vazão volumétrica",
                    "Velocidade na entrada (v₁)",
                    "Velocidade na garganta (v₂)"
                ],
                index=0,
                help=TOOLTIPS.get('flow_input_choice', ''),
                key='flow_input_mode_radio'
            )

            area_entrada = np.pi * (D1 / 2) ** 2
            area_garganta = np.pi * (D2 / 2) ** 2

            if flow_input_mode == "Vazão volumétrica":
                Q = parameter_slider(
                    "Q - Vazão volumétrica (m³/s)",
                    min_value=0.001,
                    max_value=0.05,
                    default_value=0.01,
                    step=0.001,
                    tooltip_key='Q',
                    key='Q_slider',
                    format_str="%.4f"
                )
            elif flow_input_mode == "Velocidade na entrada (v₁)":
                v1_input = parameter_slider(
                    "v₁ - Velocidade na entrada (m/s)",
                    min_value=0.5,
                    max_value=25.0,
                    default_value=5.0,
                    step=0.1,
                    tooltip_key='v1_input',
                    key='v1_slider',
                    format_str="%.2f"
                )
                Q = v1_input * area_entrada
                st.caption(f"Vazão equivalente: {Q*1000:.2f} L/s")
            else:
                v2_input = parameter_slider(
                    "v₂ - Velocidade na garganta (m/s)",
                    min_value=0.5,
                    max_value=35.0,
                    default_value=8.0,
                    step=0.1,
                    tooltip_key='v2_input',
                    key='v2_slider',
                    format_str="%.2f"
                )
                Q = v2_input * area_garganta
                st.caption(f"Vazão equivalente: {Q*1000:.2f} L/s")

            delta_h = None  # Será calculado
    
    # Parâmetros avançados (em expander fechado)
    with create_expander(f"{ICONS['advanced']} Parâmetros Avançados", expanded=False):
        f = parameter_slider(
            "f - Coeficiente de atrito",
            min_value=0.01,
            max_value=0.10,
            default_value=0.02,
            step=0.005,
            tooltip_key='f',
            key='f_slider'
        )
        
        Cd = parameter_slider(
            "Cd - Coeficiente de descarga",
            min_value=0.90,
            max_value=1.00,
            default_value=0.98,
            step=0.01,
            tooltip_key='Cd',
            key='Cd_slider'
        )
    
    # Validação com feedback visual
    is_valid, error_msg = validate_geometry(D1, D2)
    if not is_valid:
        error_box(error_msg)
        return
    elif error_msg:  # Aviso, não erro crítico
        warning_box(error_msg)
    
    # Criar simulador e calcular
    sim = VenturiSimulator()
    sim.calcular(D1, D2, L, rho, rho_m, Q if Q else 0, delta_h if delta_h else 0, f, Cd, mode)
    
    # ========== LAYOUT PRINCIPAL ==========
    
    from app_modules.components import section_header, display_reynolds_indicator
    
    # Métricas principais
    section_header("Resultados Principais", icon=ICONS['results'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Vazão Q", 
            f"{sim.Q*1000:.2f} L/s", 
            f"{sim.Q*3600:.1f} m³/h",
            help="Vazão volumétrica do fluido"
        )
    
    with col2:
        st.metric(
            "Desnível Δh", 
            f"{sim.delta_h*100:.2f} cm", 
            f"{sim.delta_h:.4f} m",
            help="Desnível observado no manômetro diferencial"
        )
    
    with col3:
        st.metric(
            "Velocidade v₁", 
            f"{sim.v1:.3f} m/s",
            help="Velocidade na seção de entrada"
        )
    
    with col4:
        st.metric(
            "Velocidade v₂", 
            f"{sim.v2:.3f} m/s",
            help="Velocidade na garganta (seção mais estreita)"
        )
    
    # Indicador de Reynolds
    Re = sim.calcular_reynolds()
    display_reynolds_indicator(Re)
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Abas para organizar visualizações
    tab1, tab2, tab3 = st.tabs([
        f"{ICONS['diagram']} Visão Geral", 
        f"{ICONS['data']} Dados Completos",
        f"{ICONS['info']} Sobre o Projeto"
    ])
    
    with tab1:
        st.markdown("**Diagrama Esquemático do Venturi**")
        fig = plotar_diagrama_venturi(sim)
        st.pyplot(fig)
        plt.close(fig)
        render_graph_explanation("""
        **O que este gráfico mostra:**

        Representação geométrica do medidor, destacando diâmetros D₁ e D₂, garganta e difusor.

        **Como interpretar:**

        - Observe a transição suave entre as seções, fator-chave para minimizar perdas.
        - Use o desenho para conferir se a razão β = D₂/D₁ segue a faixa recomendada (0.4–0.7).
        - A área sombreada indica o local onde ocorre a maior velocidade (garganta).

        **Dica:** Ajustes nos sliders de D₁ e D₂ atualizam o diagrama em tempo real, permitindo visualizar o impacto geométrico antes de rodar novas simulações.
        """)

        st.markdown("---")

        st.markdown("**Manômetro Diferencial em U**")
        fig = plotar_manometro(sim)
        st.pyplot(fig)
        plt.close(fig)
        render_graph_explanation("""
        **O que este gráfico mostra:**

        Modelo do manômetro diferencial em U utilizado para medir o desnível Δh entre as tomadas de pressão.

        **Como interpretar:**

        - A coluna de mercúrio (ρₘ = 13600 kg/m³) é comparada ao fluido em escoamento (ρ).
        - O desnível Δh exibido corresponde ao valor calculado com base nos parâmetros atuais.
        - Maior Δh indica maior diferença de pressão entre a entrada e a garganta do Venturi.

        **Aplicação prática:** Use esta visualização para validar se o Δh medido experimentalmente é compatível com a simulação nos modos Realista ou Medidor.
        """)

        st.markdown("---")

        st.markdown("**Perfil de Pressão ao Longo do Tubo**")
        fig = plotar_perfil_pressao(sim)
        st.pyplot(fig)
        plt.close(fig)
        render_graph_explanation("""
        **O que este gráfico mostra:**

        Evolução da pressão estática ao longo das seções do Venturi.

        **Como interpretar:**

        - A queda abrupta na garganta representa a conversão de pressão em energia cinética.
        - No difusor, a pressão se recupera parcialmente; a diferença final corresponde à perda de carga total hₗ.
        - Alterar Cd, f ou o regime de escoamento modifica o gradiente exibido.

        **Uso prático:** identifique condições com recuperação insuficiente (difusor curto ou Cd baixo) e avalie o impacto de ajustes nos parâmetros de entrada.
        """)

        st.markdown("---")

        st.markdown("**Linhas de Energia e Piezométrica**")
        fig = plotar_linhas_energia(sim)
        st.pyplot(fig)
        plt.close(fig)
        render_graph_explanation("""
        **O que este gráfico mostra:**

        As linhas de energia total e piezométrica (energia de pressão + potencial) ao longo do Venturi.

        **Como interpretar:**

        - A linha roxa (energia total) evidencia o consumo de energia devido às perdas distribuídas/localizadas.
        - A linha azul (piezométrica) acompanha a variação de pressão estática considerando a cota geométrica.
        - A separação entre as linhas revela a contribuição da energia cinética (V²/2g).

        **Insights:** monitore a inclinação para verificar se o fator de atrito f está coerente e se o regime turbulento desejado está garantindo perdas controladas.
        """)
    
    with tab2:
        st.subheader("Resultados Numéricos Completos")
        st.caption("Detalhe completo das propriedades calculadas. Use para relatórios ou calibrações.")
        
        Re = sim.calcular_reynolds()
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**GEOMETRIA:**")
            st.write(f"• D₁ = {sim.D1:.3f} m")
            st.write(f"• D₂ = {sim.D2:.3f} m")
            st.write(f"• A₁ = {sim.A1:.6f} m²")
            st.write(f"• A₂ = {sim.A2:.6f} m²")
            st.write(f"• β = D₂/D₁ = {sim.D2/sim.D1:.3f}")
            
            st.markdown("")
            st.markdown("**PROPRIEDADES:**")
            st.write(f"• ρ (fluido) = {sim.rho:.0f} kg/m³")
            st.write(f"• ρₘ (manométrico) = {sim.rho_m:.0f} kg/m³")
            
            st.markdown("")
            st.markdown("**VELOCIDADES:**")
            st.write(f"• v₁ = {sim.v1:.3f} m/s")
            st.write(f"• v₂ = {sim.v2:.3f} m/s")
            st.write(f"• Razão v₂/v₁ = {sim.v2/sim.v1:.2f}")
        
        with col_b:
            st.markdown("**PRESSÕES:**")
            st.write(f"• P₁ = {sim.P1/1000:.2f} kPa")
            st.write(f"• P₂ = {sim.P2/1000:.2f} kPa")
            st.write(f"• ΔP = {sim.delta_P/1000:.3f} kPa")
            
            st.markdown("")
            st.markdown("**MEDIÇÕES:**")
            st.write(f"• Vazão Q = {sim.Q*1000:.2f} L/s ({sim.Q*3600:.2f} m³/h)")
            st.write(f"• Δh (manômetro) = {sim.delta_h*100:.2f} cm")
            st.write(f"• Reynolds = {Re:.0f}")
            
            st.markdown("")
            st.markdown("**ENERGIA:**")
            st.write(f"• Carga cinética (1) = {sim.v1**2/(2*sim.g):.4f} m")
            st.write(f"• Carga cinética (2) = {sim.v2**2/(2*sim.g):.4f} m")
            st.write(f"• Perda de carga hₗ = {sim.h_L:.4f} m")
        
        # Indicador de regime (já mostrado acima, remover duplicação)
        st.markdown("---")
        st.markdown("**Regime de Escoamento:**")
        display_reynolds_indicator(Re)

    with tab3:
        render_sobre_projeto()
    
    # Melhorado: rodapé nativo e resumido
    st.write("")
    st.divider()
    st.caption(f"🔬 Simulador de Medidor de Venturi • Modo atual: {mode}")


if __name__ == "__main__":
    main()

