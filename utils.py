import os
import uuid
from dotenv import load_dotenv
from instagrapi import Client
import random

from moviepy.editor import VideoFileClip
load_dotenv()
ACCOUNT_USERNAME = os.environ.get("USERNAME")
ACCOUNT_PASSWORD = os.environ.get("PASSWORD")

def generate_device(username):
    return {
        "app_version": "246.0.0.54.120",
        "android_version": random.randint(23, 30),
        "android_release": "11",
        "dpi": "420dpi",
        "resolution": "1080x1920",
        "manufacturer": "Samsung",
        "device": "SM-G991B",
        "model": "Galaxy S21",
        "cpu": "exynos2100",
        "version_code": "306115652",
        "phone_id": str(uuid.uuid4()),
        "device_id": f"android-{uuid.uuid4().hex[:16]}",
        "adid": str(uuid.uuid4()),
        "session_id": str(uuid.uuid4()),
        "uuid": str(uuid.uuid4())
    }


def authenticate():
    cl = Client()
    device = generate_device(ACCOUNT_USERNAME)  # Generate a realistic random mobile device profile
    cl.set_device(device)
    #cl.load_settings("settings.json")
    cl.login(ACCOUNT_USERNAME, ACCOUNT_PASSWORD)
    cl.dump_settings("settings.json")
    print(f"Authenticated as {ACCOUNT_USERNAME}")
    return cl







def split_video_for_stories(input_path, output_dir, max_duration=15):
    """
    Splits a video into multiple parts, each no longer than max_duration seconds.

    Args:
        input_path (str): Path to the input video file.
        output_dir (str): Directory where the split clips will be saved.
        max_duration (int): Maximum duration of each story part in seconds (default: 15).
    """
    clip = VideoFileClip(input_path)
    total_duration = clip.duration
    parts = int(total_duration // max_duration) + (1 if total_duration % max_duration > 0 else 0)

    filenames = []

    for i in range(parts):
        start = i * max_duration
        end = min((i + 1) * max_duration, total_duration)

        subclip = clip.subclip(start, end)
        output_path = f"{output_dir}/story_part_{i + 1}.mp4"
        subclip.write_videofile(output_path, codec="libx264", audio_codec="aac", fps=24)

        filenames.append(output_path)

    clip.close()
    return filenames


def get_stories_from_user(cl, username):
    """
    Retrieve all current stories from a specific following channel by username.
    """
    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)
        # print(f"Found {len(stories)} stories for user '{username}'.")
        return stories
    except Exception as e:
        # print(f"Error retrieving stories for {username}: {e}")
        return []
    



def get_following_user_ids(cl):
    """
    Get the list of user IDs the account is following.
    """
    user_id = cl.user_id_from_username(ACCOUNT_USERNAME)
    following = cl.user_following(user_id)
    return [user.pk for user in following.values()]


