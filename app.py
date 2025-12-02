import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

from thermo import Chemical, Mixture
import warnings
from pathlib import Path
from fluids.friction import friction_factor
try:
    from fluids.core import roughness_Farshad
except ImportError:
    # Fallback se a função não estiver disponível
    def roughness_Farshad(material):
        # Valores padrão da biblioteca fluids
        materials_db = {
            "Steel, commercial": 0.000045,
            "Cast iron": 0.00026,
            "Brass": 0.0000015,
            "Copper": 0.0000015,
            "PVC": 0.00000015
        }
        return materials_db.get(material, 0.000045)
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
    initial_sidebar_state="collapsed"
)



def render_sistema_tubulacoes():
    """Renderiza a seção de teoria e metodologia"""
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
        **Coeficientes K típicos usados no simulador:**
        
        - Curva 15°: K = 0.04
        
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
        
        1. **Escolha o modo de operação** (Ideal ou Realista) e selecione o fluido.
        
        2. **Defina os parâmetros geométricos** (D₁, D₂ e L) na seção "Geometria".
        
        3. **Configure as condições de escoamento** escolhendo uma das três opções disponíveis:
           - **Vazão volumétrica**: defina diretamente a vazão Q
           - **Velocidade na entrada (v₁)**: defina a velocidade na seção de entrada
           - **Velocidade na garganta (v₂)**: defina a velocidade na seção mais estreita
        
        4. **Refine parâmetros avançados** (material do tubo) quando quiser estudar efeitos de atrito no modo Realista.
        
        5. **Analise as métricas principais** exibidas logo após os parâmetros
        """)


def render_sobre_projeto():
    """Renderiza o conteúdo da aba Sobre o Projeto"""
    st.header("Sobre o Projeto")
    
    try:
        project_root = Path(__file__).parent
        venturi_image = project_root / "assets" / "venturi.jpeg"
        
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
    entrada e estrangulamento. Essa diferença, combinada com a **razão entre diâmetros** $\\beta$, permite calcular a vazão
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
    - Modo **Ideal** e **Realista**, com seleção direta na interface.
    - Ajuste manual da densidade do fluido manométrico.
    
    #### Simulação do Venturi
    
    - Sliders para definir D₁, D₂ e comprimento total.
    - Três opções para definir as condições de escoamento:
      - Vazão volumétrica (Q)
      - Velocidade na entrada (v₁)
      - Velocidade na garganta (v₂)
    - Parâmetros avançados: material do tubo (para cálculo automático do coeficiente de atrito no modo Realista).
    - Indicadores automáticos de razão entre diâmetros, número de Reynolds e regime de escoamento.
    - Visualizações: diagrama esquemático, perfil de pressão e linhas de energia.
    
    ### 📊 Métodos de Cálculo
    """)
    
    st.markdown("#### Continuidade")
    st.latex(r"Q = A_1 V_1 = A_2 V_2")
    
    st.markdown("#### Número de Reynolds")
    st.latex(r"Re = \frac{\rho V D}{\mu}")
    
    st.markdown("#### Equação da Energia (Bernoulli Estendida)")
    st.latex(r"\frac{P_1}{\rho g} + \frac{V_1^2}{2g} + z_1 = \frac{P_3}{\rho g} + \frac{V_3^2}{2g} + z_3 + h_{L,total}")
    
    st.markdown("#### Perdas de Carga (Modo Realista)")
    st.markdown("A perda de carga total é a soma das perdas nos três componentes do medidor:")
    st.latex(r"h_{L,total} = h_{entrada} + h_{garganta} + h_{difusor}")
    
    st.markdown("**1. Perda na Entrada (Bocal):**")
    st.caption("Perda localizada devido à contração suave (K ≈ 0.04).")
    st.latex(r"h_{entrada} = 0,04 \frac{V_{garganta}^2}{2g}")

    st.markdown("**2. Perda na Garganta (Atrito):**")
    st.caption("Perda distribuída no trecho reto usando a equação de Darcy-Weisbach.")
    st.latex(r"h_{garganta} = f \frac{L_{garganta}}{D_{garganta}} \frac{V_{garganta}^2}{2g}")

    st.markdown("**3. Perda no Difusor (Saída):**")
    st.caption("Baseada na eficiência de recuperação de pressão ($C_p$) para difusores cônicos (Fox & McDonald).")
    st.latex(r"C_{p,ideal} = 1 - \frac{1}{AR^2} \quad \text{onde } AR = \left(\frac{D_{saida}}{D_{garganta}}\right)^2")
    st.latex(r"h_{difusor} = (C_{p,ideal} - C_{p,real}) \frac{V_{garganta}^2}{2g}")
    
    st.markdown("#### Relação Manométrica")
    st.latex(r"\Delta P = (\rho_m - \rho) g \Delta h")
    
    st.markdown("""
    ### 🛠️ Tecnologias
    
    - **Streamlit** para a interface.
    - **NumPy/Pandas** no processamento numérico.
    - **Matplotlib** nas visualizações customizadas.
    
    ### 💡 Dicas de Uso
    
    1. Ajuste a **razão entre diâmetros** dentro da faixa recomendada (1 a 2).
    2. Utilize o modo Realista para avaliar efeitos de atrito e recuperação de pressão incompleta.
    3. Varie os parâmetros de entrada para analisar diferentes cenários de escoamento.
    """)


def obter_rugosidade_material(material):
    """
    Retorna a rugosidade absoluta (em metros) do material.
    
    Args:
        material: Nome do material
    
    Returns:
        epsilon: Rugosidade absoluta (m)
    """
    try:
        epsilon = roughness_Farshad(material)
        return epsilon
    except:
        materials_db = {
            "Steel, commercial": 0.000045,
            "Cast iron": 0.00026,
            "Brass": 0.0000015,
            "Copper": 0.0000015,
            "PVC": 0.00000015
        }
        return materials_db.get(material, 0.000045)


def calcular_fator_atrito(Re, epsilon, D):
    """
    Calcula o fator de atrito de Darcy.
    
    Args:
        Re: Número de Reynolds
        epsilon: Rugosidade absoluta (m)
        D: Diâmetro (m)
    
    Returns:
        f: Fator de atrito de Darcy
    """
    if Re < 2300:
        return 64.0 / Re if Re > 0 else 0.064
    
    rugosidade_relativa = epsilon / D
    
    try:
        f = friction_factor(Re=Re, eD=rugosidade_relativa)
        return max(0.008, min(0.1, f))
    except:
        try:
            f0 = 0.25 / (np.log10(rugosidade_relativa/3.7 + 5.74/(Re**0.9)))**2
            return max(0.008, min(0.1, f0))
        except:
            return 0.02


def render_graph_explanation(description: str):
    """Renderiza expander com diretrizes de interpretação do gráfico atual."""
    st.markdown("##### Explicação do gráfico")
    with st.expander("ℹ️ Como interpretar este gráfico", expanded=False):
        st.markdown(description)


# ========== INTERFACE STREAMLIT ==========

def main():
    # Título principal
    st.markdown("""
    <div style="background: linear-gradient(135deg, #2563eb 0%, #0ea5e9 100%); padding: 2rem; border-radius: 12px; margin-bottom: 2rem; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);">
        <h1 style="color: white; margin: 0; font-size: 2rem; font-weight: 700;">🔬 Simulador Interativo de Medidor de Venturi</h1>
        <p style="color: rgba(255, 255, 0, 1); margin: 0.5rem 0 0 0; font-size: 1.1rem;">Ferramenta avançada para análise de escoamento em medidores de Venturi</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Seção teórica antes dos parâmetros
    render_sistema_tubulacoes()
    
    st.markdown("---")
    st.markdown("### ⚙️ Configuração dos Parâmetros")
    
    # Tipo de simulação
    mode = st.radio(
        "🔬 Tipo de Simulação:",
        options=['Ideal', 'Realista'],
        help="Ideal: sem perdas | Realista: com perdas",
        horizontal=True
    )
    
    st.markdown("")
    
    # Organizar parâmetros em colunas
    col1, col2 = st.columns(2)
    
    with col1:
        # Parâmetros geométricos
        with st.expander("📐 Geometria", expanded=True):
            D1 = st.slider(
                "D₁ - Diâmetro de entrada (m)",
                min_value=0.05,
                max_value=0.30,
                value=0.10,
                step=0.01,
                help="Diâmetro da seção de entrada do Venturi"
            )
            
            D2 = st.slider(
                "D₂ - Diâmetro da garganta (m)",
                min_value=0.02,
                max_value=0.15,
                value=0.05,
                step=0.01,
                help="Diâmetro da seção mais estreita (garganta)"
            )
            
            # Mostrar razão entre diâmetros
            razao_diametros = D1 / D2
            st.info(f"D₁/D₂ = {razao_diametros:.3f}")
            
            L = st.slider(
                "L - Comprimento da garganta (m)",
                min_value=0.1,
                max_value=3.0,
                value=1.0,
                step=0.1,
                help="Comprimento da garganta do Venturi"
            )
        
        # Propriedades dos fluidos
        with st.expander("💧 Fluido", expanded=True):
            lista_fluidos = {
                "Água": "water",
                "Ar": "air",
                "Etanol": "ethanol",
                "Glicerina": "glycerol",
                "Óleo de Motor (n-Octano)": "n-octane"
            }
            
            fluid_name = st.selectbox(
                "Selecione o Fluido:",
                options=list(lista_fluidos.keys()),
                help="Escolha o fluido para a simulação"
            )
            
            fluido_quimico = lista_fluidos[fluid_name]
            
            p1_input = st.number_input(
                "Pressão de Entrada P₁ (Pa manométricos)",
                value=0.0,
                step=1000.0,
                help="Pressão estática no início do tubo. Use 0 para pressão atmosférica."
            )
            
            pressao_absoluta_para_thermo = p1_input + 101325.0
            
            temp_c = st.slider("Temperatura (°C)", 0, 100, 20)
            temp_k = temp_c + 273.15
            
            if fluido_quimico == 'air':
                fluido = Mixture('air', T=temp_k, P=pressao_absoluta_para_thermo)
            else:
                fluido = Chemical(fluido_quimico, T=temp_k, P=pressao_absoluta_para_thermo)
            
            rho = fluido.rho
            mu = fluido.mu
            
            if rho is None or mu is None:
                st.error("⚠️ Erro: Não foi possível calcular as propriedades para esta temperatura. Tente aumentar a temperatura.")
                st.stop()
            
            st.metric("Densidade ρ", f"{rho:.1f} kg/m³")
            st.metric("Viscosidade dinâmica μ", f"{mu:.2e} Pa·s")
            
            # Fluido manométrico (slider)
            st.markdown("**Fluido Manométrico**")
            rho_m = st.slider(
                "ρₘ - Densidade do fluido manométrico (kg/m³)",
                min_value=1000,
                max_value=20000,
                value=13600,
                step=100,
                help="Densidade do fluido utilizado no manômetro diferencial. Use 13600 kg/m³ para mercúrio."
            )
    
    with col2:
        # Condições de escoamento
        with st.expander("🌊 Condições de Escoamento", expanded=True):
            flow_input_mode = st.radio(
                "Variável de entrada",
                options=[
                    "Vazão volumétrica",
                    "Velocidade na entrada (v₁)",
                    "Velocidade na garganta (v₂)"
                ],
                index=0,
                help="Escolha como definir o escoamento"
            )
            
            area_entrada = np.pi * (D1 / 2) ** 2
            area_garganta = np.pi * (D2 / 2) ** 2
            
            if flow_input_mode == "Vazão volumétrica":
                Q = st.slider(
                    "Q - Vazão volumétrica (m³/s)",
                    min_value=0.001,
                    max_value=0.05,
                    value=0.01,
                    step=0.001,
                    format="%.4f",
                    help="Vazão volumétrica do fluido"
                )
            elif flow_input_mode == "Velocidade na entrada (v₁)":
                v1_input = st.slider(
                    "v₁ - Velocidade na entrada (m/s)",
                    min_value=0.5,
                    max_value=25.0,
                    value=5.0,
                    step=0.1,
                    format="%.2f",
                    help="Velocidade na seção de entrada"
                )
                Q = v1_input * area_entrada
                st.caption(f"Vazão equivalente: {Q:.4f} m³/s")
            else:
                v2_input = st.slider(
                    "v₂ - Velocidade na garganta (m/s)",
                    min_value=0.5,
                    max_value=35.0,
                    value=8.0,
                    step=0.1,
                    format="%.2f",
                    help="Velocidade na garganta"
                )
                Q = v2_input * area_garganta
                st.caption(f"Vazão equivalente: {Q:.4f} m³/s")
            
        # Parâmetros avançados
        with st.expander("⚙️ Parâmetros Avançados", expanded=True):
            # Dicionário de materiais (usado em ambos os modos)
            materiais_fluids = {
                "Steel, commercial": "Aço comercial",
                "Cast iron": "Ferro fundido",
                "Brass": "Latão",
                "Copper": "Cobre",
                "PVC": "PVC"
            }
            
            if mode == 'Realista':
                # Material do tubo para cálculo de rugosidade e atrito (apenas no modo Realista)
                material_tubo = st.selectbox(
                    "Material do Tubo",
                    options=list(materiais_fluids.keys()),
                    format_func=lambda x: materiais_fluids[x],
                    index=0,
                    help="Selecione o material do tubo para calcular automaticamente o coeficiente de atrito baseado na rugosidade (dados da biblioteca fluids). Apenas usado no modo Realista."
                )
                
                # Obter rugosidade do material usando a biblioteca fluids
                epsilon = obter_rugosidade_material(material_tubo)
                st.info(f"Rugosidade absoluta: ε = {epsilon*1000:.3f} mm")
            else:
                # No modo Ideal, o material não é usado (perdas = 0)
                material_tubo = "Steel, commercial"  # Valor padrão (não usado)
                epsilon = obter_rugosidade_material(material_tubo)
                st.info("ℹ️ No modo Ideal, as perdas são zero. O material do tubo não afeta os resultados.")
            
    # Validação com feedback visual
    razao_diametros = D1 / D2
    if D2 >= D1:
        st.error("⚠️ Ajuste necessário: D₂ precisa ser menor que D₁ para garantir aceleração do escoamento.")
        st.stop()
    elif razao_diametros < 1:
        st.error(f"⚠️ Ajuste necessário: Razão entre diâmetros está muito baixa, D₁/D₂ = {razao_diametros:.3f} (mínimo recomendado: 1.0). D₂ está maior que D₁.")
        st.stop()
    elif razao_diametros > 2:
        st.error(f"⚠️ Ajuste necessário: Razão entre os diâmetros está muito alta, D₁/D₂ = {razao_diametros:.3f} (máximo recomendado: 2.0). D₂ está muito pequeno em relação a D₁.")
        st.stop()
    elif rho_m < rho + rho*0.05: 
        st.error(f"⚠️ Ajuste necessário: Densidade do fluido manométrico ρₘ " f"{rho_m:.1f} kg/m³ menor ou muito próxima da densidade do fluido ρ " f"{rho:.1f} kg/m³.")
        st.stop()
    
    # Calcular número de Reynolds e fator de atrito baseado no material
    area_garganta_calc = np.pi * (D2 / 2) ** 2
    v2_calc = Q / area_garganta_calc if Q > 0 else 1.0
    Re_calc = (rho * v2_calc * D2) / mu if mu > 0 else 10000

    if mode == 'Realista' and Re_calc < 75000:
        st.error(f"⚠️ Ajuste necessário: Para melhor análise das perdas de carga, mantenha o regime como turbulento, Re > 75000.")
        st.stop()
    
    # Calcular fator de atrito usando a rugosidade do material selecionado
    epsilon = obter_rugosidade_material(material_tubo)
    f = calcular_fator_atrito(Re_calc, epsilon, D2)
    
    # Exibir informações sobre o cálculo do atrito
    with st.expander("ℹ️ Informações do Cálculo de Atrito", expanded=True):
        if mode == 'Realista':
            # Mapeamento de nomes para exibição
            nomes_materiais = {
                "Steel, commercial": "Aço comercial",
                "Cast iron": "Ferro fundido",
                "Brass": "Latão",
                "Copper": "Cobre",
                "PVC": "PVC"
            }
            st.write(f"**Material selecionado:** {nomes_materiais.get(material_tubo, material_tubo)}")
            st.write(f"**Rugosidade absoluta:** ε = {epsilon*1000:.3f} mm")
            st.write(f"**Rugosidade relativa:** ε/D = {epsilon/D1:.6f}")
            st.write(f"**Número de Reynolds:** Re = {Re_calc:.0f}")
            st.write(f"**Coeficiente de atrito calculado:** f = {f:.4f}")
            if Re_calc < 2300:
                st.caption("Regime laminar: f = 64/Re")
            elif Re_calc < 4000:
                st.caption("Regime de transição: Equação de Colebrook-White")
            else:
                st.caption("Regime turbulento: Equação de Colebrook-White")
        else:
            st.info("No modo Ideal, as perdas por atrito são zero. O fator de atrito não é utilizado nos cálculos.")
    
    # Criar simulador e calcular
    sim = VenturiSimulator()
    sim.calcular(D1, D2, L, rho, rho_m, Q, 0, f, mode, mu, p1_input)
    
    # ========== LAYOUT PRINCIPAL ==========
    
    # Métricas principais
    st.markdown("### 📊 Resultados Principais")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            "Vazão Q",
            f"{sim.Q:.4f} m³/s",
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
    if Re < 2300:
        st.warning(f"🟢 Regime LAMINAR (Re = {Re:.0f} < 2300): Movimento suave em camadas", icon="🟢")
    elif Re < 4000:
        st.info(f"🟡 Regime de TRANSIÇÃO (Re = {Re:.0f}): Zona intermediária", icon="🟡")
    else:
        st.success(f"🔴 Regime TURBULENTO (Re = {Re:.0f} > 4000): Movimento caótico com redemoinhos", icon="🔴")
    
    st.write("")
    st.markdown("---")
    st.write("")
    
    # Abas para organizar visualizações
    tab1, tab2, tab3 = st.tabs([
        "📐 Visão Geral",
        "📊 Dados Completos",
        "ℹ️ Sobre o Projeto"
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
        """)
        
        st.markdown("---")
        
        st.markdown("**Linhas de Energia e Piezométrica**")
        fig = plotar_linhas_energia(sim)
        st.pyplot(fig)
        plt.close(fig)
        render_graph_explanation("""
        **O que este gráfico mostra:**
        
        Balanço de energia ao longo do Venturi, representado por áreas empilhadas que mostram a distribuição entre energia de pressão, energia cinética e perda de carga.
        
        **Como interpretar:**
        
        - **Energia de Pressão (azul)**: Área inferior que representa a carga piezométrica (P/ρg). 
        - **Energia Cinética (verde)**: Área intermediária que representa V²/2g.
        - **Perda de Carga (vermelho claro)**: Área superior que representa a energia dissipada por atrito e turbulência.
        - **Perda Total**: Valor indicado no final do gráfico mostra a diferença entre a energia inicial e final.
        """)
    
    with tab2:
        st.subheader("Resultados Numéricos Completos")
        st.caption(f"Detalhe completo das propriedades calculadas - Modo: {mode}. Use para relatórios ou calibrações.")
        
        # Obter P2_fim (pode não existir em versões antigas, usar fallback)
        P2_fim = getattr(sim, 'P2_fim', sim.P2)
        P3 = getattr(sim, 'P3', sim.P1)
        
        col_a, col_b = st.columns(2)
        
        with col_a:
            st.markdown("**GEOMETRIA:**")
            st.write(f"• D₁ = {sim.D1:.3f} m")
            st.write(f"• D₂ = {sim.D2:.3f} m")
            st.write(f"• A₁ = {sim.A1:.6f} m²")
            st.write(f"• A₂ = {sim.A2:.6f} m²")
            st.write(f"• D₁/D₂ = {sim.D1/sim.D2:.3f}")
            st.write(f"• L (garganta) = {sim.L_garganta:.3f} m")
            if hasattr(sim, 'L_entrada') and hasattr(sim, 'L_saida'):
                st.write(f"• L (entrada) = {sim.L_entrada:.3f} m")
                st.write(f"• L (saída) = {sim.L_saida:.3f} m")
                st.write(f"• L (total) = {sim.L:.3f} m")                                                                
            
            st.markdown("")
            st.markdown("**PROPRIEDADES DO FLUIDO:**")
            st.write(f"• ρ (fluido) = {sim.rho:.0f} kg/m³")
            st.write(f"• μ (viscosidade) = {sim.mu:.2e} Pa·s")
            st.write(f"• ρₘ (manométrico) = {sim.rho_m:.0f} kg/m³")
            
            st.markdown("")
            st.markdown("**VELOCIDADES:**")
            st.write(f"• v₁ (entrada) = {sim.v1:.3f} m/s")
            st.write(f"• v₂ (garganta) = {sim.v2:.3f} m/s")
            st.write(f"• Razão v₂/v₁ = {sim.v2/sim.v1:.2f}")
        
        with col_b:
            st.markdown("**PRESSÕES (manométricas):**")
            st.write(f"• P₁ (entrada) = {sim.P1/1000:.2f} kPa")
            st.write(f"• P₂ (início garganta) = {sim.P2/1000:.2f} kPa")
            st.write(f"• P₂ (fim garganta) = {P2_fim/1000:.2f} kPa")
            st.write(f"• P₃ (saída) = {P3/1000:.2f} kPa")
            st.write(f"• ΔP (P₁ - P₂) = {sim.delta_P/1000:.3f} kPa")
            
            if mode == 'Realista':
                perda_garganta = sim.P2 - P2_fim
                if perda_garganta > 0:
                    st.write(f"• ΔP (perda na garganta) = {perda_garganta/1000:.3f} kPa")
                recuperacao = P3 - P2_fim
                if recuperacao > 0:
                    st.write(f"• ΔP (recuperação no difusor) = {recuperacao/1000:.3f} kPa")
            
            st.markdown("")
            st.markdown("**MEDIÇÕES E PARÂMETROS:**")
            st.write(f"• Vazão Q = {sim.Q:.4f} m³/s ({sim.Q*3600:.2f} m³/h)")
            st.write(f"• Δh (manômetro) = {sim.delta_h*100:.2f} cm ({sim.delta_h:.4f} m)")
            st.write(f"• Reynolds (Re) = {Re:.0f}")
            if mode == 'Realista':
                st.write(f"• Fator de atrito (f) = {sim.f:.4f}")
            
            st.markdown("")
            st.markdown("**ENERGIA:**")
            st.write(f"• Perda de carga total hₗ = {sim.h_L:.4f} m")
        
        # Informações específicas do modo
        st.markdown("---")
        st.markdown(f"**Informações do Modo {mode}:**")
        if mode == 'Ideal':
            st.info("""
            **Modo Ideal:**
            - Sem perdas por atrito (hₗ = 0)
            - P₂ (início) = P₂ (fim) na garganta (sem perdas)
            - P₃ = P₁ (recuperação total de pressão)
            - Ideal para comparação teórica e validação de cálculos
            """)
        else:
            st.info("""
            **Modo Realista:**
            - Considera perdas por atrito nas paredes
            - P₂ (fim) < P₂ (início) devido às perdas na garganta
            - P₃ < P₁ devido às perdas totais (entrada + garganta + difusor)
            - Mais próximo das condições reais de operação
            """)
    
    with tab3:
        render_sobre_projeto()
    
    # Melhorado: rodapé nativo e resumido
    st.write("")
    st.divider()
    st.caption(f"🔬 Simulador de Medidor de Venturi • Modo atual: {mode}")


if __name__ == "__main__":
    main()
