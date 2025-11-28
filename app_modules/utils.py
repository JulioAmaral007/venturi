"""
Funções Utilitárias para o Simulador de Venturi
Fornece funções auxiliares para conversões, formatação e cálculos.
"""

from typing import Dict, Any


def format_scientific(value: float, decimals: int = 2) -> str:
    """
    Formata um número em notação científica se necessário.
    
    Args:
        value: Valor a formatar
        decimals: Número de casas decimais
    
    Returns:
        String formatada
    """
    if abs(value) < 0.001 or abs(value) > 10000:
        return f"{value:.{decimals}e}"
    return f"{value:.{decimals}f}"


def convert_flow_rate(Q: float, from_unit: str = 'm3/s', to_unit: str = 'L/s') -> float:
    """
    Converte vazão entre diferentes unidades.
    
    Args:
        Q: Vazão no formato original
        from_unit: Unidade de origem ('m3/s', 'L/s', 'm3/h', 'L/min')
        to_unit: Unidade de destino
    
    Returns:
        Vazão convertida
    """
    # Converter tudo para m³/s primeiro
    conversions_to_m3s = {
        'm3/s': 1.0,
        'L/s': 0.001,
        'm3/h': 1/3600,
        'L/min': 0.001/60,
        'gpm': 0.00006309,  # galões por minuto
    }
    
    # Converter de m³/s para unidade desejada
    conversions_from_m3s = {
        'm3/s': 1.0,
        'L/s': 1000,
        'm3/h': 3600,
        'L/min': 60000,
        'gpm': 15850.3,
    }
    
    Q_m3s = Q * conversions_to_m3s.get(from_unit, 1.0)
    return Q_m3s * conversions_from_m3s.get(to_unit, 1.0)


def convert_pressure(P: float, from_unit: str = 'Pa', to_unit: str = 'kPa') -> float:
    """
    Converte pressão entre diferentes unidades.
    
    Args:
        P: Pressão no formato original
        from_unit: Unidade de origem ('Pa', 'kPa', 'bar', 'psi', 'atm')
        to_unit: Unidade de destino
    
    Returns:
        Pressão convertida
    """
    # Converter tudo para Pa primeiro
    conversions_to_pa = {
        'Pa': 1.0,
        'kPa': 1000,
        'bar': 100000,
        'psi': 6894.76,
        'atm': 101325,
        'mmHg': 133.322,
    }
    
    # Converter de Pa para unidade desejada
    conversions_from_pa = {
        'Pa': 1.0,
        'kPa': 0.001,
        'bar': 0.00001,
        'psi': 0.000145038,
        'atm': 0.00000986923,
        'mmHg': 0.00750062,
    }
    
    P_pa = P * conversions_to_pa.get(from_unit, 1.0)
    return P_pa * conversions_from_pa.get(to_unit, 1.0)


def get_fluid_properties(fluid_name: str) -> Dict[str, Any]:
    """
    Retorna as propriedades de um fluido preset.
    
    Args:
        fluid_name: Nome do fluido
    
    Returns:
        Dicionário com propriedades (rho, nu, description)
    """
    from .constants import FLUID_PRESETS
    
    return FLUID_PRESETS.get(fluid_name, FLUID_PRESETS['Água (20°C)'])


def get_manometric_density(fluid_name: str) -> float:
    """
    Retorna a densidade de um fluido manométrico.
    
    Args:
        fluid_name: Nome do fluido manométrico
    
    Returns:
        Densidade em kg/m³
    """
    from .constants import MANOMETRIC_FLUIDS
    
    return MANOMETRIC_FLUIDS.get(fluid_name, 13600)


def calculate_beta(D1: float, D2: float) -> float:
    """
    Calcula a razão beta.
    
    Args:
        D1: Diâmetro de entrada
        D2: Diâmetro da garganta
    
    Returns:
        Razão beta (D2/D1)
    """
    return D2 / D1


def is_beta_in_recommended_range(beta: float) -> bool:
    """
    Verifica se beta está na faixa recomendada.
    
    Args:
        beta: Razão beta
    
    Returns:
        True se estiver na faixa 0.4-0.7
    """
    return 0.4 <= beta <= 0.7


def get_reynolds_regime(Re: float) -> str:
    """
    Determina o regime de escoamento baseado em Reynolds.
    
    Args:
        Re: Número de Reynolds
    
    Returns:
        String com o regime ('Laminar', 'Transição', 'Turbulento')
    """
    if Re < 2300:
        return 'Laminar'
    elif Re < 4000:
        return 'Transição'
    else:
        return 'Turbulento'


def is_reynolds_adequate(Re: float) -> bool:
    """
    Verifica se o número de Reynolds é adequado para medições.
    
    Args:
        Re: Número de Reynolds
    
    Returns:
        True se Re > 4000 (turbulento)
    """
    return Re > 4000


def format_reynolds(Re: float) -> str:
    """
    Formata o número de Reynolds com separadores de milhares.
    
    Args:
        Re: Número de Reynolds
    
    Returns:
        String formatada
    """
    return f"{Re:,.0f}"


def calculate_velocity(Q: float, D: float) -> float:
    """
    Calcula velocidade média a partir de vazão e diâmetro.
    
    Args:
        Q: Vazão volumétrica (m³/s)
        D: Diâmetro (m)
    
    Returns:
        Velocidade média (m/s)
    """
    import numpy as np
    A = np.pi * (D / 2) ** 2
    return Q / A


def calculate_area(D: float) -> float:
    """
    Calcula área da seção circular.
    
    Args:
        D: Diâmetro (m)
    
    Returns:
        Área (m²)
    """
    import numpy as np
    return np.pi * (D / 2) ** 2
