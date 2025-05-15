import os
from dotenv import load_dotenv


from utils import authenticate, split_video_for_stories

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")


def repost_reel(cl, username, code):
    """
    Télécharge un Reel spécifique d'un utilisateur et le republie.

    :param cl: Instance de l'objet Client d'Instagrapi.
    :param username: Nom d'utilisateur du compte source.
    :param reel_id: ID du Reel à republier.
    """
    try:
        # Récupérer les informations de l'utilisateur
        # user_info = cl.user_info_by_username(username)
        # print(f"User info: {user_info}")

        # Télécharger le Reel
        media_pk =  cl.media_pk_from_code(code)
        media_info = cl.media_info(media_pk)
        media_path = cl.video_download(media_info.id)
        print(f"Downloaded Reel to {media_path}")

        if media_info.video_duration > 15:
            # Split the video into parts if it's longer than 15 seconds
            os.makedirs(f"./videos/input/{code}", exist_ok=True)
            output_dir = os.path.dirname(f"./videos/input/{code}")
            split_filenames = split_video_for_stories(media_path, output_dir)
            print(f"Split video into {len(split_filenames)} parts.")
            # Upload each part to the story

            for filename in split_filenames:
                cl.video_upload_to_story(filename, f"Credits @{username}")
                print(f"Uploaded {filename} to story.")
            # Clean up split files
            for filename in split_filenames:
                os.remove(filename)
        else:
            # Load video and resize
            # clip = VideoFileClip(media_path) # .resize(height=1280).set_position("center")

            # Trim the original clip before creating the composite
            #if clip.duration > 15:
            #    clip = clip.subclip(0, 15)  # ✅ safe here

            # Create composite canvas
            #final_clip = CompositeVideoClip([clip], size=(720, 1280))
            #final_clip = final_clip.set_duration(clip.duration)  # ✅ set matching duration

            # Export final video
            #final_clip.write_videofile(f"{code}_story_final.mp4", codec="libx264", audio_codec="aac", fps=24)

            cl.video_upload_to_story(
                f"{code}_story_final.mp4",
                f"Credits @{username}"
            )     
        print("Reposted Reel successfully.")
    except Exception as e:
        print(f"Error reposting Reel: {e}")
        return f"Error reposting Reel: {e}"
    return



def main():
    cl = authenticate()
    target_username = input("Enter the username to fetch the Reel from: ").strip()
    reel_id = input("Enter the Reel ID to repost: ").strip()

    print(f"Reposting Reel from @{target_username} with ID {reel_id}...")
    repost_reel(cl, target_username, reel_id)



if __name__ == "__main__":  
    main()