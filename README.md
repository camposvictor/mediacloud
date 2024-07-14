# MediaCloud

## Configuração do Ambiente

Certifique-se de ter Python instalado no seu sistema.

### Criação e Ativação de Ambiente Virtual

Recomenda-se usar um ambiente virtual para isolar dependências do projeto. Você pode criar e ativar um ambiente virtual da seguinte maneira:

#### No Windows

```bash
# Cria um ambiente virtual
python -m venv myenv

# Ativa o ambiente virtual
myenv\Scripts\activate
```

#### No macOS e Linux

```bash
# Cria um ambiente virtual
python3 -m venv myenv

# Ativa o ambiente virtual
source myenv/bin/activate
```

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

### Configuração do Banco de Dados

Por padrão, este projeto usa SQLite para facilitar o desenvolvimento. Configure outras opções de banco de dados conforme necessário.

```bash
# Execute as migrações para criar tabelas no banco de dados
python manage.py migrate
```

### Configuração de Variáveis de Ambiente

Certifique-se de configurar corretamente variáveis de ambiente necessárias, como chaves secretas, URLs de serviço, etc. Crie um arquivo `.env` na raiz do projeto, se necessário.

### Executando o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

O servidor será executado em `http://localhost:8000/` por padrão.

## Uso do Projeto

Explique como usar ou testar seu projeto. Inclua detalhes importantes sobre URLs, funcionalidades principais, etc.
