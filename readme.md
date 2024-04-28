# Animal Crossing Dynamic Player (ACDP)

Hey there! This is a project I've been working on called ACDP, a Python program that plays Animal Crossing music according to you.

## How it works

I am sure you are wondering, how does this work??
Well, it uses a few Python packages, mainly python-weather, to determine what to play.
If it is raining where you are, the music will have rain, same with snow or sun. It also checks the time. If it is 1am, it'll play the 1am music, and same for any other time.
You can only have one OST downloaded at a time to save space.

Here is a video demonstrating how to use: [YouTube [OUTDATED]](https://youtu.be/uTfuLiuBtt8)

## Which version should I use?

ACDP currently has three available versions:

- a download version (`play.py`)
- a streamed version (`network.py`)
- an iOS version (via Shortcuts)

The download version downloads the music to your computer for fast and easy listening, however, it could take a while. You only need to download once. As long as the downloads are available (you can check any time at [oscie cloud](https://cloud.oscie.net)), there should be no issues.

The streamed version streams the music directly. This is a new feature, and may not work 100% of the time. If anything happens, please let me know in my [Discord server](https://discord.gg/ymb84qM54A) in #acdp, or create an issue on [GitHub](https://github.com/oscie57/acdp/issues).

The iOS version streams the music directly and is accessed via the Shortcuts app. This is brand new and is barely tested, so it is not public. If you'd like to use it, please join my [Discord server](https://discord.gg/ymb84qM54A) and ask in #acdp. It currently only supports games of `normal` type (New Leaf, New Horizons, City Folk), and likely will only ever.

Both the download and streamed versions require the configuration file to be filled out properly, so make sure to read below.

## Space Requirements

Space requirements for the download version have been made dynamic, meaning they can only be viewed in the program.

You can also view the game list in [list.json](https://github.com/oscie57/acdp/blob/main/list.json)

## Set-up

1. Make sure you have Python installed! (This was tested on Python 3.10)
2. Run `pip install -r requirements.txt` to install the required packages.
3. Create a file called `.env` and fill the information below
4. Make sure you have `.env` and `play.py`/`network.py` in the **same folder!**
5. Run `python3 play.py`/`python3 network.py` (or `py play.py`/`py network.py` on Windows) and it should run!

That's it, you're all ready to go!

## Configuration

The `.env` file is how the program gets the correct configuration.

An example:

```env
VOLUME=15
AREA=Sutton, London
ROOST=True
```

### VOLUME

The `VOLUME` setting allows you to set the volume that the application plays at, but backwards.

The volume will be `100 - VOLUME`, so for example, having `VOLUME=15` would mean the volume is 85%.

### AREA

The area is used to figure out the weather in your location. For example, you could have `AREA=Madrid, Spain`.

### ROOST

Currently, some games that support The Roost in-game will have a random chance of playing their song (1-in-1000). As long as the game is supported (check `list.json`) and `ROOST` is set to True in `.env`, it might play.

## File list

Upon downloading, feel free to delete the `README.md`, `list.json`, and `.gitignore` files.

You only need `.env` and `play.py` to use (you will need `requirements.txt` to set up, but you can remove it later).

## Bugs

If you have any bugs, please report them at the [issues page](https://github.com/oscie57/ACDP/issues) or in `#acdp` at my [Discord server](https://discord.gg/ymb84qM54A)!

## Why use this / Use-Cases

Apparently I have to clarify this. This can be used to play music in the background while studying, sleeping, working, or doing anything really, that was the main intention.
