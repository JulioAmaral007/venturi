"""
Componentes Reutilizáveis para a Interface do Simulador de Venturi
Fornece funções helper para criar elementos de UI consistentes e acessíveis.
"""

import streamlit as st
from typing import Optional, Union
from .constants import TOOLTIPS, ICONS, COLORS


def help_icon(key: str, tooltip_key: Optional[str] = None) -> str:
    """
    Retorna um ícone de ajuda com tooltip.
    
    Args:
        key: Chave única para o componente
        tooltip_key: Chave do tooltip em TOOLTIPS (se None, usa key)
    
    Returns:
        String formatada com ícone e tooltip
    """
    tooltip_text = TOOLTIPS.get(tooltip_key or key, '')
    if tooltip_text:
        return f" {ICONS['help']}"
    return ""


def metric_card(label: str, value: str, delta: Optional[str] = None, 
                help_text: Optional[str] = None, icon: Optional[str] = None):
    """
    Cria um card de métrica estilizado.
    
    Args:
        label: Rótulo da métrica
        value: Valor principal
        delta: Valor secundário ou variação
        help_text: Texto de ajuda (tooltip)
        icon: Ícone para exibir
    """
    display_label = f"{icon} {label}" if icon else label
    st.metric(
        label=display_label,
        value=value,
        delta=delta,
        help=help_text
    )


def parameter_slider(label: str, min_value: float, max_value: float, 
                     default_value: float, step: float, 
                     tooltip_key: Optional[str] = None,
                     key: Optional[str] = None,
                     format_str: str = "%.3f") -> float:
    """
    Cria um slider com label e tooltip integrados.
    
    Args:
        label: Rótulo do parâmetro
        min_value: Valor mínimo
        max_value: Valor máximo
        default_value: Valor padrão
        step: Incremento
        tooltip_key: Chave do tooltip em TOOLTIPS
        key: Chave única do componente
        format_str: Formato de exibição do valor
    
    Returns:
        Valor selecionado
    """
    help_text = TOOLTIPS.get(tooltip_key, None) if tooltip_key else None
    
    return st.slider(
        label=label,
        min_value=min_value,
        max_value=max_value,
        value=default_value,
        step=step,
        format=format_str,
        help=help_text,
        key=key
    )


def info_box(message: str, icon: str = "💡"):
    """Cria uma caixa de informação usando componente nativo."""
    st.info(f"{icon} {message}")


def warning_box(message: str, icon: str = "⚠️"):
    """Cria uma caixa de aviso usando componente nativo."""
    st.warning(f"{icon} {message}")


def success_box(message: str, icon: str = "✅"):
    """Cria uma caixa de sucesso usando componente nativo."""
    st.success(f"{icon} {message}")


def error_box(message: str, icon: str = "❌"):
    """Cria uma caixa de erro usando componente nativo."""
    st.error(f"{icon} {message}")


def section_header(title: str, icon: Optional[str] = None):
    """
    Cria um cabeçalho de seção consistente.
    
    Args:
        title: Título da seção
        icon: Ícone opcional
    """
    display_title = f"{icon} {title}" if icon else title
    st.markdown(f"### {display_title}")


def subsection_header(title: str, icon: Optional[str] = None):
    """
    Cria um subcabeçalho consistente.
    
    Args:
        title: Título da subseção
        icon: Ícone opcional
    """
    display_title = f"{icon} {title}" if icon else title
    st.markdown(f"#### {display_title}")


def create_expander(title: str, icon: Optional[str] = None, 
                    expanded: bool = False, help_text: Optional[str] = None):
    """
    Cria um expander estilizado.
    
    Args:
        title: Título do expander
        icon: Ícone opcional
        expanded: Se deve começar expandido
        help_text: Texto de ajuda
    
    Returns:
        Contexto do expander
    """
    display_title = f"{icon} {title}" if icon else title
    
    # Adicionar help text ao título se fornecido
    if help_text:
        display_title += f" {ICONS['help']}"
    
    return st.expander(display_title, expanded=expanded)


def display_beta_ratio(D1: float, D2: float):
    """
    Exibe a razão beta com indicador visual.
    
    Args:
        D1: Diâmetro de entrada
        D2: Diâmetro da garganta
    """
    beta = D2 / D1
    
    # Determinar se está na faixa recomendada
    if 0.4 <= beta <= 0.7:
        icon = "✅"
        color = "green"
    elif 0.3 <= beta < 0.4 or 0.7 < beta <= 0.8:
        icon = "⚠️"
        color = "orange"
    else:
        icon = "❌"
        color = "red"
    
    st.markdown(
        f"**β = D₂/D₁ = {beta:.3f}** {icon}",
        help=TOOLTIPS.get('beta', '')
    )


def display_reynolds_indicator(Re: float):
    """
    Exibe indicador do regime de escoamento baseado em Reynolds.
    
    Args:
        Re: Número de Reynolds
    """
    if Re < 2300:
        regime = "Laminar"
        icon = "⚠️"
        message = f"Regime **{regime}** (Re = {Re:,.0f})"
        st.warning(f"{icon} {message}", icon=icon)
    elif Re < 4000:
        regime = "Transição"
        icon = "🔄"
        message = f"Regime de **{regime}** (Re = {Re:,.0f})"
        st.info(f"{icon} {message}", icon=icon)
    else:
        regime = "Turbulento"
        icon = "✅"
        message = f"Regime **{regime}** (Re = {Re:,.0f})"
        st.success(f"{icon} {message}", icon=icon)


def fluid_preset_selector(key: str = "fluid_preset") -> str:
    """
    Cria um seletor de presets de fluidos.
    
    Args:
        key: Chave única do componente
    
    Returns:
        Nome do fluido selecionado
    """
    from .constants import FLUID_PRESETS
    
    fluid_names = list(FLUID_PRESETS.keys())
    
    selected = st.selectbox(
        label="Tipo de Fluido",
        options=fluid_names,
        index=0,  # Água (20°C) por padrão
        help=TOOLTIPS.get('fluid_preset', ''),
        key=key
    )
    
    # Mostrar descrição do fluido selecionado
    if selected and selected in FLUID_PRESETS:
        description = FLUID_PRESETS[selected]['description']
        st.caption(f"_{description}_")
    
    return selected


def manometric_fluid_selector(key: str = "manometric_fluid") -> str:
    """
    Cria um seletor de fluidos manométricos.
    
    Args:
        key: Chave única do componente
    
    Returns:
        Nome do fluido manométrico selecionado
    """
    from .constants import MANOMETRIC_FLUIDS
    
    fluid_names = list(MANOMETRIC_FLUIDS.keys())
    
    selected = st.selectbox(
        label="Fluido Manométrico",
        options=fluid_names,
        index=0,  # Mercúrio por padrão
        help="Fluido usado no manômetro diferencial em U",
        key=key
    )
    
    return selected


def validate_geometry(D1: float, D2: float) -> tuple[bool, Optional[str]]:
    """
    Valida os parâmetros geométricos.
    
    Args:
        D1: Diâmetro de entrada
        D2: Diâmetro da garganta
    
    Returns:
        Tupla (is_valid, error_message)
    """
    from .constants import ERROR_MESSAGES, VALIDATION_LIMITS
    
    # Verificar se D2 < D1
    if D2 >= D1:
        return False, ERROR_MESSAGES['D2_greater_than_D1']
    
    # Verificar razão beta
    beta = D2 / D1
    if beta < 0.4 or beta > 0.7:
        # Aviso, não erro crítico
        return True, ERROR_MESSAGES['beta_out_of_range']
    
    return True, None


def display_flow_rate_conversions(Q: float):
    """
    Exibe conversões de vazão em diferentes unidades.
    
    Args:
        Q: Vazão em m³/s
    """
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("m³/s", f"{Q:.4f}")
    with col2:
        st.metric("L/s", f"{Q*1000:.2f}")
    with col3:
        st.metric("m³/h", f"{Q*3600:.2f}")
