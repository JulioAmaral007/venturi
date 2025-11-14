import numpy as np
import streamlit as st
from .simulator import VenturiSimulator
from .plots import plotar_perfil_pressao, plotar_linhas_energia


def executar_exemplos():
    """Interface para executar os exemplos práticos do simulador."""
    st.markdown('<div style="background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"><h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">📚 Exemplos Práticos</h1><p style="color: rgba(255, 255, 0, 1); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Explore diferentes casos de uso do medidor de Venturi através de exemplos pré-configurados</p></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.subheader("📋 Selecione o Exemplo")
    
    exemplo = st.sidebar.selectbox(
        "Escolha um exemplo:",
        [
            "1. Comparação: Ideal vs Realista",
            "2. Curva de Calibração",
            "3. Modo Medidor (Δh → Q)",
            "4. Sensibilidade ao Cd",
            "5. Análise de Número de Reynolds"
        ]
    )
    
    st.sidebar.markdown("---")
    st.sidebar.info("💡 **Dica:** Cada exemplo demonstra um aspecto importante do funcionamento do medidor de Venturi.")
    
    if "1." in exemplo:
        exemplo_1_comparacao_modos()
    elif "2." in exemplo:
        exemplo_2_curva_calibracao()
    elif "3." in exemplo:
        exemplo_3_modo_medidor()
    elif "4." in exemplo:
        exemplo_4_sensibilidade_cd()
    elif "5." in exemplo:
        exemplo_5_reynolds()


def exemplo_1_comparacao_modos():
    st.markdown('<div style="color: white; padding: 1rem 1.5rem; margin: 0; font-weight: 600;">🔵🔴 Exemplo 1: Comparação Modo Ideal vs Modo Realista</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo compara o comportamento do medidor de Venturi em duas condições:<br>
    • <strong>Modo Ideal</strong>: Escoamento sem perdas (Cd = 1.0, sem atrito)<br>
    • <strong>Modo Realista</strong>: Escoamento com perdas por atrito e coeficiente de descarga real
    </div>
    """, unsafe_allow_html=True)
    
    D1 = 0.10
    D2 = 0.05
    Q = 0.015
    
    sim_ideal = VenturiSimulator()
    sim_ideal.calcular(D1, D2, 1.0, 1000, 13600, Q, 0, 0.02, 1.0, 'Ideal')
    
    sim_real = VenturiSimulator()
    sim_real.calcular(D1, D2, 1.0, 1000, 13600, Q, 0, 0.025, 0.96, 'Realista')
    
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
    
    st.markdown("---")
    st.markdown("### 📈 Visualizações Comparativas")
    tab1, tab2 = st.tabs(["Perfil de Pressão", "Linhas de Energia"])
    with tab1:
        fig = plotar_perfil_pressao(sim_real)
        st.pyplot(fig)
        plt_close(fig)
    with tab2:
        fig = plotar_linhas_energia(sim_real)
        st.pyplot(fig)
        plt_close(fig)


def exemplo_2_curva_calibracao():
    st.markdown('<div style="color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Exemplo 2: Curva de Calibração do Medidor</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo gera uma <strong>curva de calibração</strong> relacionando a vazão volumétrica (Q) 
    com o desnível manométrico (Δh) para um medidor de Venturi específico.
    </div>
    """, unsafe_allow_html=True)
    
    sim = VenturiSimulator()
    vazoes = np.linspace(0.005, 0.030, 20)
    desniveis = []
    pressoes = []
    reynolds = []
    with st.spinner('Gerando curva de calibração...'):
        for q in vazoes:
            sim.calcular(0.10, 0.05, 1.0, 1000, 13600, q, 0, 0.02, 0.97, 'Realista')
            desniveis.append(sim.delta_h * 100)
            pressoes.append(sim.delta_P / 1000)
            reynolds.append(sim.calcular_reynolds())
    
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Resumo da Calibração</div>', unsafe_allow_html=True)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Faixa de Vazão", f"{vazoes[0]*1000:.1f} - {vazoes[-1]*1000:.1f} L/s")
    with col2:
        st.metric("Faixa de Desnível", f"{desniveis[0]:.2f} - {desniveis[-1]:.2f} cm")
    with col3:
        st.metric("Faixa de ΔP", f"{pressoes[0]:.2f} - {pressoes[-1]:.2f} kPa")
    
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
    
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Curva de Calibração</div>', unsafe_allow_html=True)
    import matplotlib.pyplot as plt
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
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">🔬 Exemplo 3: Modo Medidor - Calcular Vazão a partir de Δh</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo demonstra o uso <strong>prático</strong> do medidor de Venturi: 
    medir o desnível manométrico (Δh) e calcular a vazão (Q) correspondente.
    </div>
    """, unsafe_allow_html=True)
    
    sim = VenturiSimulator()
    desniveis = [0.05, 0.10, 0.15, 0.20, 0.25]
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
    
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Relação Q = f(√Δh)</div>', unsafe_allow_html=True)
    import matplotlib.pyplot as plt
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 5))
    ax1.set_facecolor('white')
    ax1.plot(df['Δh (cm)'], df['Q (L/s)'], 'o-', color='#ef4444', linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax1.set_xlabel('Desnível Manométrico Δh (cm)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_ylabel('Vazão Q (L/s)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_title('Vazão vs Desnível', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax2.set_facecolor('white')
    ax2.plot(np.sqrt(df['Δh (cm)']), df['Q (L/s)'], 'o-', color='#2563eb', linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax2.set_xlabel('√(Δh) [√cm]', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_ylabel('Vazão Q (L/s)', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_title('Vazão vs √Desnível (Relação Linear)', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    💡 <strong>Observação Importante:</strong><br>
    • A vazão é proporcional à raiz quadrada do desnível: <strong>Q ∝ √(Δh)</strong><br>
    • Dobrando Δh, a vazão aumenta por um fator de √2 ≈ 1.41<br>
    • O gráfico Q vs √(Δh) é aproximadamente linear
    </div>
    """, unsafe_allow_html=True)


def exemplo_4_sensibilidade_cd():
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">⚙️ Exemplo 4: Sensibilidade ao Coeficiente de Descarga (Cd)</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo analisa como o <strong>coeficiente de descarga (Cd)</strong> afeta as medições de vazão.
    O Cd leva em conta perdas e efeitos não ideais no escoamento.
    </div>
    """, unsafe_allow_html=True)
    
    sim = VenturiSimulator()
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
        resultados.append({'Cd': cd, 'Q (L/s)': sim.Q * 1000, 'Variação (%)': variacao, 'ΔP (kPa)': sim.delta_P / 1000})
    
    st.markdown("### 📋 Efeito de Cd na Vazão (Δh fixo = 15 cm)")
    import pandas as pd
    df = pd.DataFrame(resultados)
    st.dataframe(df.style.format({'Cd': '{:.2f}', 'Q (L/s)': '{:.3f}', 'Variação (%)': '{:.2f}', 'ΔP (kPa)': '{:.3f}'}), width='stretch')
    
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
    
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Visualização do Efeito de Cd</div>', unsafe_allow_html=True)
    import matplotlib.pyplot as plt
    fig, ax = plt.subplots(figsize=(10, 6), facecolor='white')
    ax.set_facecolor('white')
    ax.plot(df['Cd'], df['Q (L/s)'], 'o-', color='#10b981', linewidth=2.5, markersize=8, markeredgecolor='white', markeredgewidth=2)
    ax.set_xlabel('Coeficiente de Descarga (Cd)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_ylabel('Vazão Q (L/s)', fontsize=12, fontweight='bold', color='#000000')
    ax.set_title('Sensibilidade da Vazão ao Coeficiente Cd', fontsize=14, fontweight='bold', color='#000000', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.axhline(y=vazao_min, color='#ef4444', linestyle='--', alpha=0.5, linewidth=1.5, label=f'Q mín = {vazao_min:.3f} L/s')
    ax.axhline(y=vazao_max, color='#10b981', linestyle='--', alpha=0.5, linewidth=1.5, label=f'Q máx = {vazao_max:.3f} L/s')
    ax.legend(frameon=True, fancybox=True, shadow=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    st.markdown(f"""
    <div style=\"background: #fffbeb; color: #000000; border-left: 4px solid #f59e0b; padding: 1rem; border-radius: 8px; margin: 1rem 0;\">
    ⚠️ <strong>IMPORTANTE:</strong><br>
    • Uma variação de 10% em Cd causa <strong>{variacao_total:.1f}%</strong> de variação na vazão!<br>
    • É crucial ter um Cd preciso para medições confiáveis<br>
    • O Cd típico para Venturi varia entre 0.95 e 0.98<br>
    • O Cd depende do número de Reynolds e da geometria do medidor
    </div>
    """, unsafe_allow_html=True)


def exemplo_5_reynolds():
    """Exemplo 5: Análise de Número de Reynolds e Regimes de Escoamento"""
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">🌊 Exemplo 5: Análise de Número de Reynolds</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    Este exemplo analisa o <strong>número de Reynolds</strong> e seus efeitos no comportamento do medidor de Venturi.
    O número de Reynolds determina o regime de escoamento (laminar, transição ou turbulento) e influencia 
    diretamente o coeficiente de descarga (Cd) e a precisão das medições.
    </div>
    """, unsafe_allow_html=True)
    
    # Parâmetros fixos
    D1 = 0.10  # m
    D2 = 0.05  # m
    
    # Faixa de vazões para cobrir diferentes regimes
    vazoes = np.linspace(0.001, 0.030, 30)  # m³/s
    resultados = []
    
    with st.spinner('Calculando número de Reynolds para diferentes vazões...'):
        for q in vazoes:
            sim = VenturiSimulator()
            sim.calcular(D1, D2, 1.0, 1000, 13600, q, 0, 0.02, 0.97, 'Realista')
            Re = sim.calcular_reynolds()
            
            # Determinar regime
            if Re < 2300:
                regime = "Laminar"
                cor_regime = "#f59e0b"
            elif Re < 4000:
                regime = "Transição"
                cor_regime = "#2563eb"
            else:
                regime = "Turbulento"
                cor_regime = "#10b981"
            
            # Cd aproximado baseado em Reynolds (simplificado)
            if Re < 2000:
                cd_estimado = 0.92
            elif Re < 10000:
                cd_estimado = 0.94 + (Re - 2000) / 8000 * 0.03
            else:
                cd_estimado = 0.97
            
            resultados.append({
                'Q (L/s)': q * 1000,
                'v₁ (m/s)': sim.v1,
                'Re': Re,
                'Regime': regime,
                'Cd estimado': cd_estimado,
                'Δh (cm)': sim.delta_h * 100
            })
    
    import pandas as pd
    df = pd.DataFrame(resultados)
    
    # Estatísticas por regime
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 1.5rem 0 1rem 0; font-weight: 600;">📊 Distribuição dos Regimes de Escoamento</div>', unsafe_allow_html=True)
    
    laminar_count = len(df[df['Re'] < 2300])
    transicao_count = len(df[(df['Re'] >= 2300) & (df['Re'] < 4000)])
    turbulento_count = len(df[df['Re'] >= 4000])
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total de Pontos", len(df))
    with col2:
        st.metric("Laminar (Re < 2300)", laminar_count, delta=None)
    with col3:
        st.metric("Transição (2300-4000)", transicao_count, delta=None)
    with col4:
        st.metric("Turbulento (Re > 4000)", turbulento_count, delta=None)
    
    # Tabela resumida
    st.markdown("---")
    st.markdown("### 📋 Tabela de Resultados (Amostra)")
    
    # Mostrar apenas alguns pontos representativos
    indices_amostra = [0, len(df)//4, len(df)//2, 3*len(df)//4, len(df)-1]
    df_amostra = df.iloc[indices_amostra].copy()
    
    styled_df = df_amostra.style.format({
        'Q (L/s)': '{:.3f}',
        'v₁ (m/s)': '{:.3f}',
        'Re': '{:,.0f}',
        'Cd estimado': '{:.3f}',
        'Δh (cm)': '{:.2f}'
    })
    
    st.dataframe(styled_df, width='stretch')
    
    # Gráficos
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📈 Visualizações do Número de Reynolds</div>', unsafe_allow_html=True)
    
    import matplotlib.pyplot as plt
    
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(14, 10))
    
    # Gráfico 1: Re vs Q
    ax1.set_facecolor('white')
    cores = ['#f59e0b' if r < 2300 else ('#2563eb' if r < 4000 else '#10b981') 
             for r in df['Re']]
    ax1.scatter(df['Q (L/s)'], df['Re'], c=cores, s=50, alpha=0.7, edgecolors='white', linewidth=1)
    ax1.axhline(y=2300, color='#f59e0b', linestyle='--', linewidth=2, label='Re = 2300 (Laminar/Turbulento)')
    ax1.axhline(y=4000, color='#2563eb', linestyle='--', linewidth=2, label='Re = 4000 (Transição/Turbulento)')
    ax1.axhline(y=10000, color='#10b981', linestyle=':', linewidth=1.5, label='Re = 10⁴ (Recomendado mínimo)')
    ax1.set_xlabel('Vazão Q (L/s)', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_ylabel('Número de Reynolds', fontsize=11, fontweight='bold', color='#000000')
    ax1.set_title('Número de Reynolds vs Vazão', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax1.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax1.legend(frameon=True, fancybox=True, shadow=True, fontsize=9)
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    
    # Gráfico 2: Re vs v₁
    ax2.set_facecolor('white')
    ax2.scatter(df['v₁ (m/s)'], df['Re'], c=cores, s=50, alpha=0.7, edgecolors='white', linewidth=1)
    ax2.axhline(y=2300, color='#f59e0b', linestyle='--', linewidth=2)
    ax2.axhline(y=4000, color='#2563eb', linestyle='--', linewidth=2)
    ax2.axhline(y=10000, color='#10b981', linestyle=':', linewidth=1.5)
    ax2.set_xlabel('Velocidade v₁ (m/s)', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_ylabel('Número de Reynolds', fontsize=11, fontweight='bold', color='#000000')
    ax2.set_title('Número de Reynolds vs Velocidade', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax2.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax2.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    
    # Gráfico 3: Cd estimado vs Re
    ax3.set_facecolor('white')
    ax3.plot(df['Re'], df['Cd estimado'], 'o-', color='#8b5cf6', linewidth=2, markersize=5, alpha=0.7)
    ax3.axvline(x=2300, color='#f59e0b', linestyle='--', linewidth=1.5, alpha=0.5)
    ax3.axvline(x=4000, color='#2563eb', linestyle='--', linewidth=1.5, alpha=0.5)
    ax3.axvline(x=10000, color='#10b981', linestyle=':', linewidth=1.5, alpha=0.7)
    ax3.set_xlabel('Número de Reynolds', fontsize=11, fontweight='bold', color='#000000')
    ax3.set_ylabel('Coeficiente de Descarga (Cd)', fontsize=11, fontweight='bold', color='#000000')
    ax3.set_title('Cd Estimado vs Número de Reynolds', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax3.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax3.set_ylim([0.90, 1.00])
    ax3.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    
    # Gráfico 4: Distribuição de regimes
    ax4.set_facecolor('white')
    regimes_count = [laminar_count, transicao_count, turbulento_count]
    labels = ['Laminar\n(Re < 2300)', 'Transição\n(2300-4000)', 'Turbulento\n(Re > 4000)']
    cores_barras = ['#f59e0b', '#2563eb', '#10b981']
    bars = ax4.bar(labels, regimes_count, color=cores_barras, alpha=0.7, edgecolor='white', linewidth=2)
    ax4.set_ylabel('Número de Pontos', fontsize=11, fontweight='bold', color='#000000')
    ax4.set_title('Distribuição dos Regimes de Escoamento', fontsize=12, fontweight='bold', color='#000000', pad=15)
    ax4.grid(True, alpha=0.2, linestyle='--', linewidth=1, axis='y')
    for i, (bar, count) in enumerate(zip(bars, regimes_count)):
        ax4.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                str(count), ha='center', va='bottom', fontweight='bold', fontsize=11)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)
    
    # Análise e conclusões
    st.markdown("---")
    st.markdown('<div style="background: linear-gradient(90deg, #2563eb 0%, #0ea5e9 100%); color: white; padding: 1rem 1.5rem; border-radius: 8px; margin: 0 0 1rem 0; font-weight: 600;">📊 Análise e Conclusões</div>', unsafe_allow_html=True)
    
    re_min = df['Re'].min()
    re_max = df['Re'].max()
    re_medio = df['Re'].mean()
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Re Mínimo", f"{re_min:,.0f}")
    with col2:
        st.metric("Re Médio", f"{re_medio:,.0f}")
    with col3:
        st.metric("Re Máximo", f"{re_max:,.0f}")
    
    st.markdown("""
    <div style="background: #eff6ff; color: #000000; border-left: 4px solid #2563eb; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
    <strong>Observações Importantes:</strong><br><br>
    
    • <strong>Regime Laminar (Re < 2300):</strong><br>
      &nbsp;&nbsp;⚠️ Baixas vazões resultam em escoamento laminar<br>
      &nbsp;&nbsp;⚠️ Cd menor e menos estável<br>
      &nbsp;&nbsp;⚠️ Não recomendado para medidores de vazão<br><br>
    
    • <strong>Regime de Transição (2300 < Re < 4000):</strong><br>
      &nbsp;&nbsp;🔄 Comportamento instável e imprevisível<br>
      &nbsp;&nbsp;🔄 Cd varia significativamente<br>
      &nbsp;&nbsp;🔄 Evitar esta faixa em aplicações práticas<br><br>
    
    • <strong>Regime Turbulento (Re > 4000):</strong><br>
      &nbsp;&nbsp;✅ Comportamento estável e previsível<br>
      &nbsp;&nbsp;✅ Cd mais alto e constante<br>
      &nbsp;&nbsp;✅ Recomendado para medidores de vazão<br><br>
    
    • <strong>Recomendação ISO 5167:</strong> Re > 2×10⁴ para medidores calibrados<br>
    • <strong>Prática Industrial:</strong> Re > 10⁴ é geralmente desejável<br>
    • <strong>Cd aumenta com Re</strong> até estabilizar para Re > 10⁵
    </div>
    """, unsafe_allow_html=True)


def plt_close(fig):
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass


