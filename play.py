import os, python_weather, asyncio, sys, time, aiohttp, requests, random
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style, init
from timer_py import Timer

from common import (
    b, g, p, o, c, y,
    pocketcalc,
    keywords_rain, keywords_snow
)

init()
load_dotenv()


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


if roost == "True" and os.path.exists("./files/roost.mp3"):
    playroost = True
else:
    playroost = False


def filecheck():
    if not os.path.exists("./files/"):
        os.mkdir("./files/")

    if not os.path.exists("./files/rain/"):
        os.mkdir("./files/rain/")

    if not os.path.exists("./files/snow/"):
        os.mkdir("./files/snow/")

    if not os.path.exists("./files/clear/"):
        os.mkdir("./files/clear/")


async def videoDL(outfile, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(outfile, "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)
    except Exception as e:
        print(f"**`ERROR:`** {type(e).__name__} - {e}")


async def getweather():
    async with python_weather.Client(format=python_weather.IMPERIAL) as client:
        weather = await client.get(area)

        sky = weather.current.description

        await client.close()

        return sky


async def gamecheck():
    global playcount
    playcount = 0

    filecheck()

    print("Checking for games...")

    if not os.path.exists("./files/name.txt"):
        await downloader_menu()

    with open("./files/name.txt", "r") as f:
        game = f.read()
        print(g(game) + " has been detected, enjoy the music!\n")

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

        print(Style.RESET_ALL + "[" + datetime.now().strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + " - " + b(gameweather.capitalize()) + Fore.YELLOW)

        if game == "Animal Crossing: Pocket Camp":
            dir = f"./files/{pocketcalc(gametime)}.mp3"
        else:
            if playroost == True:
                rack = random.randint(1, 100)
                if rack == 5:
                    dir = "./files/roost.mp3"
                else:
                    dir = f"./files/{gameweather}/{gametime}.mp3"
            else:
                dir = f"./files/{gameweather}/{gametime}.mp3"

        playcount = playcount + 1
        song = AudioSegment.from_mp3(dir)
        if rack == 5:
            song = song
        else:
            song = song - volume

        play(song)


async def downloader_menu():

    gameslist = []

    for game in games['available']:
        gameslist.append(game['shortname'])

    print("\nWelcome to the " + p("ACDP") + " (" + p("Animal Crossing Dynamic Player") + ") music downloader.\nIf you're seeing this, " + c("chances are, you do not have the audio files downloaded.\n") + "\n" + c("Space Requirements:"))

    for game in games['available']:
        print(f"- {g(game['shortname'])} requires ~{b(game['size'])}")

    game = input("\nPlease " + b("choose a game") + " to download the OST: " + Fore.GREEN)

    if game not in gameslist:
        print(Style.RESET_ALL + "\n'" + b(game) + "' is not a valid option. Valid options include:\n" + g(str(gameslist).replace("[", "").replace("]", "")) + "\n")
        await downloader_menu()

    for gameitem in games['available']:
        if gameitem['shortname'] == game:
            gamecode = gameitem['code']

    await downloader_game(code=gamecode)


async def downloader_game(code:str):
    
    for gameitem in games['available']:
        if gameitem['code'] == code:
            game = gameitem['name']
            type = gameitem['type']
            roos = gameitem['roost']

    for item in games['unsupported']:
        if code == item['code']:
            print(Style.RESET_ALL + "\n" + g(game) + " is currently unsupported, sorry!")
            sys.exit(0)

    print(Style.RESET_ALL + "\n\nDownload started for " + g(game) + "!\n")

    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ".\nPlease make sure there are " + b("no files in them before continuing.") + "\nThis may take a while, please wait...\n")

    if type == "norain":

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            print("\rDownloading " + b("Snow ") + "(" + b(str(num)) + "/24)...", end="")
            await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/snow/{num}.mp3")
        print("\rDownloading " + b("Snow ") + "(" + b("24") + "/24)...Done!")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            print("\rDownloading " + b("Clear ") + "(" + b(str(num)) + "/24)...", end="")
            await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/clear/{num}.mp3")
        print("\rDownloading " + b("Clear ") + "(" + b("24") + "/24)...Done!")

    elif type == "periodic":

        tracklist = ["campsite", "morning", "day", "evening", "night"]

        for track in tracklist:
            print("\rDownloading Tracks (" + b(track.capitalize()) + ")...", end="")
            await videoDL(outfile = f"./files/{track}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/{track}.mp3")
        print("\rDownloading Tracks...Done!")

    else:

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            print("\rDownloading " + b("Rain ") + "(" + b(str(num)) + "/24)...", end="")
            await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/rain/{num}.mp3")
        print("\rDownloading " + b("Rain ") + "(" + b("24") + "/24)...Done!")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            print("\rDownloading " + b("Snow ") + "(" + b(str(num)) + "/24)...", end="")
            await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/snow/{num}.mp3")
        print("\rDownloading " + b("Snow ") + "(" + b("24") + "/24)...Done!")

        for i in range (24):
            if len(str(i)) == 1:
                num = f"0{i}"
            else:
                num = i
            print("\rDownloading " + b("Clear ") + "(" + b(str(num)) + "/24)...", end="")
            await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/clear/{num}.mp3")
        print("\rDownloading " + b("Clear ") + "(" + b("24") + "/24)...Done!")

    if roos == True:
        print("\rDownloading " + b("Roost") + "...", end="")
        await videoDL(outfile = "./files/roost.mp3", url = f"https://cloud.oscie.net/acdp/{code}/roost.mp3")
        print("\rDownloading " + b("Roost") + "...Done!")

    with open("./files/name.txt", "x") as f:
        f.write(game)

    print(c("Download complete") + ", your " + b("music") + " should start quickly!\n")


async def main():
    print("\nWelcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing") + " games' music based around the " + b("weather") + " and " + b("time") + " around you.\n")

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
