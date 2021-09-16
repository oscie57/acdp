import os, python_weather, asyncio, aiohttp, sys
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play

load_dotenv()

print("Welcome to the Animal Crossing Dynamic Player!\nThe ACDP lets you listen to Animal Crossing: New Horizons (and other games') music based on the weather and time around you.")

area = str(os.getenv("AREA"))

def filecheck():
    if not os.path.exists("./files"):
        print("You are missing important folders!")
        print("Adding folders now...\n")
        os.makedirs("./files")

    if not os.path.exists("./files/rain"):
        os.makedirs("./files/rain")

    if not os.path.exists("./files/clear"):
        os.makedirs("./files/clear")

    if not os.path.exists("./files/snow"):
        os.makedirs("./files/snow")

    if not os.path.exists(".env"):
        print("To run, we need to use dotenv to get your location. There should be a file called '.env' in the same directory as 'play.py', please add the following:\n")
        print('"AREA=[town]"')
        print("But replace [town] with your town, for example: 'AREA=Sutton, London'\n")
        return

    if not os.path.exists("games.txt"):
        print("We need 'games.txt' to run! This allows you to download the OST's for this application. Please redownload it from GitHub.")
        return
    
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

        print(f"\n[{datetime.now().strftime('%H:%M - %d/%m')}] {sky}")
        dir = f"./files/{gameweather}/{gametime}.mp3"

        song = AudioSegment.from_mp3(dir)
        play(song)

        

async def downloaderMain():
    with open("./games.txt", "r") as f:
        gamesfile = f.readlines()

    gameslist = []

    for content in gamesfile:
        gameslist.append(content.splitlines()[0])


    print("\n\nWelcome to the ACDP (Animal Crossing Dynamic Player) music downloader!\nIf you're seeing this, chances are, you do not have the Audio files downloaded.\n\nSpace Requirements:\n - New Leaf requires ~1.8GB\n - New Horizons requires ~400MB\n")
    game = input("Please choose a game to download the OST: ")
    if game not in gameslist:
        print(f"That is not a valid option. Valid options include:\n{gameslist}\n")
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
    if os.path.exists("./files/rain/"):
        print("If there are audio files in the 'files/[weather]' folders, this may not work. Please make sure there are no files in them before continuing.")

    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_{i}AM.mp3")
        print(f"Downloading Rain ({i}AM)...")
        os.rename(f"./files/rain/{i}a.mp3", f"./files/rain/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_{i}PM.mp3")
        print(f"Downloading Rain ({i + 12}PM)...")
        os.rename(f"./files/rain/{i + 12}p.mp3", f"./files/rain/{i + 12}.mp3")

    downloaderRen(weather = "rain")

    await videoDL(outfile = f"./files/rain/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewLeaf_12PM.mp3")


    if os.path.exists("./files/clear"):
        os.removedirs("./files/clear")
        os.makedirs("./files/clear")

    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_{i}AM.mp3")
        os.rename(f"./files/clear/{i}a.mp3", f"./files/clear/{i}.mp3")
        print(f"Downloading Clear ({i}AM)...")
    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_{i}PM.mp3")
        print(f"Downloading Clear ({i + 12}PM)...")
        os.rename(f"./files/clear/{i + 12}p.mp3", f"./files/clear/{i + 12}.mp3")


    downloaderRen(weather = "clear")

    await videoDL(outfile = f"./files/clear/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewLeaf_12PM.mp3")


    if os.path.exists("./files/snow"):
        os.removedirs("./files/snow")
        os.makedirs("./files/snow")

    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_{i}AM.mp3")
        print(f"Downloading Snow ({i}AM)...")
        os.rename(f"./files/snow/{i}a.mp3", f"./files/snow/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_{i}PM.mp3")
        print(f"Downloading Snow ({i + 12}PM)...")
        os.rename(f"./files/snow/{i + 12}p.mp3", f"./files/snow/{i + 12}.mp3")

    downloaderRen(weather = "snow")
    
    await videoDL(outfile = f"./files/snow/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewLeaf_12PM.mp3")

async def downloaderACNH():
    if os.path.exists("./files/rain/"):
        print("If there are audio files in the 'files/[weather]' folders, this may not work. Please make sure there are no files in them before continuing.")

    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_{i}AM.mp3")
        print(f"Downloading Rain ({i}AM)...")
        os.rename(f"./files/rain/{i}a.mp3", f"./files/rain/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/rain/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_{i}PM.mp3")
        print(f"Downloading Rain ({i + 12}PM)...")
        os.rename(f"./files/rain/{i + 12}p.mp3", f"./files/rain/{i + 12}.mp3")

    downloaderRen(weather = "rain")

    await videoDL(outfile = f"./files/rain/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FRainNewHorizons_12PM.mp3")


    if os.path.exists("./files/clear"):
        os.removedirs("./files/clear")
        os.makedirs("./files/clear")

    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_{i}AM.mp3")
        print(f"Downloading Clear ({i}AM)...")
        os.rename(f"./files/clear/{i}a.mp3", f"./files/clear/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/clear/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_{i}PM.mp3")
        print(f"Downloading Clear ({i + 12}PM)...")
        os.rename(f"./files/clear/{i + 12}p.mp3", f"./files/clear/{i + 12}.mp3")

    downloaderRen(weather = "clear")

    await videoDL(outfile = f"./files/clear/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FNormalNewHorizons_12PM.mp3")


    if os.path.exists("./files/snow"):
        os.remove("./files/snow")
        os.makedirs("./files/snow")

    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i}a.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_{i}AM.mp3")
        print(f"Downloading Snow ({i}AM)...")
        os.rename(f"./files/snow/{i}a.mp3", f"./files/snow/{i}.mp3")
    for i in range(13):
        await videoDL(outfile = f"./files/snow/{i + 12}p.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_{i}PM.mp3")
        print(f"Downloading Snow ({i + 12}PM)...")
        os.rename(f"./files/snow/{i + 12}p.mp3", f"./files/snow/{i + 12}.mp3")

    downloaderRen(weather = "snow")
    
    await videoDL(outfile = f"./files/snow/12.mp3", url = f"https://cdn.glitch.com/a032b7da-b36c-4292-9322-7d4c98be233b%2FSnowNewHorizons_12PM.mp3")

    print("Done downloading! Your music should start quickly!\n\n")

def downloaderRen(weather):
    os.remove(f"./files/{weather}/0.mp3")
    os.remove(f"./files/{weather}/12.mp3")
    os.rename(f"./files/{weather}/24.mp3", f"./files/{weather}/00.mp3")
    print(f"Changing filenames ({weather})..")

    os.rename(f"./files/{weather}/1.mp3", f"./files/{weather}/01.mp3")
    os.rename(f"./files/{weather}/2.mp3", f"./files/{weather}/02.mp3")
    os.rename(f"./files/{weather}/3.mp3", f"./files/{weather}/03.mp3")
    os.rename(f"./files/{weather}/4.mp3", f"./files/{weather}/04.mp3")
    os.rename(f"./files/{weather}/5.mp3", f"./files/{weather}/05.mp3")
    os.rename(f"./files/{weather}/6.mp3", f"./files/{weather}/06.mp3")
    os.rename(f"./files/{weather}/7.mp3", f"./files/{weather}/07.mp3")
    os.rename(f"./files/{weather}/8.mp3", f"./files/{weather}/08.mp3")
    os.rename(f"./files/{weather}/9.mp3", f"./files/{weather}/09.mp3")

def resetOST():
    print("Resetting Files...")
    os.remove("./files")
    return

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(getweather())
    loop.run_until_complete(gamecheck())
    loop.run_until_complete(videoDL())
    loop.run_until_complete(downloaderMain())
    loop.run_until_complete(downloaderACNH())
    loop.run_until_complete(downloaderACNL())
