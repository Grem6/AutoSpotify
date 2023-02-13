from colorama import Back, Fore, Style
from song_scrapper import song_scrapper
from data_dump import file_dump
from authenticator import authen_create
import time
from spotipy_main import auto_spotify
import os.path
from rich.console import Console
from rich.markdown import Markdown
console = Console()


url = 'https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF'

print(Fore.GREEN)


print(
    """     
 _______  __   __  _______  _______    _______  _______  _______  _______  ___   _______  __   __ 
|   _   ||  | |  ||       ||       |  |       ||       ||       ||       ||   | |       ||  | |  |
|  |_|  ||  | |  ||_     _||   _   |  |  _____||    _  ||   _   ||_     _||   | |    ___||  |_|  |
|       ||  |_|  |  |   |  |  | |  |  | |_____ |   |_| ||  | |  |  |   |  |   | |   |___ |       |
|       ||       |  |   |  |  |_|  |  |_____  ||    ___||  |_|  |  |   |  |   | |    ___||_     _|
|   _   ||       |  |   |  |       |   _____| ||   |    |       |  |   |  |   | |   |      |   |  
|__| |__||_______|  |___|  |_______|  |_______||___|    |_______|  |___|  |___| |___|      |___|    
  
""")

print(Style.RESET_ALL)


MARKDOWN = """
**Automated top song finder for spotify**

*refer read-me for more info*

- Version: 1.0
- Gecko-version: 0.32.2
- Browser-client: firefox⭐
- Developer: **Grem**
- Github    | Grem6
- Instagram | @grem.san

"""


md = Markdown(MARKDOWN)
console.print(md)
auth_config = os.path.exists('auth.conf')
if not auth_config:
    authen_create()
song_scrapper(url)
time.sleep(5)
file_dump()
time.sleep(5)
auto_spotify()
input("Press enter to exit;")
