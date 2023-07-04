# imports
from gtts import gTTS
from dotenv import load_dotenv
import speech_recognition as sr
import openai
import os
import playsound

load_dotenv()

# function to convert text to speech ( using gTTS module )
def speak(text):
    tts = gTTS(text=text,  lang='en-US')

    filename = "abc.mp3"
    tts.save(filename)
    playsound.playsound(filename)
    os.remove(filename)

openai.api_key = os.getenv("OPENAI_API_KEY")

model_id = 'gpt-3.5-turbo'

system_msg = 'you are conversational model which replies to users in 25-30 words'

conversations = [{"role": "system", "content": system_msg}]

# function which makes request to the ChatGPT model
def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )

    speak(response['choices'][0].message.content)

    conversations.append({'role': response.choices[0].message.role, 'content': response.choices[0].message.content})

# infinite loops which takes user input in speech, converts to text and calls the chatgpt function
while True:
    if len(conversations) > 6:
        del conversations[1:2]
    prompt = ''
    r = sr.Recognizer()

    try:
        with sr.Microphone() as source2:
            r.adjust_for_ambient_noise(source2, duration=0.2)
            audio2 = r.listen(source2)
            MyText = r.recognize_google(audio2)
            MyText = MyText.lower()
            prompt = MyText
    except sr.RequestError as e:
        print('Could not request results, {}'.format(e))
    except sr.UnknownValueError:
        print('Unknown error')

    
    conversations.append({"role": "user", "content": prompt})

    ChatGPT_conversation(conversations)
