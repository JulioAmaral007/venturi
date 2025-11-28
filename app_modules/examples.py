import numpy as np
import streamlit as st
from .simulator import VenturiSimulator
from .plots import plotar_perfil_pressao, plotar_linhas_energia


def executar_exemplos():
    """Interface para executar os exemplos práticos do simulador."""
    # Título usando HTML (mantido para consistência visual)
    st.markdown('<div style="background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);"><h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">📚 Exemplos Práticos</h1><p style="color: rgba(255, 255, 0, 1); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Explore diferentes casos de uso do medidor de Venturi através de exemplos pré-configurados</p></div>', unsafe_allow_html=True)
    
    st.sidebar.markdown("---")
    st.sidebar.header("📋 Selecione o Exemplo")
    exemplo = st.sidebar.selectbox(
        "Escolha um cenário de estudo:",
        [
            "1. Comparação: Ideal vs Realista",
            "2. Curva de Calibração",
            "3. Modo Medidor (Δh → Q)",
            "4. Sensibilidade ao Cd",
            "5. Análise de Número de Reynolds"
        ],
        help="Cada opção destaca um aspecto específico do Venturi: perdas, calibração, medição, Cd ou regime de escoamento."
    )
    st.sidebar.markdown("---")
    st.sidebar.info(
        "💡 Dica: Use os exemplos como referência rápida antes de realizar suas próprias simulações.",
        icon="📎"
    )
    
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
    st.markdown("### 🔵🔴 Exemplo 1: Comparação Modo Ideal vs Modo Realista")
    st.info("""
    Este exemplo compara o comportamento do medidor de Venturi em duas condições:
    
    • **Modo Ideal**: Escoamento sem perdas (Cd = 1.0, sem atrito)
    • **Modo Realista**: Escoamento com perdas por atrito e coeficiente de descarga real
    """)
    
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
    
    st.write("")
    st.subheader("📈 Visualizações Comparativas")
    tab1, tab2 = st.tabs(["Perfil de Pressão", "Linhas de Energia"])
    with tab1:
        fig = plotar_perfil_pressao(sim_real)
        st.pyplot(fig)
        plt_close(fig)
    with tab2:
        fig = plotar_linhas_energia(sim_real)
        st.pyplot(fig)
        plt_close(fig)
    st.success("Conclusão: perdas elevam ΔP e Δh, reduzindo a energia disponível no modo realista.", icon="✅")


def exemplo_2_curva_calibracao():
    st.markdown("### 📈 Exemplo 2: Curva de Calibração do Medidor")
    st.info("""
    Este exemplo gera uma **curva de calibração** relacionando a vazão volumétrica (Q) 
    com o desnível manométrico (Δh) para um medidor de Venturi específico.
    """)
    
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
    
    st.markdown("#### 📊 Resumo da Calibração")
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
    st.markdown("#### 📈 Curva de Calibração")
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
    st.success("✅ A curva mostra a relação quadrática entre vazão e desnível: **Q ∝ √(Δh)**")


def exemplo_3_modo_medidor():
    # Melhorado: contexto rápido para quem usa o Venturi como instrumento
    st.header("🔬 Exemplo 3 · Modo Medidor (Δh → Q)")
    st.caption("Converta leituras de Δh em vazão e visualize a relação Q x √Δh.")
    st.write("")
    st.info(
        "Ideal para calibração em campo: escolha o Δh medido e confira instantaneamente a vazão correspondente.",
        icon="🧷"
    )
    with st.expander("Condições adotadas"):
        st.write("• D₁ = 0,10 m | D₂ = 0,05 m | Cd = 0,98 | f = 0,02")
        st.write("• Δh varia de 5 a 25 cm (incrementos de 5 cm)")
    
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
    st.subheader("📋 Resultados para Diferentes Desníveis")
    st.dataframe(df.style.format({
        'Δh (cm)': '{:.1f}',
        'Q (L/s)': '{:.2f}',
        'Q (m³/h)': '{:.2f}',
        'v₁ (m/s)': '{:.3f}',
        'v₂ (m/s)': '{:.3f}',
        'ΔP (kPa)': '{:.3f}'
    }), width='stretch')
    
    st.divider()
    st.subheader("📈 Relação Q = f(√Δh)")
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
    
    st.info(
        "Resumo: Q ∝ √Δh · Duplicar o desnível aumenta a vazão por √2 (~1,41) · O gráfico Q vs √Δh é quase linear.",
        icon="💡"
    )


def exemplo_4_sensibilidade_cd():
    # Melhorado: reforça a importância do Cd de forma clara
    st.header("⚙️ Exemplo 4 · Sensibilidade ao Coeficiente Cd")
    st.caption("Entenda quanto uma pequena alteração em Cd impacta a vazão.")
    st.write("")
    st.info(
        "Cd representa perdas e efeitos não ideais do Venturi. Variações nele alteram diretamente a vazão calculada.",
        icon="🧠"
    )
    with st.expander("Valores avaliados"):
        st.write("Cd de 0,90 a 1,00 (11 pontos) com Δh fixo em 15 cm.")
    
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
    
    st.subheader("📋 Efeito de Cd na Vazão (Δh = 15 cm)")
    import pandas as pd
    df = pd.DataFrame(resultados)
    st.dataframe(df.style.format({'Cd': '{:.2f}', 'Q (L/s)': '{:.3f}', 'Variação (%)': '{:.2f}', 'ΔP (kPa)': '{:.3f}'}), width='stretch')
    
    st.divider()
    st.subheader("📊 Análise Estatística")
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
    
    st.divider()
    st.subheader("📈 Visualização do Efeito de Cd")
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
    
    st.warning(
        f"Atenção: 10% de variação em Cd pode gerar {variacao_total:.1f}% de diferença em Q. "
        "Conheça o Cd do seu equipamento (normalmente 0,95–0,98) e acompanhe mudanças de regime.",
        icon="⚠️"
    )


def exemplo_5_reynolds():
    """Exemplo 5: Análise de Número de Reynolds e Regimes de Escoamento"""
    # Melhorado: explicação didática e uso de componentes nativos
    st.header("🌊 Exemplo 5 · Número de Reynolds e Regimes")
    st.caption("Identifique em qual regime seu Venturi opera e como isso afeta Cd.")
    st.write("")
    st.info(
        "Re < 2300 → laminar • 2300 < Re < 4000 → transição • Re > 4000 → turbulento. "
        "Use este painel para entender a influência da vazão no regime.",
        icon="🌐"
    )
    with st.expander("Configuração fixa do Venturi"):
        st.write("• D₁ = 0,10 m | D₂ = 0,05 m | Cd base = 0,97 | f = 0,02")
        st.write("• Vazões simuladas: 0,001 a 0,030 m³/s (30 pontos)")
    
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
    st.subheader("📊 Distribuição dos Regimes de Escoamento")
    
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
    st.divider()
    st.subheader("📋 Tabela de Resultados (Amostra)")
    
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
    st.divider()
    st.subheader("📈 Visualizações do Número de Reynolds")
    
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
    st.divider()
    st.subheader("📊 Análise e Conclusões")
    
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
    
    st.info(
        "Regime laminar (Re < 2300): Cd mais baixo e medições instáveis.\n"
        "Regime de transição (2300–4000): evite operar aqui, pois Cd varia bastante.\n"
        "Regime turbulento (Re > 4000): ideal para medição, com Cd estável.\n"
        "Referências: ISO 5167 recomenda Re > 2×10⁴ · prática industrial busca Re > 10⁴.",
        icon="ℹ️"
    )


def plt_close(fig):
    try:
        import matplotlib.pyplot as plt
        plt.close(fig)
    except Exception:
        pass


