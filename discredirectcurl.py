# -*- coding: UTF-8 -*-

import json
import re
import hexchat
import requests

__module_name__ = "hextodiscurl"
__module_version__ = "1.0"
__module_description__ = "Redirect HexChat->Discord"

URL = r"http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
HOOKURL = "put API key here"


def forward_cb(word, word_eol, userdata):
    nick = word[0]
    message = word[1]

    # Prevent URLs from being embedded in Discord (optional)
    message = message.split()
    messages = ""
    for text in message:
        if re.match(URL, text):
            messages = (messages + ("``" + text + "``" + " "))
        else:
            messages += (text + " ")

    payload = json.dumps({"username": nick, "content": messages})
    requests.post(HOOKURL, headers={'Content-type':'application/json'}, data=payload)
    return hexchat.EAT_NONE


hexchat.hook_print("Channel Message", forward_cb)
hexchat.hook_print("Your Message", forward_cb)
hexchat.hook_print("Channel Msg Hilight", forward_cb)
hexchat.prnt(__module_name__ + " version " + __module_version__ + " loaded.")
