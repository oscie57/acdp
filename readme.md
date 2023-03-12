# Animal Crossing Dynamic Player (ACDP)

Hey there! This is a project I've been working on called ACDP, a Python program that plays Animal Crossing music according to you.

## How it works

I am sure you are wondering, how does this work??
Well, it uses a few Python packages, mainly python-weather, to determine what to play.
If it is raining where you are, the music will have rain, same with snow or sun. It also checks the time. If it is 1am, it'll play the 1am music, and same for any other time.
You can only have one OST downloaded at a time to save space.

Here is a video demonstrating how to use: [YouTube [OUTDATED]](https://youtu.be/uTfuLiuBtt8)

## Space Requirements

Space requirements have been made dynamic, meaning they can only be viewed in the program.

You can also view the game list in [list.json](https://github.com/oscie57/acdp/blob/main/list.json)

## Set-up

1. Make sure you have Python installed! (This was tested on Python 3.10)
2. Run `pip install -r requirements.txt` to install the required packages.
3. Create a file called `.env`
4. Inside that file, add `AREA=` and put your area afterwards.
For example: `AREA=Madrid, Spain`
5. Make sure you have `.env` and `play.py` in the **same folder!**
6. Run `python3 play.py` (or `py play.py` on Windows) and it should run!

That's it, you're all ready to go!

## File list

Upon downloading, feel free to delete the `README.md`, `list.json`, and `.gitignore` files.

You only need `.env` and `play.py` to use (you will need `requirements.txt` to set up, but you can remove it later).

## Bugs

If you have any bugs, please report them at the [issues page](https://github.com/oscie57/ACDP/issues)!

## Why use this / Use-Cases

Apparently I have to clarify this. This can be used to play music in the background while studying, sleeping, working, or doing anything really, that was the main intention.
