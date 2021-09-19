import os, python_weather, asyncio, sys
from dotenv import load_dotenv
from datetime import datetime
from pydub import AudioSegment
from pydub.playback import play
from dl import downloaderACNH, downloaderACNL, videoDL

load_dotenv()

print("Welcome to the Animal Crossing Dynamic Player!\nThe ACDP lets you listen to Animal Crossing: New Horizons (and other games') music based on the weather and time around you.")

area = str(os.getenv("AREA"))

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
        print("\n\nTo run, we need to use dotenv to get your location. There should be a file called '.env' in the same directory as 'play.py', please add the following:\n")
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


if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
        loop.run_until_complete(getweather())
        loop.run_until_complete(gamecheck())
        loop.run_until_complete(downloaderMain())
    except KeyboardInterrupt:
        print("\n\nExiting program...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
