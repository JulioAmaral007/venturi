# 🔬 Simulador de Medidor de Venturi

**Aplicação web interativa para simulação e análise de medidores de Venturi**

Desenvolvido com Python + Streamlit | Interface moderna e responsiva

---

## 🚀 Início Rápido (3 passos)

### 1️⃣ Instalar dependências

```bash
pip install -r requirements.txt
```

### 2️⃣ Executar aplicação

```bash
streamlit run app.py
```

### 3️⃣ Usar!

O navegador abre automaticamente em `http://localhost:8501` 🎉

---

## 📋 Sobre o Projeto

Este simulador implementa três modos operacionais para análise completa de medidores de Venturi:

### 🎯 Modos de Operação

1. **Modo Ideal** - Escoamento sem perdas (Bernoulli puro)
2. **Modo Realista** - Inclui perdas de carga e coeficiente de descarga
3. **Modo Medidor** - Calcula vazão a partir do desnível manométrico

### ✨ Recursos

- ✅ Interface web moderna e responsiva
- ✅ 9 parâmetros ajustáveis via sliders
- ✅ 4 visualizações gráficas dinâmicas
- ✅ Resultados em tempo real
- ✅ Funciona em desktop, tablet e celular
- ✅ Pode ser hospedado online gratuitamente

---

## 📊 Interface

### Sidebar (Controles)

- Seleção de modo
- Parâmetros geométricos (D₁, D₂, L)
- Propriedades dos fluidos (ρ, ρₘ)
- Condições de escoamento (Q ou Δh)
- Parâmetros avançados (f, Cd)

### Área Principal

- **Métricas:** Vazão, Desnível, Velocidades
- **Abas:**
  - 📐 Diagrama do Venturi
  - 🔬 Manômetro em U
  - 📈 Perfil de Pressão
  - ⚡ Linhas de Energia
  - 📋 Resultados Completos

---

## 🎓 Exemplo de Uso

### Calcular vazão a partir do desnível medido

Você mediu **Δh = 12 cm** no manômetro. Qual a vazão?

```bash
# 1. Execute o app
streamlit run app.py

# 2. Na interface:
#    - Modo: Medidor
#    - Δh: 0.12 m
#    - Cd: 0.98

# 3. Resultado automático:
#    Q ≈ 14-15 L/s
```

---

## 🌐 Compartilhar e Deploy

### Na Rede Local

```bash
# Execute e compartilhe o Network URL
streamlit run app.py
```

Outros dispositivos na mesma rede podem acessar via `http://SEU_IP:8501`

### Online (Grátis)

1. Acesse [streamlit.io/cloud](https://streamlit.io/cloud)
2. Conecte seu repositório GitHub
3. Deploy com 1 clique
4. Compartilhe o link público!

---

## 📐 Fundamentação Teórica

### Equações Implementadas

**Equação da Continuidade:**

```
Q = A₁v₁ = A₂v₂
```

**Equação de Bernoulli (Ideal):**

```
P₁/(ρg) + v₁²/(2g) = P₂/(ρg) + v₂²/(2g)
```

**Equação do Medidor de Venturi:**

```
Q = Cd·A₂·√[2gΔh(ρₘ-ρ) / (ρ(1-(A₂/A₁)²))]
```

**Desnível Manométrico:**

```
Δh = ΔP / ((ρₘ - ρ)g)
```

**Perda de Carga (Darcy-Weisbach):**

```
hₗ = f(L/D)(v²/2g)
```

📖 **Teoria completa:** [Venturi.md](Venturi.md)

---

## 🔧 Tecnologias

- **Python 3.8+** - Linguagem de programação
- **Streamlit** - Framework web interativo
- **NumPy** - Cálculos numéricos
- **Matplotlib** - Visualizações gráficas

---

## 📁 Estrutura do Projeto

```
hisdrostatica/
├── app.py                 # 🎯 Aplicação principal
├── exemplo_uso.py         # 📝 Exemplos programáticos
├── requirements.txt       # 📦 Dependências
├── README.md             # 📖 Este arquivo
├── GUIA_STREAMLIT.md     # 📚 Guia detalhado
└── Venturi.md            # 🎓 Teoria completa
```

---

## 💻 Uso Programático

Além da interface web, você pode usar o simulador em scripts Python:

```python
from app import VenturiSimulator

# Criar simulador
sim = VenturiSimulator()

# Configurar
sim.calcular(
    D1=0.10, D2=0.05, L=1.0,
    rho=1000, rho_m=13600,
    Q=0.015, delta_h=0,
    f=0.02, Cd=0.98,
    mode='Ideal'
)

# Resultados
print(f"v₁ = {sim.v1:.3f} m/s")
print(f"v₂ = {sim.v2:.3f} m/s")
print(f"Δh = {sim.delta_h*100:.2f} cm")
```

📝 **Mais exemplos:** [exemplo_uso.py](exemplo_uso.py)

---

## 🎨 Personalização

### Mudar Tema

1. Execute o app
2. Clique em `⚙️ Settings` (canto superior direito)
3. `Choose app theme` → Light/Dark

### Modificar Código

Edite `app.py` para:

- Adicionar novos gráficos
- Incluir mais fluidos
- Exportar dados
- Customizar visual

---

## 📱 Acesso Mobile

A aplicação é totalmente responsiva!

1. Execute no computador
2. Veja o `Network URL` no terminal
3. Acesse do celular/tablet
4. Use normalmente! 📱

---

## 🐛 Solução de Problemas

### "Streamlit não encontrado"

```bash
pip install streamlit
```

### "Porta em uso"

```bash
streamlit run app.py --server.port 8502
```

### Navegador não abre

Abra manualmente: `http://localhost:8501`

### App lento

- Reduza resolução dos gráficos
- Feche outras abas do navegador
- Reinicie o servidor (Ctrl+C e execute novamente)

---

## 🎯 Aplicações

### Educação

- Ensino de Mecânica dos Fluidos
- Demonstrações em aula
- Trabalhos e exercícios

### Profissional

- Dimensionamento de medidores
- Análise de escoamentos
- Geração de curvas de calibração

### Pesquisa

- Validação de modelos teóricos
- Análise de sensibilidade
- Comparação de configurações

---

## 📚 Documentação

- **Início Rápido:** Este README
- **Guia Completo:** [GUIA_STREAMLIT.md](GUIA_STREAMLIT.md)
- **Teoria:** [Venturi.md](Venturi.md)
- **Exemplos:** [exemplo_uso.py](exemplo_uso.py)

---

## 🎓 Valores de Referência

### Fluidos Comuns

- Água (20°C): ρ = 1000 kg/m³
- Mercúrio: ρₘ = 13600 kg/m³
- Óleo: ρ ≈ 850-900 kg/m³

### Parâmetros Típicos

- Razão β = D₂/D₁: 0.4 - 0.7
- Coeficiente de descarga Cd: 0.95 - 0.99
- Reynolds mínimo: Re > 10⁴

### Vantagens do Venturi

- ✅ Perda de carga permanente baixa (5-20%)
- ✅ Alta precisão (erro < 1% quando calibrado)
- ✅ Adequado para fluidos com sólidos em suspensão
- ✅ Ampla faixa de medição

---

## 📄 Licença

MIT License - Livre para uso acadêmico e comercial

---

## 👨‍💻 Desenvolvimento

Desenvolvido para fins educacionais e de pesquisa em Mecânica dos Fluidos.

**Versão:** 2.0 (Streamlit)  
**Status:** ✅ Estável e funcional  
**Atualização:** Outubro 2025

---

## 🚀 Comece Agora!

```bash
# Clone/baixe o projeto
# Instale as dependências
pip install -r requirements.txt

# Execute!
streamlit run app.py
```

**🎉 Pronto! Interface abrirá automaticamente no navegador.**

---

**📞 Dúvidas?** Consulte [GUIA_STREAMLIT.md](GUIA_STREAMLIT.md) para documentação completa.
