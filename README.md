# 🏗️ Bot de Checklist de Obras

Bot desenvolvido em Python para registrar e acompanhar pendências de obras diretamente pelo Telegram.

O projeto nasceu de uma necessidade observada na minha experiência profissional em engenharia: durante a execução de uma obra, diversas pendências são identificadas e muitas vezes registradas em grupos de mensagens, dificultando sua organização, acompanhamento e posterior conclusão.

A proposta do bot é utilizar o próprio Telegram como interface para transformar essas informações em registros estruturados e persistentes.

## 🎯 Objetivo do projeto

Criar uma ferramenta simples para apoiar o controle de pendências de obra sem exigir que a equipe utilize um sistema externo.

O grupo do Telegram funciona como ponto central do checklist, enquanto o cadastro de uma nova pendência é realizado em conversa privada com o bot.

Após a confirmação, a informação é armazenada em banco de dados e publicada novamente no grupo da obra.

## ⚙️ Funcionalidades

Atualmente o sistema permite:

- cadastrar novas pendências pelo Telegram;
- iniciar o cadastro a partir do grupo e continuar a interação no privado;
- informar descrição e local da pendência;
- definir prioridade como baixa, normal ou alta;
- definir prazo para resolução;
- anexar fotografia opcional;
- revisar os dados antes da confirmação;
- armazenar as pendências em banco SQLite;
- publicar automaticamente a nova pendência no grupo;
- listar pendências abertas;
- exibir fotografia quando disponível;
- concluir uma pendência através do ID;
- separar registros pelo grupo de origem;
- restringir a utilização a grupo autorizado;
- manter os dados persistentes no ambiente de produção;
- tratar erros básicos de rede e timeout durante o envio de mensagens.

## 🔄 Fluxo de utilização

O cadastro foi desenvolvido utilizando um fluxo conversacional.

1. O usuário executa `/nova` no grupo autorizado.
2. O bot disponibiliza um botão para continuar o cadastro no privado.
3. No chat privado, o bot solicita:
   - descrição;
   - local;
   - prioridade;
   - prazo;
   - fotografia opcional.
4. O bot apresenta os dados para conferência.
5. O usuário confirma ou cancela o cadastro.
6. Após a confirmação, a pendência é salva no SQLite.
7. A nova pendência é publicada automaticamente no grupo da obra.

Esse fluxo evita que todas as etapas do cadastro ocupem o grupo e mantém nele apenas a informação consolidada.

## 💬 Comandos

| Comando | Função |
|---|---|
| `/nova` | Inicia o cadastro de uma nova pendência |
| `/listar` | Lista as pendências abertas do grupo |
| `/concluir ID` | Marca a pendência informada como concluída |
| `/cancelar` | Cancela um cadastro em andamento |

## 🛠️ Tecnologias utilizadas

- **Python**
- **python-telegram-bot**
- **SQLite**
- **Git**
- **GitHub**
- **Docker**
- **Fly.io**
- **python-dotenv**

## 🗄️ Persistência de dados

As pendências são armazenadas em um banco SQLite.

Cada registro pode armazenar informações como:

- ID;
- descrição;
- status;
- local;
- prioridade;
- prazo;
- referência da fotografia;
- grupo de origem.

O caminho do banco pode ser configurado através da variável de ambiente `DATABASE_PATH`.

No ambiente de produção, o banco utiliza armazenamento persistente para evitar a perda dos registros durante reinicializações da aplicação.

## 🐳 Containerização

A aplicação possui um `Dockerfile` responsável pela criação do ambiente necessário para execução do bot.

A imagem:

1. utiliza Python como base;
2. define o diretório da aplicação;
3. instala as dependências presentes em `requirements.txt`;
4. copia os arquivos do projeto;
5. inicia o bot através de `bot.py`.

Isso permite executar a aplicação em um ambiente reproduzível e facilita sua publicação.

## ☁️ Deploy

O projeto está configurado para deploy no **Fly.io**.

A configuração utiliza:

- container Docker;
- região de execução configurada no Fly.io;
- volume persistente para o banco SQLite;
- variáveis de ambiente para informações sensíveis e configurações da aplicação.

## 🔐 Variáveis de ambiente

Para executar o projeto é necessário configurar as seguintes variáveis:

```env
TELEGRAM_BOT_TOKEN=seu_token
GRUPO_AUTORIZADO_ID=id_do_grupo
DATABASE_PATH=caminho_do_banco
```

O arquivo `.env` não deve ser enviado ao repositório.

## ▶️ Executando localmente

Clone o repositório:

```bash
git clone https://github.com/pslipe/bot-checklist-obras.git
cd bot-checklist-obras
```

Crie e ative um ambiente virtual:

```bash
python -m venv .venv
```

No Windows:

```bash
.venv\Scripts\activate
```

Instale as dependências:

```bash
pip install -r requirements.txt
```

Configure as variáveis de ambiente e execute:

```bash
python bot.py
```

## 📂 Estrutura principal

```text
bot-checklist-obras/
├── bot.py
├── database.py
├── requirements.txt
├── Dockerfile
├── fly.toml
├── .dockerignore
├── .gitignore
└── README.md
```

### `bot.py`

Responsável pela interação com o Telegram, comandos, fluxo conversacional, validações e envio das mensagens.

### `database.py`

Responsável pela conexão com SQLite, criação e atualização da estrutura do banco e operações relacionadas às pendências.

## 📚 Aprendizados

Este projeto foi desenvolvido como parte da minha transição profissional para desenvolvimento de software e permitiu aplicar conceitos como:

- organização de uma aplicação Python;
- funções e programação assíncrona;
- integração com API/biblioteca externa;
- fluxo conversacional e gerenciamento de estados;
- persistência com banco de dados;
- operações SQL;
- tratamento de entradas e validações;
- variáveis de ambiente;
- tratamento de erros;
- versionamento com Git e GitHub;
- containerização com Docker;
- persistência de dados em produção;
- deploy de uma aplicação.

Além dos aspectos técnicos, o projeto permitiu transformar um problema observado no ambiente de engenharia e obras em uma solução de software funcional.

## 🚀 Próximas evoluções

Algumas possibilidades planejadas para evolução do projeto:

- registrar o usuário responsável pela criação da pendência;
- atribuir um responsável para cada pendência;
- implementar edição e exclusão;
- melhorar filtros e consultas;
- adicionar notificações de prazo;
- gerar resumos automáticos;
- ampliar cobertura de testes;
- evoluir a estrutura e organização do código;
- desenvolver uma interface web para acompanhamento.

## 👨‍💻 Autor

**Felipe Pereira Silva**

Engenheiro Eletricista em transição para Desenvolvimento de Software, estudante de Análise e Desenvolvimento de Sistemas, com foco em Backend e Python.

- GitHub: `@pslipe`
- LinkedIn: `linkedin.com/in/pslipe`