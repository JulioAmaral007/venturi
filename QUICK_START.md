# ⚡ Início Rápido

## 🚀 3 Passos

### 1. Instalar

```bash
pip install -r requirements.txt
```

### 2. Executar

```bash
streamlit run app.py
# título principal só aparece no modo "Simulação Interativa"
```

### 3. Usar

Interface abre em `http://localhost:8501` 🎉

---

## 📱 Primeira Simulação

1. **Escolha o modo** na sidebar:

   - `Ideal`: Sem perdas
   - `Realista`: Com perdas
   - `Medidor`: Calcular vazão

2. **Ajuste os parâmetros** com os sliders

3. **Veja os resultados** nas abas!

---

## 🎯 Exemplo Prático (Δh → Q)

**Calcular vazão com Δh = 12 cm:**

1. Modo: `Medidor`
2. Δh: `0.12 m`
3. Veja o resultado! ≈ 14 L/s

Observação: a interface agora foi modularizada (simulador/plots/exemplos em `app_modules/`).

---

## 🌐 Compartilhar

### Rede Local:

Execute e use o `Network URL` mostrado no terminal

### Online:

Deploy grátis em [streamlit.io/cloud](https://streamlit.io/cloud)

---

## ❓ Problemas?

**Streamlit não encontrado:**

```bash
pip install streamlit
```

**Porta em uso:**

```bash
streamlit run app.py --server.port 8502
```

---

## 📚 Quer mais?

- **Guia Completo:** [GUIA_STREAMLIT.md](GUIA_STREAMLIT.md)
- **Teoria:** [Venturi.md](Venturi.md)
- **Exemplos:** [exemplo_uso.py](exemplo_uso.py)

---

**🎉 Pronto para começar!**

```bash
streamlit run app.py
```
