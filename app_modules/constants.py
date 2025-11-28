"""
Constantes de Design e Configuração do Simulador de Venturi
Define paleta de cores, espaçamentos, presets de fluidos e outras constantes.
"""

# ========== DESIGN SYSTEM ==========

# Paleta de Cores
COLORS = {
    'primary': '#2563eb',      # Azul principal
    'secondary': '#0ea5e9',    # Azul claro
    'success': '#10b981',      # Verde
    'warning': '#f59e0b',      # Amarelo/Laranja
    'error': '#ef4444',        # Vermelho
    'info': '#3b82f6',         # Azul informativo
    'purple': '#8b5cf6',       # Roxo (para energia)
    'gray': '#64748b',         # Cinza
}

# Espaçamentos (em pixels)
SPACING = {
    'xs': '8px',
    'sm': '16px',
    'md': '24px',
    'lg': '32px',
    'xl': '48px',
}

# Tamanhos de Fonte
FONT_SIZES = {
    'xs': '12px',
    'sm': '14px',
    'base': '16px',
    'lg': '20px',
    'xl': '24px',
    'xxl': '32px',
}

# ========== PRESETS DE FLUIDOS ==========

FLUID_PRESETS = {
    'Água (20°C)': {
        'rho': 1000,           # kg/m³
        'nu': 1.004e-6,        # m²/s (viscosidade cinemática)
        'description': 'Água à temperatura ambiente'
    },
    'Água (4°C)': {
        'rho': 1000,
        'nu': 1.567e-6,
        'description': 'Água na densidade máxima'
    },
    'Água (60°C)': {
        'rho': 983,
        'nu': 0.478e-6,
        'description': 'Água aquecida'
    },
    'Óleo SAE 10': {
        'rho': 870,
        'nu': 40e-6,
        'description': 'Óleo lubrificante leve'
    },
    'Óleo SAE 30': {
        'rho': 890,
        'nu': 110e-6,
        'description': 'Óleo lubrificante médio'
    },
    'Gasolina': {
        'rho': 720,
        'nu': 0.6e-6,
        'description': 'Combustível líquido'
    },
    'Etanol': {
        'rho': 789,
        'nu': 1.52e-6,
        'description': 'Álcool etílico'
    },
    'Glicerina (20°C)': {
        'rho': 1260,
        'nu': 1180e-6,
        'description': 'Fluido muito viscoso'
    },
    'Personalizado': {
        'rho': 1000,
        'nu': 1e-6,
        'description': 'Defina suas próprias propriedades'
    }
}

# Fluidos manométricos comuns
MANOMETRIC_FLUIDS = {
    'Mercúrio': 13600,         # kg/m³
    'Água': 1000,
    'Óleo leve': 850,
    'Tetracloreto de carbono': 1590,
}

# ========== TOOLTIPS E AJUDA ==========

TOOLTIPS = {
    # Modos
    'modo_ideal': 'Simula escoamento sem perdas (Cd = 1.0, sem atrito). Útil para análise teórica.',
    'modo_realista': 'Simula escoamento com perdas por atrito e coeficiente de descarga real. Mais próximo da realidade.',
    'modo_medidor': 'Calcula a vazão (Q) a partir do desnível manométrico medido (Δh). Uso prático do medidor.',
    
    # Geometria
    'D1': 'Diâmetro interno da tubulação de entrada (seção 1). Deve ser maior que D₂.',
    'D2': 'Diâmetro da garganta (seção mais estreita do Venturi). Deve ser menor que D₁.',
    'L': 'Comprimento total do medidor de Venturi, incluindo convergente, garganta e divergente.',
    'beta': 'Razão entre diâmetros β = D₂/D₁. Valores típicos: 0.4 a 0.7. Menor β = maior sensibilidade.',
    
    # Fluidos
    'rho': 'Densidade do fluido que escoa pelo medidor. Afeta a pressão e o número de Reynolds.',
    'nu': 'Viscosidade cinemática (ν = μ/ρ). Afeta diretamente o número de Reynolds.',
    'rho_m': 'Densidade do fluido manométrico (geralmente mercúrio). Usado para calcular Δh.',
    'fluid_preset': 'Selecione um fluido comum ou "Personalizado" para definir propriedades manualmente.',
    
    # Escoamento
    'Q': 'Vazão volumétrica do fluido. Quanto maior a vazão, maior a velocidade e a queda de pressão.',
    'flow_input_choice': 'Escolha se deseja informar diretamente a vazão ou a velocidade.',
    'v1_input': 'Velocidade média na seção de entrada (D₁). O simulador converte automaticamente para vazão.',
    'v2_input': 'Velocidade média na garganta (D₂). O simulador converte automaticamente para vazão.',
    'delta_h': 'Desnível observado no manômetro diferencial. Relacionado à queda de pressão.',
    
    # Parâmetros avançados
    'f': 'Coeficiente de atrito de Darcy-Weisbach. Depende da rugosidade e do número de Reynolds. Típico: 0.015-0.025.',
    'Cd': 'Coeficiente de descarga. Corrige efeitos não ideais. Para Venturi: 0.95-0.98. Depende do número de Reynolds.',
    
    # Resultados
    'reynolds': 'Número de Reynolds (Re = ρvD/μ). Indica o regime: Laminar (Re<2300), Transição (2300-4000), Turbulento (Re>4000).',
    'regime_laminar': 'Escoamento em camadas ordenadas. Não recomendado para medidores de vazão.',
    'regime_transicao': 'Escoamento instável. Evitar esta faixa em aplicações práticas.',
    'regime_turbulento': 'Escoamento caótico mas previsível. Ideal para medidores de vazão.',
}

# ========== CONFIGURAÇÕES DE GRÁFICOS ==========

PLOT_CONFIG = {
    'figure_facecolor': 'white',
    'axes_facecolor': 'white',
    'grid_alpha': 0.2,
    'grid_linestyle': '--',
    'grid_linewidth': 1,
    'title_fontsize': 13,
    'title_fontweight': 'bold',
    'title_color': '#000000',
    'title_pad': 15,
    'label_fontsize': 11,
    'label_fontweight': 'bold',
    'label_color': '#000000',
    'legend_fontsize': 10,
    'tick_labelsize': 10,
    'line_width': 2.5,
    'marker_size': 8,
    'marker_edge_width': 2,
    'marker_edge_color': 'white',
}

# ========== VALIDAÇÃO ==========

VALIDATION_LIMITS = {
    'D1_min': 0.01,      # m
    'D1_max': 1.0,       # m
    'D2_min': 0.005,     # m
    'D2_max': 0.5,       # m
    'beta_min': 0.2,     # D2/D1
    'beta_max': 0.8,     # D2/D1
    'L_min': 0.1,        # m
    'L_max': 10.0,       # m
    'Q_min': 0.0001,     # m³/s
    'Q_max': 1.0,        # m³/s
    'delta_h_min': 0.001,  # m
    'delta_h_max': 2.0,    # m
    'f_min': 0.005,
    'f_max': 0.1,
    'Cd_min': 0.85,
    'Cd_max': 1.0,
}

# ========== ÍCONES ==========

ICONS = {
    'geometry': '📐',
    'fluid': '💧',
    'flow': '🌊',
    'advanced': '🔧',
    'settings': '⚙️',
    'mode': '🎯',
    'results': '📊',
    'diagram': '📐',
    'manometer': '🔬',
    'pressure': '📈',
    'energy': '⚡',
    'data': '📋',
    'examples': '📚',
    'help': '❓',
    'info': '💡',
    'warning': '⚠️',
    'success': '✅',
    'error': '❌',
    'science': '🔬',
}

# ========== MENSAGENS ==========

ERROR_MESSAGES = {
    'D2_greater_than_D1': '⚠️ Erro: O diâmetro da garganta (D₂) deve ser menor que o diâmetro de entrada (D₁).',
    'beta_out_of_range': '⚠️ Aviso: A razão β = D₂/D₁ está fora da faixa típica (0.4-0.7). Resultados podem ser imprecisos.',
    'reynolds_too_low': '⚠️ Aviso: Número de Reynolds muito baixo (Re < 2300). Escoamento laminar não é ideal para medidores.',
    'reynolds_transition': '⚠️ Aviso: Regime de transição (2300 < Re < 4000). Comportamento instável.',
}

SUCCESS_MESSAGES = {
    'reynolds_good': '✅ Número de Reynolds adequado (Re > 4000). Regime turbulento ideal para medições.',
    'beta_good': '✅ Razão β dentro da faixa recomendada (0.4-0.7).',
}
