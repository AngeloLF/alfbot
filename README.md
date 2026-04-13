# alfbot

Make run bots (for now only Telegram bot available).

You can install the package with the *.toml* :
```bash
pip install e .
```

The dependencies are *coloralf* and *python-telegram-bot* (for now).

For information, none of the functions here ever raise an exception, to not breack a processus : the code print **red warning** if you raise an Exception of any kind.
But, each function as a raiseException argument that can be turn to `True` if you want. There is also a global parameters `RAISE_EXCEPTION`, that can be turn to `True`.




## Bots type

### Telegram Bot

To use telegrame bot:

```python
from alfbot import telegram_bot as tbot

tbot.send(text=text, image=image, bot="name_bot_1", uid="name_chat_1")
```

Arguments `text` and `ìmage` can be either *str* and *list* of *str*. For image, the *str* is the path of the image.
Arguments *bot* and *uid* is not required is you set well (like say part "Json file for tokens and ids").




## Json file for tokens and ids

Obviously, we need a "secure" file to save your tokens and ids. So all bots need a json file. By default, is "alfbot_params.json", and it's save a the user root (like ~/alfbot_params.json). But you can change this.

First, there is the json file format :
```json
{
    "telegram":{
        "bots":{
            "name_bot_1" : "xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",
            "name_bot_2" : "xxxxxxxxxx:xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
        },
        "uids":{
            "name_chat_1" : "3141592654",
            "name_chat_2" : "-1234567899"
        }
    }
}
```

All "send" fonction take a default value for bot, uid, and path and name of the json file.
You can change easily these value like this (for example just after imports):

```python 
PATH_JSON = os.path.expanduser("~/")
DEFAULT_JSON = "alfbot_params.json"
DEFAULT_BOT = "ccalf"
DEFAULT_UID = "alf"
```