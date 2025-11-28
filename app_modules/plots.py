import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def plotar_diagrama_venturi(sim):
    """Plota o diagrama esquemático do Venturi."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, sim.L)
    ax.set_ylim(-sim.D1, sim.D1)
    ax.set_aspect('equal')
    
    x_points = np.linspace(0, sim.L, 100)
    
    def radius_at_x(x):
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        r1 = sim.D1 / 2
        r2 = sim.D2 / 2
        
        if x < L_conv:
            t = x / L_conv
            r = r1 - (r1 - r2) * t
        elif x < L_conv + L_throat:
            r = r2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            r = r2 + (r1 - r2) * t
        return r
    
    y_upper = [radius_at_x(x) for x in x_points]
    y_lower = [-radius_at_x(x) for x in x_points]
    
    ax.fill_between(x_points, y_lower, y_upper, color='lightblue', 
                    alpha=0.3, edgecolor='blue', linewidth=2)
    ax.plot(x_points, y_upper, 'b-', linewidth=2)
    ax.plot(x_points, y_lower, 'b-', linewidth=2)
    
    x1 = sim.L * 0.15
    x2 = sim.L * 0.5
    ax.plot(x1, 0, 'o', color='#ef4444', markersize=8, label='Ponto 1')
    ax.plot(x2, 0, 'o', color='#10b981', markersize=8, label='Ponto 2')
    
    ax.text(x1, -sim.D1 * 0.7, f'v₁={sim.v1:.2f} m/s', 
           ha='center', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#ef4444', linewidth=2))
    ax.text(x2, -sim.D1 * 0.7, f'v₂={sim.v2:.2f} m/s', 
           ha='center', fontsize=10, fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='#10b981', linewidth=2))
    
    ax.set_xlabel('Posição (m)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_ylabel('Raio (m)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_title(f'Diagrama do Medidor de Venturi - Modo {sim.mode}', 
                fontsize=13, fontweight='bold', color='#000000', pad=15)
    ax.legend(loc='upper right', frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    return fig


def plotar_manometro(sim):
    """Plota o manômetro em U."""
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(-0.5, 2.5)
    ax.set_ylim(-0.05, 0.8)
    ax.set_aspect('equal')
    
    tube_width = 0.2
    base_height = 0.08
    
    left_x = 0.5
    left_height = base_height + sim.delta_h / 2
    
    right_x = 1.3
    right_height = base_height + sim.delta_h / 2 + sim.delta_h
    
    # Base
    base = Rectangle((left_x, 0), right_x - left_x + tube_width, base_height,
                    facecolor='gray', edgecolor='black', linewidth=2)
    ax.add_patch(base)
    
    # Tubos
    left_tube = Rectangle((left_x, base_height), tube_width, left_height,
                         facecolor='lightcoral', edgecolor='black', linewidth=2, alpha=0.7)
    ax.add_patch(left_tube)
    
    right_tube = Rectangle((right_x, base_height), tube_width, right_height,
                          facecolor='lightgreen', edgecolor='black', linewidth=2, alpha=0.7)
    ax.add_patch(right_tube)
    
    # Mercúrio
    mercury = Rectangle((left_x, 0), right_x - left_x + tube_width, base_height - 0.01,
                       facecolor='silver', edgecolor='darkgray', linewidth=1)
    ax.add_patch(mercury)
    
    # Indicação de Δh
    y_left = base_height + left_height
    y_right = base_height + right_height
    mid_x = (left_x + right_x) / 2 + tube_width / 2 + 0.15
    
    ax.plot([mid_x, mid_x], [y_left, y_right], 'r-', linewidth=2)
    ax.plot([mid_x - 0.05, mid_x + 0.05], [y_left, y_left], 'r-', linewidth=2)
    ax.plot([mid_x - 0.05, mid_x + 0.05], [y_right, y_right], 'r-', linewidth=2)
    
    ax.text(mid_x + 0.2, (y_left + y_right) / 2, f'Δh={sim.delta_h*100:.1f} cm',
           fontsize=11, color='red', fontweight='bold', rotation=90, va='center')
    
    ax.text(left_x + tube_width / 2, -0.03, 'P₁', ha='center', fontsize=11, fontweight='bold')
    ax.text(right_x + tube_width / 2, -0.03, 'P₂', ha='center', fontsize=11, fontweight='bold')
    
    ax.set_title('Manômetro Diferencial em U', fontsize=13, fontweight='bold', 
                 color='black', pad=15)
    ax.axis('off')
    
    return fig


def plotar_perfil_pressao(sim):
    """Plota o perfil de pressão ao longo do tubo."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x_points = np.linspace(0, sim.L, 100)
    pressures = []
    
    for x in x_points:
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        
        if x < L_conv:
            t = x / L_conv
            P = sim.P1 - sim.delta_P * t
        elif x < L_conv + L_throat:
            P = sim.P2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            if sim.mode == 'Realista':
                P_recovery = sim.P2 + sim.delta_P * t * (1 - sim.h_L / (sim.delta_P / (sim.rho * sim.g)))
            else:
                P_recovery = sim.P2 + sim.delta_P * t
            P = P_recovery
        
        pressures.append(P / 1000)
    
    ax.fill_between(x_points, 0, pressures, alpha=0.3, color='#3b82f6')
    ax.plot(x_points, pressures, color='#2563eb', linewidth=3, label='Pressão ao longo do tubo')
    
    ax.axhline(y=sim.P1/1000, color='#ef4444', linestyle='--', alpha=0.5, linewidth=1.5,
              label=f'P₁ = {sim.P1/1000:.2f} kPa')
    ax.axhline(y=sim.P2/1000, color='#10b981', linestyle='--', alpha=0.5, linewidth=1.5,
              label=f'P₂ = {sim.P2/1000:.2f} kPa')
    
    ax.set_xlabel('Posição ao longo do tubo (m)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_ylabel('Pressão (kPa)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_title('Perfil de Pressão ao Longo do Medidor', fontsize=13, fontweight='bold', 
                 color='#000000', pad=15)
    ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    
    return fig


def plotar_linhas_energia(sim):
    """Plota Linha de Energia (LE) e Linha Piezométrica (LP)."""
    fig, ax = plt.subplots(figsize=(10, 5))
    x_points = np.linspace(0, sim.L, 100)
    LP = []
    LE = []
    
    for x in x_points:
        L_conv = sim.L / 3
        L_throat = sim.L / 3
        
        if x < L_conv:
            t = x / L_conv
            P = sim.P1 - sim.delta_P * t
            v = sim.v1 + (sim.v2 - sim.v1) * t
        elif x < L_conv + L_throat:
            P = sim.P2
            v = sim.v2
        else:
            t = (x - L_conv - L_throat) / (sim.L - L_conv - L_throat)
            if sim.mode == 'Realista':
                P_recovery = sim.P2 + sim.delta_P * t * (1 - sim.h_L / (sim.delta_P / (sim.rho * sim.g)))
            else:
                P_recovery = sim.P2 + sim.delta_P * t
            P = P_recovery
            v = sim.v2 - (sim.v2 - sim.v1) * t
        
        lp = P / (sim.rho * sim.g)
        LP.append(lp)
        
        le = lp + v**2 / (2 * sim.g)
        LE.append(le)
    
    ax.fill_between(x_points, 0, LE, alpha=0.15, color='#8b5cf6', label='Energia Total')
    ax.plot(x_points, LE, color='#8b5cf6', linewidth=3, label='Linha de Energia (LE)')
    
    ax.fill_between(x_points, 0, LP, alpha=0.15, color='#3b82f6', label='Carga Piezométrica')
    ax.plot(x_points, LP, color='#3b82f6', linewidth=3, label='Linha Piezométrica (LP)')
    
    ax.fill_between(x_points, LP, LE, alpha=0.3, color='#10b981', label='Energia Cinética')
    
    if sim.mode == 'Realista' and sim.h_L > 0:
        LE_initial = LE[0]
        LE_final = LE[-1]
        ax.annotate(f'Perda: hₗ = {sim.h_L:.4f} m', 
                   xy=(sim.L * 0.85, LE_final),
                   fontsize=10, color='#991b1b', fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.5', facecolor='white', 
                             edgecolor='#ef4444', linewidth=1))
    
    ax.set_xlabel('Posição ao longo do tubo (m)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_ylabel('Carga (m)', fontsize=11, fontweight='bold', color='#000000')
    ax.set_title('Linha de Energia e Linha Piezométrica', fontsize=13, fontweight='bold', 
                 color='#000000', pad=15)
    ax.legend(loc='best', frameon=True, fancybox=True, shadow=True)
    ax.grid(True, alpha=0.2, linestyle='--', linewidth=1)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_ylim(bottom=0)
    
    return fig


