import random      # For picking random jokes or greetings
import datetime    # To get the current date and time
import webbrowser  # To open websites like Google or YouTube
import pyowm       # For weather information from OpenWeatherMap
import pyttsx3     # Text-to-speech engine
import wikipedia   # To search Wikipedia
from pygame import mixer   # For playing audio/music
import speech_recognition as sr  # To recognize voice input
from newsapi import NewsApiClient  # To fetch news headlines
import os# to access python process environmental variables
from dotenv import load_dotenv

# Initialize text-to-speech engine
engine = pyttsx3.init() #creates engine obj which is of the search engine sw in system by defualt
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)
engine.setProperty('volume', 1.0)  # max volume
rate = engine.getProperty('rate')
engine.setProperty('rate', rate - 25)
load_dotenv()#reads .env file and sets each key-value pair as an environment variable in your Python program temporarily.

# News API
api_key = os.getenv("NEWS_API_KEY")  #api key created from newapi website
newsapi = NewsApiClient(api_key=api_key)#creates newsapi obj with this api key

# Commands and responses
greetings = ['hey there', 'hello', 'hi', 'hai', 'hey!']
questions = ['how are you', 'how are you doing']
responses = ["I'm fine, thank you!", "Doing well!"]
creators = ['who made you', 'who created you']
creator_replies = ['I was created by Jo.', 'Some human I never got to know.']
time_queries = ['what time is it', 'what is the time', 'time']
identity_queries = ['who are you', 'what is your name']
open_browser_cmds = ['open browser', 'open google']
music_cmds = ['play music', 'play songs', 'play a song', 'open music player']
joke_cmds = ['tell a joke', 'tell me a joke', 'say something funny', 'tell something funny']
jokes = [
    "Can a kangaroo jump higher than a house? Of course, a house doesn't jump at all.",
    "My dog used to chase people on a bike a lot. It got so bad, finally I had to take his bike away.",
    "Doctor: I'm sorry but you suffer from a terminal illness and have only 10 to live. Patient: 10 what? Months? Weeks? Doctor: Nine."
]
youtube_cmds = ['open youtube', 'i want to watch a video']
weather_cmds = ['tell me the weather', 'weather', 'what about the weather']
exit_cmds = ['exit', 'close', 'goodbye', 'nothing']
color_cmds = ['what is your color', 'what is your colour', 'choose a color', 'what is your favourite colour',
              'what is your favourite color']
colors = ['red', 'green', 'black', 'blue', 'yellow']
thank_cmds = ['thank you']
thank_replies = ['you\'re welcome', 'glad I could help you']
news_cmds = ['todays news', 'news headlines', 'news']

# Initialize mixer once (not obj creation)(only needs to be called once)
mixer.init()


def speak(text):
    engine.say(text)# add the arg to the queue to speak
    engine.runAndWait()#starts speech engine and makes it speak all in queue in order


def listen():
    r = sr.Recognizer()#Creates a recognizer object from speech_recognition for hearing sound
    try:
        with sr.Microphone() as source:## Use microphone as input
            print("Listening...")
            audio = r.listen(source)  # Record user's voice
        return r.recognize_google(audio).lower()#Converts speech to text
    except (sr.UnknownValueError, sr.RequestError, OSError) as e:
        if isinstance(e, sr.UnknownValueError):
            speak("I didn't get that. Please try again.")
        elif isinstance(e, sr.RequestError):
            speak("Cannot reach Google. Check your internet connection.")
        elif isinstance(e, OSError):
            speak("No microphone detected. Please connect one.")
        return None


def open_google():
    webbrowser.open('https://www.google.com')


def open_youtube():
    webbrowser.open('https://www.youtube.com')


def play_music():
    try:
        mixer.music.stop()
        mixer.music.load(
            r"C:\Users\ranga\Desktop\interview\Academic Projects\Voice Assistant\multimedia\Vazhithunaiye.mp3")
        mixer.music.play()
        speak("Playing music.")
    except Exception as e:
        print(f"Music error: {e}")
        speak("Sorry, I could not play music.")


def tell_joke():
    joke = random.choice(jokes)
    print(joke)
    speak(joke)


def get_weather():
    try:
        owm_key = os.getenv("OWMAPI_KEY")  # read from .env
        owm = pyowm.OWM(owm_key)  # use the new key to connect to the weather service
        mgr = owm.weather_manager()#manage weather data
        observation = mgr.weather_at_place('Chennai, IN')
        w = observation.weather#Stores weather details.
        temperature = w.temperature('celsius')["temp"]
        humidity = w.humidity
        status = w.status
        speak(f"The weather is {status} with temperature {temperature} degrees Celsius and humidity {humidity} percent.")
        print(f"Temperature: {temperature}°C, Humidity: {humidity}%, Status: {status}")
    except Exception as e:
        print(f"Weather error: {e}")
        speak("Sorry, I could not get the weather information.")


def get_news():
    try:
        top_headlines = newsapi.get_top_headlines(country="in", page_size=5)#Fetches top 5 Indian news headlines.
        articles = top_headlines.get("articles", [])
        if not articles:
            speak("No news found at the moment.")
            return
        for article in articles:
            print(article["title"])
            speak(article["title"])
    except Exception as e:
        print(f"News error: {e}")
        speak("Sorry, I could not fetch news.")


def tell_time():
    now = datetime.datetime.now()#Gets current time.
    current_time = now.strftime("%H:%M")
    print("Current time:", current_time)
    speak("The time is " + current_time)


def search_wikipedia(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        print(summary)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError:
        speak("Your query is ambiguous, please be more specific.")
    except (wikipedia.exceptions.PageError, Exception):
        speak("I could not find a Wikipedia page on that topic. Let me search on Google for you.")
        webbrowser.open_new(f'https://www.google.com/search?q={query}')#if no pg is found open google search page


# Main loop
while True:
    user_input = listen()
    if not user_input:
        continue

    if any(greet in user_input for greet in greetings):#check for every greet (ele) in greetings arr is in user_input
        reply = random.choice(greetings)
        print(reply)
        speak(reply)

    elif any(q in user_input for q in questions):
        reply = random.choice(responses)
        print(reply)
        speak(reply)

    elif any(q in user_input for q in creators):
        reply = random.choice(creator_replies)
        print(reply)
        speak(reply)

    elif any(q in user_input for q in thank_cmds):
        reply = random.choice(thank_replies)
        print(reply)
        speak(reply)

    elif any(q in user_input for q in color_cmds):
        color = random.choice(colors)
        print(color)
        speak(color + ". It keeps changing every microsecond.")

    elif any(q in user_input for q in news_cmds):
        get_news()

    elif any(q in user_input for q in music_cmds):
        play_music()

    elif any(q in user_input for q in identity_queries):
        reply = "I am your personal AI assistant."
        print(reply)
        speak(reply)

    elif any(q in user_input for q in youtube_cmds):
        open_youtube()
        speak("Opening YouTube.")

    elif any(q in user_input for q in exit_cmds):
        speak("See you later!")
        break

    elif any(q in user_input for q in weather_cmds):
        get_weather()

    elif any(q in user_input for q in time_queries):
        tell_time()

    elif any(q in user_input for q in open_browser_cmds):
        open_google()
        speak("Opening Google.")

    elif any(q in user_input for q in joke_cmds):
        tell_joke()

    else:
        search_wikipedia(user_input)
