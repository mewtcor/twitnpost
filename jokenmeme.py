import requests
import os
import uuid
import time
import platform
from twikit import Client  # Ensure 'twikit' is the correct Twitter API client library

# Initialize global variables
tweet_counter = 0  # Initialize overall tweet counter
meme_counter = 0  # Counter for memes tweeted
joke_counter = 0  # Counter for jokes tweeted
used_image_urls = set()  # Initialize a set to track used image URLs
USERNAME = 'm3wt'
EMAIL = 'madcackle416@gmail.com'
PASSWORD = 'esirDR4E8B94'
client = None
start_time = time.time()  # Store start time for duration tracking

# Define a function to clear the console
def clear_console():
    if platform.system() == "Windows":
        os.system('cls')  # For Windows
    else:
        os.system('clear')  # For Unix/Linux/MacOS

# Define functions for fetching memes and jokes
def fetch_meme(tag="memes"):
    global used_image_urls
    while True:
        url = f"https://meme-api.com/gimme/{tag}"
        response = requests.get(url, headers={"Accept": "application/json"})
        if response.ok:
            data = response.json()
            meme_url = data.get("url")
            meme_title = data.get("title")
            meme_id = str(uuid.uuid4())

            if meme_url.endswith('.gif') or meme_url in used_image_urls:
                continue

            used_image_urls.add(meme_url)
            return {"meme_id": meme_id, "title": meme_title, "url": meme_url}
        else:
            break

def fetch_joke():
    url = "https://icanhazdadjoke.com/"
    response = requests.get(url, headers={"Accept": "application/json"})
    if response.ok:
        data = response.json()
        return data.get("joke")
    else:
        return None

# Define a function to download images
def download_image(image_info):
    if image_info:
        image_url = image_info["url"]
        image_id = image_info["meme_id"]
        response = requests.get(image_url)
        if response.status_code == 200:
            os.makedirs('images', exist_ok=True)
            file_extension = image_url.split('.')[-1]
            file_path = os.path.join('images', f"{image_id}.{file_extension}")
            with open(file_path, 'wb') as file:
                file.write(response.content)
            return file_path
    return None

# Integrated posting to Twitter for both memes and jokes
def post_to_twitter(content, is_joke=False):
    global tweet_counter, meme_counter, joke_counter, client
    if is_joke:
        joke_counter += 1  # Increment joke counter
        tweet_content = f"{content} #dadjoke #jokes"
        client.create_tweet(text=tweet_content)
    else:
        meme_counter += 1  # Increment meme counter
        image_path = download_image(content)
        if image_path:
            media_id = [client.upload_media(image_path, 0)]
            tweet_content = content['title'] + " #memes"
            client.create_tweet(text=tweet_content, media_ids=media_id)
        else:
            return False

    tweet_counter += 1
    print(f"Tweet {tweet_counter} posted to Twitter.")
    return True

# Define the countdown function
def countdown(t):
    while t:
        mins, secs = divmod(t, 60)
        timeformat = '{:02d}:{:02d}'.format(mins, secs)
        print(timeformat, end='\r')
        time.sleep(1)
        t -= 1

# Main function to alternate between meme and joke tweets
def main():
    global client, start_time
    client = Client('en-nz')
    client.login(auth_info_1=USERNAME, auth_info_2=EMAIL, password=PASSWORD)

    meme_flag = True  # Start with a meme
    while True:
        clear_console()  # Clear the console before each loop iteration

        if meme_flag:
            content = fetch_meme()
            if content:
                print("Posting a meme...")
                post_to_twitter(content)
        else:
            joke = fetch_joke()
            if joke:
                print("Posting a joke...")
                post_to_twitter(joke, is_joke=True)

        meme_flag = not meme_flag  # Toggle flag to alternate
        
        # Print counters and total duration
        current_time = time.time()
        execution_duration = current_time - start_time
        print(f"Total memes tweeted: {meme_counter}, Total jokes tweeted: {joke_counter}")
        print(f"Script running for: {execution_duration // 3600} hours, {(execution_duration % 3600) // 60} minutes, {execution_duration % 60:.0f} seconds")

        print("Starting countdown for 1 hour...")
        countdown(3600)  # 1 hour countdown

if __name__ == '__main__':
    main()
