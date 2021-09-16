# Animal Crossing Dynamic Player (ACDP)
Hey there! This is a project I've been working on called ACDP, a Python program that plays Animal Crossing music according to you.
## How it works
I am sure you are wondering, how does this work??
Well, it uses a few Python packages, mainly python-weather, to determine what to play.
If it is raining where you are, the music will have rain, same with snow or sun. It also checks the time. If it is 1am, it'll play the 1am music, and same for any other time.

Here is a video demonstrating how to use: https://youtu.be/uTfuLiuBtt8
## Space Requirements
| Game         | Space  | Reason? |
| ------------ | ------ | ------- |
| New Leaf     | ~1.8GB | Currently where I get the music from, New Leaf's Clear audio tracks are 30 minutes. It is annoying since it means weather wont be able to change as often for it. |
| New Horizons | ~500MB | No |
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