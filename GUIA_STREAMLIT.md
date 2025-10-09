# 📚 Guia Completo - Simulador de Venturi

## 📖 Sobre esta Aplicação

Esta é uma aplicação web interativa desenvolvida com **Streamlit** para simulação e análise de medidores de Venturi. Streamlit permite criar interfaces web profissionais usando apenas Python, sem necessidade de HTML, CSS ou JavaScript.

---

## 🚀 Instalação e Execução

### Requisitos

- Python 3.8 ou superior
- Conexão com internet (apenas para instalação)

### Instalação

```bash
# Instalar todas as dependências
pip install -r requirements.txt

# OU instalar manualmente
pip install streamlit numpy matplotlib
```

### Verificar Instalação

```bash
streamlit --version
# Deve mostrar: Streamlit, version 1.28.0 ou superior
```

### Executar Aplicação

```bash
streamlit run app.py
```

**O que acontece:**

1. ⏳ Servidor web local inicia (3-5 segundos)
2. 🌐 Navegador abre automaticamente
3. 📊 Interface pronta em `http://localhost:8501`

---

## 🎨 Usando a Interface

### Sidebar (Barra Lateral Esquerda)

#### 🎯 Modo de Operação

**Ideal**

- Escoamento sem perdas
- Baseia-se na equação de Bernoulli pura
- Linha de energia constante

**Realista**

- Inclui perdas de carga por atrito
- Usa coeficiente de descarga (Cd)
- Visualização das perdas de energia

**Medidor**

- Calcula vazão a partir do desnível medido
- Simula operação real de um medidor
- Entrada: Δh → Saída: Q

#### 📐 Parâmetros Geométricos

- **D₁ (m):** Diâmetro de entrada (0.05 - 0.30 m)
- **D₂ (m):** Diâmetro da garganta (0.02 - 0.15 m)
- **L (m):** Comprimento total (0.5 - 3.0 m)

⚠️ **Importante:** D₂ deve ser sempre menor que D₁

#### 💧 Propriedades dos Fluidos

- **ρ (kg/m³):** Densidade do fluido escoando
  - Água: 1000 kg/m³
  - Óleo: 850-900 kg/m³
- **ρₘ (kg/m³):** Densidade do fluido manométrico
  - Mercúrio: 13600 kg/m³
  - Óleo: 850 kg/m³

#### 🌊 Condições de Escoamento

**Modos Ideal e Realista:**

- **Q (m³/s):** Vazão volumétrica (0.001 - 0.05 m³/s)
- O desnível Δh é calculado automaticamente

**Modo Medidor:**

- **Δh (m):** Desnível manométrico (0.01 - 0.5 m)
- A vazão Q é calculada automaticamente

#### 🔧 Parâmetros Avançados

- **f:** Coeficiente de atrito (0.01 - 0.10)
  - Típico: 0.02
- **Cd:** Coeficiente de descarga (0.90 - 1.00)
  - Venturi bem projetado: 0.98
  - Ideal: 1.00

---

### Área Principal

#### 📊 Métricas (Topo)

Quatro cards mostram os resultados principais:

1. **Vazão Q**

   - Valor em L/s
   - Valor em m³/h (abaixo)

2. **Desnível Δh**

   - Valor em cm
   - Valor em m (abaixo)

3. **Velocidade v₁**

   - Velocidade na entrada (m/s)

4. **Velocidade v₂**
   - Velocidade na garganta (m/s)

#### 📑 Abas de Visualização

**1. 📐 Diagrama**

- Desenho esquemático do Venturi
- Indicação dos pontos de medição
- Velocidades em cada ponto

**2. 🔬 Manômetro**

- Visualização do tubo em U
- Indicação visual do desnível Δh
- Cores diferenciadas para fluidos

**3. 📈 Pressão**

- Gráfico de pressão ao longo do tubo
- Visualização da queda de pressão
- Recuperação de pressão no difusor

**4. ⚡ Energia**

- Linha de Energia (LE)
- Linha Piezométrica (LP)
- Visualização de perdas (modo Realista)

**5. 📋 Resultados**

- Todos os dados numéricos
- Geometria, velocidades, pressões
- Número de Reynolds
- Indicador de regime de escoamento

---

## 🎓 Exemplos Práticos

### Exemplo 1: Análise Básica (Modo Ideal)

**Objetivo:** Entender o comportamento ideal do Venturi

```
1. Execute: streamlit run app.py
2. Configurações:
   - Modo: Ideal
   - D₁: 0.10 m
   - D₂: 0.05 m
   - Q: 0.015 m³/s
3. Observe:
   - v₁ ≈ 1.9 m/s
   - v₂ ≈ 7.6 m/s
   - Δh ≈ 12 cm
   - Sem perdas de energia
```

### Exemplo 2: Efeito das Perdas (Modo Realista)

**Objetivo:** Comparar ideal vs realista

```
1. Mesmo setup do Exemplo 1
2. Mude para Modo: Realista
3. Configure:
   - f: 0.025
   - Cd: 0.96
4. Observe:
   - Δh ligeiramente maior
   - Perda de energia visível na aba Energia
   - Diferença = efeito das perdas
```

### Exemplo 3: Usar como Medidor

**Objetivo:** Calcular vazão a partir de medição

```
Situação: Você mediu Δh = 15 cm no manômetro
```

```
1. Modo: Medidor
2. Configurações:
   - Δh: 0.15 m
   - Cd: 0.98 (Venturi calibrado)
   - D₁: 0.10 m
   - D₂: 0.05 m
3. Resultado:
   - Q ≈ 18 L/s
```

### Exemplo 4: Análise de Sensibilidade

**Objetivo:** Entender efeito do β = D₂/D₁

```
Teste 1: β = 0.3 (D₁=10cm, D₂=3cm)
- Alta sensibilidade
- Grande Δh para mesma vazão
- Mais perda de carga

Teste 2: β = 0.5 (D₁=10cm, D₂=5cm) ✅ RECOMENDADO
- Boa sensibilidade
- Perdas moderadas

Teste 3: β = 0.7 (D₁=10cm, D₂=7cm)
- Baixa sensibilidade
- Pequeno Δh
- Menos perdas
```

---

## 🌐 Compartilhamento e Deploy

### 1. Rede Local (LAN)

```bash
# Execute normalmente
streamlit run app.py

# No terminal, procure por:
# Network URL: http://192.168.1.100:8501

# Compartilhe esse endereço!
```

Qualquer dispositivo na mesma rede pode acessar.

### 2. Deploy Online (Streamlit Cloud - GRÁTIS)

**Passo a Passo:**

1. **Preparar Repositório**

   ```bash
   git add .
   git commit -m "Simulador de Venturi"
   git push origin main
   ```

2. **Acessar Streamlit Cloud**

   - Visite: https://streamlit.io/cloud
   - Faça login com GitHub

3. **Criar App**

   - Clique em "New app"
   - Selecione seu repositório
   - Branch: main
   - Main file: app.py
   - Clique "Deploy"

4. **Resultado**
   - URL pública: `https://seu-app.streamlit.app`
   - Compartilhe com qualquer pessoa!
   - Gratuito para projetos públicos

---

## 📱 Acesso Mobile

A interface é totalmente responsiva!

### Como acessar do celular:

1. **Na mesma rede WiFi:**

   ```
   Execute no PC e use o Network URL
   http://192.168.x.x:8501
   ```

2. **Online:**

   ```
   Após deploy, acesse o link Streamlit Cloud
   https://seu-app.streamlit.app
   ```

3. **Funciona perfeitamente em:**
   - 📱 iPhone/Android
   - 📟 Tablets
   - 💻 Notebooks
   - 🖥️ Desktops

---

## ⚙️ Personalização

### Tema (Claro/Escuro)

1. Clique em `⚙️` (canto superior direito)
2. `Settings` → `Choose app theme`
3. Escolha: Light / Dark / Custom

### Modificar Código

Edite `app.py` para adicionar recursos:

**Adicionar novo gráfico:**

```python
def plotar_novo_grafico(sim):
    fig, ax = plt.subplots(figsize=(10, 5))
    # Seu código aqui
    return fig

# No main():
with tab6:  # Adicionar nova aba
    st.subheader("Novo Gráfico")
    fig = plotar_novo_grafico(sim)
    st.pyplot(fig)
```

**Exportar dados:**

```python
import pandas as pd

# Criar DataFrame
dados = {
    'Q (L/s)': [sim.Q * 1000],
    'Δh (cm)': [sim.delta_h * 100],
    # ... mais dados
}
df = pd.DataFrame(dados)

# Botão de download
st.download_button(
    "📥 Baixar Dados",
    df.to_csv(index=False),
    "resultados.csv",
    "text/csv"
)
```

---

## ⚡ Dicas de Performance

### Cache de Cálculos

Use `@st.cache_data` para funções pesadas:

```python
@st.cache_data
def calcular_curva_calibracao(vazoes):
    resultados = []
    for q in vazoes:
        # Cálculos...
        resultados.append(...)
    return resultados
```

### Session State

Para manter dados entre interações:

```python
if 'historico' not in st.session_state:
    st.session_state.historico = []

st.session_state.historico.append(sim.Q)
```

---

## 🐛 Solução de Problemas

### Erro: "Streamlit não encontrado"

```bash
pip install --upgrade streamlit
```

### Erro: "Porta 8501 em uso"

```bash
# Use outra porta
streamlit run app.py --server.port 8502
```

### Gráficos não aparecem

- Use `st.pyplot(fig)` não `plt.show()`
- Sempre feche figuras: `plt.close(fig)`

### App está lento

- Reduza pontos nos gráficos
- Use `@st.cache_data`
- Feche outras abas do navegador

### Navegador não abre

- Abra manualmente: `http://localhost:8501`
- Verifique firewall

---

## 📚 Recursos Adicionais

### Documentação Oficial

- **Streamlit:** https://docs.streamlit.io
- **NumPy:** https://numpy.org/doc/
- **Matplotlib:** https://matplotlib.org/

### Tutoriais Streamlit

- Getting Started: https://docs.streamlit.io/get-started
- Galeria de Apps: https://streamlit.io/gallery

### Exemplos Prontos

```bash
# Ver demos do Streamlit
streamlit hello
```

---

## 💡 Ideias de Expansão

### Nível Fácil

- [ ] Adicionar fluidos pré-configurados (dropdown)
- [ ] Botão "Reset" para valores padrão
- [ ] Mais temas personalizados
- [ ] Unidades alternativas (imperial)

### Nível Médio

- [ ] Exportar gráficos como PNG
- [ ] Gerar curva de calibração automática
- [ ] Comparar múltiplos cenários lado a lado
- [ ] Histórico de simulações

### Nível Avançado

- [ ] Animação do escoamento
- [ ] Upload de dados experimentais (CSV)
- [ ] Análise de incertezas
- [ ] Comparação com outros medidores (placa de orifício)
- [ ] API REST para integrações

---

## 🎯 Comandos Úteis

```bash
# Executar
streamlit run app.py

# Executar em porta específica
streamlit run app.py --server.port 8080

# Executar sem abrir navegador
streamlit run app.py --server.headless true

# Executar permitindo acesso externo
streamlit run app.py --server.address 0.0.0.0

# Ver configurações
streamlit config show

# Limpar cache
streamlit cache clear
```

---

## 📞 Suporte

- **Teoria:** [Venturi.md](Venturi.md)
- **Exemplos:** [exemplo_uso.py](exemplo_uso.py)
- **README:** [README.md](README.md)

---

**🎉 Aproveite o simulador!**

Streamlit torna a análise de medidores de Venturi interativa, moderna e acessível para todos.
