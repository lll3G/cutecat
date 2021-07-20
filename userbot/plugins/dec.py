from telethon import events
from telethon.errors.rpcerrorlist import YouBlockedUserError

@bot.on(admin_cmd(pattern="dec ?(.*)"))
@bot.on(sudo_cmd(pattern="dec ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to a media message")
        return
    chat = "@hcdecryptor_bot"
    if reply_message.sender.bot:
        await edit_or_reply(event, "Reply to actual users message.")
        return
    catevent = await edit_or_reply(event, "`Executing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1326174178)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await catevent.edit("Please unblock `@hcdecryptor_bot `and try again")
            return
        if response.text.startswith("Forward"):
            await catevent.edit(
                "can you kindly disable your forward privacy settings for good?"
            )
        else:
            if response.text.startswith("Tidak"):
                await catevent.edit(
                    "Decrypt Failed."
                )
            else:
                await catevent.edit(
                    f"**This is the result**\n {response.message.message}"
                )

@bot.on(admin_cmd(pattern="evozi ?(.*)"))
@bot.on(sudo_cmd(pattern="evozi ?(.*)", allow_sudo=True))
async def _(event):
    if event.fwd_from:
        return
    if not event.reply_to_msg_id:
        await edit_or_reply(event, "Reply to any user message.")
        return
    reply_message = await event.get_reply_message()
    if not reply_message.media:
        await edit_or_reply(event, "reply to a media message")
        return
    chat = "@decrypt_evozi_bot"
    if reply_message.sender.bot:
        await edit_or_reply(event, "Reply to actual users message.")
        return
    catevent = await edit_or_reply(event, "`Executing...`")
    async with event.client.conversation(chat) as conv:
        try:
            response = conv.wait_event(
                events.NewMessage(incoming=True, from_users=1795403022)
            )
            await event.client.forward_messages(chat, reply_message)
            response = await response
        except YouBlockedUserError:
            await catevent.edit("Please unblock `@decrypt_evozi_bot `and try again")
            return
        if response.text.startswith("Forward"):
            await catevent.edit(
                "can you kindly disable your forward privacy settings for good?"
            )
        else:
            if response.text.startswith("Tidak"):
                await catevent.edit(
                    "Decrypt Failed."
                )
            else:
                await catevent.edit(
                    f"**This is the result**\n {response.message.message}"
                )
