import logging
from time import sleep
from credentials import TOKEN_BOT
from telegram import Update
from telegram.ext import ApplicationBuilder,  CommandHandler, MessageHandler, ContextTypes, filters


logging.basicConfig (
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

async def start (update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.effective_user.name

    await context.bot.send_chat_action (
            chat_id= update.effective_chat.id,
            action="typing"
        )

    sleep(1.5) # For wait 1500ms 😴

    await context.bot.send_message (
        chat_id= update.effective_chat.id,
        text= f"Hello {username} \nSend me a word and you will have your avatar 🥴\n**Examples** : *cool*, *smile* or *dark* ",
        parse_mode="Markdown"
    )

async def getAvatar (update: Update, context: ContextTypes.DEFAULT_TYPE):
    userWord = update.message.text
    messageId = update.message.message_id

    falseKeyword = ["?", "#", "/", "_", ".", ":", ";", "-", "*", "+", ",", "$","€","%", "=", "(",")", "[", "]", "§", "{", "}", "!", "@", "²", "<", ">"]

    for letter in falseKeyword:
        if letter in userWord:
            await context.bot.send_chat_action (
                chat_id= update.effective_chat.id,
                action="typing"
            )

            sleep(1.5) # For wait 1500ms 😴

            await context.bot.send_message (
                chat_id= update.effective_chat.id,
                text= "Please just send me a word like : *cool* or *dark* \nWithout special characters 😕",
                parse_mode="Markdown"
            )

            return

    try :

        URL = f"https://adorable-avatars.broken.services/{userWord}.png"

        # Now we can reply whit a photo to the user 🥱

        await context.bot.send_chat_action (
            chat_id= update.effective_chat.id,
            action="upload_photo"
        )

        sleep(1.5) # For wait 1500ms 😴

        await context.bot.send_photo (
            chat_id= update.effective_chat.id,
            photo=URL,
            reply_to_message_id=messageId
        )

    except:

        await context.bot.send_message (
            chat_id= update.effective_chat.id,
            text="There was a problem in the name you used, please enter different name 😵"
        )


if __name__ == "__main__":

    avatarApp = ApplicationBuilder().token(TOKEN_BOT).build()

    startHandler = CommandHandler("start", start)
    avatarHandler = MessageHandler(filters.TEXT & (~filters.COMMAND), getAvatar)

    avatarApp.add_handler(startHandler)
    avatarApp.add_handler(avatarHandler)

    avatarApp.run_polling()




































# by @th3fr3dy 😉