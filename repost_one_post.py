import os
from dotenv import load_dotenv

from utils import authenticate

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")



def get_following_user_ids(cl):
    """
    Get the list of user IDs the account is following.
    """
    user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    following = cl.user_following(user_id)
    return [user.pk for user in following.values()]

def get_recent_posts_and_stories(cl, user_ids, posts_per_user=3):
    """
    Retrieve recent posts and stories from a list of user IDs.
    """
    print(f"Fetching recent posts and stories for {len(user_ids)} users...")
    data = {}
    for uid in user_ids:
        username = cl.user_info(uid).username
        # Get recent posts
        posts = cl.user_medias(uid, amount=posts_per_user)
        # Get stories
        stories = cl.user_stories(uid)
        data[username] = {
            "posts": posts,
            "stories": stories
        }
    return data



def repost_media(cl, media):
    """
    Download a story and repost it to your own story.
    """
    print(f"Reposting media: {media}")
    # Download the story media
    media_path = cl.media_download(media.pk)
    print(f"Downloaded story to {media_path}")
    exit()
    # Safely get caption if it exists, else use empty string
    caption = getattr(story, "caption", "")

    # Ajouter des hashtags à la légende
    # hashtags = "#inspiration #photography #AIgenerated #iurixtech #artificialintelligence #techinnovation, #digitalart, #creativeAI"
    hashtags = "#iurixtech"
    caption = f"{caption}\n\n{hashtags} owner: @{story.user.username}"

    # Ajouter une localisation
    locations = []
    if hasattr(story, "locations") and story.locations:
        locations = story.locations[0]
        # print(f"Using location: {location.name}")

    # Ajouter des stickers si disponibles
    stickers = []
    if hasattr(story, "stickers") and story.stickers:
        stickers = story.stickers
        # print(f"Found {len(stickers)} stickers in the original story.")
    print(f"Reposting story with caption: {media_path} {story.media_type} {caption}")
    # Déterminer le type de média et republier en conséquence
    if story.media_type == 1:  # Photo
        cl.photo_upload_to_story(media_path, caption=caption, locations=locations, stickers=stickers)
        print("Reposted photo story.")
    elif story.media_type == 2:  # Vidéo
        owner = cl.user_info_by_username(story.user.username)
        upload_id = cl.video_upload_to_story(
            media_path,
            f"Credits @{owner}")
        print(f"Video uploaded with ID: {upload_id}")
        
        # result = cl.video_configure_to_story(upload_id)
        # print(f"Story successfully configured and posted! {result}")
        
        print("Reposted video story.")
    else:
        # print("Unsupported story media type.")
        return "Unsupported story media type."
    return


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
            cl.photo_upload(
                path=media_path,
                caption=media.caption_text or ""
            )
            cl.photo_upload_to_story(path=media_path)
            print("Reposted photo.")
        elif media.media_type == 8:  # Album/Carousel
            media_paths = cl.album_download(media.pk)
            cl.album_upload(
                paths=media_paths,
                caption=media.caption_text or ""
            )
            for path in media_paths:
                cl.photo_upload_to_story(path=path)
            print("Reposted album.")
        else:
            print("Unsupported media type")

if __name__ == "__main__":  
    main()