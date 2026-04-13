import asyncio
import sys, os, json
import traceback

import coloralf as c
from telegram import Bot, InputFile

PATH_JSON = os.path.expanduser("~/")
DEFAULT_JSON = "alfbot_params.json" # need to be a json ! see README for the format
DEFAULT_BOT = "ccalf"
DEFAULT_UID = "alf"
RAISE_EXCEPTION = False



async def main(text=None, image=None, bot=None, uid=None, raiseException=None):

    # define file params
    file_param = f"{PATH_JSON}{DEFAULT_JSON}"

    # take default param is bot or/and uid is None
    if bot is None:
        bot = DEFAULT_BOT
    if uid is None:
        uid = DEFAULT_UID
    if raiseException is None:
        raiseException = RAISE_EXCEPTION

    # Verify json param
    if os.path.exists(file_param):

        with open(file_param, "r") as f:
            params = json.load(f)


        # verify bot token and chat ids
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

        if not token_id_ok:
            
            if raiseException:
                raise Exception(f"bot or uid is not know")
        
        else:

            # seed message
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

                if str(e) == "httpx.ConnectError: [Errno 8] nodename nor servname provided, or not known":
                    print(f"{c.r}No connection ... verify wifi{c.d}")
                else:
                    error_msg = traceback.format_exc()
                    print(f"\n{c.r}Error {e}{c.d}")
                    print(f"{c.lr}{error_msg}{c.d}")


    elif raiseException:
        raise Exception(f"File param {file_param} don't exist")
    else:
        print(f"{c.r}WARNING [in telegram_bot.py] : file param {c.tu}{file_param}{c.ru} don't exist{c.d}")




# principal function
def send(text=None, image=None, bot=None, uid=None, raiseException=False):

    try:

        asyncio.run(main(text, image, bot, uid, raiseException))
   
    except Exception as e:

        error_msg = traceback.format_exc()
        print(f"{c.r}{c.tb}WARNING [in telegram_bot.py] : this exception is not normal (call the maker :)){c.d}")
        print(f"{c.r}Error {e}{c.d}")
        print(f"{c.lr}{error_msg}{c.d}")

        if raiseException:
            raise e





if __name__ == '__main__':

    # for test the bot with default bot & uid
    if "test" in sys.argv[1:]:

        print(f"Begin test ...")

        if "message" in sys.argv[1:] or "m" in sys.argv[1:]:

            send("Test solo")
            send("Test formatage : *en* *gras* --- _en_ _italique_ --- ~barré~ --- `code`")

        if "image" in sys.argv[1:] or "s" in sys.argv[1:]:

            send(text="Test image (*chou*) : ", image=["./chou128.png"])

        if len(sys.argv) == 2:

            print("Need 'message' or 'image' for test ...")

        print(f"Test end.")
        
    # for test with choosing the msg, bot and uid
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

