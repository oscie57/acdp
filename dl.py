import os, aiohttp

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
        os.removedirs("./files/snow")
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