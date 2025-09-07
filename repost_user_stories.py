import os
from dotenv import load_dotenv
from utils import authenticate, get_stories_from_user

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")


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



def repost_story(cl, story):
    """
    Download a story and repost it to your own story.
    """

    # Download the story media
    media_path = cl.story_download(story.pk)
    print(f"Downloaded story to {media_path}")

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
    # user_info = cl.user_info_by_username(target_username)
    # print(f"User info: {user_info}")
           
    stories = get_stories_from_user(cl, target_username)

    print(f"Stories objects: {stories}")

    if stories:
        # Repost the first story
        print("Reposting story...")
        repost_story(cl, stories[0])
    else:
        print("No stories found to repost.")

if __name__ == "__main__":  
    main()