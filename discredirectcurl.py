# -*- coding: UTF-8 -*-

import pycurl, json, re, hexchat, certifi
#from io import BytesIO

__module_name__ = "hextodiscurl"
__module_version__ = "1.0"
__module_description__ = "Redirect HexChat->Discord"

URL = "http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+"
HOOKURL = "put API key here"


def forward_cb(word,word_eol,userdata):
    nick = word[0]
    message = word[1]

    # Prevent URLs from being embedded in Discord (optional)
    message = message.split()
    messages = ""
    for text in message:
        if re.match(URL,text):
            messages = (messages + ("``" + text + "``" + " "))
        else:
            messages += (text + " ")

    payload = json.dumps({"username":nick,"content":messages})
    #buf = BytesIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, HOOKURL)
    c.setopt(pycurl.HTTPHEADER, ['Content-type:application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.CAINFO, certifi.where())
    c.setopt(pycurl.POSTFIELDS, payload)
    c.setopt(pycurl.VERBOSE, 1)
    #c.setopt(pycurl.WRITEFUNCTION, buf.write)
    c.setopt(pycurl.USERAGENT,
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64;en; rv:5.0) Gecko/20110619 Firefox/5.0")
    c.perform()
    c.close()
    #hexchat.prnt(str(buf.getvalue()))
    #buf.close()
    return hexchat.EAT_NONE

hexchat.hook_print("Channel Message", forward_cb)
hexchat.hook_print("Your Message", forward_cb)
hexchat.hook_print("Channel Msg Hilight", forward_cb)
hexchat.prnt(__module_name__ + " version " + __module_version__ + " loaded.")
