from gtts import gTTS

# Read the text file
with open("response.txt", "r") as file:
    text = file.read().replace("\n", " ")

# Create a TTS object
tts = gTTS(text)

# Save the MP3 file
tts.save("response.mp3")
