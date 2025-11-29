sim# 🚀 Como Rodar o Projeto - Simulador de Medidor de Venturi

Este guia fornece instruções passo a passo para executar o simulador de medidor de Venturi em sua máquina.

## 📋 Pré-requisitos

Antes de começar, certifique-se de ter instalado:

- **Python 3.8 ou superior** (recomendado: Python 3.9+)
- **pip** (gerenciador de pacotes Python)
- **Git** (opcional, apenas se for clonar o repositório)

### Verificar instalação do Python

Abra o terminal (ou Prompt de Comando no Windows) e execute:

```bash
python --version
```

ou

```bash
python3 --version
```

Você deve ver algo como `Python 3.8.x` ou superior.

## 📦 Instalação

### 1. Clone ou baixe o projeto

Se você já tem o projeto, pule esta etapa. Caso contrário:

```bash
git clone <url-do-repositorio>
cd venturi
```

### 2. Criar ambiente virtual (Recomendado)

É uma boa prática usar um ambiente virtual para isolar as dependências do projeto:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

Quando o ambiente virtual estiver ativado, você verá `(venv)` no início da linha do terminal.

### 3. Instalar dependências

Com o ambiente virtual ativado, instale todas as dependências necessárias:

```bash
pip install -r requirements.txt
```

Isso instalará automaticamente:
- `numpy` - Cálculos numéricos
- `matplotlib` - Visualizações e gráficos
- `streamlit` - Framework web para a interface
- `pandas` - Manipulação de dados
- `thermo` - Propriedades termodinâmicas dos fluidos
- `fluids` - Cálculos de mecânica dos fluidos

**Nota:** A instalação pode levar alguns minutos dependendo da sua conexão com a internet.

## ▶️ Executar a Aplicação

### Método 1: Execução direta (Recomendado)

Com o ambiente virtual ativado e as dependências instaladas, execute:

```bash
streamlit run app.py
```

### Método 2: Especificando a porta

Se a porta padrão (8501) estiver em uso, você pode especificar outra porta:

```bash
streamlit run app.py --server.port 8502
```

### O que acontece?

Após executar o comando, você verá uma mensagem no terminal indicando que o servidor Streamlit está rodando. Algo como:

```
You can now view your Streamlit app in your browser.

Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

### Acessar a aplicação

1. O navegador deve abrir automaticamente
2. Se não abrir, copie o **Local URL** (geralmente `http://localhost:8501`) e cole no seu navegador
3. A interface do simulador será exibida

## 🎯 Usando o Simulador

### Interface Principal

A aplicação possui uma interface web interativa com:

- **Sidebar**: Controles para configurar parâmetros
- **Área principal**: Visualizações e resultados

### Passos básicos:

1. **Escolha o modo de simulação:**
   - **Ideal**: Sem perdas por atrito (modelo teórico)
   - **Realista**: Com perdas por atrito (modelo prático)

2. **Configure os parâmetros:**
   - Geometria (diâmetros D₁, D₂, comprimento L)
   - Fluido (água, ar, etanol, etc.)
   - Condições de escoamento (vazão ou velocidade)

3. **Visualize os resultados:**
   - Métricas principais (vazão, desnível, velocidades)
   - Gráficos interativos
   - Dados completos da simulação

## 🛠️ Solução de Problemas

### Erro: "streamlit: command not found"

**Causa:** Streamlit não está instalado ou o ambiente virtual não está ativado.

**Solução:**
```bash
pip install streamlit
```

Ou certifique-se de que o ambiente virtual está ativado antes de executar.

### Erro: "ModuleNotFoundError"

**Causa:** Alguma dependência não foi instalada corretamente.

**Solução:**
```bash
pip install -r requirements.txt --upgrade
```

### Erro: "Port already in use"

**Causa:** A porta 8501 já está sendo usada por outro processo.

**Solução:**
```bash
streamlit run app.py --server.port 8502
```

Ou feche o processo que está usando a porta 8501.

### Erro ao instalar dependências

**Causa:** Problemas com a conexão ou versão do pip.

**Solução:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Aplicação não abre no navegador

**Solução:**
1. Copie o URL exibido no terminal (ex: `http://localhost:8501`)
2. Cole no seu navegador
3. Certifique-se de que não há firewall bloqueando a conexão

## 📝 Estrutura do Projeto

```
venturi/
├── app.py                    # Aplicação principal Streamlit
├── app_modules/              # Módulos do simulador
│   ├── simulator.py         # Classe VenturiSimulator
│   └── plots.py             # Funções de visualização
├── assets/                   # Imagens e recursos
├── requirements.txt          # Dependências Python
└── README.md                 # Documentação geral
```

## 🔄 Atualizar o Projeto

Se você fez alterações no código ou quer atualizar as dependências:

1. **Atualizar dependências:**
```bash
pip install -r requirements.txt --upgrade
```

2. **Reiniciar a aplicação:**
   - Pare a aplicação (Ctrl+C no terminal)
   - Execute novamente: `streamlit run app.py`

## 📚 Recursos Adicionais

- **Documentação completa**: Veja `README.md` para mais informações sobre o projeto
- **Documentação técnica**: Consulte `Venturi.md` para fundamentação teórica
- **Streamlit**: Documentação oficial em https://docs.streamlit.io/

## 💡 Dicas

- Use o modo **Ideal** para entender os conceitos básicos
- Use o modo **Realista** para simulações mais próximas da realidade
- Experimente diferentes fluidos e temperaturas para ver como as propriedades afetam os resultados
- Ajuste a razão β (D₂/D₁) dentro da faixa recomendada (0.4 - 0.7) para melhores resultados

## ❓ Precisa de Ajuda?

Se encontrar problemas não listados aqui:

1. Verifique se todas as dependências estão instaladas corretamente
2. Certifique-se de estar usando Python 3.8 ou superior
3. Verifique os logs de erro no terminal para mais detalhes
4. Consulte a documentação do Streamlit: https://docs.streamlit.io/

---

**Desenvolvido para ensino de mecânica dos fluidos e instrumentação industrial** 🔬

