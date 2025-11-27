# 🚀 Deploy no Railway via Web Dashboard (SEM CLI)

## ✅ **Por Que Este Método?**

- ✅ **Sem problemas de CLI**
- ✅ **Tudo pelo navegador**
- ✅ **Mais visual e fácil**
- ✅ **Funciona em qualquer ambiente**

---

## 📋 **Pré-requisitos:**

- Conta no Railway (já criada)
- Conta no GitHub (para conectar o código)

---

## 🎯 **Passo a Passo Completo:**

### **1️⃣ Preparar o Código no GitHub**

#### **Opção A: Criar Repositório Novo (Recomendado)**

1. Acesse: https://github.com/new
2. Nome do repositório: `pricepro-backend`
3. Marque como **Private** (recomendado)
4. Clique em **"Create repository"**

5. No terminal VNC, execute:

```bash
cd /home/ubuntu/pricepro_backend

# Inicializar git (se ainda não foi feito)
git init

# Adicionar arquivos
git add .

# Fazer commit
git commit -m "Deploy inicial do PricePro Backend"

# Conectar ao repositório remoto
# SUBSTITUA 'seu-usuario' pelo seu username do GitHub
git remote add origin https://github.com/seu-usuario/pricepro-backend.git

# Enviar para o GitHub
git branch -M main
git push -u origin main
```

**⚠️ Se pedir credenciais do GitHub:**
- Username: seu username do GitHub
- Password: use um **Personal Access Token** (não a senha)
  - Crie um token em: https://github.com/settings/tokens
  - Marque: `repo` (Full control of private repositories)
  - Copie o token e use como senha

---

### **2️⃣ Criar Projeto no Railway**

1. Acesse: https://railway.app/new

2. Clique em **"Deploy from GitHub repo"**

3. Se for a primeira vez:
   - Clique em **"Configure GitHub App"**
   - Autorize o Railway a acessar seus repositórios
   - Selecione **"Only select repositories"**
   - Escolha o repositório `pricepro-backend`
   - Clique em **"Install & Authorize"**

4. Selecione o repositório `pricepro-backend`

5. Clique em **"Deploy Now"**

---

### **3️⃣ Adicionar PostgreSQL**

1. No dashboard do projeto, clique em **"+ New"**

2. Selecione **"Database"** → **"Add PostgreSQL"**

3. Aguarde o provisionamento (1-2 minutos)

4. O Railway vai criar automaticamente a variável `DATABASE_URL`

---

### **4️⃣ Configurar Variáveis de Ambiente**

1. Clique no seu serviço (card do backend)

2. Vá para a aba **"Variables"**

3. Clique em **"+ New Variable"** e adicione:

```env
SECRET_KEY=7GJEoJsaIcM8owxemRJIr598e8PysLxL
APP_NAME=PricePro
DEBUG=False
ALLOWED_ORIGINS=https://*.preview.abacusai.app,https://*.abacusai.app
REDIS_ENABLED=False
```

**⚠️ IMPORTANTE:**
- **NÃO** adicione `DATABASE_URL` manualmente
- O Railway já conectou automaticamente com o PostgreSQL

4. Clique em **"Deploy"** para aplicar as mudanças

---

### **5️⃣ Gerar Domínio Público**

1. Clique no seu serviço (card do backend)

2. Vá para a aba **"Settings"**

3. Role até **"Networking"**

4. Clique em **"Generate Domain"**

5. **COPIE A URL GERADA!** 🎯
   - Exemplo: `https://pricepro-backend-production-abc123.up.railway.app`

---

### **6️⃣ Verificar Deploy**

1. Clique na aba **"Deployments"**

2. Aguarde aparecer **"Success"** (pode levar 2-5 minutos)

3. Clique em **"View Logs"** para verificar se está tudo OK

Procure por:
```
✅ Uvicorn running on http://0.0.0.0:PORT
✅ Application startup complete
```

---

### **7️⃣ Testar Backend**

Abra no navegador (substitua pela sua URL):
```
https://sua-url-railway.up.railway.app/docs
```

Se aparecer a documentação do FastAPI (Swagger UI), **está funcionando!** 🎉

---

## 🎯 **Próximo Passo:**

### **ME ENVIE A URL DO RAILWAY!**

Depois eu vou:
1. ✅ Atualizar o `.env` do frontend
2. ✅ Fazer rebuild
3. ✅ Testar a conexão

**E tudo vai funcionar!** 🚀

---

## 🆘 **Problemas Comuns:**

### **❌ Deploy falhou**
➡️ Verifique os logs em **"Deployments"** → **"View Logs"**

### **❌ "Module not found"**
➡️ Certifique-se que o `requirements.txt` está correto

### **❌ "Cannot connect to database"**
➡️ Verifique se o PostgreSQL foi provisionado na aba **"Data"**

### **❌ "Port already in use"**
➡️ O Railway configura a porta automaticamente via `$PORT`

---

## 💡 **Dicas:**

- **Logs em tempo real:** Aba "Deployments" → "View Logs"
- **Redeploy manual:** Settings → "Redeploy"
- **Custos:** Dashboard → "Usage" (você tem $5/mês grátis)

---

## 📞 **Precisa de Ajuda?**

Se tiver qualquer erro:
1. Copie a mensagem de erro completa
2. Me envie aqui no chat
3. Vou te ajudar a resolver!
