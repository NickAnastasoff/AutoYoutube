import cv2
import random
import moviepy.editor as mp
import openai
import json
import os
import datetime
import time
from googleapiclient.http import MediaFileUpload
import pandas as pd
from google_apis import create_service

pathToVideos = "/Users/nickanastasoff/Desktop/Coding/VideoFiles/"
client_file = '/Users/nickanastasoff/Desktop/Coding/VideoFiles/client_secret_339597661959-p1l8b2ulp1mf74aehv161105lc5sdm94.apps.googleusercontent.com.json'

# Load the audio file
audio = mp.AudioFileClip(pathToVideos + "/breathing-again-full.wav")
duration = audio.duration
start_time = random.uniform(0, duration - 6)
clip = audio.subclip(start_time, start_time + 6)
clip.write_audiofile("Fact/random_clip.wav")
# Open the JSON file

with open('Fact/Settings.json') as json_file:
    data = json.load(json_file)
    channel_name = data["channel_name"]
    channel_topics = data['channel_topics'][0]
    random_topic = random.choice(list(channel_topics.keys()))
    array_data = channel_topics[random_topic]
    random_element = random.choice(array_data)
    print("video backround: " + random_element)

openai.api_key = os.environ["OPENAI_API_KEY"]

gptPrompt = '{\n"type":"Psychology Fact",\n"opening_text": "Did you know that according to psychology, people who talk to themselves...",\n"ending_text": "are more likely to have a high IQ. Talking to yourself makes your brain work more efficiently!"\n"type":"Sports fact",\n"opening_text": "Only one sport has been played on the moon...",\n"ending_text": "50 years ago, Alan Shepardan, an Apollo 14 astronaut, played golf on the moon!"\n"type":"Productivity Fact",\n"opening_text": "The most most productive day of the week is...",\n"ending_text": "Tuesday! After 40 hours of work per week, productivity decreases by 50%, and who really feels productive on Monday?"\n"type":"' + str(random_topic) + '",'

response = openai.Completion.create(
model="text-davinci-003",
prompt=gptPrompt,
temperature=0.7,
max_tokens=1000,
top_p=1,
frequency_penalty=0.0,
presence_penalty=0.0,
)

file = open("Fact/article.json","w")
file.write('{\n\"type":"'+ str(random_topic) + '",' + json.loads(str(response))['choices'][0]['text'] + "}")
file.close()
with open("Fact/article.json") as json_file:
    data = json.load(json_file)
    openingText = data["opening_text"]
    endingText = data["ending_text"]
    Title = data["type"].upper()
    videoDescription = "Music provided by TakeTones. Free Download Music: https://taketones.com/search/free-music #shorts #phsycology #boy #girl #fact"

print("video title: " + Title)

phoneheight = 1920
phonewidth = 1080

# this changes here
path = pathToVideos + random_element
files = os.listdir(path)
files = files[ : -1]
randomFile = random.choice(files)
print("files in folder: " + str(files))
print("chosen file: " + randomFile)

clip = mp.VideoFileClip(pathToVideos + random_element + "/" + randomFile)
duration = clip.duration
start_time = random.uniform(0, duration - 6)
subclip = clip.subclip(start_time, start_time + 6)
subclip.write_videofile("Fact/clip.mp4")
cap = cv2.VideoCapture("Fact/clip.mp4")
frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
my_video = mp.VideoFileClip(subclip.filename, audio=True)
w,h = moviesize = my_video.size

Ratio = int(w / phonewidth)

print("screen ratio: "+str(Ratio))

end_text = mp.TextClip(endingText, font='Amiri-regular', color='white', fontsize=60 * Ratio, size = ((phonewidth-100) * Ratio, (500) * Ratio), method='caption')
end_txt_col = end_text.on_color(size=(end_text.w, end_text.h+20), color=(0,0,0), pos=(0,'center'), col_opacity=.5)
end_txt_mov = end_txt_col.set_pos(lambda t: ((w-end_txt_col.w)/2, (h-end_txt_col.h)/2)).set_duration(4).set_start(4)

start_text = mp.TextClip(openingText, font='Amiri-regular', color='white', fontsize=60 * Ratio, size = ((phonewidth-100) * Ratio, (500) * Ratio), method='caption')
start_txt_col = start_text.on_color(size=(start_text.w, start_text.h+20), color=(0,0,0), pos=(0,'center'), col_opacity=.5)
start_txt_mov = start_txt_col.set_pos(lambda t: ((w-start_txt_col.w)/2, (h-start_txt_col.h)/2)).set_duration(4) .set_start(0)

my_text = mp.TextClip(Title.upper(), font='Amiri-regular', color='white', fontsize=70 * Ratio, size = ((phonewidth-100) * Ratio, (100) * Ratio), method='caption')
txt_col = my_text.on_color(size=(my_text.w, my_text.h+20), color=(0,0,0), pos=(0,'center'), col_opacity=1)
txt_mov = txt_col.set_pos(lambda t: ((w-txt_col.w)/2, (h-txt_col.h)/4))

final = mp.CompositeVideoClip([my_video, start_txt_mov, end_txt_mov, txt_mov])
final_clip = final.set_audio(audio)
final_clip.subclip(0,6).write_videofile("Fact/Short.mov",fps=30,codec='libx264')

os.remove("Fact/clip.mp4")
os.remove("Fact/random_clip.wav")
os.remove("Fact/article.json")

# youtube api 

def video_categories():
    video_categories = service.videoCategories().list(part='snippet', regionCode='US').execute()
    df = pd.DataFrame(video_categories.get('items'))
    return pd.concat([df['id'], df['snippet'].apply(pd.Series)[['title']]], axis=1)

API_NAME = 'youtube'
API_VERSION = 'v3'
SCOPES = ['https://www.googleapis.com/auth/youtube']
# SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
service = create_service(client_file, API_NAME, API_VERSION, SCOPES)

print(video_categories())

upload_time = (datetime.datetime.now() + datetime.timedelta(days=0)).isoformat() + '.000Z'
request_body = {
    'snippet': {
        'title': Title,
        'description': videoDescription,
        'categoryId': '29',
        'tags': []
    },
    'status': {
        'privacyStatus': 'private',
        'publishedAt': upload_time,
        'selfDeclaredMadeForKids': False
    },
    'notifySubscribers': False
}

video_file = 'Fact/Short.mov'
media_file = MediaFileUpload(video_file)
#print(media_file.size() / pow(1024, 2), 'mb')
#print(media_file.to_json())
#print(media_file.mimetype())

response_video_upload = service.videos().insert(
    part='snippet,status',
    body=request_body,
    media_body=media_file
).execute()
uploaded_video_id = response_video_upload.get('id')

video_id = uploaded_video_id

counter = 0
response_update_video = service.videos().list(id=video_id, part='status').execute()
update_video_body = response_update_video['items'][0]

while 10 > counter:
    if update_video_body['status']['uploadStatus'] == 'processed':
        update_video_body['status']['privacyStatus'] = 'public'
        service.videos().update(
            part='status',
            body=update_video_body
        ).execute()
        print('Video {0} privacy status is updated to "{1}"'.format(update_video_body['id'], update_video_body['status']['privacyStatus']))
        break
    # adjust the duration based on your video size
    time.sleep(10)
    response_update_video = service.videos().list(id=video_id, part='status').execute()
    update_video_body = response_update_video['items'][0]
    counter += 1

os.remove("token files/token_youtube_v3.json")
os.remove("Fact/__pycache__/google_apis.cpython-310.pyc")