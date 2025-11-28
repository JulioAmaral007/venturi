import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from thermo import Chemical, Mixture
import warnings
warnings.filterwarnings('ignore')
from app_modules.simulator import VenturiSimulator
from app_modules.plots import (
    plotar_diagrama_venturi,
    plotar_perfil_pressao,
    plotar_linhas_energia,
)


st.set_page_config(
    page_title="Simulador de Venturi",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    st.sidebar.header("⚙️ Parâmetros de Controle")
    st.sidebar.info(
        "Preencha os dados na ordem sugerida para gerar resultados mais consistentes.",
        icon="🧭"
    )   

    st.title("🔬 Simulador Interativo de Medidor de Venturi")
    st.caption("Configure os parâmetros, visualize o comportamento hidráulico e compare modos de operação.")
    st.write("")

    with st.sidebar.container():
        st.sidebar.subheader("⚗️ Tipo de Simulação")
        mode = st.sidebar.radio(
            "Selecione o cenário:",
            options=['Ideal', 'Realista'],
            help="Ideal: sem perdas | Realista: com perdas"
        )
    
    st.sidebar.markdown("---")

    with st.sidebar.container():
        st.sidebar.subheader("📐 Geometria do Venturi")
        D1 = st.sidebar.slider(
            "D₁ - Diâmetro de entrada (m)",
            0.05, 0.30, 0.10, 0.01,
            help="Defina o diâmetro do trecho de entrada do Venturi."
        )
        D2 = st.sidebar.slider(
            "D₂ - Diâmetro da garganta (m)",
            0.02, 0.15, 0.05, 0.01,
            help="A garganta precisa ser menor para acelerar o escoamento."
        )
        beta = D2/D1
        L = st.sidebar.slider(
            "L - Comprimento da garganta (m)",
            0.5, 3.0, 1.0, 0.1,
            help="Comprimento da garganta do equipamento considerado na análise."
        )
        st.sidebar.info(f"B: {beta:.2e}")
    
    st.sidebar.markdown("---")

    with st.sidebar.expander("💧 Propriedades dos Fluidos", expanded=True):
        p1_input = st.sidebar.number_input(
            "Pressão de Entrada P₁ (Pa manométricos)", 
            value=0.0, 
            step=1000.0,
            help="Pressão estática no início do tubo. Use 0 para pressão atmosférica."
        )

        pressao_absoluta_para_thermo = p1_input + 101325.0

        lista_fluidos = {
            "Água": "water",
            "Ar": "air",
            "Etanol": "ethanol",
            "Glicerina": "glycerol",
            "Óleo de Motor (n-Octano)": "n-octane" 
        }
        nome_selecionado = st.sidebar.selectbox("Selecione o Fluido:", list(lista_fluidos.keys()))
        fluido_quimico = lista_fluidos[nome_selecionado]

        temp_c = st.sidebar.slider("Temperatura (°C)", 0, 100, 20)
        temp_k = temp_c + 273.15

        if fluido_quimico == 'air':
            fluido = Mixture('air', T=temp_k, P=pressao_absoluta_para_thermo)
        else:
            fluido = Chemical(fluido_quimico, T=temp_k, P=pressao_absoluta_para_thermo)

        rho = fluido.rho  
        mu = fluido.mu   

        if rho is None or mu is None:
            st.sidebar.error("⚠️ Erro: Não foi possível calcular as propriedades para esta temperatura. Tente aumentar a temperatura.")
            st.stop() 

        rho_m = st.slider(
            "ρₘ - Densidade do fluido manométrico (kg/m³)",
            10000, 15000, 13600, 100,
            help="Use 13600 kg/m³ para mercúrio ou ajuste conforme o manômetro."
        )

        st.sidebar.info(f"ρ: {rho:.1f} kg/m³ | μ: {mu:.2e} Pa.s")
    
    st.sidebar.markdown("---")
    
    with st.sidebar.container():
        st.sidebar.subheader("🌊 Condições de Escoamento")
        if mode == 'Medidor':
            st.sidebar.caption("Informe o desnível observado no manômetro para estimar a vazão.")
            delta_h = st.sidebar.slider(
                "Δh - Desnível manométrico (m)",
                0.01, 0.5, 0.1, 0.01,
                help="Valor medido diretamente no manômetro diferencial."
            )
            Q = None  
        else:
            st.sidebar.caption("Informe a vazão desejada para que o simulador calcule o desnível.")
            Q = st.sidebar.slider(
                "Q - Vazão volumétrica (m³/s)",
                0.001, 0.05, 0.01, 0.001,
                help="Ajuste conforme o regime de operação que deseja analisar."
            )
            delta_h = None 
    
    st.sidebar.markdown("---")
    
    with st.sidebar.expander("🔧 Ajustes Finos", expanded=False):
        st.caption("Use apenas se quiser avaliar perdas e calibração com mais detalhe.")
        f = st.slider(
            "f - Coeficiente de atrito",
            0.01, 0.10, 0.02, 0.005,
            help="Relaciona-se às perdas distribuídas no tubo."
        )
        Cd = st.slider(
            "Cd - Coeficiente de descarga",
            0.90, 1.00, 0.98, 0.01,
            help="Coeficiente experimental que ajusta a vazão real."
        )

    beta = D2/D1

    if D2 >= D1 or (beta<0.3) or (beta>0.75):
        st.error("⚠️ Ajuste necessário: D₂ precisa ser menor que D₁ para garantir aceleração do escoamento.")
        st.stop()
    
    sim = VenturiSimulator()
    sim.calcular(D1, D2, L, rho, rho_m, Q if Q else 0, delta_h if delta_h else 0, f, Cd, mode, mu, p1_input)
    
    resumo_container = st.container()
    with resumo_container:
        st.header("📊 Resumo Instantâneo")
        st.caption("Confira os valores principais antes de explorar os gráficos.")
        st.write("")
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Vazão Q", f"{sim.Q*1000:.2f} L/s", f"{sim.Q*3600:.1f} m³/h")
        with col2:
            st.metric("Desnível Δh", f"{sim.delta_h*100:.2f} cm", f"{sim.delta_h:.4f} m")
        with col3:
            st.metric("Velocidade v₁", f"{sim.v1:.3f} m/s")
        with col4:
            st.metric("Velocidade v₂", f"{sim.v2:.3f} m/s")
    
    st.write("")
    st.markdown("---")
    st.write("")
 
    st.subheader("Visualize o comportamento do escoamento")
    st.caption("Explore diagramas, manômetros e curvas de energia em abas organizadas.")
    st.write("")
    tab1, tab2, tab3, tab4 = st.tabs([
        "📐 Diagrama", "📈 Pressão", "⚡ Energia", "📋 Resultados Completos"
    ])
    
    with tab1:
        st.subheader("Diagrama Esquemático do Venturi")
        st.info("Observe a geometria e a distribuição dos diâmetros definidos na barra lateral.", icon="📌")
        fig = plotar_diagrama_venturi(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    
    with tab2:
        st.subheader("Perfil de Pressão ao Longo do Tubo")
        st.info("O perfil mostra como a pressão varia entre P₁ e P₂ conforme a seção se estreita.", icon="🧵")
        fig = plotar_perfil_pressao(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab3:
        st.subheader("Linhas de Energia e Piezométrica")
        st.info("Compare energia disponível e perdas ao longo do Venturi.", icon="⚡")
        fig = plotar_linhas_energia(sim)
        st.pyplot(fig)
        plt.close(fig)
    
    with tab4:
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
        
        st.markdown("---")

        if Re < 2300:
            st.warning("Regime LAMINAR (Re < 2300): medições tendem a ser menos sensíveis.", icon="⚠️")
        elif Re < 4000:
            st.info("Regime de TRANSIÇÃO (2300 < Re < 4000): condições intermediárias, atenção aos parâmetros.", icon="🔄")
        else:
            st.success("Regime TURBULENTO (Re > 4000): operação típica para Venturi industriais.", icon="✅")
    
    st.write("")
    st.divider()
    st.caption(f"🔬 Simulador de Medidor de Venturi • Modo atual: {mode}")


if __name__ == "__main__":
    main()

