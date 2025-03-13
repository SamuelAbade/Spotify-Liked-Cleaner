import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id="client_id",
    client_secret="secret_client",
    redirect_uri="redirect_uri",
    scope="user-library-read user-library-modify playlist-read-private"
))

# Devuelve todo el Liked Songs
def get_liked_songs():
    liked_songs = {}
    results = sp.current_user_saved_tracks(limit=50)
    while results:
        for item in results['items']:
            track = item['track']
            liked_songs[track['id']] = {
                "name": track['name'],
                "album_id": track['album']['id'],
                "album_name": track['album']['name']
            }
        results = sp.next(results) if results['next'] else None
    return liked_songs

# Devuelve todas las canciones de todas las playlists
def get_all_playlist_songs():
    playlist_songs = set()
    results = sp.current_user_playlists(limit=50)
    while results:
        for playlist in results['items']:
            playlist_id = playlist['id']
            tracks = sp.playlist_tracks(playlist_id)
            while tracks:
                for item in tracks['items']:
                    track = item['track']
                    if track:
                        playlist_songs.add(track['id'])
                tracks = sp.next(tracks) if tracks['next'] else None
        results = sp.next(results) if results['next'] else None
    return playlist_songs

# Devuelve los álbumes guardados
def get_saved_albums():
    saved_albums = set()
    results = sp.current_user_saved_albums(limit=50)
    while results:
        for item in results['items']:
            album = item['album']
            saved_albums.add(album['id'])
        results = sp.next(results) if results['next'] else None
    return saved_albums

# Divide la lista en bloques (Para no saltar limite del api de spotify que es de 50 args)
def chunks(lst, n):
    """Divide la lista 'lst' en sublistas de tamaño 'n'."""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]

# Elimina de Liked Songs si están en playlist
def remove_songs_from_liked_by_playlist(liked_songs, playlist_songs):
    to_remove = [track_id for track_id in liked_songs if track_id in playlist_songs]
    removed_songs = []
    if to_remove:
        for batch in chunks(to_remove, 50):
            sp.current_user_saved_tracks_delete(batch)
            removed_songs.extend([liked_songs[track_id]["name"] for track_id in batch])
        print(f"Se eliminaron {len(to_remove)} canciones de 'Liked Songs' (por playlists).")
    else:
        print("No hay canciones para eliminar por playlists.")
    return removed_songs

# Elimina de Liked Songs si álbum esta guardado
def remove_songs_from_liked_by_album(liked_songs, saved_albums):
    to_remove = [track_id for track_id, info in liked_songs.items() if info["album_id"] in saved_albums]
    removed_songs = []
    if to_remove:
        for batch in chunks(to_remove, 50):
            sp.current_user_saved_tracks_delete(batch)
            removed_songs.extend([liked_songs[track_id]["name"] for track_id in batch])
        print(f"Se eliminaron {len(to_remove)} canciones de 'Liked Songs' (por álbum guardado).")
    else:
        print("No hay canciones para eliminar por álbum guardado.")
    return removed_songs

# Menu principal
if __name__ == "__main__":
    liked_songs = get_liked_songs()
    print(f"Tienes {len(liked_songs)} canciones en 'Liked Songs'.")
    print("Selecciona una opción:")
    print("1) Eliminar canciones en 'Liked Songs' que estén en alguna playlist")
    print("2) Eliminar canciones en 'Liked Songs' cuyo álbum esté guardado")
    print("3) Ejecutar ambas opciones")
    
    opcion = input("Ingresa el número de la opción: ").strip()
    
    removed_overall = []
    
    if opcion == "1":
        playlist_songs = get_all_playlist_songs()
        removed_overall = remove_songs_from_liked_by_playlist(liked_songs, playlist_songs)
    elif opcion == "2":
        saved_albums = get_saved_albums()
        removed_overall = remove_songs_from_liked_by_album(liked_songs, saved_albums)
    elif opcion == "3":
        # Primero eliminar por playlists, luego actualizar y eliminar por álbum
        playlist_songs = get_all_playlist_songs()
        removed_by_playlist = remove_songs_from_liked_by_playlist(liked_songs, playlist_songs)
        # Se actualiza la lista de "Liked Songs" tras la eliminación anterior
        liked_songs = get_liked_songs()
        saved_albums = get_saved_albums()
        removed_by_album = remove_songs_from_liked_by_album(liked_songs, saved_albums)
        removed_overall = removed_by_playlist + removed_by_album
    else:
        print("Opción no válida. Saliendo.")
    
    if removed_overall:
        print("Canciones eliminadas:")
        for song in removed_overall:
            print(f"- {song}")
    else:
        print("No se eliminó ninguna canción.")
