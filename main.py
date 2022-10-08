import requests
from bs4 import BeautifulSoup

SPOTIPY_CLIENT_SECRET = "Your Spotipy Client Secret"
SPOTIPY_CLIENT_ID = "Spotipy Client ID"
SPOTIPY_REDIRECT_URI = 'http://127.0.0.1:5500/'

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
year = date.split("-")[0]

# Gets response from billboard.com and saves it into a variable.
response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
top100 = response.text

# Inputs top100 into BeautifulSoup to parse through and collects all title tags.
soup = BeautifulSoup(top100, 'html.parser')
songs = soup.find_all(class_="c-title a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 lrv-u-font-size-18@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-330 u-max-width-230@tablet-only")

# Gets the top song on the billboard 100.
top_song = soup.select_one(selector="h3", class_="c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet")

top_100 = []

# Beyonnce is the artist with holding the top song at the time. Adds her to the top_100 list.
beyonce = top_song.getText()
beyonce_stripped = beyonce.strip("\t\n")
top_100.append(beyonce_stripped)

# Reformat the song_names by stripping dividers.
for song in songs:
    song_name = song.getText().strip("\t\n")
    top_100.append(song_name)


# Inputs top const variables and returns profile information.
def authorization_flow(scope=""):
    import spotipy
    from spotipy.oauth2 import SpotifyOAuth

    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                                               client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="playlist-modify-private"))
    return sp


# Creates sp and get our use id.
sp = authorization_flow(scope="playlist-modify-private")
user = sp.current_user()
user_id = user["id"]

playlist_name = f"Hot 100: {date}"

# Creates playlist
response = sp.user_playlist_create(
    user=user_id,
    name=playlist_name,
    public=False,
    collaborative=False,
    description="Hot 100 from billboard.com"
)

playlist_id = response["id"]

song_uris = []

# Adds songs to the playlist.
for song in top_100:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        song_uris.append(result['tracks']['items'][0]['uri'])
    except IndexError:
        print(f"{song} doesn't exist on spotify. Skipped")

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)
