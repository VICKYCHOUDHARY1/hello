from telethon import TelegramClient, events
import asyncio
from Mikobot import bot

@bot.on(events.ChatAction)
async def handler(event):
    if event.user_joined:
        welcome_message = f"Welcome to the group, {event.user.first_name}!"
        image_path = '/extra/welcome.jpg'  # image path
        await event.reply(welcome_message, file=image_path)

if __name__ == '__main__':
    bot.run_until_disconnected()
