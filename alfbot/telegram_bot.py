import asyncio
import sys, os, json

import coloralf as c
from telegram import Bot, InputFile

path_home = os.path.expanduser("~/")



async def main(text=None, image=None, bot="ccalf", uid="alf", raiseException=True):

    file_param = f"{path_home}alfbot_params.json"
    if os.path.exists(file_param):
        with open(file_param, "r") as f:
            params = json.load(f)

        ### verify bot token and chat ids
        token_id_ok = True

        if bot in params["telegram"]["bots"].keys():
            TOKEN = params["telegram"]["bots"][bot]
        else:
            token_id_ok = False
            print(f"{c.r}WARNING [in telegram_bot.py] : bot {c.tu}{bot}{c.ru} not know{c.d}")
            print(f"{c.r}* List of bot in {file_param} : {", ".join(list(params['telegram']['bots'].keys()))}{c.d}")

        if uid in params["telegram"]["uids"].keys():
            CHAT_ID = params["telegram"]["uids"][uid]
        else:
            token_id_ok = False
            print(f"{c.r}WARNING [in telegram_bot.py] : user id {c.tu}{uid}{c.ru} not know{c.d}")
            print(f"{c.r}* List of uid in {file_param} : {", ".join(list(params['telegram']['uids'].keys()))}{c.d}")

        if raiseException and not token_id_ok:
            raise Exception(f"bot or uid is not know")


        try:

            bot = Bot(TOKEN)
            bot_name_class = await bot.getMyName()
            bot_name = bot_name_class.name

            if text is not None:

                texts = text if isinstance(text, (list)) else [text]

                for t in texts:

                    await bot.send_message(chat_id=CHAT_ID, text=f"{t.replace('-', '\\-')}", parse_mode="MarkdownV2")
                    print(f"{c.ti}<{bot_name}> send : {t}{c.d}")


            if image is not None:

                images = image if isinstance(image, (list)) else [image]

                for i in images:
                    with open(i, 'rb') as photo_file:
                        await bot.send_photo(chat_id=CHAT_ID, photo=InputFile(photo_file))
                        print(f"{c.ti}<{bot_name}> send image : {i}{c.d}")

        except Exception as e:
            error_msg = traceback.format_exc()
            print(f"\n{c.r}Error {e} on {img}{c.d}")
            print(f"{c.lr}{error_msg}{c.d}")


    elif raiseException:
        raise Exception(f"File param {file_param} don't exist")
    else:
        print(f"{c.r}WARNING [in telegram_bot.py] : file param {c.tu}{file_param}{c.ru} don't exist{c.d}")


def send_message(text, bot="ccalf", uid="alf"):

    asyncio.run(main(text=text, bot=bot, uid=uid))

def send_image(text=None, image=None):

    asyncio.run(main(text=text, image=image))




if __name__ == '__main__':

    if "test" in sys.argv[1:]:

        print(f"Begin test ...")

        if "message" in sys.argv[1:] or "m" in sys.argv[1:]:

            send_message("Test solo")
            send_message("Test formatage : *en* *gras* --- _en_ _italique_ --- ~barré~ --- `code`")

        if "image" in sys.argv[1:] or "s" in sys.argv[1:]:

            send_image(text="Test image (*chou*) : ", image=["./chou128.png"])

        if len(sys.argv) == 2:

            print("Need 'message' or 'image' for test ...")

        print(f"Test end.")
    
    else:

        msg = None
        bot = None
        uid = None

        for argv in sys.argv[1:]:

            if argv.startswith("msg=") : msg = argv.split("=")[1]
            if argv.startswith("bot=") : bot = argv.split("=")[1]
            if argv.startswith("uid=") : uid = argv.split("=")[1]

        all_args = True

        if msg is None:
            all_args = False
            print(f"{c.r}WARNING [in telegram_bot.py] : 'msg' needed in args (msg='my message'){c.d}")

        if bot is None:
            all_args = False
            print(f"{c.r}WARNING [in telegram_bot.py] : 'bot' needed in args (bot=ccalf){c.d}")

        if uid is None:
            all_args = False
            print(f"{c.r}WARNING [in telegram_bot.py] : 'uid' needed in args (uid=alf){c.d}")

        if all_args:
            send_message(msg, bot=bot, uid=uid)
        else:
            raise Exception(f"Need msg, bot and uid args")

