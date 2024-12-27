from pyrogram import filters

from Mikobot import app
from Mikobot.state import state

# Configuration - The PALM API URL
PALM_API_URL = "https://lexica.qewertyy.dev/models"
MODEL_ID = 1  # Modify this if you have a specific model ID to use


# Function to call the PALM API and get the response
async def get_palm_response(api_params):
    try:
        response = await state.post(PALM_API_URL, params=api_params)
        if response.status_code == 200:
            data = response.json()
            return data.get(
                "content", "Error: Empty response received from the PALM API."
            )
        else:
            return f"Error: Request failed with status code {response.status_code}."
    except fetch.RequestError as e:
        return f"Error: An error occurred while calling the PALM API. {e}"


# Command handler for /palm
@app.on_message(filters.text)
async def palm_chatbot(client, message):
    if not message.text.startswith("Miko"):
        return
        # your code here
    args = message.text.split(maxsplit=1)
    if len(args) < 2:
        await message.reply("Give me a query to search.")
        return

    input_text = args[1]

    # Send the "giving results" message first
    result_msg = await message.reply("🔍")

    # Call the PALM API to get the chatbot response asynchronously
    api_params = {"model_id": MODEL_ID, "prompt": input_text}
    api_response = await get_palm_response(api_params)

    # Delete the "giving results" message
    await result_msg.delete()

    # Send the chatbot response to the user
    await message.reply(api_response)


__help__ = """
<blockquote><b><u>Aʟʟ Cᴏᴍᴍᴀɴᴅ ᴜsᴇ /:</u></b></blockquote>
<blockquote>➥ /askgpt &lt;wʀɪᴛᴇ ǫᴜᴇʀʏ&gt;: ᴀ ᴄʜᴀᴛɢᴘᴛ ʀᴇsᴘᴏɴᴅɪɴɢ ᴛᴏ ᴜsᴇʀ ǫᴜᴇʀɪᴇs.

➥ /palm &lt;wʀɪᴛᴇ ᴘʀᴏᴍᴛ&gt;: Pᴇʀғᴏʀᴍs ᴀ ᴘᴀʟᴍ sᴇᴀʀᴄʜ ᴜsɪɴɢ ᴀ ᴄʜᴀᴛɢᴘᴛ.

➥ /upscale &lt;ʀᴇᴘʟʏ ᴛᴏ ɪᴍᴀɢᴇ&gt;: Uᴘsᴄᴀʟᴇs ʏᴏᴜʀ ɪᴍᴀɢᴇ ǫᴜɪʟɪᴛʏ.</blockquote>
"""

__mod_name__ = "˹ ᴄʜᴀᴛʙᴏᴛ ˼"
