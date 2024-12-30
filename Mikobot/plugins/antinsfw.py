# <============================================== IMPORTS =========================================================>
from os import remove
from pyrogram import Client, filters
from Database.mongodb.toggle_mongo import is_nsfw_on, nsfw_off, nsfw_on
from Mikobot import BOT_USERNAME, DRAGONS
from Mikobot.state import arq
from Mikobot.utils.can_restrict import can_restrict
from Mikobot.utils.errors import capture_err

# <=======================================================================================================>
app = Client(
    "group_help",
    api_id=123456,  # Replace with your API ID
    api_hash="your_api_hash",  # Replace with your API Hash
    bot_token="your_bot_token"  # Replace with your bot token
)


# <================================================ FUNCTION =======================================================>
async def get_file_id_from_message(message):
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
            if not message.sticker.thumbs:
                return
            file_id = message.sticker.thumbs[0].file_id
        else:
            file_id = message.sticker.file_id

    if message.photo:
        file_id = message.photo.file_id

    if message.animation:
        if not message.animation.thumbs:
            return
        file_id = message.animation.thumbs[0].file_id

    if message.video:
        if not message.video.thumbs:
            return
        file_id = message.video.thumbs[0].file_id
    return file_id


@app.on_message(
    (
        filters.document
        | filters.photo
        | filters.sticker
        | filters.animation
        | filters.video
    )
    & ~filters.private,
    group=8,
)
@capture_err
async def detect_nsfw(_, message):
    if not await is_nsfw_on(message.chat.id):
        return
    if not message.from_user:
        return
    file_id = await get_file_id_from_message(message)
    if not file_id:
        return
    file = await _.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    if not results.ok:
        return
    results = results.result
    remove(file)
    nsfw = results.is_nsfw
    if message.from_user.id in DRAGONS:
        return
    if not nsfw:
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


@app.on_message(filters.command(["nsfwscan", f"nsfwscan@{BOT_USERNAME}"]))
@capture_err
async def nsfw_scan_command(_, message):
    if not message.reply_to_message:
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    reply = message.reply_to_message
    if (
        not reply.document
        and not reply.photo
        and not reply.sticker
        and not reply.animation
        and not reply.video
    ):
        await message.reply_text(
            "Reply to an image/document/sticker/animation to scan it."
        )
        return
    m = await message.reply_text("Scanning")
    file_id = await get_file_id_from_message(reply)
    if not file_id:
        return await m.edit("Something wrong happened.")
    file = await _.download_media(file_id)
    try:
        results = await arq.nsfw_scan(file=file)
    except Exception:
        return
    remove(file)
    if not results.ok:
        return await m.edit(results.result)
    results = results.result
    await m.edit(
        f"""
**➢ Neutral:** `{results.neutral} %`
**➢ Porn:** `{results.porn} %`
**➢ Hentai:** `{results.hentai} %`
**➢ Sexy:** `{results.sexy} %`
**➢ Drawings:** `{results.drawings} %`
**➢ NSFW:** `{results.is_nsfw}`
"""
    )


@app.on_message(
    filters.command(["antinsfw", f"antinsfw@{BOT_USERNAME}"]) & ~filters.private
)
@can_restrict
async def nsfw_enable_disable(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /antinsfw [on/off]")
        return

    status = message.text.split(None, 1)[1].strip().lower()
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

    print(f"NSFW system status for chat {chat_id} is now {status}")


# <=================================================== HELP ====================================================>


__mod_name__ = "˹ ᴀɴᴛɪ-ɴsғᴡ ˼"

__help__ = """
<blockquote>🔞 Helps in detecting NSFW material and removing it.</blockquote>

<b><u>➠ Command:</u></b>

<blockquote>➯ /antinsfw [on/off]: Enables Anti-NSFW system.

➯ /nsfwscan <reply to message>: Scans the file replied to.</blockquote>
"""
# <================================================ END =======================================================>
