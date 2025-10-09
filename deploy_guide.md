# 🚀 Guia de Deploy - Simulador de Venturi

## Opção 1: Streamlit Cloud (GRATUITO) ⭐ RECOMENDADO

### Pré-requisitos:
- Conta no GitHub
- Código no repositório GitHub

### Passos:

1. **Criar repositório no GitHub:**
   ```bash
   git init
   git add .
   git commit -m "Simulador de Venturi - Streamlit App"
   git branch -M main
   git remote add origin https://github.com/SEU_USUARIO/simulador-venturi.git
   git push -u origin main
   ```

2. **Acessar Streamlit Cloud:**
   - Vá para: https://share.streamlit.io/
   - Faça login com sua conta GitHub

3. **Deploy:**
   - Clique em "New app"
   - Selecione seu repositório
   - Branch: `main`
   - Main file path: `app.py`
   - Clique em "Deploy!"

### Vantagens:
- ✅ Totalmente gratuito
- ✅ Deploy automático ao fazer push
- ✅ HTTPS automático
- ✅ Sem configuração de servidor

---

## Opção 2: Heroku

### Arquivos necessários:

**Procfile:**
```
web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
```

**runtime.txt:**
```
python-3.11.0
```

### Comandos:
```bash
# Instalar Heroku CLI
# Criar app
heroku create seu-app-venturi

# Deploy
git push heroku main
```

---

## Opção 3: Railway

1. Conecte conta GitHub
2. Selecione repositório
3. Deploy automático

---

## Opção 4: Render

1. Conecte GitHub
2. Selecione repositório
3. Configuração automática

---

## Opção 5: VPS/Cloud Provider

### Para AWS/GCP/Azure:
- Use Docker
- Configure nginx
- SSL com Let's Encrypt

### Dockerfile:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.address", "0.0.0.0"]
```

---

## 🎯 RECOMENDAÇÃO

**Para começar rapidamente:** Use **Streamlit Cloud**
**Para produção:** Use **Railway** ou **Render**
**Para controle total:** Use **VPS** com Docker
