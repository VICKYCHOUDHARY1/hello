# https://github.com/Infamous-Hydra/YaeMiko
# https://github.com/Team-ProjectCodeX
# https://t.me/O_okarma

# <============================================== IMPORTS =========================================================>
from pyrogram.types import InlineKeyboardButton as ib
from telegram import InlineKeyboardButton

from Mikobot import BOT_USERNAME, OWNER_ID, SUPPORT_CHAT

# <============================================== CONSTANTS =========================================================>
START_IMG = [
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
    "https://files.catbox.moe/8pnohy.jpg",
]

HEY_IMG = "https://telegra.ph/file/33a8d97739a2a4f81ddde.jpg"

ALIVE_ANIMATION = [
    "https://telegra.ph//file/f9e2b9cdd9324fc39970a.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/c4c2759c5fc04cefd207a.mp4",
    "https://telegra.ph//file/b1fa6609b1c4807255927.mp4",
    "https://telegra.ph//file/f3c7147da6511fbe27c25.mp4",
    "https://telegra.ph//file/39071b73c02e3ff5945ca.mp4",
    "https://telegra.ph//file/8d4d7d06efebe2f8becd0.mp4",
    "https://telegra.ph//file/6efdd8e28756bc2f6e53e.mp4",
]

FIRST_PART_TEXT = "✨ *ʜᴇʟʟᴏ* `{}` . . ."

PM_START_TEXT = "<blockquote>➥ I ᴀᴍ ɢʀᴏᴜᴘ ᴍᴀɴᴀɢᴍᴇɴᴛ,ᴀɴᴅ ᴘʀᴏᴛᴇᴄᴛᴏʀ\n➥ Rᴇᴍᴏᴠᴇ ᴄᴏᴘʏʀɪɢʜᴛ ᴍᴇssᴀɢᴇ!\n➥ Dᴇʟᴇᴛᴇ sᴘᴀᴍ ʙᴀᴅ ᴡᴏʀᴅ, ʙᴜssɪɴᴇss,ʟɪɴᴋᴇᴛᴄ. ᴀɴᴅ sᴇɴᴅ ᴡᴀʀɴɪɴɢ</blockquote>\n<blockquote>➥ Dᴇᴠᴇʟᴏᴘᴇʀ:-  ˹ νιкяαηт ˼ @II_JAAT_ON_FIRE_II</blockquote>"
START_BTN = [
    [
        InlineKeyboardButton(
            text="˹ ᴧᴅᴅ ɱҽ ʙᴧʙʏ ˼",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="˹ ʜᴇʟᴘ ˼", callback_data="extra_command_handler"),
        InlineKeyboardButton(text="˹ ᴅᴇᴛᴀɪʟs ˼", callback_data="Miko_"),
    ],
    [
        InlineKeyboardButton(text="˹ sᴏᴜʀᴄᴇ ˼", callback_data="git_source"),
        InlineKeyboardButton(text="˹ Oᴡɳᴇʀ ˼", url=f"tg://user?id={OWNER_ID}"),
    ],
]


GROUP_START_BTN = [
    [
        InlineKeyboardButton(
            text="˹ ᴧᴅᴅ ɱҽ ʙᴧʙʏ ˼",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
    [
        InlineKeyboardButton(text="˹ sᴜᴘᴘᴏʀᴛ ˼", url=f"https://t.me/{SUPPORT_CHAT}"),
        InlineKeyboardButton(text="˹ Oᴡɳᴇʀ ˼", url=f"tg://user?id={OWNER_ID}"),
    ],
]

ALIVE_BTN = [
    [
        ib(text="˹ ᴜᴘᴅᴀᴛᴇs ˼", url="https://t.me/II_JAAT_ON_FIRE_II"),
        ib(text="˹ sᴜᴘᴘᴏʀᴛ ˼", url=f"https://t.me/{SUPPORT_CHAT}"),
    ],
    [
        ib(
            text="˹ ᴧᴅᴅ ɱҽ ʙᴧʙʏ ˼",
            url=f"https://t.me/{BOT_USERNAME}?startgroup=true",
        ),
    ],
]

HELP_STRINGS = """```
☉ Hᴇʀᴇ ɪs ʏᴏᴜʀ ᴀʟʟ ʜᴇʟᴘᴇʀ 
ᴀʟʟ ᴄᴏᴍᴍᴀɴᴅs ᴄᴀɴ ʙᴇ ᴜsᴇᴅ ᴡɪᴛʜ : /```
[ㅤ](https://files.catbox.moe/avwnu7.jpg)
"""
