import os
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, ConversationHandler, MessageHandler, filters, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database import buscar_pendencias, criar_pendencia, atualizar_pendencia_concluida
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo
from telegram.error import TimedOut, NetworkError


DESCRICAO = 1
LOCAL = 2
PRIORIDADE = 3
PRAZO = 4
ESCOLHA_FOTO = 5
RECEBER_FOTO = 6
CONFIRMACAO = 7



load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
GRUPO_AUTORIZADO_ID = int(os.getenv("GRUPO_AUTORIZADO_ID"))

if TOKEN:
    app = Application.builder().token(TOKEN).build()
    print("Token carregado com sucesso!")
else:
    raise RuntimeError("Token do Telegram não encontrado.")

def grupo_autorizado(update):
    return update.effective_chat.id == GRUPO_AUTORIZADO_ID

async def exibir_pendencia(update, contexto):
    mensagem = update.effective_message
    prioridade = contexto.user_data["prioridade"]
    if prioridade == "Baixa":
        emoji_prioridade = "🟢"
    elif prioridade == "Normal":
        emoji_prioridade = "🟡"
    elif prioridade == "Alta":
        emoji_prioridade = "🔴"
    else:
        emoji_prioridade = "⚪"
    await mensagem.reply_text(f"🏗️ Confira a pendência! \n\n"
        f"📝 Descrição: {contexto.user_data['descricao']}\n"
        f"📍 Local: {contexto.user_data['local']}\n"
        f"{emoji_prioridade} Prioridade: {contexto.user_data['prioridade']}\n"
        f"📅 Prazo: {contexto.user_data['prazo']}")

async def start(update, contexto):
    if contexto.args:
        dados = contexto.args[0]
        if dados.startswith("nova_"):
            contexto.user_data.clear()
            grupo_id = int(dados.replace("nova_", ""))
            if grupo_id == GRUPO_AUTORIZADO_ID:
                contexto.user_data["grupo_id"] = grupo_id
                return await nova_pendencia(update, contexto)
            else:
                await update.message.reply_text("⛔ Este grupo não está autorizado a usar o bot.")

async def nova_pendencia(update, contexto):
    chat = update.effective_chat
    id_grupo = chat.id

    if chat.type != "private" and not grupo_autorizado(update):
        await update.message.reply_text("⛔ Este grupo não está autorizado a usar o bot.")

    elif chat.type == "private":
        if contexto.user_data.get("grupo_id") is None:
            await update.message.reply_text("⛔ Inicie uma nova pendência pelo grupo de CheckList.")
            return ConversationHandler.END
        else:
            await update.message.reply_text("Qual a descrição da pendência?")
            return DESCRICAO

    else:
        botao = [
            [
                InlineKeyboardButton("🔗 Acessar o BOT", url=f"https://t.me/gestor_checklist_obras_bot?start=nova_{id_grupo}")
            ]
        ]
        teclado = InlineKeyboardMarkup(botao)
        await update.message.reply_text("Continue a inclusão da pendência no privado!", reply_markup=teclado)

async def receber_descricao(update, contexto):
    contexto.user_data["descricao"] = update.message.text
    await update.message.reply_text("Qual o local da pendência?")
    return LOCAL

async def receber_local(update, contexto):    
    contexto.user_data["local"] = update.message.text
    botoes = [
            [
                InlineKeyboardButton("🟢 Baixa", callback_data="Baixa"),
                InlineKeyboardButton("🟡 Normal", callback_data="Normal"),
                InlineKeyboardButton("🔴 Alta", callback_data="Alta")
            ]
        ]
    teclado = InlineKeyboardMarkup(botoes)
    await update.message.reply_text("Qual a prioridade da pendência?", reply_markup=teclado)

    return PRIORIDADE

async def receber_prioridade(update, contexto):
    query = update.callback_query
    await query.answer()
    contexto.user_data["prioridade"] = query.data
    await query.edit_message_text(f"Prioridade selecionada: {query.data}")
    await query.message.reply_text("Qual o prazo para resolução da pendência? (em dias)")

    return PRAZO

async def receber_prazo(update, contexto):
    data_atual = datetime.now(ZoneInfo("America/Sao_Paulo"))
    if update.message.text.isdigit():
           
        prazo_dias = int(update.message.text)
        data_vencimento = data_atual + timedelta(days=prazo_dias)
        contexto.user_data["prazo"] = data_vencimento.strftime("%d/%m/%Y")

        botoes = [
            [
                InlineKeyboardButton("📷 Enviar Foto", callback_data="Com_Foto"),
                InlineKeyboardButton("❌ Sem Foto", callback_data="Sem_Foto")
            ]
        ]
        teclado = InlineKeyboardMarkup(botoes)

        await update.message.reply_text("Deseja anexar uma foto à pendência?", reply_markup=teclado)

        return ESCOLHA_FOTO
    else:
        await update.message.reply_text("Digite um valor válido de dias!")
        await update.message.reply_text("Qual o prazo para resolução da pendência? (em dias)")
        return PRAZO


async def escolher_foto(update, contexto):
    query = update.callback_query
    await query.answer()

    if query.data == "Com_Foto":
        await query.message.reply_text("Envie sua foto! ")
        return RECEBER_FOTO
    else:
        contexto.user_data["foto_file_id"] = None
        return await mostrar_confirmacao(update, contexto)


async def receber_foto(update, contexto):
    contexto.user_data["foto_file_id"] = update.message.photo[-1].file_id
    return await mostrar_confirmacao(update, contexto)

async def mostrar_confirmacao(update, contexto):
    mensagem = update.effective_message

    botoes = [
        [
        InlineKeyboardButton("✅ Confirmar", callback_data="Confirmar"),
        InlineKeyboardButton("❌ Cancelar", callback_data="Cancelar")
        ]
    ]
    teclado = InlineKeyboardMarkup(botoes)

    await exibir_pendencia(update, contexto)
    await mensagem.reply_text("Deseja cadastrar?", reply_markup=teclado)
    return CONFIRMACAO

async def confirmar_cadastro(update, contexto):
    query = update.callback_query
    await query.answer()
    await query.edit_message_reply_markup(reply_markup=None)
    
    if query.data == "Confirmar":
        
        id_pendencia = criar_pendencia(contexto.user_data["descricao"], contexto.user_data["local"], contexto.user_data["prioridade"], contexto.user_data["prazo"], contexto.user_data["foto_file_id"], contexto.user_data["grupo_id"])
        await query.message.reply_text("✅ Pendência Salva com Sucesso! ")

        prioridade = contexto.user_data["prioridade"]
        if prioridade == "Baixa":
            emoji_prioridade = "🟢"
        elif prioridade == "Normal":
            emoji_prioridade = "🟡"
        elif prioridade == "Alta":
            emoji_prioridade = "🔴"
        else:
            emoji_prioridade = "⚪"

        foto_file_id = contexto.user_data["foto_file_id"]
        try:
            if foto_file_id:
                await contexto.bot.send_photo(
                chat_id=contexto.user_data["grupo_id"],
                photo=foto_file_id,
                caption=f"🏗️ Nova Pendência!! #{id_pendencia}\n\n"
                f"📝 Descrição: {contexto.user_data['descricao']}\n"
                f"📍 Local: {contexto.user_data['local']}\n"
                f"{emoji_prioridade} Prioridade: {contexto.user_data['prioridade']}\n"
                f"📅 Prazo: {contexto.user_data['prazo']}\n")
            else:
                await contexto.bot.send_message(
                chat_id = contexto.user_data["grupo_id"],
                text = f"🏗️ Nova Pendência!! #{id_pendencia}\n\n"
                f"📝 Descrição: {contexto.user_data['descricao']}\n"
                f"📍 Local: {contexto.user_data['local']}\n"
                f"{emoji_prioridade} Prioridade: {contexto.user_data['prioridade']}\n"
                f"📅 Prazo: {contexto.user_data['prazo']}\n"
                )
        except TimedOut:
            await query.message.reply_text("⚠️ A pendência foi salva, mas houve timeout ao publicar no grupo. "
                "Confira o grupo antes de tentar novamente.")

        except NetworkError:
            await query.message.reply_text("⚠️ A pendência foi salva, mas houve erro de rede ao publicar no grupo.")
    else:
        await query.message.reply_text("❌ Pendência não registrada")
    contexto.user_data.clear()
    return ConversationHandler.END




async def listar_pendencias(update,contexto):

    if not grupo_autorizado(update):
        await update.message.reply_text("⛔ Este grupo não está autorizado a usar o bot.")
    else:
        grupo_id = update.effective_chat.id
        pendencias_banco = buscar_pendencias(grupo_id)
        
        await update.message.reply_text("🛠️ Checklist de Pendências da Obra")
        if not pendencias_banco:
            await update.message.reply_text("Sem Pendências Para Listar!")
        else:
            for pendencia in pendencias_banco:

                if pendencia[4] == "Baixa":
                    emoji_prioridade = "🟢"
                elif pendencia[4] == "Normal":
                    emoji_prioridade = "🟡"
                elif pendencia[4] == "Alta":
                    emoji_prioridade = "🔴"
                else:
                    emoji_prioridade = "⚪"

                texto_pendencia = (
                    f"‼️ ID: {pendencia[0]}\n"
                    f"📝 DESCRIÇÃO: {pendencia[1]}\n"
                    f"🚧 STATUS: {pendencia[2]}\n"
                    f"📍 LOCAL: {pendencia[3]}\n"
                    f"{emoji_prioridade} PRIORIDADE: {pendencia[4]}\n"
                    f"📅 PRAZO: {pendencia[5]}\n")
                try:
                    if pendencia[6]:
                        await contexto.bot.send_photo(
                            chat_id=grupo_id,
                            photo=pendencia[6],
                            caption=texto_pendencia
                        )
                    else:
                        await update.message.reply_text(texto_pendencia)

                except TimedOut:
                    print(f"Timeout ao enviar pendência ID {pendencia[0]}")

                except NetworkError:
                    print(f"Erro de rede ao enviar pendência ID {pendencia[0]}")


async def concluir_pendencia (update, contexto):

    if not grupo_autorizado(update):
        await update.message.reply_text("⛔ Este grupo não está autorizado a usar o bot.")
    else:
        grupo_id = update.effective_chat.id
        if not contexto.args:
            await update.message.reply_text("Uso correto: \n/concluir Id da Pendência Concluida")  
        elif not contexto.args[0].isdigit():
            await update.message.reply_text("Digite um número de ID válido")
        else:
            id_selecionado = int(contexto.args[0])
            resultado = atualizar_pendencia_concluida(id_selecionado, grupo_id)
            if not resultado:
                await update.message.reply_text("Sem Pendências e/ou número de ID não corresponde a nenhuma pendência!") 
            else:
                await update.message.reply_text("Pendência atualizada com sucesso!")                 

async def cancelar_pendencia (update, contexto):
    await update.message.reply_text("Cancelada a inclusão de nova pendência.")
    contexto.user_data.clear()
    return ConversationHandler.END




conversa_nova = ConversationHandler(
    entry_points=[
        CommandHandler("nova", nova_pendencia),
        CommandHandler("start", start)
    ],
    states={
        DESCRICAO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receber_descricao
            )
        ],
        LOCAL: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receber_local
            )
        ],
        PRIORIDADE: [
            CallbackQueryHandler(receber_prioridade)
        ],
        PRAZO: [
            MessageHandler(
                filters.TEXT & ~filters.COMMAND,
                receber_prazo
            )
        ],
        ESCOLHA_FOTO: [
            CallbackQueryHandler(escolher_foto)
        ],
        RECEBER_FOTO: [
            MessageHandler(
                filters.PHOTO,
                receber_foto
            )
        ],
        CONFIRMACAO: [
            CallbackQueryHandler(confirmar_cadastro)
        ]
    },
    fallbacks=[
        CommandHandler("cancelar", cancelar_pendencia)
    ]
)


app.add_handler(conversa_nova)

app.add_handler(
    CommandHandler("listar", listar_pendencias)
)

app.add_handler(
    CommandHandler("concluir", concluir_pendencia)
)


app.run_polling()



