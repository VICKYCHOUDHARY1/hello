from os import remove
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes
from Database.mongodb.toggle_mongo import is_nsfw_on, nsfw_off, nsfw_on
from Mikobot import BOT_USERNAME, DRAGONS
from Mikobot.state import arq
from Mikobot import function
from Mikobot.utils.can_restrict import can_restrict
from Mikobot.utils.errors import capture_err

# <================================================ FUNCTION =======================================================>
async def get_file_id_from_message(update: Update):
    """Message से फ़ाइल ID प्राप्त करें"""
    message = update.message
    file_id = None

    if message.document:
        if int(message.document.file_size) > 3145728:
            return
        mime_type = message.document.mime_type
        if mime_type not in ("image/png", "image/jpeg"):
            return
        file_id = message.document.file_id

    if message.sticker:
        if message.sticker.is_animated:
            if not message.sticker.thumb:
                return
            file_id = message.sticker.thumb.file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo[-1].file_id

    if message.animation:
        if not message.animation.thumb:
            return
        file_id = message.animation.thumb.file_id

    if message.video:
        if not message.video.thumb:
            return
        file_id = message.video.thumb.file_id
    return file_id


async def detect_nsfw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """NSFW सामग्री को स्कैन और हटाने का कार्य"""
    message = update.message

    # Check if Anti-NSFW is enabled
    if not await is_nsfw_on(message.chat.id):
        return

    if not message.from_user:
        return

    # Get file ID from the message
    file_id = await get_file_id_from_message(update)
    if not file_id:
        return

    # Download the media file
    file = await context.bot.get_file(file_id)
    file_path = await file.download_to_drive()

    try:
        results = await arq.nsfw_scan(file=file_path)
    except Exception:
        return

    if not results.ok:
        return

    results = results.result
    remove(file_path)

    if message.from_user.id in DRAGONS:
        return

    if not results.is_nsfw:
        return

    try:
        await message.delete()
    except Exception:
        return

    await message.reply_text(
        f"""
**🔞 NSFW Image Detected & Deleted Successfully!**

**✪ User:** {message.from_user.mention} [`{message.from_user.id}`]
**✪ Safe:** `{results.neutral} %`
**✪ Porn:** `{results.porn} %`
**✪ Adult:** `{results.sexy} %`
**✪ Hentai:** `{results.hentai} %`
**✪ Drawings:** `{results.drawings} %`
"""
    )


async def nsfw_scan_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """NSFW सामग्री को स्कैन करने का कमांड हैंडलर"""
    message = update.message

    if not message.reply_to_message:
        await message.reply_text("Reply to an image/document/sticker/animation to scan it.")
        return

    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text("Reply to an image/document/sticker/animation to scan it.")
        return

    m = await message.reply_text("Scanning...")
    file_id = await get_file_id_from_message(update)

    if not file_id:
        return await m.edit_text("Something wrong happened.")  # Use edit_text instead of edit

    file = await context.bot.get_file(file_id)
    file_path = await file.download_to_drive()

    try:
        results = await arq.nsfw_scan(file=file_path)
    except Exception:
        return

    remove(file_path)

    if not results.ok:
        return await m.edit_text(results.result)  # Use edit_text instead of edit

    results = results.result
    await m.edit_text(  # Use edit_text instead of edit
        f"""
**➢ Neutral:** `{results.neutral} %`
**➢ Porn:** `{results.porn} %`
**➢ Hentai:** `{results.hentai} %`
**➢ Sexy:** `{results.sexy} %`
**➢ Drawings:** `{results.drawings} %`
**➢ NSFW:** `{results.is_nsfw}`
"""
    )


async def nsfw_enable_disable(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """NSFW स्कैन को सक्षम या अक्षम करने का कमांड हैंडलर"""
    message = update.message

    if len(context.args) != 1:
        await message.reply_text("Usage: /antinsfw [on/off]")
        return

    status = context.args[0].strip().lower()
    chat_id = message.chat.id

    if status in ("on", "yes"):
        if await is_nsfw_on(chat_id):
            await message.reply_text("Anti-NSFW is already enabled.")
            return
        await nsfw_on(chat_id)
        await message.reply_text(
            "Enabled AntiNSFW System. I will delete messages containing inappropriate content."
        )
    elif status in ("off", "no"):
        if not await is_nsfw_on(chat_id):
            await message.reply_text("Anti-NSFW is already disabled.")
            return
        await nsfw_off(chat_id)
        await message.reply_text("Disabled Anti-NSFW system.")
    else:
        await message.reply_text("Unknown suffix. Use /antinsfw [on/off].")


# <================================================ HANDLERS =======================================================>

function(CommandHandler("nsfwscan", nsfw_scan_command, block=False))
function(CommandHandler("antinsfw", nsfw_enable_disable, block=False))

# Handle all media messages (photos, documents, stickers, videos)
function(
    MessageHandler(
        filters.PHOTO | filters.Document.ALL | filters.Sticker.ALL | filters.VIDEO,
        detect_nsfw,
        block=False
    )
)
