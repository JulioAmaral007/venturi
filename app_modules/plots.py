import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Polygon

def plotar_diagrama_venturi(sim):

    fig, ax = plt.subplots(figsize=(14, 9)) 
    
    COR_P1 = '#ef4444'      
    COR_P2 = '#10b981'      
    COR_P2FIM = '#059669'   
    COR_P3 = '#8b5cf6'      
    COR_FLUIDO = '#e0f2fe'
    COR_BORDA_TUBO = '#0369a1'
    COR_MERCURIO = '#4b5563'

    margem_visual = sim.D1 * 0.8
    x_points = np.linspace(-margem_visual, sim.L + margem_visual, 500)
    
    def radius_at_x(x):
        L1 = sim.L_entrada
        L2 = sim.L_garganta
        r1 = sim.D1 / 2
        r2 = sim.D2 / 2
        
        def smooth_step(t):
            return (1 - np.cos(t * np.pi)) / 2

        if x < 0: return r1
        elif x < L1:
            t = x / L1
            return r1 - (r1 - r2) * smooth_step(t)
        elif x < L1 + L2: return r2
        elif x <= sim.L:
            x_no_cone = x - (L1 + L2)
            t = x_no_cone / sim.L_saida
            t = min(t, 1.0)
            return r2 + (r1 - r2) * smooth_step(t)
        else: return r1
    
    y_upper = [radius_at_x(x) for x in x_points]
    y_lower = [-y for y in y_upper]
    
    ax.fill_between(x_points, y_lower, y_upper, color=COR_FLUIDO, 
                    alpha=0.6, edgecolor=COR_BORDA_TUBO, linewidth=2)
    ax.axhline(0, color='black', linestyle='-.', alpha=0.3, linewidth=1)

    x_p1 = 0.0 
    y_p1 = -radius_at_x(x_p1)

    x_p2 = sim.L_entrada + (sim.L_garganta * 0.05) 
    y_p2 = -radius_at_x(x_p2)

    x_p2fim = sim.L_entrada + (sim.L_garganta * 0.95)
    y_p2fim = -radius_at_x(x_p2fim)

    x_p3 = sim.L
    y_p3 = -radius_at_x(x_p3)

    limite_visual_max = max(sim.D1 * 3.0, 0.5)
    if sim.delta_h > limite_visual_max:
        delta_h_plot = limite_visual_max
        travado = True
    else:
        delta_h_plot = sim.delta_h
        travado = False
        
    centro_manometro = y_p1 - (sim.D1 * 0.5) - (delta_h_plot * 0.5) - 0.1
    nivel_esq = centro_manometro - (delta_h_plot / 2)
    nivel_dir = centro_manometro + (delta_h_plot / 2)
    fundo_U = min(nivel_esq, nivel_dir) - (sim.D1 * 0.4)

    # Desenho do Tubo em U (Conectando P1 e P2)
    # Linhas descendo
    ax.plot([x_p1, x_p1], [y_p1, nivel_esq], color='gray', linewidth=1.5, alpha=0.7)
    ax.plot([x_p2, x_p2], [y_p2, nivel_dir], color='gray', linewidth=1.5, alpha=0.7)
    
    # Fluido Manométrico
    ax.plot([x_p1, x_p1], [fundo_U, nivel_esq], color=COR_MERCURIO, linewidth=8, solid_capstyle='butt')
    ax.plot([x_p2, x_p2], [fundo_U, nivel_dir], color=COR_MERCURIO, linewidth=8, solid_capstyle='butt')
    ax.plot([x_p1, x_p2], [fundo_U, fundo_U], color=COR_MERCURIO, linewidth=8, solid_capstyle='butt')

    # Marcadores de Nível
    ax.plot([x_p1-0.04, x_p1+0.04], [nivel_esq, nivel_esq], color=COR_P1, linewidth=3)
    ax.plot([x_p2-0.04, x_p2+0.04], [nivel_dir, nivel_dir], color=COR_P2, linewidth=3)

    # Cota Delta H
    mid_x = (x_p1 + x_p2) / 2
    aviso = "\n(Escala Reduzida)" if travado else ""
    cor_texto = 'red' if travado else '#b91c1c'
    
    ax.plot([mid_x, mid_x], [nivel_esq, nivel_dir], color=cor_texto, linestyle='--', linewidth=1)
    if travado:
        y_mid = (nivel_esq + nivel_dir) / 2
        ax.text(mid_x, y_mid, "//", color=cor_texto, ha='center', va='center', fontweight='bold', fontsize=16, backgroundcolor='white')

    ax.text(mid_x + 0.05, (nivel_esq + nivel_dir)/2, 
            f'Δh = {sim.delta_h*100:.1f} cm{aviso}', 
            color=cor_texto, fontweight='bold', fontsize=11, va='center',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor=cor_texto, boxstyle='round,pad=0.2'))

    # ==========================================
    # 4. ANOTAÇÕES (CAIXAS DE TEXTO)
    # ==========================================
    
    # Função auxiliar para formatar texto
    def criar_anotacao(x, y, titulo, pressao, velocidade, cor):
        texto = f"{titulo}\nP = {pressao/1000:.2f} kPa\nv = {velocidade:.2f} m/s"
        ax.annotate(texto, xy=(x, 0), xytext=(x, sim.D1*1.3),
                    ha='center', va='bottom', color=cor, fontweight='bold', fontsize=10,
                    bbox=dict(boxstyle="round,pad=0.3", fc="white", ec=cor, lw=2),
                    arrowprops=dict(arrowstyle="->", color=cor))

    # P1 (Entrada)
    criar_anotacao(x_p1, 0, "P₁ (Entrada)", sim.P1, sim.v1, COR_P1)

    # P2 (Início Garganta)
    criar_anotacao(x_p2, 0, "P₂ (Início)", sim.P2, sim.v2, COR_P2)

    # P2_fim (Fim Garganta) - Verifica se existe o atributo P2_fim (criado no simulator)
    p2_fim_val = getattr(sim, 'P2_fim', sim.P2) # Fallback se não tiver atrito calculado
    
    # Se a garganta for muito curta, não mostramos P2_fim para não sobrepor
    if sim.L_garganta > 0.15:
        criar_anotacao(x_p2fim, 0, "P₂ (Fim)", p2_fim_val, sim.v2, COR_P2FIM)
        
        # Linha vertical indicando o fim da garganta
        ax.plot([x_p2fim, x_p2fim], [y_p2fim, sim.D1*1.2], color=COR_P2FIM, linestyle=':', alpha=0.5)

    # P3 (Saída)
    criar_anotacao(x_p3, 0, "P₃ (Saída)", sim.P3, sim.v1, COR_P3)

    # ==========================================
    # 5. FINALIZAÇÃO
    # ==========================================
    ax.set_title('Diagrama do Venturi (Geometria Real)', fontsize=16, fontweight='bold', pad=50)
    ax.set_xlabel('Posição Axial (m)')
    ax.set_ylabel('Raio (m)')
    
    ax.set_xlim(-margem_visual, sim.L + margem_visual)
    
    top_limit = sim.D1 * 3.5 # Mais espaço para as caixas de texto
    bottom_limit = fundo_U - 0.2
    ax.set_ylim(bottom_limit, top_limit)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.15, linestyle='--')
    ax.set_aspect('equal')
    
    return fig

def plotar_perfil_pressao(sim):
    
    fig, ax = plt.subplots(figsize=(10, 5))
    x_start = -sim.D1 * 0.5
    x_p1 = 0.0
    x_p2_start = sim.L_entrada
    x_p2_end = sim.L_entrada + sim.L_garganta
    x_p3 = sim.L
    x_end = sim.L + sim.D1 * 0.5
    
    X = [x_start, x_p1, x_p2_start, x_p2_end, x_p3, x_end]
    P = np.array([sim.P1, sim.P1, sim.P2, sim.P2_fim, sim.P3, sim.P3]) / 1000.0
    
    ax.plot(X, P, color='#2563eb', linewidth=3, label='Pressão Estática P(x)')
    ax.axhline(sim.P1/1000, color='#ef4444', linestyle='--', alpha=0.5, label=f'P₁')
    ax.axhline(sim.P2/1000, color='#10b981', linestyle='--', alpha=0.5, label=f'P₂')
    
    ax.axvline(x_p2_end, color='gray', linestyle=':', alpha=0.3)

    if sim.mode == 'Realista':
        ax.axhline(sim.P3/1000, color='orange', linestyle=':', alpha=0.7)
        mid_x_end = (x_p3 + x_end) / 2
        ax.annotate(f'Perda: {(sim.P1 - sim.P3)/1000:.2f} kPa', 
                   xy=(mid_x_end, sim.P3/1000), 
                   xytext=(mid_x_end, (sim.P1 + sim.P3)/2000),
                   arrowprops=dict(arrowstyle='<->', color='orange'),
                   color='orange', fontweight='bold', ha='center', va='center',
                   bbox=dict(facecolor='white', edgecolor='orange', boxstyle='round,pad=0.2'))

    ax.set_xlabel('Posição Axial (m)', fontweight='bold')
    ax.set_ylabel('Pressão (kPa)', fontweight='bold')
    ax.set_title('Perfil de Pressão ao Longo do Medidor', fontweight='bold', pad=15)
    ax.grid(True, alpha=0.2, linestyle='--')
    ax.legend(loc='best')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    return fig

def plotar_linhas_energia(sim):
    """Mantém o plot de linhas de energia (já atualizado anteriormente)."""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Geometria e Arrays
    x_vals = np.linspace(0, sim.L, 200)
    L1, L2 = sim.L_entrada, sim.L_garganta
    X_key = [0, L1, L1 + L2, sim.L]
    Areas = [sim.A1, sim.A2, sim.A2, sim.A1]
    V_key = [sim.Q / a for a in Areas]
    Hv_key = np.array([v**2 / (2 * sim.g) for v in V_key])
    gamma = sim.rho * sim.g
    Hp_key = np.array([sim.P1/gamma, sim.P2/gamma, sim.P2_fim/gamma, sim.P3/gamma])
    
    # Datum Offset para evitar gráficos negativos
    min_p = np.min(Hp_key)
    datum_offset = abs(min_p) + 0.1 if min_p < 0 else 0.0
    Hp_key_plot = Hp_key + datum_offset
    
    # Interpolação
    X_plot = np.linspace(0, sim.L, 500)
    Hp_plot = np.interp(X_plot, X_key, Hp_key_plot)
    Hv_plot = np.interp(X_plot, X_key, Hv_key)
    EGL_plot = Hp_plot + Hv_plot
    EGL_ideal = np.full_like(X_plot, EGL_plot[0])

    # Plotagem
    ax.fill_between(X_plot, EGL_plot, EGL_ideal, color='#ef4444', alpha=0.2, label='Perda de Carga')
    ax.fill_between(X_plot, Hp_plot, EGL_plot, color='#10b981', alpha=0.5, label='Energia Cinética')
    ax.fill_between(X_plot, 0, Hp_plot, color='#3b82f6', alpha=0.4, label='Energia de Pressão')
    
    if datum_offset > 0:
        ax.axhline(datum_offset, color='black', linestyle=':', label='Pressão Zero')

    ax.plot(X_plot, EGL_plot, color='#b91c1c', linewidth=2)
    
    perda_total = EGL_ideal[-1] - EGL_plot[-1]
    if perda_total > 0.001:
        ax.annotate(f"Perda Total:\n{perda_total:.3f} m", 
                    xy=(sim.L, (EGL_ideal[-1] + EGL_plot[-1])/2),
                    xytext=(sim.L + 0.1, (EGL_ideal[-1] + EGL_plot[-1])/2),
                    arrowprops=dict(arrowstyle='-[, widthB=0.5', color='red'),
                    color='red', fontweight='bold', va='center')

    ax.set_xlabel('Posição (m)', fontweight='bold')
    ax.set_ylabel('Energia / Carga (m)', fontweight='bold')
    ax.set_title('Balanço de Energia', fontweight='bold', pad=15)
    ax.set_xlim(0, sim.L * 1.15)
    ax.set_ylim(bottom=0)
    ax.legend(loc='lower left', frameon=True)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.grid(True, alpha=0.2, linestyle='--')
    return fig


