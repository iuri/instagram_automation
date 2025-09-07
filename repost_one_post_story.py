import os
from dotenv import load_dotenv
from utils import authenticate

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")

def main():
    cl = authenticate()
    target_username = input("Enter the username to fetch stories from: ").strip()
    code = input("Enter the Post ID to repost: ").strip()  
    user_info = cl.user_info_by_username(target_username)
    print(f"User info: {user_info}")
    if code:
        print(f"Fetching media info for post ID: {code}")
        media = cl.media_info(cl.media_pk_from_code(code))
        print(f"Media info: {media}")

        # repost_media(cl, media)


        # Repost based on type
        if media.media_type == 1:  # Photo
            # Download file
            media_path = cl.photo_download(media.pk)
            cl.photo_upload_to_story(path=media_path)
           
        else:
            print("Unsupported media type")

if __name__ == "__main__":  
    main()