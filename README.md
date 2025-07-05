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