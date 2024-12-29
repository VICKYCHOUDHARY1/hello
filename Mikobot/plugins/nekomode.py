# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# PROVIDED BY https://t.me/ProjectCodeX
# NEKOS

# <============================================== IMPORTS =========================================================>
import nekos
from telethon import events

from Database.mongodb.toggle_mongo import is_nekomode_on, nekomode_off, nekomode_on
from Mikobot import tbot
from Mikobot.state import state  # Import the state function

# <=======================================================================================================>

url_sfw = "https://api.waifu.pics/sfw/"

allowed_commands = [
    "waifu",
    "neko",
    "shinobu",
    "megumin",
    "bully",
    "cuddle",
    "cry",
    "hug",
    "awoo",
    "kiss",
    "lick",
    "pat",
    "smug",
    "bonk",
    "yeet",
    "blush",
    "smile",
    "spank",
    "wave",
    "highfive",
    "handhold",
    "nom",
    "bite",
    "glomp",
    "slap",
    "hTojiy",
    "wink",
    "poke",
    "dance",
    "cringe",
    "tickle",
]


# <================================================ FUNCTION =======================================================>
@tbot.on(events.NewMessage(pattern="/wallpaper"))
async def wallpaper(event):
    chat_id = event.chat_id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = "wallpaper"
        img_url = nekos.img(
            target
        )  # Replace nekos.img(target) with the correct function call
        await event.reply(file=img_url)


@tbot.on(events.NewMessage(pattern="/nekomode on"))
async def enable_nekomode(event):
    chat_id = event.chat_id
    await nekomode_on(chat_id)
    await event.reply("Nekomode has been enabled.")


@tbot.on(events.NewMessage(pattern="/nekomode off"))
async def disable_nekomode(event):
    chat_id = event.chat_id
    await nekomode_off(chat_id)
    await event.reply("Nekomode has been disabled.")


@tbot.on(events.NewMessage(pattern=r"/(?:{})".format("|".join(allowed_commands))))
async def nekomode_commands(event):
    chat_id = event.chat_id
    nekomode_status = await is_nekomode_on(chat_id)
    if nekomode_status:
        target = event.raw_text[1:].lower()  # Remove the slash before the command
        if target in allowed_commands:
            url = f"{url_sfw}{target}"

            response = await state.get(url)
            result = response.json()
            animation_url = result["url"]

            # Send animation
            await event.respond(file=animation_url)


__help__ = """
<blockquote>➥ Sᴇɴᴅs ғᴜɴ Gifs/Images
➥ /nekomode on : Eɴᴀʙʟᴇs ғᴜɴ ɴᴇᴋᴜ ᴍᴏᴅᴇ.
➥ /nekomode off : Dɪsᴀʙʟᴇs ғᴜɴ ɴᴇᴋᴏ ᴍᴏᴅᴇ.</blockquote>

<blockquote>➯ /bully: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ʙᴜʟʟʏ Gɪғs.
➯ /neko: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ɴᴇᴋᴏ Gɪғs.
➯ /wallpaper: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀʟʟᴘᴀᴘᴇʀs.
➯ /highfive: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ʜɪɢʜғɪᴠᴇ Gɪғs.
➯ /tickle: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴛɪᴄᴋʟᴇ Gɪғs.
➯ /wave: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀᴠᴇ Gɪғs.
➯ /smile: sᴇɴᴅs ʀᴀɴᴅᴏᴍ sᴍɪʟᴇ Gɪғs.
➯ /feed: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ғᴇᴇᴅɪɴɢ Gɪғs.
➯ /blush: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ʙʟᴜsʜ Gɪғs.
➯ /avatar: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴀᴠᴀᴛᴀʀ stickers.
➯ /waifu: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴡᴀɪғᴜ stickers.
➯ /kiss: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴋɪssɪɴɢ Gɪғs.
➯ /cuddle: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄᴜᴅᴅʟᴇ Gɪғs.
➯ /cry: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄʀʏ Gɪғs.
➯ /bonk: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ᴄᴜᴅᴅʟᴇ Gɪғs.
➯ /smug: sᴇɴᴅs ʀᴀɴᴅᴏᴍ sᴍᴜɢ Gɪғs.
➯ /slap: sᴇɴᴅs ʀᴀɴᴅᴏᴍ sʟᴀᴘ Gɪғs.
➯ /hug: ɢᴇᴛ ʜᴜɢɢᴇᴅ ᴏʀ ʜᴜɢ ᴀ user.
➯ /pat: ᴘᴀᴛs ᴀ ᴜsᴇʀ ᴏʀ ɢᴇᴛ ᴘᴀᴛᴛᴇᴅ.
➯ /spank: sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ sᴘᴀɴᴋ ɢɪғ.
➯ /dance: sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴅᴀɴᴄᴇ ɢɪғ.
➯ /poke: sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴘᴏᴋᴇ ɢɪғ.
➯ /wink: sᴇɴᴅs ᴀ ʀᴀɴᴅᴏᴍ ᴡɪɴᴋ ɢɪғ.
➯ /bite: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ʙɪᴛᴇ Gɪғs.
➯ /handhold: sᴇɴᴅs ʀᴀɴᴅᴏᴍ ʜᴀɴᴅʜᴏʟᴅ Gɪғs.</blockquote>
"""

__mod_name__ = "˹ ɴᴇᴋᴏ ˼"
# <================================================ END =======================================================>
