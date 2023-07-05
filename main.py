import logging
from telegram import Update, User
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters
import os
from dotenv import load_dotenv
import openai
load_dotenv()
openai.api_key = os.getenv('openai')
botkey = os.getenv('botkey')
whitelist = os.getenv('whitelist')
user = Update.effective_user
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
customsystemprompt = False
customsystemprompttext = ""
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(context._user_id) == str(whitelist):
        user = update.effective_user
        text = "Hello " + user.first_name + ""
        await context.bot.send_message(chat_id=update.effective_chat.id, text=text)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You're not whitelisted on the bot!")

async def help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Help Commands Include: " " "
                                                                          "/help - Get this message")
async def change_system_role(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(context._user_id) == str(whitelist):
        newmessage = "Your New Custom System Prompt is " + " " + update.message.text
        global customsystemprompttext
        customsystemprompttext = update.message.text
        global customsystemprompt
        customsystemprompt = True
        await context.bot.send_message(chat_id=update.effective_chat.id, text=newmessage)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="You're not whitelisted on the bot!")

async def askgpt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(context._user_id) == str(whitelist):
        if customsystemprompt == False:
            user = update.effective_user
            systemrole = "You are a kind helpful assistant. The person you're talking to is named " + str(user.full_name) + " they're your boss"
            print(systemrole)

            messages = [
                {"role": "system", "content": systemrole},
            ]
            message = update.message.text
            if message:
                messages.append(
                    {"role": "user", "content": message},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )

            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            response = reply
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
        else:
            systemrole = customsystemprompttext
            print(systemrole)

            messages = [
                {"role": "system", "content": systemrole},
            ]
            message = update.message.text
            if message:
                messages.append(
                    {"role": "user", "content": message},
                )
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo", messages=messages
                )

            reply = chat.choices[0].message.content
            messages.append({"role": "assistant", "content": reply})
            response = reply
            await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


    else:
        responsewhitelist = "You're not Whitelisted Friend " + str(context._user_id)
        await context.bot.send_message(chat_id=update.effective_chat.id, text=responsewhitelist)



if __name__ == '__main__':
    application = ApplicationBuilder().token(botkey).build()

    start_handler = CommandHandler('start', start)
    askgpt_handler = MessageHandler(filters.TEXT & (~filters.COMMAND), askgpt)
    help_handler = CommandHandler('help', help)
    change_system_role_handler = CommandHandler('system', change_system_role)
    application.add_handler(start_handler)
    application.add_handler(askgpt_handler)
    application.add_handler(change_system_role_handler)
    application.add_handler(help_handler)


    application.run_polling()
