# Samsara Arcade Arc Bot
## I. Features:
- Showcasing a specific character kit.
- Generate a team.
- Generate 2 teams with no overlaps.
- Generate multiple teams. Now with options about whether or not you want the team to overlap.
- Automatically print them in showdown format, making it easy to copy and paste into PokemonShowdown
- Play piano (maybe not).
- Punch Teledji Adeledji (implementing).
- And more to be added (when needed).
## II. Installation:
1. Download python (>= 3.13.1) (remember to check to add Python to PATH).
2. Install pip
3. Use the following command to get the requirements.
```shell
pip install -r requirements.txt
```
4. Add a ".env" file, containing a single line:
```
TOKEN=[Add your bot token here]
```
5. Run `main.py`
## III. Bug reports:
Please report the bugs to @adorable_puddle on Discord. Attached with the log files in the logs folder (not logs/old).
## IV. Known Issues:
1. KeyError: 'TOKEN'

For some reason, I have no idea why Python decided not to read environment variables sometimes.
During installation of Python, ensure that Python is added to PATH. Afterward, restart the computer.
If it doesn't work, a possible hotfix would be to open the source code and replace
```py
client.run(os.environ["TOKEN"], log_handler=log_handler)
```
with 
```py
client.run("Insert your bot token here", log_handler=log_handler)
```

2. Gender is not displayed in PokePaste format

It turns out that the pokemon-formats library I have been using (its `Showdown.jsonToShowdown()` function), just ignore gender while making the paste. Fun.

I have decided to clone the entire function itself into the script and fix it myself.

3. Tera doesn't exist

So, it turns out that pokemon-formats library is made before Tera was a thing and so it just doesn't record tera. There is no permanent fix for this unless you are willing to enter the source code of the library itself and fix it there.

4. Nature's Madness

Once again, this is a problem with the pokemon-formats library itself.

The check condition in the library is checked with a line of if-elif, by checking if a line contains the keyword, the library can figure out what data it is inputing. However, this create a minor issue where if the move contains any of the keyword, because the move check is the last of the list, any of the previous check would catch it first, hence deleting the move.

This is fixed by, once again, jumping directly into the source code.

At this point I might as well considered forking it myself if I found the library's github.

For the time being, the previous 2 bugs are **unfixable**. I will come up with a fix at some point in the future.