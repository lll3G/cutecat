import json
import requests
from . import catub, edit_delete, edit_or_reply

PLACE = ""

plugin_category = "extra"

@catub.cat_cmd(
    pattern="azan(?: |$)(.*)",
    command=("azan", plugin_category),
    info={
        "header": "Shows you the Islamic prayer times of the given city name.",
        "note": "you can set default city by using {tr}setcity command.",
        "usage": "{tr}azan <city>",
        "examples": "{tr}azan baghdad ",
    },
)
async def get_adzan(adzan):
    if not adzan.pattern_match.group(1):
        LOCATION = PLACE
        if not LOCATION:
            await adzan.edit("Please specify a city or a state.")
            return
    else:
        LOCATION = adzan.pattern_match.group(1)

    # url = f'http://muslimsalat.com/{LOKASI}.json?key=bd099c5825cbedb9aa934e255a81a5fc'
    url = f"https://api.pray.zone/v2/times/today.json?city={LOCATION}&timeformat=2"
    request = requests.get(url)
    if request.status_code == 500:
        return await adzan.edit(f"Couldn't find city `{LOCATION}`")

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
        f"**Jadwal Sholat 🌹🌹**:\n"
        f"📅 `{date} | {timezone}`\n"
        f"🌏 `{city} | {country}`\n\n"
        f"**Imsak :** `{imsak}`\n"
        f"**Subuh :** `{subuh}`\n"
        f"**Zuhur :** `{zuhur}`\n"
        f"**Ashar :** `{ashar}`\n"
        f"**Maghrib :** `{maghrib}`\n"
        f"**Isya :** `{isya}`\n"
    )

    await adzan.edit(result)
