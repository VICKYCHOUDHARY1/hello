# SOURCE https://github.com/Team-ProjectCodeX
# CREATED BY https://t.me/O_okarma
# API BY https://www.github.com/SOME-1HING
# PROVIDED BY https://t.me/ProjectCodeX

# <============================================== IMPORTS =========================================================>
import json
import random

from pyrogram import Client, filters
from pyrogram.types import InputMediaPhoto, Message

from Mikobot import app
from Mikobot.state import state

# <=======================================================================================================>

BINGSEARCH_URL = "https://sugoi-api.vercel.app/search"
NEWS_URL = "https://sugoi-api.vercel.app/news?keyword={}"


# <================================================ FUNCTION =======================================================>
@app.on_message(filters.command("news"))
async def news(_, message: Message):
    keyword = (
        message.text.split(" ", 1)[1].strip() if len(message.text.split()) > 1 else ""
    )
    url = NEWS_URL.format(keyword)

    try:
        response = await state.get(url)  # Assuming state is an asynchronous function
        news_data = response.json()

        if "error" in news_data:
            error_message = news_data["error"]
            await message.reply_text(f"Error: {error_message}")
        else:
            if len(news_data) > 0:
                news_item = random.choice(news_data)

                title = news_item["title"]
                excerpt = news_item["excerpt"]
                source = news_item["source"]
                relative_time = news_item["relative_time"]
                news_url = news_item["url"]

                message_text = f"𝗧𝗜𝗧𝗟𝗘: {title}\n𝗦𝗢𝗨𝗥𝗖𝗘: {source}\n𝗧𝗜𝗠𝗘: {relative_time}\n𝗘𝗫𝗖𝗘𝗥𝗣𝗧: {excerpt}\n𝗨𝗥𝗟: {news_url}"
                await message.reply_text(message_text)
            else:
                await message.reply_text("No news found.")

    except Exception as e:  # Replace with specific exception type if possible
        await message.reply_text(f"Error: {str(e)}")


@app.on_message(filters.command("bingsearch"))
async def bing_search(client: Client, message: Message):
    try:
        if len(message.command) == 1:
            await message.reply_text("Please provide a keyword to search.")
            return

        keyword = " ".join(
            message.command[1:]
        )  # Assuming the keyword is passed as arguments
        params = {"keyword": keyword}

        response = await state.get(
            BINGSEARCH_URL, params=params
        )  # Use the state.get method

        if response.status_code == 200:
            results = response.json()
            if not results:
                await message.reply_text("No results found.")
            else:
                message_text = ""
                for result in results[:7]:
                    title = result.get("title", "")
                    link = result.get("link", "")
                    message_text += f"{title}\n{link}\n\n"
                await message.reply_text(message_text.strip())
        else:
            await message.reply_text("Sorry, something went wrong with the search.")
    except Exception as e:
        await message.reply_text(f"An error occurred: {str(e)}")


# Command handler for the '/bingimg' command
@app.on_message(filters.command("bingimg"))
async def bingimg_search(client: Client, message: Message):
    try:
        text = message.text.split(None, 1)[
            1
        ]  # Extract the query from command arguments
    except IndexError:
        return await message.reply_text(
            "Provide me a query to search!"
        )  # Return error if no query is provided

    search_message = await message.reply_text("🔎")  # Display searching message

    # Send request to Bing image search API using state function
    bingimg_url = "https://sugoi-api.vercel.app/bingimg?keyword=" + text
    resp = await state.get(bingimg_url)
    images = json.loads(resp.text)  # Parse the response JSON into a list of image URLs

    media = []
    count = 0
    for img in images:
        if count == 7:
            break

        # Create InputMediaPhoto object for each image URL
        media.append(InputMediaPhoto(media=img))
        count += 1

    # Send the media group as a reply to the user
    await message.reply_media_group(media=media)

    # Delete the searching message and the original command message
    await search_message.delete()
    await message.delete()


# Command handler for the '/googleimg' command
@app.on_message(filters.command("googleimg"))
async def googleimg_search(client: Client, message: Message):
    try:
        text = message.text.split(None, 1)[
            1
        ]  # Extract the query from command arguments
    except IndexError:
        return await message.reply_text(
            "Provide me a query to search!"
        )  # Return error if no query is provided

    search_message = await message.reply_text("💭")  # Display searching message

    # Send request to Google image search API using state function
    googleimg_url = "https://sugoi-api.vercel.app/googleimg?keyword=" + text
    resp = await state.get(googleimg_url)
    images = json.loads(resp.text)  # Parse the response JSON into a list of image URLs

    media = []
    count = 0
    for img in images:
        if count == 7:
            break

        # Create InputMediaPhoto object for each image URL
        media.append(InputMediaPhoto(media=img))
        count += 1

    # Send the media group as a reply to the user
    await message.reply_media_group(media=media)

    # Delete the searching message and the original command message
    await search_message.delete()
    await message.delete()


# <=======================================================================================================>


# <=================================================== HELP ====================================================>
__mod_name__ = "˹ sᴇᴀʀᴄʜ ˼"

__help__ = """
<b><u>➠ Sᴇᴀʀᴄʜ ᴄᴏᴍᴍᴀɴᴅs :</u></b>
<blockquote>➯ /googleimg &lt;search query&gt;: ɪᴛ ʀᴇᴛʀɪᴇᴠᴇs ᴀɴᴅ ᴅɪsᴘʟᴀʏ ɪᴍᴀɢᴇs ᴏʙᴛᴀɪɴᴇᴅ ᴛʜʀᴏᴜɢʜᴛ ᴀ ɢᴏᴏɢʟᴇ ɪᴍᴀɢᴇ sᴇᴀʀᴄʜ.

➯ /bingimg &lt;search query&gt;: ɪᴛ ʀᴇᴛʀɪᴇᴠᴇs ᴀɴᴅ ᴅɪsᴘʟᴀʏ ɪᴍᴀɢᴇs ᴏʙᴛᴀɪɴᴇᴅ ᴛʜʀᴏᴜɢʜᴛ ᴀ ʙɪɴɢ ɪᴍᴀɢᴇ sᴇᴀʀᴄʜ.

➯ /news &lt;search query&gt; : sᴇᴀʀᴄʜ ɴᴇᴡs.

➯ /bingsearch &lt;search query&gt; : ɢᴇᴛ sᴇᴀʀᴄʜ ʀᴇsᴜɪʟᴛ ᴡɪᴛʜ ʟɪɴᴋs.</blockquote>

<b><u>➠ Exᴀᴍᴘʟᴇ :</u></b>
<blockquote>➯ /bingsearch app: ʀᴇᴛᴜʀɴ sᴇᴀʀᴄʜ ʀᴇsᴜɪʟᴛs.</blockquote>
"""
# <================================================ END =======================================================>
