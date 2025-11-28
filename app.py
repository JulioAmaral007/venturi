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
        
        # Se personalizado, permitir edição
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
        else:
            rho = fluid_props['rho']
            st.metric("Densidade ρ", f"{rho} kg/m³")
        
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
    
    # Abas para organizar visualizações (reduzido de 3 para 2)
    tab1, tab2 = st.tabs([
        f"{ICONS['diagram']} Visão Geral", 
        f"{ICONS['data']} Dados Completos"
    ])
    
    with tab1:
        # Primeira linha: Diagrama e Manômetro
        col_diag, col_man = st.columns([1.2, 1])
        
        with col_diag:
            st.markdown("**Diagrama Esquemático do Venturi**")
            fig = plotar_diagrama_venturi(sim)
            st.pyplot(fig)
            plt.close(fig)
        
        with col_man:
            st.markdown("**Manômetro Diferencial em U**")
            fig = plotar_manometro(sim)
            st.pyplot(fig)
            plt.close(fig)
        
        st.markdown("---")
        
        # Segunda linha: Perfil de Pressão e Linhas de Energia lado a lado
        col_press, col_energy = st.columns(2)
        
        with col_press:
            st.markdown("**Perfil de Pressão ao Longo do Tubo**")
            fig = plotar_perfil_pressao(sim)
            st.pyplot(fig)
            plt.close(fig)
        
        with col_energy:
            st.markdown("**Linhas de Energia e Piezométrica**")
            fig = plotar_linhas_energia(sim)
            st.pyplot(fig)
            plt.close(fig)
    
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
    
    # Melhorado: rodapé nativo e resumido
    st.write("")
    st.divider()
    st.caption(f"🔬 Simulador de Medidor de Venturi • Modo atual: {mode}")


if __name__ == "__main__":
    main()

