"""
Exemplos de Uso do Simulador de Venturi
Demonstra diferentes formas de utilizar o simulador
"""

from venturi_simulator import VenturiSimulator
import numpy as np
import matplotlib.pyplot as plt


def exemplo_1_comparacao_modos():
    """Exemplo 1: Comparação entre Modo Ideal e Modo Realista"""
    print("=" * 70)
    print("EXEMPLO 1: Comparação Modo Ideal vs Modo Realista")
    print("=" * 70)
    
    # Parâmetros comuns
    D1 = 0.10  # m
    D2 = 0.05  # m
    Q = 0.015  # m³/s
    
    # Modo Ideal
    sim_ideal = VenturiSimulator()
    sim_ideal.mode = 'Ideal'
    sim_ideal.D1 = D1
    sim_ideal.D2 = D2
    sim_ideal.Q = Q
    sim_ideal._calculate()
    
    print("\n🔵 MODO IDEAL (sem perdas):")
    print(f"  Velocidade na entrada (v₁): {sim_ideal.v1:.3f} m/s")
    print(f"  Velocidade na garganta (v₂): {sim_ideal.v2:.3f} m/s")
    print(f"  Queda de pressão (ΔP): {sim_ideal.delta_P/1000:.3f} kPa")
    print(f"  Desnível manométrico (Δh): {sim_ideal.delta_h*100:.2f} cm")
    print(f"  Perda de carga (hₗ): {sim_ideal.h_L:.6f} m (zero)")
    
    # Modo Realista
    sim_real = VenturiSimulator()
    sim_real.mode = 'Realista'
    sim_real.D1 = D1
    sim_real.D2 = D2
    sim_real.Q = Q
    sim_real.f = 0.025  # Coeficiente de atrito
    sim_real.Cd = 0.96  # Coeficiente de descarga
    sim_real._calculate()
    
    print("\n🔴 MODO REALISTA (com perdas):")
    print(f"  Velocidade na entrada (v₁): {sim_real.v1:.3f} m/s")
    print(f"  Velocidade na garganta (v₂): {sim_real.v2:.3f} m/s")
    print(f"  Queda de pressão (ΔP): {sim_real.delta_P/1000:.3f} kPa")
    print(f"  Desnível manométrico (Δh): {sim_real.delta_h*100:.2f} cm")
    print(f"  Perda de carga (hₗ): {sim_real.h_L:.6f} m")
    
    print("\n📊 DIFERENÇAS:")
    diff_p = ((sim_real.delta_P - sim_ideal.delta_P) / sim_ideal.delta_P) * 100
    diff_h = ((sim_real.delta_h - sim_ideal.delta_h) / sim_ideal.delta_h) * 100
    print(f"  ΔP aumentou: {diff_p:.2f}%")
    print(f"  Δh aumentou: {diff_h:.2f}%")
    print(f"  Perda de energia: {sim_real.h_L:.6f} m")
    print()


def exemplo_2_curva_calibracao():
    """Exemplo 2: Geração de Curva de Calibração"""
    print("=" * 70)
    print("EXEMPLO 2: Curva de Calibração do Medidor")
    print("=" * 70)
    
    # Criar simulador
    sim = VenturiSimulator()
    sim.mode = 'Realista'
    sim.D1 = 0.10
    sim.D2 = 0.05
    sim.Cd = 0.97
    sim.f = 0.02
    
    # Faixa de vazões
    vazoes = np.linspace(0.005, 0.030, 20)  # m³/s
    desniveis = []
    pressoes = []
    
    print("\nGerando curva de calibração...")
    print(f"{'Q (L/s)':<12} {'Δh (cm)':<12} {'ΔP (kPa)':<12} {'Re':<12}")
    print("-" * 50)
    
    for q in vazoes:
        sim.Q = q
        sim._calculate()
        desniveis.append(sim.delta_h * 100)  # cm
        pressoes.append(sim.delta_P / 1000)   # kPa
        
        if len(desniveis) % 4 == 0:  # Mostrar a cada 4 pontos
            Re = sim._calculate_reynolds()
            print(f"{q*1000:<12.2f} {sim.delta_h*100:<12.2f} {sim.delta_P/1000:<12.2f} {Re:<12.0f}")
    
    print(f"\n📈 RESUMO DA CALIBRAÇÃO:")
    print(f"  Faixa de vazão: {vazoes[0]*1000:.1f} - {vazoes[-1]*1000:.1f} L/s")
    print(f"  Faixa de desnível: {desniveis[0]:.2f} - {desniveis[-1]:.2f} cm")
    print(f"  Faixa de ΔP: {pressoes[0]:.2f} - {pressoes[-1]:.2f} kPa")
    
    # Plotar curva
    plt.figure(figsize=(10, 6))
    plt.plot(vazoes * 1000, desniveis, 'bo-', linewidth=2, markersize=6)
    plt.xlabel('Vazão (L/s)', fontsize=12)
    plt.ylabel('Desnível Manométrico Δh (cm)', fontsize=12)
    plt.title('Curva de Calibração do Medidor de Venturi', fontsize=14, fontweight='bold')
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig('curva_calibracao.png', dpi=150)
    print(f"\n✅ Gráfico salvo como 'curva_calibracao.png'")
    print()


def exemplo_3_modo_medidor():
    """Exemplo 3: Uso do Modo Medidor (calcular vazão a partir de Δh)"""
    print("=" * 70)
    print("EXEMPLO 3: Modo Medidor - Calcular Vazão a partir de Δh")
    print("=" * 70)
    
    # Criar simulador
    sim = VenturiSimulator()
    sim.mode = 'Medidor'
    sim.D1 = 0.10
    sim.D2 = 0.05
    sim.Cd = 0.98
    
    # Diferentes desníveis
    desniveis = [0.05, 0.10, 0.15, 0.20, 0.25]  # m
    
    print("\nCalculando vazões para diferentes desníveis manométricos:")
    print(f"{'Δh (cm)':<12} {'Q (L/s)':<12} {'Q (m³/h)':<12} {'v₁ (m/s)':<12} {'v₂ (m/s)':<12}")
    print("-" * 65)
    
    for dh in desniveis:
        sim.delta_h = dh
        sim._calculate()
        
        print(f"{dh*100:<12.1f} {sim.Q*1000:<12.2f} {sim.Q*3600:<12.2f} {sim.v1:<12.3f} {sim.v2:<12.3f}")
    
    print("\n💡 OBSERVAÇÃO:")
    print("  A vazão é proporcional à √(Δh)")
    print("  Dobrando Δh, a vazão aumenta por um fator de √2 ≈ 1.41")
    print()


def exemplo_4_sensibilidade_cd():
    """Exemplo 4: Análise de Sensibilidade ao Coeficiente de Descarga"""
    print("=" * 70)
    print("EXEMPLO 4: Sensibilidade ao Coeficiente de Descarga (Cd)")
    print("=" * 70)
    
    # Criar simulador
    sim = VenturiSimulator()
    sim.mode = 'Medidor'
    sim.D1 = 0.10
    sim.D2 = 0.05
    sim.delta_h = 0.15  # m (fixo)
    
    # Diferentes valores de Cd
    cd_values = np.linspace(0.90, 1.00, 11)
    vazoes = []
    
    print(f"\nAnalisando efeito de Cd na vazão (Δh fixo = {sim.delta_h*100:.0f} cm):")
    print(f"{'Cd':<12} {'Q (L/s)':<12} {'Variação %':<12}")
    print("-" * 40)
    
    q_referencia = None
    
    for cd in cd_values:
        sim.Cd = cd
        sim._calculate()
        vazoes.append(sim.Q * 1000)  # L/s
        
        if q_referencia is None:
            q_referencia = sim.Q * 1000
            variacao = 0
        else:
            variacao = ((sim.Q * 1000 - q_referencia) / q_referencia) * 100
        
        print(f"{cd:<12.2f} {sim.Q*1000:<12.3f} {variacao:<12.2f}")
    
    print(f"\n📊 ANÁLISE:")
    print(f"  Vazão mínima (Cd=0.90): {vazoes[0]:.3f} L/s")
    print(f"  Vazão máxima (Cd=1.00): {vazoes[-1]:.3f} L/s")
    variacao_total = ((vazoes[-1] - vazoes[0]) / vazoes[0]) * 100
    print(f"  Variação total: {variacao_total:.1f}%")
    print(f"\n⚠️  IMPORTANTE:")
    print(f"  Uma variação de 10% em Cd causa {variacao_total:.1f}% de variação na vazão!")
    print(f"  É crucial ter um Cd preciso para medições confiáveis.")
    print()


def exemplo_5_efeito_beta():
    """Exemplo 5: Efeito da Razão Beta (β = D₂/D₁)"""
    print("=" * 70)
    print("EXEMPLO 5: Efeito da Razão Beta (β = D₂/D₁)")
    print("=" * 70)
    
    # Parâmetros fixos
    D1 = 0.10  # m
    Q = 0.015  # m³/s (fixo)
    
    # Diferentes valores de D2 (β)
    beta_values = np.linspace(0.3, 0.7, 9)
    
    print(f"\nAnalisando efeito de β na queda de pressão (D₁={D1*100:.0f} cm, Q={Q*1000:.0f} L/s):")
    print(f"{'β':<12} {'D₂ (cm)':<12} {'Δh (cm)':<12} {'ΔP (kPa)':<12} {'v₂ (m/s)':<12}")
    print("-" * 60)
    
    for beta in beta_values:
        D2 = beta * D1
        
        sim = VenturiSimulator()
        sim.mode = 'Ideal'
        sim.D1 = D1
        sim.D2 = D2
        sim.Q = Q
        sim._calculate()
        
        print(f"{beta:<12.2f} {D2*100:<12.2f} {sim.delta_h*100:<12.2f} {sim.delta_P/1000:<12.2f} {sim.v2:<12.2f}")
    
    print(f"\n📊 OBSERVAÇÕES:")
    print(f"  - Menor β → Maior velocidade na garganta")
    print(f"  - Menor β → Maior queda de pressão")
    print(f"  - β típico para Venturi: 0.4 - 0.7")
    print(f"  - Compromisso entre sensibilidade e perda de carga")
    print()


def main():
    """Executa todos os exemplos"""
    print("\n" + "=" * 70)
    print("   EXEMPLOS DE USO DO SIMULADOR DE MEDIDOR DE VENTURI")
    print("=" * 70 + "\n")
    
    # Executar exemplos
    exemplo_1_comparacao_modos()
    exemplo_2_curva_calibracao()
    exemplo_3_modo_medidor()
    exemplo_4_sensibilidade_cd()
    exemplo_5_efeito_beta()
    
    print("=" * 70)
    print("   EXEMPLOS CONCLUÍDOS COM SUCESSO!")
    print("=" * 70)
    print("\n💡 Dica: Execute 'run_simulator()' para interface interativa completa!\n")


if __name__ == "__main__":
    main()

