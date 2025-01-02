# <============================================== IMPORTS =========================================================>
import base64
import aiohttp
from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import CommandHandler, ContextTypes
from Mikobot import LOGGER as logger
from Mikobot import function

# <=======================================================================================================>

# <================================================ CONSTANTS =====================================================>
API_URL = "https://lexica.qewertyy.dev/models"
PALM_MODEL_ID = 0
GPT_MODEL_ID = 5

# <================================================ FUNCTIONS =====================================================>

async def get_api_response(model_id, api_params, api_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(api_url, json=api_params) as response:
                if response.status == 200:
                    data = await response.json()
                    return data.get(
                        "content", f"Error: Empty response received from the {model_id} API."
                    )
                else:
                    return f"Error: Request failed with status code {response.status}."
    except aiohttp.ClientError as e:
        return f"Error: An error occurred while calling the {model_id} API. {e}"


async def palm_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: Missing input text after /palm command.",
        )
        return

    input_text = " ".join(args)

    result_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="🌴 Processing..."
    )

    api_params = {"model_id": PALM_MODEL_ID, "prompt": input_text}
    api_response = await get_api_response("PALM", api_params, API_URL)

    await result_msg.delete()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=api_response)


async def gpt_chatbot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if not args:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Error: Missing input text after /askgpt command.",
        )
        return

    input_text = " ".join(args)

    result_msg = await context.bot.send_message(
        chat_id=update.effective_chat.id, text="💬 Processing..."
    )

    api_params = {"model_id": GPT_MODEL_ID, "prompt": input_text}
    api_response = await get_api_response("GPT", api_params, API_URL)

    await result_msg.delete()
    await context.bot.send_message(chat_id=update.effective_chat.id, text=api_response)


async def upscale_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        if update.message.reply_to_message and update.message.reply_to_message.photo:
            progress_msg = await update.message.reply_text(
                "Enhancing your image, please wait..."
            )

            image = await update.message.reply_to_message.photo[-1].get_file()
            image_path = await image.download_to_drive()

            with open(image_path, "rb") as image_file:
                image_data = image_file.read()

            b64_image = base64.b64encode(image_data).decode("utf-8")
            payload = {
                "resize_mode": 0,
                "show_extras_results": True,
                "gfpgan_visibility": 0,
                "codeformer_visibility": 0,
                "codeformer_weight": 1,
                "upscaling_resize": 2,
                "upscaler_1": "4xUltrasharpV10",
                "upscaler_2": "R-ESRGAN 4x+",
                "upscale_first": False,
                "image": b64_image,
            }
            headers = {
                "Content-Type": "application/json",
                "Authorization": "Basic cGljYXRvYXBpOko3XnMxazYqaTJA"
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(
                    "http://110.93.223.194:5670/sdapi/v1/extra-single-image",
                    json=payload,
                    headers=headers
                ) as response:
                    if response.status == 200:
                        response_data = await response.json()
                        enhanced_image = response_data.get('image')
                        enhanced_image_binary = base64.b64decode(enhanced_image)
                        upscaled_file_path = "upscaled_image.png"

                        with open(upscaled_file_path, "wb") as output_file:
                            output_file.write(enhanced_image_binary)

                        await context.bot.delete_message(
                            chat_id=update.message.chat_id, message_id=progress_msg.message_id
                        )

                        await update.message.reply_document(
                            document=open(upscaled_file_path, "rb"),
                            caption=f"<b>Enhance your image.</b>\n<b>Enhanced By:</b> @{context.bot.username}",
                            parse_mode=ParseMode.HTML,
                        )
                    else:
                        raise Exception(f"Upscaling failed with status code {response.status}")
        else:
            await update.message.reply_text("Please reply to an image to upscale it.")

    except Exception as e:
        logger.error(f"Failed to upscale the image: {e}")
        await update.message.reply_text(
            "Failed to upscale the image. Please try again later."
        )



# <================================================ HANDLERS =======================================================>
function(CommandHandler("enhance", upscale_image, block=False))
function(CommandHandler("palm", palm_chatbot, block=False))
function(CommandHandler("askgpt", gpt_chatbot, block=False))
# <================================================ END =======================================================>
