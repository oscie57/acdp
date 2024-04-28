import os, python_weather, asyncio, sys, requests, json, io
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style, init
from timer_py import Timer

from common import (
    b, g, p, o, c, y,
    pocketcalc,
    keywords_snow, keywords_rain
)

init()
load_dotenv()

cloudurl = "https://cloud.oscie.net/acdp"

if not os.path.exists(".env"):
    print("\nTo run, we need to use " + b("dotenv") + " to get your location. There should be a file called " + b("'.env'") + "in the same directory as " + b("'play.py'") + ". Read the README.md for more information.")
    sys.exit(0)


timer = Timer('Timer')
timer.start()

volume = int(os.getenv("VOLUME"))
area = str(os.getenv("AREA"))
roost = str(os.getenv("ROOST"))

try:
    games = requests.get(f"https://cloud.oscie.net/acdp/list.json", timeout=10).json()
except:
    print("Could not connect to the server, please try again later.")
    sys.exit(0)


async def getweather():
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(area)

        sky = weather.current.description

        await client.close()

        return sky


def game_select():

    gameslist = []

    for game in games['available']:
        gameslist.append(game['shortname'])

    print("\nWelcome to the " + p("ACDP") + " game selector.\nIf you're seeing this, chances are you haven't selected a game.\nPlease select a game by typing the name:\n")

    for game in games['available']:
        print(f"- {g(game['shortname'])} requires ~{b('0 MB (Network Mode)')}")

    game = input("\nPlease " + b("choose a game") + ": " + Fore.GREEN)

    for gameitem in games['available']:
        if game == gameitem['shortname']:
            gamedata = gameitem

    namejson = {
        "long": gamedata['name'],
        "short": gamedata['shortname'],
        "code": gamedata['code']
    }

    with open('./selection.json', 'x') as f:
        json.dump(namejson, f)


async def gamecheck():
    global playcount
    playcount = 0

    print("Checking for games...\n")

    if not os.path.exists("./selection.json"):
        game_select()

    with open("./selection.json", "r") as f:
        game = json.load(f)
        print(g(game['long']) + " has been detected.\nTo change the game, delete 'selection.json'. Enjoy the music!\n")

    while True:
        sky = await getweather()
        sky2 = sky.lower()

        if game == "Animal Crossing":
            if any(i in sky2 for i in keywords_snow):
                gameweather = "snow"
            else:
                gameweather = "clear"
        else:
            if any(i in sky2 for i in keywords_snow):
                gameweather = "snow"
            elif any(i in sky2 for i in keywords_rain):
                gameweather = "rain"
            else:
                gameweather = "clear"

        gametime = datetime.now().strftime("%H")

        print(Style.RESET_ALL + "[" + datetime.now().strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + Fore.YELLOW)

        if game['long'] == "Animal Crossing: Pocket Camp":
            url = f"{cloudurl}/acpc/{pocketcalc(gametime)}.mp3"
        else:
            url = f"{cloudurl}/{game['code']}/{gameweather}/{gametime}.mp3"

        mp3file = requests.get(url)
        content = io.BytesIO(mp3file.content)

        playcount = playcount + 1
        song = AudioSegment.from_mp3(content)
        song = song - volume

        play(song)


async def main():
    print("\nWelcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing") + " games' music based around the " + b("weather") + " and " + b("time") + " around you.\n")
    print(y("This is a BETA version of the ") + p("Animal Crossing Dynamic Player") + y(", created for network streaming.\nThere may be bugs, and playback may occasionally break due to external factors.\nIf this happens, please let me know in my Discord server (https://discord.ggymb84qM54A) in #acdp,\nor create an issue on GitHub (https://github.com/oscie57/acdp/issues).\n"))

    await gamecheck()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(c("\n\nExiting program...\n"))
        print("While using this app, you listened to the music " + b(str(playcount)) + " times!")

        minutes = timer.elapsed(print=False) // 60
        print("you also listened for " + b(str(int(timer.elapsed(print=False)))) + f" seconds! ({b(str(int(minutes)))} minutes)")

        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
