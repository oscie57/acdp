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

def b(text):
    return Fore.BLUE + text + Style.RESET_ALL
def g(text):
    return Fore.GREEN + text + Style.RESET_ALL
def p(text):
    return Fore.MAGENTA + text + Style.RESET_ALL
def o(text):
    return Fore.ORANGE + text + Style.RESET_ALL
def c(text):
    return Fore.CYAN + text + Style.RESET_ALL

print("Welcome to the " + p("Animal Crossing Dynamic Player") + "!\nThe " + p("ACDP") + " lets you listen to " + g("Animal Crossing: New Horizons") + " (and other games') music based around the " + b("weather") +  " and " + b("time") + " around you.")

area = str(os.getenv("AREA"))
games = [
    "New Leaf",
    "New Horizons"
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

        print(f"\n\n[" + datetime.now().strftime(c('%H:%M - %d/%m')) + "] " + b(sky) + Fore.YELLOW)
        dir = f"./files/{gameweather}/{gametime}.mp3"

        song = AudioSegment.from_mp3(dir)
        play(song)

        
async def downloaderMain():

    gameslist = []

    for content in games:
        gameslist.append(content.splitlines()[0])

    Style.RESET_ALL

    print("\nWelcome to the " + p("ACDP") + " (" + p("Animal Crossing Dynamic Player") + ") music downloader!\nIf you're seeing this, " + c("chances are, you do not have the Audio files downloaded.") + "\n" + c("Space Requirements:") + "\n - " + g("New Leaf") + " requires " + b("~1.8GB") + "\n - " + g("New Horizons") + " requires " + b("~400MB\n"))
    game = input("Please " + b("choose a game") + " to download the OST: " + Fore.GREEN)
    if game not in gameslist:
        print(Style.RESET_ALL + "'" + b(game) + "' is not a valid option. Valid options include:\n" + g(str(gameslist)) + "\n")
        await downloaderMain()
    if game == "New Horizons":
        await downloaderACNH()
    elif game == "New Leaf":
        await downloaderACNL()

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

    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_{i}AM.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/rain/{i}a.mp3", f"./files/rain/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_{i}PM.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/rain/{i + 12}p.mp3", f"./files/rain/{i + 12}.mp3")

    downloaderRen(weather = "rain")

    await videoDL(outfile = f"./files/rain/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_12PM.mp3")


    if os.path.exists("./files/clear"):
        os.removedirs("./files/clear")
        os.makedirs("./files/clear")

    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_{i}AM.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/clear/{i}a.mp3", f"./files/clear/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_{i}PM.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/clear/{i + 12}p.mp3", f"./files/clear/{i + 12}.mp3")


    downloaderRen(weather = "clear")

    await videoDL(outfile = f"./files/clear/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_12PM.mp3")


    if os.path.exists("./files/snow"):
        os.removedirs("./files/snow")
        os.makedirs("./files/snow")

    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_{i}AM.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/snow/{i}a.mp3", f"./files/snow/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_{i}PM.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/snow/{i + 12}p.mp3", f"./files/snow/{i + 12}.mp3")

    downloaderRen(weather = "snow")
    
    await videoDL(outfile = f"./files/snow/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_12PM.mp3")

    print(c("Done downloading!") + " Your " + b("music") + " should start quickly!\n\n")

async def downloaderACNH():
    Style.RESET_ALL
    if os.path.exists("./files/rain/"):
        print(Style.RESET_ALL + "If there are " + b("audio files") + " in the 'files/[weather]' folders, " + c("this may not work") + ". Please make sure there are " + b("no files in them before continuing."))

    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_{i}AM.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/rain/{i}a.mp3", f"./files/rain/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_{i}PM.mp3")
        print("Downloading " + b("Rain ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/rain/{i + 12}p.mp3", f"./files/rain/{i + 12}.mp3")

    downloaderRen(weather = "rain")

    await videoDL(outfile = f"./files/rain/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_12PM.mp3")


    if os.path.exists("./files/clear"):
        os.removedirs("./files/clear")
        os.makedirs("./files/clear")

    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_{i}AM.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/clear/{i}a.mp3", f"./files/clear/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_{i}PM.mp3")
        print("Downloading " + b("Clear ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/clear/{i + 12}p.mp3", f"./files/clear/{i + 12}.mp3")

    downloaderRen(weather = "clear")

    await videoDL(outfile = f"./files/clear/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_12PM.mp3")


    if os.path.exists("./files/snow"):
        os.removedirs("./files/snow")
        os.makedirs("./files/snow")

    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_{i}AM.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i)) + ")...")
        os.rename(f"./files/snow/{i}a.mp3", f"./files/snow/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_{i}PM.mp3")
        print("Downloading " + b("Snow ") + "(" + b(str(i + 12)) + ")...")
        os.rename(f"./files/snow/{i + 12}p.mp3", f"./files/snow/{i + 12}.mp3")

    downloaderRen(weather = "snow")
    
    await videoDL(outfile = f"./files/snow/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_12PM.mp3")

    print(c("Done downloading!") + " Your " + b("music") + " should start quickly!\n\n")

def downloaderRen(weather):
    os.remove(f"./files/{weather}/0.mp3")
    os.remove(f"./files/{weather}/12.mp3")
    os.rename(f"./files/{weather}/24.mp3", f"./files/{weather}/00.mp3")
    print("Changing filenames (" + b(weather) + ")...")

    os.rename(f"./files/{weather}/1.mp3", f"./files/{weather}/01.mp3")
    os.rename(f"./files/{weather}/2.mp3", f"./files/{weather}/02.mp3")
    os.rename(f"./files/{weather}/3.mp3", f"./files/{weather}/03.mp3")
    os.rename(f"./files/{weather}/4.mp3", f"./files/{weather}/04.mp3")
    os.rename(f"./files/{weather}/5.mp3", f"./files/{weather}/05.mp3")
    os.rename(f"./files/{weather}/6.mp3", f"./files/{weather}/06.mp3")
    os.rename(f"./files/{weather}/7.mp3", f"./files/{weather}/07.mp3")
    os.rename(f"./files/{weather}/8.mp3", f"./files/{weather}/08.mp3")
    os.rename(f"./files/{weather}/9.mp3", f"./files/{weather}/09.mp3")


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather())
        loop.run_until_complete(gamecheck())
        loop.run_until_complete(downloaderMain())
        loop.run_until_complete(downloaderACNH())
        loop.run_until_complete(downloaderACNL())
    except KeyboardInterrupt:
        print(c("\n\nExiting program..."))
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
