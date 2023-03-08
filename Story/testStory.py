# IMPORTS

import openai
import requests
import json
import random
from PIL import Image
import json
import pyttsx3
import time
from moviepy.editor import *

# VARIBLES

# Initialize the TTS engine
engine = pyttsx3.init()
# Set the speed and volume rate
engine.setProperty('rate', 150)
engine.setProperty('volume', 1)

prompt = "write a short, 3 paragraph, horror story:"
storyToJsonPrompt = 'Please provide a short story that you would like me to analyze. Once you\'ve provided the story, I will return five keywords from five key events in the story, these keywords will be as decriptive as possible, as in sprint instead of walk, in a JSON array.Story: Once upon a time, there was a young boy named Jack. One day, Jack climbed a giant beanstalk and discovered a castle in the clouds. In the castle, he found a golden harp, a goose that laid golden eggs, and a giant who was fast asleep. Jack stole the harp and the goose, but the giant woke up and chased him down the beanstalk. Jack chopped down the beanstalk, causing the giant to fall to his death.JSON output: \n{\n"prompts":["beanstalk", "harp", "theft", "chase", "destruction"]\n}\nStory:'
openai.api_key = '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'

# MAIN FUNCTIONS
def findstory():
    print("finding story")
    rungpt(prompt)
    with open("response.txt", "w") as f:
        f.write(response)

def imagePrompts():
    global story
    global images
    print("getting image prompts")
    with open("response.txt", "r") as file:
       story = file.read()
    rungpt(storyToJsonPrompt + story + "JSON output:")
    with open("prompts.json", "w") as f:
        f.write(response)
    with open('prompts.json') as f:
        data = json.load(f)
        images = len(data["prompts"])

def image(keyword):
    print("finding image: " + keyword)
    global imageNum
    access_key = "jOcdgbjZX5ic3TbyQBHW4AcVqIsJFDUr1OYNynXnP_Q"
    api_url = f"https://api.unsplash.com/search/photos?query={keyword}&client_id={access_key}&orientation=portrait"
    response = requests.get(api_url)
    result = json.loads(response.text)
    images = result["results"]
    chosen_image = random.choice(images)
    image_url = chosen_image["urls"]["regular"]
    image_data = requests.get(image_url).content
    with open("unsplash" + str(imageNum) + ".jpg", "wb") as f:
        f.write(image_data)

def render():
    global story
    print("putting it all together")

    # Generate speech and create an audio clip
    tts(story, "story_audio.mp3")
    audio = AudioFileClip("story_audio.mp3")
    
    # Generate the images and create video clips
    clips = []
    for imageNum in range(images):
        keyword = data["prompts"][imageNum]
        image("scary " + keyword)
        image_path = f"unsplash{imageNum}.jpg"
        image_clip = ImageClip(image_path).set_duration(5)
        clips.append(image_clip)
    
    # Concatenate the video clips
    video = concatenate_videoclips(clips)
    
    # Add the audio clip to the video clip
    final_clip = video.set_audio(audio)
    
    # Save the final video
    final_clip.write_videofile("story_with_audio.mp4", fps=24, codec='libx264')


# SIDE FUNCTIONS
def rungpt(prompt):
    global response
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.0,
    )
    response = response['choices'][0]['text']

    return response

def tts(textIn, filename):
    engine.save_to_file(textIn, filename)
    engine.runAndWait()

# RUN FUNCTIONS
findstory()
imagePrompts()
with open('prompts.json') as f:
    data = json.load(f)
for imageNum in range(images):
    keyword = data["prompts"][imageNum]
    image("scary " + keyword)
render()