from flask import Flask, render_template, abort, request, url_for, flash, redirect
import dotenv
import os
import time
import random
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import chaocipher
from chaocipher import encrypt_init, decrypt_init
from DES_algorithm import runDES
from letter_swap_decrypter import decrypt_message


app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('APP_KEY')

dotenv.load_dotenv()

spotify_key = os.environ.get('SPOTIFY_KEY')
spotify_secret = os.environ.get('SPOTIFY_SECRET')

print('keys: ',spotify_key, ', ',spotify_secret)

last_msg = ''
last_key = ''
last_shift = 0

@app.route('/home/')
def home():
    return render_template('index.html')


@app.route('/hexconverter/', methods=['GET', 'POST'])
def hexconverter():
    if request.method == 'POST':
        hex_color = request.form['hex_color']
        rgb_color = hex_to_rgb(hex_color)
        return render_template('hexconverter.html', hex_color=hex_color, rgb_color=rgb_color)
    return render_template('hexconverter.html')

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    try:
        return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError:
        return 'Not a valid hex color.'

@app.route('/album_search/', methods=['GET', 'POST'])
def album_search():
    if request.method == 'POST':
        # Search for the artist by name
        artist_name = request.form['artist_name']
        album_list = ''
        try:
            search_results = sp.search(q=artist_name, type='artist', limit=1)
        except:
            album_list = "No Artist by that name. Did you spell and capitalize(or not) correctly?"
            return render_template('album_search.html', artist_name=artist_name, album_list=album_list) 
        # Extract the artist ID from the search results
        artist_id = search_results['artists']['items'][0]['id']
        albums = []
        album_names = []
        durations = []

        album_results = sp.artist_albums(artist_id=artist_id,  limit=50)
        # print(album_results)
        for album in album_results['items']:
            add_album = True
            print(album['name'])
            print(album['id'])
            print(album['album_group'])
            print(album['album_type'])
            print('releast date precision: ',album['release_date_precision'])
            if album['album_group']!='album' or album['release_date_precision']!='day':
                add_album = False
            for artist in album['artists']:
                print(artist['name'])
                if artist['name']!=artist_name:
                    add_album = False
            print()
            if add_album:
                if album['name'] not in album_names:
                    album_names.append(album['name'])
                    albums.append([album['name'],album['id']])
        if len(albums)>0:
            for album in albums:
                print('Album Title: ',album[0])
                album_list += 'Album Title: ' + album[0] + '\n'
                tracks = sp.album_tracks(album_id=album[1])
                for idx, track in enumerate(tracks['items']):
                    duration_ms = track['duration_ms']
                    duration_s = duration_ms/1000
                    duration_min = round(duration_s/60, 2)
                    durations.append(duration_min)
                    print(idx, track['name'], ' // ', duration_min)
                    album_list += str(idx) + ': ' + track['name'] + ' // ' + str(duration_min) + '\n'
                print()
                album_list += '\n'
            avg_duration = round(sum(durations)/len(durations),2)
            print('Average Song Length: ', avg_duration)
            album_list += 'Average Song Length: ' + str(avg_duration)
        else:
            album_list = 'No albums found. Did you spell and capitalize (or not) their name correctly? (must be the same as how their name is listed on Spotify)'
        return render_template('album_search.html', artist_name=artist_name, album_list=album_list)
    return render_template('album_search.html')


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chaocipher/')
def chaocipher():
    return render_template('chaocipher.html')

@app.route('/encrypt/', methods=['GET', 'POST'])
def encrypt():
    if request.method == 'POST':
        message = request.form['message']
        keyword = request.form['keyword']
        shift = request.form['shift']
        print('trying to encrypt')
        encrypted_package = encrypt_init(message, keyword, shift)
        return render_template('encrypt.html', encrypted_message=encrypted_package[0], keyword=keyword, shift=shift)
    return render_template('encrypt.html')

@app.route('/decrypt/', methods=['GET', 'POST'])
def decrypt():
    if request.method == 'POST':
        message = request.form['message']
        keyword = request.form['keyword']
        shift = request.form['shift']
        decrypted_package = decrypt_init(message, keyword, shift)
        return render_template('decrypt.html', decrypted_message=decrypted_package[0], keyword=keyword, shift=shift)
    return render_template('decrypt.html')


@app.route('/DESpage/')
def DESpage():
    return render_template('DES.html')

@app.route('/decryptDES/', methods=['GET', 'POST'])
def decryptDES():
    global last_msg, last_key
    if request.method == 'POST':
        response = 'decrypting with DES'
        message = request.form['message']
        key = request.form['key']
        ascii = request.form['ascii']
        decrypt=True
        print('ascii: ',ascii)
        encrypted_package = []
        back2ascii = False
        if ascii == 'yes':
            back2ascii = True
        print('back2ascii = ',back2ascii)
        if not is_hexadecimal(key):
            response = 'Key is not hexadecimal. Try again.'
            print(response)
        elif len(str(key))!=16:
            response = "Key isn't 16 digits. Replacing with a random key."
            decrypted_package = runDES(message, None, decrypt, ascii)
        else:
            print(response)
            decrypted_package = runDES(message, key, decrypt, ascii)
        # last_msg = encrypted_package[0]
        # last_key = encrypted_package[1]
        return render_template('decryptDES.html', response=response, decrypted_message=decrypted_package[0], key=decrypted_package[1])
    print('last message: ',last_msg, 'last key: ',last_key)
    return render_template('decryptDES.html', prev_encrypted_message=last_msg, prev_key=last_key)

@app.route('/encryptDES/', methods=['GET', 'POST'])
def encryptDES():
    global last_msg, last_key
    if request.method == 'POST':
        response = 'encrypting with DES'
        message = request.form['message']
        key = request.form['key']
        encrypted_package = []
        if not is_hexadecimal(key):
            response = 'Key is not hexadecimal. Try again.'
            print(response)
        elif len(str(key))!=16:
            response = "Key isn't 16 digits. Replacing with a random key."
            encrypted_package = runDES(message)
        else:
            print(response)
            encrypted_package = runDES(message, key)
        last_msg = encrypted_package[0]
        last_key = encrypted_package[1]
        return render_template('encryptDES.html', response=response, encrypted_message=encrypted_package[0], key=encrypted_package[1])
    return render_template('encryptDES.html')

def is_hexadecimal(value):
    return all(c.isdigit() or c.lower() in 'abcdef' for c in value)

@app.route('/cryptogram_solver/', methods=['GET', 'POST'])
def cryptogram_solver():
    default_cryptogram = 'aeuc dg bhlui gh ukgdcq, whn bkc ihlugdlui euvt whnziuvo lhzu fw euvtdcq whnziuvo vuii.'
    if request.method == 'POST':
        response = 'decrypting message'
        message = request.form['cryptogram_text']
        default_cryptogram = message
        encrypted_package = decrypt_message(message)
        return render_template('cryptogram_solver.html', default_cryptogram=default_cryptogram, decrypted_text=encrypted_package[0], elapsed=encrypted_package[1])
    return render_template('cryptogram_solver.html', default_cryptogram=default_cryptogram)

client_credentials_manager = SpotifyClientCredentials(spotify_key, spotify_secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

if __name__=='__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT',8080)))
