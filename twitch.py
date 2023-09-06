import os
import subprocess
import streamlink
import time

def check_stream(streamer_name):
    streams = streamlink.streams(f"https://www.twitch.tv/{streamer_name}")
    return "best" in streams

def record_stream(streamer_name):
    while True:
        print(f"Le stream de {streamer_name} n'est pas en ligne. Attente de 5 secondes...")
        time.sleep(5)  # Attendre 5 secondes avant de vérifier à nouveau
        if check_stream(streamer_name):
            output_folder = streamer_name
            os.makedirs(output_folder, exist_ok=True)
            output_filename = os.path.join(output_folder, "output.mkv")

            stream = streamlink.streams(f"https://www.twitch.tv/{streamer_name}")["best"]

            ffmpeg_cmd = [
                "ffmpeg",
                "-i", stream.url,
                "-c:v", "libx264",  # Utilisez libx264 pour la vidéo H.264
                "-c:a", "aac",
                "-preset", "ultrafast",
                "-tune", "zerolatency",
                output_filename
            ]

            print(f"Enregistrement en cours pour {streamer_name}...")
            try:
                subprocess.run(ffmpeg_cmd, check=True)
                print(f"Enregistrement terminé pour {streamer_name}. La vidéo est dans le dossier : {output_folder}")
            except subprocess.CalledProcessError as e:
                print(f"Erreur lors de l'enregistrement pour {streamer_name}: {e}")
            except KeyboardInterrupt:
                print(f"Enregistrement interrompu pour {streamer_name}. La vidéo est dans le dossier : {output_folder}")


if __name__ == "__main__":
    streamer_name = input("Nom du streamer Twitch : ")
    record_stream(streamer_name)
