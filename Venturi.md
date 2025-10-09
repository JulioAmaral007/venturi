# 📖 Medidor de Venturi - Fundamentação Teórica

## Introdução

O medidor de Venturi é um dispositivo de medição de vazão baseado no princípio de Bernoulli, inventado por Giovanni Battista Venturi no século XVIII. É amplamente utilizado em aplicações industriais devido à sua precisão e baixa perda de carga permanente.

## Princípio de Funcionamento

### Geometria do Venturi

O medidor de Venturi consiste em três seções principais:

1. **Seção Convergente**: Redução gradual do diâmetro (ângulo típico: 21° ± 2°)
2. **Garganta**: Seção de diâmetro constante mínimo
3. **Seção Divergente**: Recuperação gradual do diâmetro (ângulo típico: 5° a 15°)

```
     ┌─────────────────────────────────────────┐
     │                                         │
D₁ ──┤         ╲                     ╱         ├── D₁
     │          ╲                   ╱          │
     │           ╲─────────────────╱           │
     │            └─── D₂ ───┘                │
     │                                         │
     └─────────────────────────────────────────┘

     ├─ Convergente ─┤─ Garganta ─┤─ Divergente ─┤
```

## Equações Fundamentais

### 1. Equação da Continuidade

Para um fluido incompressível em regime permanente:

```
Q = A₁v₁ = A₂v₂ = constante
```

Onde:

- Q = vazão volumétrica (m³/s)
- A₁, A₂ = áreas das seções 1 e 2 (m²)
- v₁, v₂ = velocidades médias nas seções 1 e 2 (m/s)

### 2. Equação de Bernoulli

Para escoamento sem perdas entre dois pontos em um tubo horizontal:

```
P₁/ρg + v₁²/2g + z₁ = P₂/ρg + v₂²/2g + z₂
```

Para tubo horizontal (z₁ = z₂):

```
P₁/ρg + v₁²/2g = P₂/ρg + v₂²/2g
```

### 3. Queda de Pressão (Ideal)

Combinando as equações acima:

```
ΔP = P₁ - P₂ = ½ρ(v₂² - v₁²)
```

Substituindo pela continuidade:

```
ΔP = ½ρQ²[(1/A₂²) - (1/A₁²)]
```

### 4. Equação do Medidor (Real)

Considerando perdas e introduzindo o coeficiente de descarga Cd:

```
Q = Cd·A₂·√[2ΔP / (ρ(1 - β⁴))]
```

Onde:

- β = D₂/D₁ (razão de diâmetros)
- Cd = coeficiente de descarga (tipicamente 0.95-0.99)

### 5. Relação com Manômetro Diferencial

O desnível Δh em um manômetro em U é dado por:

```
Δh = ΔP / [(ρₘ - ρ)g]
```

Onde:

- ρₘ = densidade do fluido manométrico (kg/m³)
- ρ = densidade do fluido em escoamento (kg/m³)
- g = aceleração da gravidade (m/s²)

### 6. Vazão a partir do Desnível

Combinando as equações:

```
Q = Cd·A₂·√[2g·Δh·(ρₘ - ρ) / (ρ(1 - β⁴))]
```

## Perdas de Energia

### Perda de Carga

No escoamento real, há perdas de energia por atrito. A perda de carga total pode ser calculada pela fórmula de Darcy-Weisbach:

```
hₗ = f·(L/D)·(v²/2g)
```

Onde:

- f = coeficiente de atrito (adimensional)
- L = comprimento do tubo (m)
- D = diâmetro hidráulico (m)
- v = velocidade média (m/s)

### Equação de Bernoulli Modificada

Incluindo perdas:

```
P₁/(ρg) + v₁²/(2g) + z₁ = P₂/(ρg) + v₂²/(2g) + z₂ + hₗ
```

## Linhas de Energia

### Linha de Energia (LE)

Representa a energia total por unidade de peso:

```
LE = P/(ρg) + v²/(2g) + z
```

- No escoamento ideal: LE é constante (horizontal)
- No escoamento real: LE decresce na direção do fluxo

### Linha Piezométrica (LP)

Representa a carga piezométrica:

```
LP = P/(ρg) + z
```

A distância vertical entre LE e LP representa a carga cinética (v²/2g).

## Coeficiente de Descarga (Cd)

O coeficiente de descarga é a razão entre a vazão real e a vazão teórica:

```
Cd = Q_real / Q_teórico
```

### Fatores que Afetam Cd:

1. **Número de Reynolds**: Cd aumenta com Re, estabilizando para Re > 10⁵
2. **Razão β**: Cd varia com a razão D₂/D₁
3. **Rugosidade**: Superfícies mais lisas → Cd maior
4. **Geometria**: Ângulos de convergência/divergência

### Valores Típicos:

- Venturi de alta qualidade: Cd = 0.98 - 0.99
- Venturi industrial: Cd = 0.95 - 0.97
- Venturi tosco: Cd = 0.90 - 0.95

## Número de Reynolds

O número de Reynolds indica o regime de escoamento:

```
Re = (ρvD)/μ = (vD)/ν
```

Onde:

- μ = viscosidade dinâmica (Pa·s)
- ν = viscosidade cinemática (m²/s)

### Regimes:

- **Laminar**: Re < 2300
- **Transição**: 2300 < Re < 4000
- **Turbulento**: Re > 4000

Para medidores de vazão, geralmente Re > 10⁴ é desejável.

## Vantagens do Medidor de Venturi

### Vantagens:

1. **Baixa Perda de Carga Permanente**

   - Recuperação de 80-95% da pressão
   - Economia de energia em sistemas de bombeamento

2. **Alta Precisão**

   - Erro típico: ±0.5% a ±1%
   - Calibrado: pode chegar a ±0.25%

3. **Robustez**

   - Adequado para fluidos com sólidos em suspensão
   - Sem partes móveis
   - Longa vida útil

4. **Ampla Faixa de Medição**

   - Rangeability típico: 4:1 a 10:1
   - Funciona em ampla faixa de Reynolds

5. **Sem Manutenção**
   - Não requer calibração frequente
   - Resistente ao desgaste

### Desvantagens:

1. **Alto Custo Inicial**

   - Fabricação cara devido à precisão geométrica
   - Instalação mais complexa

2. **Tamanho**

   - Requer espaço considerável (5-20 diâmetros)
   - Peso elevado

3. **Tempo de Instalação**
   - Requer trechos retos antes e depois
   - Montagem cuidadosa

## Comparação com Outros Medidores

| Característica | Venturi        | Placa de Orifício | Bocal          |
| -------------- | -------------- | ----------------- | -------------- |
| Perda de Carga | Baixa (5-20%)  | Alta (40-90%)     | Média (30-60%) |
| Custo          | Alto           | Baixo             | Médio          |
| Precisão       | Alta (±0.5-1%) | Média (±2-5%)     | Boa (±1-2%)    |
| Manutenção     | Mínima         | Frequente         | Moderada       |
| Espaço         | Grande         | Pequeno           | Médio          |
| Sólidos        | Adequado       | Inadequado        | Parcial        |

## Aplicações Industriais

### Indústrias:

1. **Tratamento de Água**

   - Medição de vazão em estações de tratamento
   - Sistemas de distribuição

2. **Petróleo e Gás**

   - Medição em refinarias
   - Gasodutos e oleodutos

3. **Química e Petroquímica**

   - Processos com fluidos corrosivos
   - Alta precisão requerida

4. **Geração de Energia**

   - Sistemas de refrigeração
   - Circuitos de água

5. **Mineração**
   - Transporte de polpa
   - Fluidos com sólidos

## Instalação e Considerações Práticas

### Requisitos de Instalação:

1. **Trechos Retos**

   - Montante: 5-20 diâmetros
   - Jusante: 3-5 diâmetros

2. **Alinhamento**

   - Perfeitamente horizontal ou vertical
   - Sem inclinações

3. **Tomadas de Pressão**

   - Localizadas precisamente
   - Sem vazamentos

4. **Manômetro**
   - Apropriado para a faixa de medição
   - Livre de bolhas de ar

### Manutenção:

- Inspeção periódica das tomadas de pressão
- Verificação de vazamentos
- Limpeza quando necessário
- Recalibração conforme normas

## Normas e Padrões

### Principais Normas:

- **ISO 5167**: Medição de vazão de fluidos
- **ASME MFC-3M**: Medidores de vazão
- **ABNT NBR**: Normas brasileiras

### Requisitos:

- Razão β: 0.3 ≤ β ≤ 0.75
- Número de Reynolds: Re > 2×10⁴
- Ângulo de convergência: 21° ± 2°
- Ângulo de divergência: 5° a 15°

## Cálculo de Incertezas

A incerteza na medição de vazão depende de:

1. **Incerteza em Cd**: Tipicamente ±0.5%
2. **Incerteza em ΔP**: Depende do manômetro (±0.1% a ±1%)
3. **Incerteza nas dimensões**: ±0.05% para Venturi calibrado
4. **Incerteza em ρ**: Depende da temperatura (±0.1% típico)

### Incerteza Total:

```
u_Q/Q = √[(u_Cd/Cd)² + (u_A/A)² + 0.25(u_ΔP/ΔP)² + 0.25(u_ρ/ρ)²]
```

## Exemplos Numéricos

### Exemplo 1: Cálculo de Vazão

**Dados:**

- D₁ = 0.10 m, D₂ = 0.05 m
- ρ = 1000 kg/m³ (água)
- ρₘ = 13600 kg/m³ (mercúrio)
- Δh = 0.15 m
- Cd = 0.98

**Solução:**

```
β = 0.05/0.10 = 0.5
A₂ = π(0.05)²/4 = 0.001963 m²

Q = 0.98 × 0.001963 × √[2×9.81×0.15×(13600-1000)/(1000×(1-0.5⁴))]
Q = 0.001963 × √[18.63] = 0.0146 m³/s = 14.6 L/s
```

### Exemplo 2: Cálculo de Desnível

**Dados:**

- D₁ = 0.10 m, D₂ = 0.05 m
- Q = 0.015 m³/s
- ρ = 1000 kg/m³
- ρₘ = 13600 kg/m³

**Solução:**

```
v₁ = Q/A₁ = 0.015/0.007854 = 1.91 m/s
v₂ = Q/A₂ = 0.015/0.001963 = 7.64 m/s

ΔP = 0.5×1000×(7.64² - 1.91²) = 27348 Pa

Δh = 27348/[(13600-1000)×9.81] = 0.221 m = 22.1 cm
```

## Referências

1. Fox, R. W., McDonald, A. T., & Pritchard, P. J. (2010). _Introdução à Mecânica dos Fluidos_. 7ª ed. LTC.

2. White, F. M. (2011). _Fluid Mechanics_. 7th ed. McGraw-Hill.

3. Çengel, Y. A., & Cimbala, J. M. (2015). _Mecânica dos Fluidos: Fundamentos e Aplicações_. 3ª ed. AMGH.

4. ISO 5167-4 (2003). _Measurement of fluid flow by means of pressure differential devices - Part 4: Venturi tubes_.

5. Miller, R. W. (1996). _Flow Measurement Engineering Handbook_. 3rd ed. McGraw-Hill.

---

**Nota:** Este documento serve como referência teórica para o simulador interativo de medidor de Venturi. Para aplicações práticas, consulte as normas técnicas específicas e profissionais qualificados.
