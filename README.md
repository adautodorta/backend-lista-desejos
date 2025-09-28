# 🎯 Backend Lista de Desejos

Uma API RESTful desenvolvida em Python com Flask para gerenciar listas de desejos pessoais. O sistema permite que usuários autenticados criem, visualizem, atualizem e removam itens de suas listas de desejos, com funcionalidades de busca e autenticação JWT.

## 🚀 Funcionalidades

- **Autenticação JWT**: Sistema seguro de autenticação usando tokens JWT do Supabase
- **CRUD Completo**: Criar, ler, atualizar e deletar itens da lista de desejos
- **Busca Inteligente**: Pesquisar itens por nome com busca parcial
- **Multi-usuário**: Cada usuário possui sua própria lista de desejos isolada
- **Documentação Swagger**: API totalmente documentada e testável
- **CORS Habilitado**: Suporte para requisições cross-origin
- **Validação de Dados**: Validação robusta de entrada de dados

## 🛠️ Tecnologias Utilizadas

- **Python 3.13**
- **Flask** - Framework web
- **Flask-RESTful** - Extensão para APIs REST
- **Supabase** - Banco de dados e autenticação
- **JWT** - Autenticação via tokens
- **Swagger/Flasgger** - Documentação da API
- **Gunicorn** - Servidor WSGI para produção

## 📋 Pré-requisitos

- Python 3.13 ou superior
- Conta no Supabase
- Git

## 🔧 Instalação e Configuração

### 1. Clone o repositório
```bash
git clone <url-do-repositorio>
cd backend-lista-desejos
```

### 2. Crie e ative o ambiente virtual
```bash
python -m venv venv

# No macOS/Linux:
source venv/bin/activate

# No Windows:
venv\Scripts\activate
```

### 3. Instale as dependências
```bash
pip install -r requirements.txt
```

### 4. Configure as variáveis de ambiente
Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:

```env
SUPABASE_URL=sua_url_do_supabase
SUPABASE_KEY=sua_chave_do_supabase
SUPABASE_JWT_SECRET=seu_jwt_secret_do_supabase
```

### 5. Configure o banco de dados no Supabase
Crie uma tabela chamada `lista_desejos` com a seguinte estrutura:

```sql
CREATE TABLE lista_desejos (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    valor INTEGER NOT NULL, -- Valor em centavos
    link TEXT,
    user_id UUID NOT NULL,
);
```

## 🚀 Como Executar

### Desenvolvimento
```bash
python app.py
```

A API estará disponível em: `http://localhost:5000`

### Produção
```bash
gunicorn app:app
```

## 📚 Documentação da API

Acesse a documentação interativa do Swagger em:
- **Desenvolvimento**: `http://localhost:5000/apidocs`
- **Produção**: `https://sua-url.com/apidocs`

## 🔐 Autenticação

Todas as rotas (exceto a documentação) requerem autenticação JWT. Inclua o token no header:
