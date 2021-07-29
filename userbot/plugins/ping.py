#======================================================================================================================================
import os
import asyncio
from datetime import datetime

from userbot import catub
from . import hmention, reply_id

"""
try:
    from . import PING_PIC, PING_TEXT
except:
    pass
"""
plugin_category = "extra"

PING_PIC = os.environ.get("PING_PIC")  # or Config.PING_PIC
PING_TEXT = os.environ.get("CUSTOM_PING_TEXT", None) or " 𝔓𝔢𝔯𝔣𝔢𝔠𝔱𝔩𝔶 𝔅𝔞𝔩𝔞𝔫𝔠𝔢𝔡, 𝔞𝔰 𝔞𝔩𝔩 𝔱𝔥𝔦𝔰 𝔰𝔥𝔬𝔲𝔩𝔡 𝔟𝔢 !! \n " 


@catub.cat_cmd(
    pattern="ping$",
    command=("ping", plugin_category),
    info={
        "header": "check how long it takes to ping your userbot.",
        "option": "To show media in this cmd you need to set PING_PIC with media link, get this by replying the media by .tgm",
        "usage": ["{tr}ping", ],
    },
)
async def _(event):
    if event.fwd_from:
        return
    reply_to_id = await reply_id(event)
    start = datetime.now()
    cat = await edit_or_reply(event, "<b><i>“Everyone fails at who they are supposed to be. The measure of a person, of a hero…is how well they succeed at being who they are” !! ⚡ </b></i>", "html")
    end = datetime.now()
    await cat.delete()
    ms = (end - start).microseconds / 1000
    if PING_PIC:
        caption = f"<b><i>{ PING_TEXT}<i><b>\n<code>⚜️ {ms} ms</code>\n⚜️ <b><i>  Aѵҽղցҽɾ  ☞  {hmention}</b></i>"
        await event.client.send_file(
            event.chat_id,
            PING_PIC,
            caption=caption,
            parse_mode="html",
            reply_to=reply_to_id,
            link_preview=False,
            allow_cache=True,
        )
    else:
        await event.edit_or_reply(event, "<code>Add PING_PIC first nubh.<code>", "html")

#======================================================================================================================================
