# Animal Crossing Dynamic Player (ACDP)
Hey there! This is a project I've been working on called ACDP, a Python program that plays Animal Crossing music according to you.
## How it works
I am sure you are wondering, how does this work??
Well, it uses a few Python packages, mainly python-weather, to determine what to play.
If it is raining where you are, the music will have rain, same with snow or sun. It also checks the time. If it is 1am, it'll play the 1am music, and same for any other time.
You can only have one OST downloaded at a time to save space.

Here is a video demonstrating how to use: https://youtu.be/uTfuLiuBtt8
## Space Requirements
| Game         | Space  | Notes   |
| ------------ | ------ | ------- |
| New Leaf     | ~120MB | None    |
| New Horizons | ~180MB | None    |
| City Folk    | ~130MB | This includes `Animal Crossing: Wild World` for DS and `Animal Crossing: Let's go to the City` for Wii |
## Set-up
1. Make sure you have Python installed! (This was tested on Python 3.8)
2. Run `pip install -r requirements.txt` to install the required packages.
3. Create a file called `.env`
4. Inside that file, add `AREA=` and put your area afterwards.
For example: `AREA=Madrid, Spain`
5. Make sure you have `games.txt`, `.env` and `play.py` in the **same folder!**

That's it, you're all ready to go!
## Bugs!
If you have any bugs, please report them at the [issues page](https://github.com/scor57/ACDP/issues)!
## Why use this / Use-Cases
Apparently I have to clarify this. This can be used to play music in the background while studying, working, or doing anything really, that was the main intention.
