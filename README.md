# rsbot-discord
A discord bot that simulates drops for Oldschool Runescape beasts. Scapes data from [Old School Runescape Wikia](oldschoolrunescape.wikia.com/) originally requested by [/u/Make2Much](https://www.reddit.com/user/Make2much/). Unfortunately, drop rates had to be approximated for common/uncommon/rare drops if the droprate isn't known.

### Commands
`!help` - sends the help message with example !slay command

`!slay chicken` - simulates a chicken kill and loot

### Requirements
* [Python3](https://www.python.org/downloads/) - programming language used. When installing, make sure you check the option or manually set the "Environment Variables" (It's a checkbox on windows 10)
* discord.py - needed to interact with discord.
* beautifulsoup - for webscraping [osrs wikia](http://oldschoolrunescape.wikia.com/)

### Installation
Assuming Windows. For other Operating Systems, download/install python3+ and pip and the instructions continue the same.

* Get the newest version of [python3](https://www.python.org/downloads/). Make sure you tick the checkbox for "Environment variables"

Once python and pip are installed/configured,

* `pip install beautifulsoup4` to install beautifulsoup.

* `python3 -m pip install -U discord.py` to install discord.py

All dependencies are now met!
* You still need to create a discord app, set it as a bot user, and get its secret token. Instructions can be found [here](https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token)
* Edit osrsbot.py with a text editor and place your secret token accordingly!
* The droprates can be modified at the top of the file if you'd like to tinker with common/uncommon/etc. If the droprate is known, no tinkering is necessary.
* For bosses with multiple drops (Zulrah, etc) you can add them at the top of the file @ multipleDropMobs. Just be careful to follow the correct format.

### Running
* Open cmd.exe and navigate to the folder the project is stored in
* `python3 osrsbot.py`


**The bot is now running**

# Author
[**zenxr**](https://github.com/zenxr)
