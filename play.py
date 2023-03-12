import os, python_weather, asyncio, sys, time, aiohttp, requests
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from colorama import Fore, Style, init
from timer_py import Timer


init()
load_dotenv()


def b(text: str):
    return Fore.BLUE + text + Style.RESET_ALL
def g(text: str):
    return Fore.GREEN + text + Style.RESET_ALL
def p(text: str):
    return Fore.MAGENTA + text + Style.RESET_ALL
def o(text: str):
    return Fore.ORANGE + text + Style.RESET_ALL
def c(text: str):
    return Fore.CYAN + text + Style.RESET_ALL


timer = Timer('Timer')
timer.start()

area = str(os.getenv("AREA"))
games = requests.get(f"https://cloud.oscie.net/acdp/list.json").json()


def filecheck():
    if not os.path.exists("./files/"):
        os.mkdir("./files/")

    if not os.path.exists("./files/rain/"):
        os.mkdir("./files/rain/")

    if not os.path.exists("./files/snow/"):
        os.mkdir("./files/snow/")

    if not os.path.exists("./files/clear/"):
        os.mkdir("./files/clear/")

    if not os.path.exists(".env"):
        print("\n\nTo run, we need to use " + b("dotenv") + " to get your location. There should be a file called " + b("'.env'") + "in the same directory as " + b("'play.py'") + ", please add the following:\n")
        print(b("AREA") + "=" + b("town"))
        print("But replace " + b("town") + " with your town, for example: '" + b("AREA=Sutton, London") + "'\n")
        sys.exit(0)


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

        global sky
        sky = weather.current.description

        await client.close()


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
        if "Rain" in sky or "rain" in sky or "rainy" in sky or "Rainy" in sky or "Mist" in sky or "mist" in sky:
            gameweather = "rain"
        elif "snow" in sky or "Snow" in sky or "snowy" in sky or "Snowy" in sky:
            gameweather = "snow"
        else:
            gameweather = "clear"

        gametime = datetime.now().strftime("%H")

        print(Style.RESET_ALL + "[" + datetime.now().strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + Fore.YELLOW)

        dir = f"./files/{gameweather}/{gametime}.mp3"

        playcount = playcount + 1
        song = AudioSegment.from_mp3(dir)
        song = song - 15

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

    for item in games['unsupported']:
        if code == item['code']:
            print(Style.RESET_ALL + "\n" + g(game) + " is currently unsupported, sorry!")
            sys.exit(0)

    print(Style.RESET_ALL + "\n\nDownload started for " + g(game) + "!\n")

    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ".\nPlease make sure there are " + b("no files in them before continuing.") + "\nThis may take a while, please wait...\n")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/rain/{num}.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/snow/{num}.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/{code}/clear/{num}.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    with open("./files/name.txt", "x") as f:
        f.write(game)

    print(c("Done downloading") + "! Your " + b("music") + " should start quickly!\n")


async def main():
    print("\nWelcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing") + " games' music based around the " + b("weather") + " and " + b("time") + " around you.\n")

    await getweather()
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
