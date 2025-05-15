import os

from dotenv import load_dotenv
import random

from utils import authenticate, get_stories_from_user, repost_story

load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")



def get_following_usernames(cl):
    """
    Get the list of usernames the account is following.
    """
    try:
        user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
        user_ids = cl.user_following(user_id)
        user_names = [user.username for user in user_ids.values()]
        # print(f"Found {len(user_names)} followed accounts.")
    except Exception as e:
        # print(f"Error retrieving followed accounts: {e}")
        return []
    return user_names

def get_recent_posts_and_stories(cl, user_ids, posts_per_user=3):
    """
    Retrieve recent posts and stories from a list of user IDs.
    """
    # print(f"Fetching recent posts and stories for {len(user_ids)} users...")
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


def select_stories():
    cl = authenticate()
    # user_ids = get_following_user_ids(cl)
    # print(f"Found {len(user_ids)} followed accounts.")
    # exclude_list = ["hlacara", "lucastorreslta", "tomrlon", "mcjneto"]
    
    while True:
        usernames = get_following_usernames(cl)
        # print(f"Found {usernames} followed accounts.")
        
        # select a random integer from 1 to 5 
        random_number = random.randint(1, 5)
        # print(f"Random number of users to select: {random_number}")
        
        # Select 3 random users from list
        random_users = random.sample(usernames, random_number)
        # print(f"Selected random users: {random_users}")
        stories = []
        for username in random_users:
            user_info = cl.user_info_by_username(username)
            # print(f"User info: {user_info}")
            # user_info = cl.user_info(story.user.pk)
            if user_info.account_type in [2, 3]:  # 2: Business, 3: Creator
                user_stories = get_stories_from_user(cl, username)
                # print(f"Stories objects: {len(user_stories)}")
                # Check if there are any stories
                if user_stories:
                    # print(f"Story: {user_stories[0]}")
                    stories.append(user_stories[0])
                # else:
                    # print("No stories found to repost.")
            # else:
                # print(f"User {story.user.username} is not a business or creator account. Skipping story repost.")
                

        # Check if there are any stories to repost
        if stories:
            break
    # print(f"Found {len(stories)} stories to repost.")
    for story in stories:
        # Repost the story    
        # print(f"Reposting story...: {story}")
        repost_story(cl, story)



if __name__ == "__main__":
    select_stories()