import os, python_weather, asyncio, sys, time, aiohttp
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from colorama import init, Fore, Back, Style

def reminder():
    for i in range(500000):
        print("Remember to add colours to ACNH Downloader")
        time.sleep(5)
    sys.exit(0)

init()

#reminder() # comment this line out to stop

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

print("Welcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing: New Horizons") + " (and other games') music based around the " + b("weather") +  " and " + b("time") + " around you.")

area = str(os.getenv("AREA"))
games = [
    "New Leaf",
    "New Horizons",
    "City Folk"
]

def filecheck():
    if not os.path.exists("./files"):
        os.makedirs("./files")

    if not os.path.exists("./files/rain"):
        os.makedirs("./files/rain")

    if not os.path.exists("./files/clear"):
        os.makedirs("./files/clear")

    if not os.path.exists("./files/snow"):
        os.makedirs("./files/snow")

    if not os.path.exists(".env"):
        print("\n\nTo run, we need to use " + b("dotenv") + " to get your location. There should be a file called " + b("'.env'") + "in the same directory as " + b("'play.py'") + ", please add the following:\n")
        print(b("AREA") + "=" + b("town"))
        print("But replace " + b("town") + " with your town, for example: '" + b("AREA=Sutton, London") + "'\n")
        sys.exit(0)
    
async def getweather():
    client = python_weather.Client(format=python_weather.IMPERIAL)
    weather = await client.find(area)

    global sky
    sky = weather.current.sky_text

    await client.close()


async def gamecheck():
    global playcount
    playcount = 0
    filecheck()
    if not os.path.exists("./files/clear/12.mp3"):
        await downloaderMain()
    while True:
        global gameweather
        global gametime

        await getweather()

        if sky == "Light Rain" or sky == "Rain" or sky == "Rain Showers":
            gameweather = "rain"
        elif sky == "Light Snow" or sky == "Snow" or sky == "Snow Showers":
            gameweather = "snow"
        else:
            gameweather = "clear"

        gametime = datetime.now().strftime("%H")

        print(Style.RESET_ALL + "\n[" + datetime.now().strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + Fore.YELLOW)
        dir = f"./files/{gameweather}/{gametime}.mp3"

        playcount = playcount + 1
        song = AudioSegment.from_mp3(dir)
        song = song - 15
        play(song)

        
async def downloaderMain():

    gameslist = []

    for content in games:
        gameslist.append(content.splitlines()[0])

    Style.RESET_ALL

    print("\nWelcome to the " + p("ACDP") + " (" + p("Animal Crossing Dynamic Player") + ") music downloader!\nIf you're seeing this, " + c("chances are, you do not have the Audio files downloaded.") + "\n" + c("Space Requirements:") + "\n - " + g("New Leaf") + " requires " + b("~120MB") + "\n - " + g("New Horizons") + " requires " + b("~180MB\n") + " - " + g("City Folk") + " requires " + b("~130MB\n"))
    game = input("Please " + b("choose a game") + " to download the OST: " + Fore.GREEN)
    if game not in gameslist:
        print(Style.RESET_ALL + "'" + b(game) + "' is not a valid option. Valid options include:\n" + g(str(gameslist)) + "\n")
        await downloaderMain()
    if game == "New Horizons":
        await downloaderACNH()
    elif game == "New Leaf":
        await downloaderACNL()
    elif game == "City Folk":
        await downloaderACCF()

async def videoDL(outfile, url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                with open(outfile, "wb") as f:
                    async for data in response.content.iter_chunked(1024):
                        f.write(data)
    except Exception as e:
        print(f"**`ERROR:`** {type(e).__name__} - {e}")

async def downloaderACNL():
    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ". Please make sure there are " + b("no files in them before continuing."))

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnl/rain/{num}.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnl/snow/{num}.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnl/clear/{num}.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    print(c("Done downloading") + "! Your " + b("music") + " should start quickly!\n")

async def downloaderACNH():
    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ". Please make sure there are " + b("no files in them before continuing."))

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnh/rain/{num}.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnh/snow/{num}.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/acnh/clear/{num}.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    print(c("Done downloading") + "! Your " + b("music") + " should start quickly!\n\n")

async def downloaderACCF():
    Style.RESET_ALL

    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ". Please make sure there are " + b("no files in them before continuing."))

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/rain/{num}.mp3", url = f"https://cloud.oscie.net/acdp/accf/rain/{num}.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/snow/{num}.mp3", url = f"https://cloud.oscie.net/acdp/accf/snow/{num}.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")

    for i in range (24):
        if len(str(i)) == 1:
            num = f"0{i}"
        else:
            num = i
        await videoDL(outfile = f"./files/clear/{num}.mp3", url = f"https://cloud.oscie.net/acdp/accf/clear/{num}.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")

    print(c("Done downloading") + "! Your " + b("music") + " should start quickly!\n\n")


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather())
        loop.run_until_complete(gamecheck())
        loop.run_until_complete(downloaderMain())
        loop.run_until_complete(downloaderACNH())
        loop.run_until_complete(downloaderACNL())
        loop.run_until_complete(downloaderACCF())
    except KeyboardInterrupt:
        print(c("\n\nExiting program..."))
        print("While using this app, you listened to the music " + b(str(playcount)) + " times!")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
