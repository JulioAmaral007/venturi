# 📁 Estrutura do Projeto

## 🎯 Aplicação Principal

```
app.py                    # 🌐 Aplicação Streamlit (EXECUTAR ESTE)
```

**Como executar:**

```bash
streamlit run app.py
```

---

## 📦 Arquivos do Projeto

```
hisdrostatica/
│
├── 🎯 APLICAÇÃO
│   └── app.py                    # Aplicação web principal
│
├── 📝 EXEMPLOS
│   └── exemplo_uso.py            # Exemplos de uso programático
│
├── 📚 DOCUMENTAÇÃO
│   ├── README.md                 # Visão geral e início rápido
│   ├── QUICK_START.md            # 3 passos para começar
│   ├── GUIA_STREAMLIT.md         # Guia completo e detalhado
│   ├── Venturi.md                # Teoria e fundamentos
│   └── ESTRUTURA.md              # Este arquivo
│
├── ⚙️ CONFIGURAÇÃO
│   ├── requirements.txt          # Dependências do projeto
│   └── .streamlit/
│       └── config.toml           # Configurações do Streamlit
│
└── 📊 DADOS (criado em tempo de execução)
    └── .streamlit/
        └── cache/                # Cache de performance
```

---

## 📋 Descrição dos Arquivos

### Aplicação

**`app.py`**

- Aplicação web principal
- Interface interativa com Streamlit
- 3 modos: Ideal, Realista, Medidor
- 4 visualizações gráficas

### Documentação

**`README.md`**

- Visão geral do projeto
- Início rápido (3 passos)
- Exemplos práticos
- Deploy e compartilhamento

**`QUICK_START.md`**

- Guia ultra-rápido
- Apenas o essencial para começar

**`GUIA_STREAMLIT.md`**

- Documentação completa
- Todos os recursos
- Personalização e troubleshooting

**`Venturi.md`**

- Fundamentação teórica
- Equações implementadas
- Conceitos de mecânica dos fluidos

### Código

**`exemplo_uso.py`**

- Exemplos de uso programático
- 5 exemplos diferentes:
  1. Comparação Ideal vs Realista
  2. Curva de calibração
  3. Modo Medidor
  4. Sensibilidade ao Cd
  5. Efeito do Beta (β)

### Configuração

**`requirements.txt`**

- Lista de dependências Python
- NumPy, Matplotlib, Streamlit

**`.streamlit/config.toml`**

- Configurações personalizadas
- Tema, cores, comportamento

---

## 🚀 Comandos Essenciais

### Executar Aplicação

```bash
streamlit run app.py
```

### Instalar Dependências

```bash
pip install -r requirements.txt
```

### Executar Exemplos

```bash
python exemplo_uso.py
```

---

## 📊 Estatísticas

- **Arquivos Python:** 2
- **Linhas de código:** ~500
- **Documentação:** 4 arquivos
- **Modos de operação:** 3
- **Parâmetros ajustáveis:** 9
- **Gráficos:** 4

---

## 🎯 Ordem de Leitura Sugerida

### Para Iniciantes:

1. `README.md` → Visão geral
2. `QUICK_START.md` → Começar rapidamente
3. Execute `streamlit run app.py`
4. Explore a interface!

### Para Aprofundamento:

1. `GUIA_STREAMLIT.md` → Recursos completos
2. `Venturi.md` → Teoria
3. `exemplo_uso.py` → Uso programático

---

## 📁 Arquivos Gerados

Durante a execução, podem ser criados:

```
.streamlit/
└── cache/          # Cache de performance (automático)
```

Estes arquivos são seguros para deletar (serão recriados).

---

**Versão:** 2.0 (Streamlit Only)  
**Status:** ✅ Limpo e Organizado  
**Data:** Outubro 2025
