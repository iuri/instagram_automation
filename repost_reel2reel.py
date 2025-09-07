import os
import re
from dotenv import load_dotenv

from utils import authenticate

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")



def extract_media_metadata(media):
    """
    Extract safely all relevant metadata from an instagrapi Media object.
    """
    meta = {}



    # --- Handle dict vs object ---
    is_dict = isinstance(media, dict)

    # --- User ---
    if is_dict:
        user = media.get("user", {})
        meta["username"] = user.get("username")
        meta["user_id"] = user.get("pk")
    else:
        meta["username"] = getattr(getattr(media, "user", None), "username", None)
        meta["user_id"] = getattr(getattr(media, "user", None), "pk", None)

    # --- Caption ---
    caption_text = None
    if is_dict:
        caption_text = media.get("caption_text")
    else:
        caption_text = getattr(media, "caption_text", None)
    meta["caption_text"] = caption_text

    # --- Mentions ---
    mentions = []
    if is_dict:
        usertags = media.get("usertags", [])
        if isinstance(usertags, list):
            mentions = [ut.get("user", {}).get("username") for ut in usertags if ut.get("user")]
    else:
        if hasattr(media, "usertags") and media.usertags:
            mentions = [ut.user.username for ut in media.usertags if hasattr(ut, "user")]
    meta["mentions"] = mentions

    # --- Hashtags ---
    hashtags = []
    if caption_text:
        hashtags = re.findall(r"#(\w+)", caption_text)
    meta["hashtags"] = hashtags

    # --- Location ---
    if is_dict:
        location = media.get("location", {})
        meta["location"] = location.get("name") if location else None
    else:
        meta["location"] = getattr(getattr(media, "location", None), "name", None)

    # --- Accessibility Alt Text ---
    if is_dict:
        meta["alt_text"] = media.get("accessibility_caption")
    else:
        meta["alt_text"] = getattr(media, "accessibility_caption", None)

    return meta


def repost_reel(cl, username, code):  
    try:
        # Récupérer les informations de l'utilisateur
        # user_info = cl.user_info_by_username(username)
        # print(f"User info: {user_info}")

        # Télécharger le Reel
        media_pk =  cl.media_pk_from_code(code)
        media_info = cl.media_info(media_pk)

        media_path = cl.video_download(media_info.id)
        print(f"Downloaded Reel to {media_path}")


        # Extract metadata
        meta = extract_media_metadata(media_info)
        print(meta)

        media = cl.clip_upload(
            media_path,
            caption=meta["caption_text"]
        )
        print("✅ Reel posted with metadata!")
        print(f"Reel URL: https://www.instagram.com/reel/{media.code}/")


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