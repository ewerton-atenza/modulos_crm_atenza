# 🚀 GUIA COMPLETO - CATÁLOGO ATENZA

## 📋 ÍNDICE

1. [Setup Inicial](#setup-inicial)
2. [Desenvolvimento Local](#desenvolvimento-local)
3. [Git & GitHub](#git--github)
4. [Deploy Automático](#deploy-automático)
5. [Fluxo de Trabalho](#fluxo-de-trabalho)
6. [Troubleshooting](#troubleshooting)

---

## 🔧 SETUP INICIAL

### 1. Pré-requisitos

✅ **Já instalados:**
- Docker Desktop
- Git
- VS Code

### 2. Baixar Projeto

Baixe o arquivo **`catalogo-atenza.zip`** e extraia.

### 3. Abrir no VS Code

```bash
cd catalogo-atenza
code .
```

O VS Code vai sugerir instalar extensões recomendadas → **Instalar todas!**

---

## 💻 DESENVOLVIMENTO LOCAL

### Iniciar Ambiente

```bash
# Abrir terminal no VS Code (Ctrl+`)
docker-compose up -d
```

Aguardar ~30 segundos para build inicial.

### Acessar Aplicação

Abrir navegador:
```
http://localhost:3000/?account_id=teste-atenza-123
```

### Verificar Funcionamento

1. **Abrir Console** (F12)
2. **Verificar mensagens:**
   - ✅ `🚀 Iniciando Supabase...`
   - ✅ `📋 Account ID: teste-atenza-123`
   - ✅ `✅ Account UUID: ...`
   - ✅ `✅ Dados carregados com sucesso!`

3. **Sem erros vermelhos!**

### Testar Funcionalidades

1. **Criar Categoria:**
   - Clicar "Nova Categoria"
   - Preencher: Nome, Ícone, Descrição
   - Salvar
   - ✅ Ver toast "Categoria salva!"

2. **Ver no Banco:**
   - https://supabase.atenza.digital
   - Login: `ewerton.atenza` / `atenza515351`
   - Table Editor → `categories`
   - ✅ Ver registro criado!

### Hot Reload

**Mudanças são refletidas automaticamente!**

1. Editar `src/index.html`
2. Salvar (Ctrl+S)
3. Recarregar navegador (F5)
4. ✅ Ver mudanças!

### Parar Ambiente

```bash
docker-compose down
```

---

## 📦 GIT & GITHUB

### Configurar Git (primeira vez)

```bash
git config --global user.name "Seu Nome"
git config --global user.email "seu@email.com"
```

### Inicializar Repositório

```bash
# Inicializar
git init

# Conectar ao GitHub
git remote add origin https://github.com/ewerton-atenza/modulos_crm_atenza.git

# Ver status
git status
```

### Fazer Commit

```bash
# Ver mudanças
git status

# Adicionar arquivos
git add .

# Commit
git commit -m "Feature: descrição da mudança"

# Push
git push origin main
```

**Atenção:** Push dispara deploy automático!

---

## 🚀 DEPLOY AUTOMÁTICO

### Configurar Secrets (APENAS 1 VEZ!)

#### 1. Gerar Chave SSH

```bash
ssh-keygen -t ed25519 -C "github-actions-catalogo" -f ~/.ssh/github_catalogo -N ""
```

Cria:
- `~/.ssh/github_catalogo` (privada)
- `~/.ssh/github_catalogo.pub` (pública)

#### 2. Adicionar Chave no Servidor

**Via hPanel File Manager:**
1. Navegar: `/home/u937514520/.ssh/`
2. Editar: `authorized_keys`
3. Adicionar no final:

```bash
# Ver chave pública
cat ~/.ssh/github_catalogo.pub
# Copiar TODO o conteúdo e colar no authorized_keys
```

#### 3. Configurar Secrets no GitHub

Acessar:
```
https://github.com/ewerton-atenza/modulos_crm_atenza/settings/secrets/actions
```

**Criar 3 Secrets:**

**Secret 1:**
- Name: `SSH_HOST`
- Value: `catalog.atenza.digital`

**Secret 2:**
- Name: `SSH_USER`
- Value: `u937514520`

**Secret 3:**
- Name: `SSH_PRIVATE_KEY`
- Value: Cole TODA a chave privada

```bash
# Ver chave privada
cat ~/.ssh/github_catalogo

# Copiar TUDO, incluindo:
# -----BEGIN OPENSSH PRIVATE KEY-----
# ...
# -----END OPENSSH PRIVATE KEY-----
```

### Testar Deploy Automático

```bash
# Fazer mudança simples
echo "<!-- teste deploy -->" >> src/index.html

# Commit
git add .
git commit -m "Test: CI/CD"

# Push (dispara deploy!)
git push origin main
```

### Acompanhar Deploy

```
https://github.com/ewerton-atenza/modulos_crm_atenza/actions
```

Workflow: **"Deploy para Hostinger"**

✅ Deploy completo em ~30 segundos!

### Verificar Produção

```
https://catalog.atenza.digital/?account_id=teste-atenza-123
```

---

## 🔄 FLUXO DE TRABALHO

### Workflow Diário

```
┌─────────────────────────────────────────────────┐
│                                                 │
│  1. VS Code: Editar src/index.html              │
│             ↓                                    │
│  2. Docker: localhost:3000 (testar)             │
│             ↓                                    │
│  3. Validar: Console sem erros                  │
│             ↓                                    │
│  4. Git: commit -m "Feature: X"                 │
│             ↓                                    │
│  5. Git: push origin main                       │
│             ↓                                    │
│  6. GitHub Actions: Deploy automático (~30s)    │
│             ↓                                    │
│  7. Produção: https://catalog.atenza.digital    │
│                                                 │
└─────────────────────────────────────────────────┘
```

### Exemplo Prático

**Tarefa:** Adicionar nova categoria

```bash
# 1. Iniciar Docker
docker-compose up -d

# 2. Abrir navegador
http://localhost:3000/?account_id=teste-atenza-123

# 3. Testar
- Criar categoria "Serviços"
- Verificar aparece na tela
- Verificar no Supabase

# 4. Tudo OK? Commit!
git add .
git commit -m "Feature: adiciona categoria Serviços"
git push origin main

# 5. Aguardar deploy (~30s)
# Ver em: https://github.com/ewerton-atenza/modulos_crm_atenza/actions

# 6. Validar produção
https://catalog.atenza.digital/?account_id=teste-atenza-123
```

---

## 🐛 TROUBLESHOOTING

### Docker não inicia

**Problema:** `Cannot connect to Docker daemon`

**Solução:**
1. Abrir Docker Desktop
2. Aguardar inicialização completa
3. Tentar novamente

### Porta 3000 ocupada

**Problema:** `port 3000 already in use`

**Solução:**
```bash
# Editar docker-compose.yml
# Trocar "3000:80" por "3001:80"
docker-compose up -d
# Acessar: localhost:3001
```

### Erros no Console

**Problema:** Erros JavaScript

**Solução:**
1. Abrir `src/index.html`
2. Procurar por syntax errors
3. Verificar aspas, vírgulas, parênteses
4. Salvar e recarregar

### Deploy falha

**Problema:** GitHub Actions falha

**Solução:**
1. Ver logs: GitHub → Actions → Último workflow
2. Verificar Secrets configurados
3. Testar SSH manual:
```bash
ssh -i ~/.ssh/github_catalogo u937514520@catalog.atenza.digital
```

### Git push rejeita

**Problema:** `rejected (non-fast-forward)`

**Solução:**
```bash
git pull origin main --rebase
git push origin main
```

### Mudanças não aparecem

**Problema:** Site não atualiza

**Solução:**
1. Hard reload: Ctrl+Shift+R
2. Limpar cache do navegador
3. Aguardar 1-2 minutos

---

## 📝 COMANDOS ÚTEIS

### Docker

```bash
# Iniciar
docker-compose up -d

# Parar
docker-compose down

# Ver logs
docker-compose logs -f

# Rebuild (após mudanças no Dockerfile)
docker-compose up -d --build

# Status
docker ps
```

### Git

```bash
# Status
git status

# Ver mudanças
git diff

# Histórico
git log --oneline -10

# Desfazer último commit (mantém mudanças)
git reset --soft HEAD~1

# Desfazer mudanças em arquivo
git checkout -- src/index.html
```

### Supabase (SQL)

```sql
-- Ver todas categorias
SELECT * FROM categories;

-- Ver categorias de um account
SELECT * FROM categories 
WHERE account_id = 'uuid-aqui';

-- Limpar tabela (CUIDADO!)
DELETE FROM categories;
```

---

## ✅ CHECKLIST - PRIMEIRO DEPLOY

Depois de configurar tudo:

- [ ] Docker Desktop rodando
- [ ] VS Code aberto
- [ ] `docker-compose up -d` executado
- [ ] localhost:3000 abrindo
- [ ] Console sem erros
- [ ] Modal abre e salva
- [ ] Supabase mostra dados
- [ ] Git configurado
- [ ] SSH keys geradas
- [ ] Chave pública no servidor
- [ ] 3 Secrets no GitHub
- [ ] Primeiro push feito
- [ ] GitHub Actions rodou OK
- [ ] Produção atualizada

---

## 🎯 PRÓXIMOS PASSOS

### Hoje (Setup)
- [x] Ambiente local funcionando
- [x] Docker rodando
- [x] Git configurado
- [ ] SSH keys configuradas
- [ ] Primeiro deploy automático

### Amanhã (Desenvolvimento)
- [ ] Adicionar funcionalidades
- [ ] Melhorias de UX
- [ ] Testes completos
- [ ] Deploy final

---

## 💡 DICAS

1. **Sempre teste local primeiro!**
2. **Commits pequenos e frequentes**
3. **Mensagens descritivas:** "Fix: bug X" / "Feature: Y"
4. **Monitore GitHub Actions** após push
5. **Mantenha backup** das chaves SSH

---

## 🆘 SUPORTE

Se travar, me avise com:
- Print do erro
- Comando que executou
- Logs do console
- Mensagem do GitHub Actions

---

**Ambiente pronto! Bora desenvolver!** 🚀
