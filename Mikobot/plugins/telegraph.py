# <============================================== IMPORTS =========================================================>
import os
import requests
from datetime import datetime
from PIL import Image
from pyrogram import filters
from Mikobot import app
from Mikobot.utils.errors import capture_err

# <=======================================================================================================>

TMP_DOWNLOAD_DIRECTORY = "tg-File/"
os.makedirs(TMP_DOWNLOAD_DIRECTORY, exist_ok=True)  # Ensure the directory exists

# <============================================== CATBOX FUNCTION ==================================================>
def upload_to_catbox(file_path):
    """Upload the file to Catbox."""
    url = "https://catbox.moe/user/api.php"
    data = {"reqtype": "fileupload", "json": "true"}
    
    try:
        with open(file_path, "rb") as file:
            files = {"fileToUpload": file}
            response = requests.post(url, data=data, files=files)
        
        if response.status_code == 200:
            try:
                response_json = response.json()
                return True, response_json.get("url", "")
            except ValueError:
                return True, response.text.strip()
        else:
            return False, f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return False, f"Exception occurred: {str(e)}"

# <============================================ BOT COMMAND HANDLER ================================================>
@app.on_message(filters.command(["tgm", "tmg", "telegraph"], prefixes="/"))
@capture_err
async def catbox_upload(client, message):
    """Handle /tgm, /tmg, /telegraph commands to upload media to Catbox."""
    if message.reply_to_message:
        start = datetime.now()
        r_message = message.reply_to_message

        # Download the replied media
        try:
            downloaded_file_name = await client.download_media(
                r_message, file_name=TMP_DOWNLOAD_DIRECTORY
            )
        except Exception as e:
            await message.reply_text(f"Failed to download media: {str(e)}")
            return

        # Handle image resizing for .webp files
        if downloaded_file_name.endswith(".webp"):
            resize_image(downloaded_file_name)

        # Upload to Catbox
        try:
            success, response = upload_to_catbox(downloaded_file_name)
        except Exception as e:
            await message.reply_text(f"Error during upload: {str(e)}")
            os.remove(downloaded_file_name)  # Clean up
            return

        os.remove(downloaded_file_name)  # Clean up

        if success:
            end = datetime.now()
            ms = (end - start).seconds
            await message.reply_text(
                f"➼ **Uploaded to [Catbox]({response}) in {ms} seconds.**\n\n"
                f"➼ **Copy Link:** `{response}`",
                disable_web_page_preview=False,
            )
        else:
            await message.reply_text(f"Upload failed: {response}")
    else:
        await message.reply_text(
            "Reply to a message to get a permanent Catbox link."
        )

# <============================================== IMAGE RESIZING ===================================================>
def resize_image(image):
    """Resize and convert the image to PNG."""
    im = Image.open(image)
    im.save(image, "PNG")

# <=================================================== HELP ====================================================>
__help__ = """ 
<b><u>➠ Tᴇʟᴇɢʀᴀᴘʜ :</u></b>
<blockquote>➯ /tgm, /tmg, /telegraph: Gᴇᴛ ᴛᴇʟᴇɢʀᴀᴍ ʟɪɴᴋ ᴏғ ʀᴇᴘʟɪᴇᴅ ᴍᴇᴅɪᴀ.</blockquote>
"""

__mod_name__ = "˹ ᴛᴇʟᴇɢʀᴀᴘʜ ˼"
# <================================================ END =======================================================>
