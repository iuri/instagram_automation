import os
from instagrapi import Client
from dotenv import load_dotenv

import random
import requests


load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")
ACCOUNT_PASSWORD = os.environ.get("PASSWORD")

def authenticate():
    cl = Client()
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    print(f"Authenticated as {ACCOUNT_USERNAME}")
    return cl

def get_following_user_ids(cl):
    """
    Get the list of user IDs the account is following.
    """
    user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    following = cl.user_following(user_id)
    return [user.pk for user in following.values()]




def get_following_usernames(cl, exclude_list=None):
    """
    Get the list of usernames the account is following.
    """
    try:
        user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
        user_ids = cl.user_following(user_id)
        user_names = [user.username for user in user_ids.values()]

        # Filtrer les noms d'utilisateur pour exclure ceux dans la liste d'exclusion
        user_names = [username for username in user_names if username not in exclude_list]



        print(f"Found {len(user_names)} followed accounts.")
    except Exception as e:
        print(f"Error retrieving followed accounts: {e}")
        return []
    return user_names

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


def get_stories_from_user(cl, username):
    """
    Retrieve all current stories from a specific following channel by username.
    """
    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)
        print(f"Found {len(stories)} stories for user '{username}'.")
        return stories
    except Exception as e:
        print(f"Error retrieving stories for {username}: {e}")
        return []


def repost_story(cl, story):
    """
    Download a story and repost it to your own story.
    """
    try:
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
            location = story.locations[0]
            print(f"Using location: {location.name}")

        # Ajouter des stickers si disponibles
        stickers = []
        if hasattr(story, "stickers") and story.stickers:
            stickers = story.stickers
            print(f"Found {len(stickers)} stickers in the original story.")


        # Déterminer le type de média et republier en conséquence
        if story.media_type == 1:  # Photo
            cl.photo_upload_to_story(media_path, caption=caption, locations=locations, stickers=stickers)
            print("Reposted photo story with hashtags and location.")
        elif story.media_type == 2:  # Vidéo
            cl.video_upload_to_story(media_path, caption=caption, locations=locations, stickers=stickers)
            print("Reposted video story with hashtags and location.")
        else:
            print("Unsupported story media type.")
    except Exception as e:
        print(f"Error reposting story: {e}")



def download_image_from_url(url, output_path):
    """
    Télécharge une image à partir d'une URL et la sauvegarde dans un fichier local.

    :param url: L'URL de l'image à télécharger.
    :param output_path: Le chemin où l'image sera sauvegardée.
    """
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()  # Vérifie si la requête a réussi

        with open(output_path, 'wb') as file:
            for chunk in response.iter_content(1024):
                file.write(chunk)

        print(f"Image téléchargée et sauvegardée dans : {output_path}")
    except Exception as e:
        print(f"Erreur lors du téléchargement de l'image : {e}")




def main():
    cl = authenticate()
    user_ids = get_following_user_ids(cl)
    print(f"Found {len(user_ids)} followed accounts.")
    
    exclude_list = ["hlacara", "lucastorreslta", "tomrlon", "mcjneto"]
    
    while True:
        usernames = get_following_usernames(cl, exclude_list)
        # print(f"Found {usernames} followed accounts.")
        
        # select a random integer from 1 to 5 
        random_number = random.randint(1, 5)
        print(f"Random number of users to select: {random_number}")
        
        # Select 3 random users from list
        random_users = random.sample(usernames, random_number)
        print(f"Selected random users: {random_users}")

        stories = []
        for username in random_users:
            user_stories = get_stories_from_user(cl, username)
            print(f"Stories objects: {len(user_stories)}")
            # Check if there are any stories
            if user_stories:
                # print(f"Story: {user_stories[0]}")
                stories.append(user_stories[0])
            else:
                print("No stories found to repost.")

        # Check if there are any stories to repost
        if stories:
            break
    
    for story in stories:
        # Repost the story    
        print(f"Reposting story...: {story}")
        repost_story(cl, story)


if __name__ == "__main__":
    main()