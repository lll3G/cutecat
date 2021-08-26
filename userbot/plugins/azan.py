import json
import requests
from . import catub, edit_delete, edit_or_reply

PLACE = ""

plugin_category = "extra"

@catub.cat_cmd(
    pattern="azan(?: |$)(.*)",
    command=("azan", plugin_category),
    info={
        "header": "يوضح لك أوقات الصلاة الإسلامية باسم المدينة المعطاة.",
        "note": "يمكنك تعيين المدينة الافتراضية باستخدام الأمر {tr} setcity.",
        "usage": "{tr}azan <اسم المدينة باللغة الانجليزية>",
        "examples": "{tr}azan baghdad ",
    },
)
async def get_adzan(adzan):
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("يرجى تحديد مدينة أو دولة باللغة الانجليزية.")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

    # url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}&timeformat=2"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"لا يمكنني إيجاد المـديـنه `{LOCATION}`")

    parsed = json.loads(request.text)

    city = parsed["results"]["location"]["city"]
    country = parsed["results"]["location"]["country"]
    timezone = parsed["results"]["location"]["timezone"]
    date = parsed["results"]["datetime"][0]["date"]["gregorian"]

    imsak = parsed["results"]["datetime"][0]["times"]["Imsak"]
    subuh = parsed["results"]["datetime"][0]["times"]["Fajr"]
    zuhur = parsed["results"]["datetime"][0]["times"]["Dhuhr"]
    ashar = parsed["results"]["datetime"][0]["times"]["Asr"]
    maghrib = parsed["results"]["datetime"][0]["times"]["Maghrib"]
    isya = parsed["results"]["datetime"][0]["times"]["Isha"]

    result = (
        f"**جـــدول صــــــلوآت  🌷🌹** :\n"
        f"📅 `{date} | {timezone}`\n"
        f"🌏 `{city} | {country}`\n\n"
        f"**إمـســآك :** `{imsak}`\n"
        f"**الفجــر :** `{subuh}`\n"
        f"**الظـهــر :** `{zuhur}`\n"
        f"**العصــر :** `{ashar}`\n"
        f"**المـغــرب :** `{maghrib}`\n"
        f"**العشــآء :** `{isya}`\n"
    )

    await adzan.edit(result)
