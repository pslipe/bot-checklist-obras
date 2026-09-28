# 🏗️ Bot de Checklist de Pendências de Obra

Bot desenvolvido em **Python** para gerenciamento de pendências de obras diretamente pelo **Telegram**.

O projeto nasceu de uma necessidade real de obra: centralizar o registro, acompanhamento e conclusão de pendências de forma simples, rápida e acessível para a equipe.

Atualmente, o bot está em funcionamento em ambiente real e publicado em produção.

---

## 🎯 Objetivo

Em obras, muitas pendências acabam sendo registradas em mensagens, anotações, conversas ou planilhas separadas.

Isso pode dificultar o acompanhamento e fazer com que itens importantes sejam esquecidos.

O objetivo deste projeto é utilizar o Telegram como uma interface simples para:

- registrar pendências;
- definir localização, prioridade e prazo;
- anexar fotos;
- consultar pendências abertas;
- concluir pendências;
- identificar serviços atrasados;
- enviar alertas automáticos;
- gerar um resumo semanal para acompanhamento da obra.

---

## 🚀 Funcionalidades atuais

### ➕ Cadastro de pendências

O usuário inicia o cadastro através do comando:

```text
/nova
```

O bot direciona o usuário para uma conversa privada, onde o cadastro é realizado passo a passo.

São solicitadas as seguintes informações:

- descrição da pendência;
- local;
- prioridade;
- prazo para resolução;
- foto opcional.

Após a confirmação, a pendência é armazenada no banco de dados e publicada automaticamente no grupo da obra.

---

### 📷 Anexo de fotos

O usuário pode anexar uma foto durante o cadastro.

O bot utiliza o `file_id` fornecido pelo Telegram, evitando a necessidade de armazenar fisicamente as imagens no servidor.

---

### 📋 Listagem de pendências

O comando:

```text
/listar
```

exibe todas as pendências que ainda possuem status:

```text
Pendente
```

São apresentadas informações como:

- ID;
- descrição;
- status;
- local;
- prioridade;
- prazo;
- foto, quando disponível.

---

### ✅ Conclusão de pendências

Para concluir uma pendência:

```text
/concluir ID
```

Exemplo:

```text
/concluir 12
```

A pendência deixa de aparecer nas listagens, alertas e resumos após ser concluída.

---

### ❌ Cancelamento de cadastro

Durante o processo de criação de uma nova pendência, o cadastro pode ser interrompido a qualquer momento com:

```text
/cancelar
```

Os dados temporários são descartados e nenhuma pendência é criada.

---

## 🚨 Alerta diário de pendências vencidas

Todos os dias às **07:00**, o bot consulta automaticamente o banco de dados.

Caso existam pendências cujo prazo já tenha vencido, o grupo recebe um relatório contendo todas as pendências atrasadas.

Exemplo:

```text
🚨 PENDÊNCIAS ATRASADAS

📌 Total de pendências vencidas: 3

🔴 #12 - Instalação de luminária
📍 Recepção
📅 Prazo: 25/09/2026
⏱️ 3 dia(s) em atraso
```

O relatório apresenta:

- quantidade total de pendências vencidas;
- ID;
- descrição;
- local;
- prazo;
- quantidade de dias em atraso.

Enquanto a pendência permanecer com status `Pendente`, ela continuará aparecendo no relatório diário.

Caso não existam pendências atrasadas, nenhuma mensagem é enviada.

---

## 📋 Resumo semanal

Toda **segunda-feira às 07:05**, o bot envia automaticamente um resumo das pendências ainda abertas.

O relatório apresenta:

```text
📋 RESUMO SEMANAL DE PENDÊNCIAS

📌 Total de pendências abertas: 14
🚨 Vencidas: 7
⏳ Dentro do prazo: 7
```

Em seguida, as pendências são separadas em dois grupos:

### 🚨 Pendências atrasadas

As pendências vencidas são apresentadas com a quantidade de dias de atraso.

### ⏳ Pendências dentro do prazo

As demais pendências são ordenadas de acordo com o prazo, ajudando a visualizar quais atividades precisam ser executadas primeiro.

---

## ⏰ Agendamento automático

Os alertas são executados utilizando o **JobQueue** do `python-telegram-bot`.

Horários configurados:

| Rotina | Frequência | Horário |
|---|---|---:|
| 🚨 Pendências vencidas | Todos os dias | 07:00 |
| 📋 Resumo semanal | Segunda-feira | 07:05 |

Os horários utilizam explicitamente o fuso:

```text
America/Sao_Paulo
```

Isso evita problemas relacionados ao timezone do servidor onde a aplicação está sendo executada.

---

## 💬 Comandos disponíveis

| Comando | Função |
|---|---|
| `/nova` | Cadastrar uma nova pendência |
| `/listar` | Listar pendências abertas |
| `/concluir ID` | Marcar uma pendência como concluída |
| `/cancelar` | Cancelar um cadastro em andamento |

---

## 🔄 Fluxo de cadastro

```text
Grupo da obra
      ↓
    /nova
      ↓
Link para conversa privada
      ↓
Descrição
      ↓
Local
      ↓
Prioridade
      ↓
Prazo
      ↓
Foto opcional
      ↓
Confirmação
      ↓
SQLite
      ↓
Publicação automática no grupo
```

O cadastro é realizado no privado para evitar excesso de mensagens no grupo principal.

---

## 🔐 Controle de acesso

O bot utiliza uma variável de ambiente contendo o ID do grupo autorizado.

```text
GRUPO_AUTORIZADO_ID
```

Com isso, mesmo que o bot seja encontrado ou adicionado em outro grupo, seus principais comandos permanecem restritos ao grupo configurado.

Informações sensíveis, como token do Telegram e IDs utilizados em produção, não são armazenadas diretamente no código-fonte.

---

## 💾 Banco de dados

O projeto utiliza **SQLite** para persistência das informações.

Cada pendência possui dados como:

- ID;
- descrição;
- status;
- local;
- prioridade;
- prazo;
- `file_id` da foto;
- ID do grupo.

O status inicial de uma nova pendência é:

```text
Pendente
```

Quando o comando `/concluir` é executado, seu status é atualizado.

---

## 🛠️ Tecnologias utilizadas

- Python
- Telegram Bot API
- python-telegram-bot
- JobQueue
- APScheduler
- SQLite
- python-dotenv
- ZoneInfo
- Git
- GitHub
- Docker
- Fly.io

---

## 🧠 Conceitos aplicados

Durante o desenvolvimento do projeto foram trabalhados conceitos como:

- programação assíncrona com `async` e `await`;
- funções;
- listas e dicionários;
- manipulação de datas;
- comparação de datas;
- timezone;
- tratamento de exceções;
- variáveis de ambiente;
- integração com APIs;
- handlers do Telegram;
- `ConversationHandler`;
- `CallbackQueryHandler`;
- estados de conversa;
- Inline Keyboards;
- Deep Links;
- armazenamento temporário com `context.user_data`;
- persistência com SQLite;
- consultas SQL parametrizadas;
- atualização de registros;
- utilização de `file_id` para fotos;
- agendamento de tarefas recorrentes;
- JobQueue;
- APScheduler;
- Git e GitHub;
- versionamento de código;
- Docker;
- deploy de aplicações Python;
- configuração de secrets;
- volumes persistentes;
- separação entre ambiente local e produção.

---

## 🏗️ Arquitetura atual

De forma simplificada:

```text
┌─────────────────────┐
│      Telegram       │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│       bot.py        │
│                     │
│ Handlers            │
│ ConversationHandler │
│ JobQueue            │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    database.py      │
│                     │
│ Operações SQLite    │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│    checklist.db     │
└─────────────────────┘
```

Em produção:

```text
Telegram
    ↓
Fly.io
    ↓
Container Docker
    ↓
Python Bot
    ↓
SQLite
    ↓
Volume persistente /data
```

---

## 📂 Estrutura do projeto

```text
bot-checklist-obras/
│
├── bot.py
├── database.py
├── requirements.txt
├── Dockerfile
├── fly.toml
├── .gitignore
└── README.md
```

Arquivos locais como `.env`, ambiente virtual e banco de desenvolvimento não devem ser versionados.

---

## ⚙️ Configuração local

### 1. Clone o repositório

```bash
git clone https://github.com/pslipe/bot-checklist-obras.git
```

Entre na pasta:

```bash
cd bot-checklist-obras
```

---

### 2. Crie um ambiente virtual

```powershell
python -m venv .venv
```

No Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando ativado, o terminal deve exibir algo semelhante a:

```text
(.venv)
```

---

### 3. Instale as dependências

```powershell
pip install -r requirements.txt
```

---

### 4. Configure as variáveis de ambiente

Crie um arquivo:

```text
.env
```

Exemplo:

```env
TELEGRAM_BOT_TOKEN=SEU_TOKEN
GRUPO_AUTORIZADO_ID=ID_DO_GRUPO
DATABASE_PATH=checklist.db
```

> Nunca publique seu `.env`, token do Telegram ou outras credenciais no GitHub.

---

### 5. Execute o bot

```powershell
python bot.py
```

---

## 📦 Dependências principais

O projeto utiliza:

```text
python-telegram-bot[job-queue]
python-dotenv
```

O extra `job-queue` disponibiliza as dependências necessárias para execução das tarefas automáticas.

---

## 🐳 Docker

A aplicação é empacotada utilizando Docker.

O container utiliza uma imagem Python e instala automaticamente as dependências presentes em:

```text
requirements.txt
```

Isso permite que o ambiente de produção seja reproduzível e independente das configurações da máquina de desenvolvimento.

---

## ☁️ Deploy

O bot está publicado na **Fly.io**.

A aplicação roda continuamente através de uma Fly Machine.

O banco SQLite de produção utiliza um volume persistente montado em:

```text
/data
```

O caminho do banco é definido através da variável:

```text
DATABASE_PATH=/data/checklist.db
```

Dessa forma, os dados continuam disponíveis mesmo após reinicializações ou novos deploys.

---

## 🔑 Variáveis de ambiente em produção

As informações sensíveis são configuradas através de **Fly Secrets**.

Exemplos:

```text
TELEGRAM_BOT_TOKEN
GRUPO_AUTORIZADO_ID
DATABASE_PATH
```

Nenhuma dessas informações precisa ficar diretamente no código-fonte.

---

## 📈 Status do projeto

### 🟢 MVP funcional e em produção

Atualmente o sistema possui:

- cadastro completo de pendências;
- persistência em banco de dados;
- imagens;
- prioridades;
- prazos;
- listagem;
- conclusão;
- cancelamento;
- controle de grupo autorizado;
- deploy com Docker;
- banco persistente;
- alerta automático de pendências atrasadas;
- resumo semanal automático.

O projeto está sendo utilizado em um cenário real de acompanhamento de obra.

---

## 🚀 Próximas evoluções

Possíveis evoluções futuras:

- registrar automaticamente quem criou cada pendência;
- adicionar responsável pela execução;
- permitir edição de pendências;
- permitir exclusão de pendências;
- adicionar novos filtros de consulta;
- melhorar a cobertura de testes automatizados;
- refatorar e separar responsabilidades da aplicação;
- permitir utilização por múltiplas obras;
- criar painel web para acompanhamento;
- adicionar indicadores e métricas;
- receber novas pendências através de áudio;
- transcrever mensagens de voz automaticamente;
- utilizar Inteligência Artificial para interpretar o áudio;
- extrair automaticamente descrição, local, prioridade e prazo;
- transformar o áudio em uma pendência estruturada;
- gerar resumos inteligentes da situação da obra.

---

## 🤖 Visão futura com Inteligência Artificial

Uma das evoluções planejadas é permitir que um usuário envie algo semelhante a:

```text
"Tem que corrigir amanhã o vazamento no banheiro masculino
do segundo pavimento. Coloca como prioridade alta."
```

O sistema poderá:

```text
Áudio
  ↓
Transcrição
  ↓
Inteligência Artificial
  ↓
Extração das informações
  ↓
Descrição
Local
Prioridade
Prazo
  ↓
Confirmação
  ↓
Nova pendência
```

Isso permitirá tornar o registro ainda mais rápido para uso em campo.

---

## 🎓 Contexto do projeto

Este projeto também faz parte do meu processo de desenvolvimento profissional em tecnologia.

Além de solucionar uma necessidade real da área de Engenharia e Construção, ele está sendo utilizado para aprofundar conhecimentos em:

- Python;
- desenvolvimento backend;
- bancos de dados;
- integração de APIs;
- automação;
- Git e GitHub;
- Docker;
- cloud;
- deploy;
- desenvolvimento de software aplicado a problemas reais.

---

## 📌 Motivação

Mais do que desenvolver um bot, a proposta deste projeto é transformar uma necessidade encontrada no dia a dia de uma obra em uma solução de software funcional.

O projeto continuará evoluindo a partir de necessidades identificadas durante sua utilização em ambiente real.

---

## 👨‍💻 Autor

**Felipe Pereira Silva Bianchine**

Engenheiro Eletricista em transição para Desenvolvimento de Software, com interesse em:

- desenvolvimento backend;
- Python;
- Java;
- APIs;
- automação;
- Inteligência Artificial;
- soluções tecnológicas aplicadas à Engenharia.

GitHub:

```text
https://github.com/pslipe
```

---

## 📄 Licença

Projeto desenvolvido para fins de estudo, portfólio e aplicação prática.
