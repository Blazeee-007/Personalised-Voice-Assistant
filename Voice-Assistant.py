import speech_recognition as sr
import pyttsx3
import datetime
import os
import wikipedia
import requests
import schedule
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from googleapiclient.discovery import build
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
import RPi.GPIO as GPIO
import webbrowser
import sys

# Set up the Assistant's voice
engine = pyttsx3.init()
engine.setProperty('rate', 150)  # Speed of speech
engine.setProperty('volume', 1)  # Volume (0.0 to 1.0)

# Global variable for reminders and tasks
reminders = []

# Set up GPIO for IoT/Home Automation (Raspberry Pi)
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)  # Pin 17 for controlling devices

# Google Calendar API Setup
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']

# Function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function to listen to the user's command
def listen():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for command...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
        
        try:
            command = recognizer.recognize_google(audio)
            print(f"Command received: {command}")
            return command.lower()
        except sr.UnknownValueError:
            speak("Sorry, I didn't catch that.")
            return ""
        except sr.RequestError:
            speak("Sorry, I'm having trouble connecting to the service.")
            return ""

# Function to get current time
def get_time():
    now = datetime.datetime.now()
    return now.strftime("%H:%M %p")  # Time in 12-hour format

# Function to search Wikipedia
def search_wikipedia(query):
    speak("Searching Wikipedia...")
    try:
        summary = wikipedia.summary(query, sentences=2)
        speak(summary)
    except wikipedia.exceptions.DisambiguationError as e:
        speak(f"Multiple results found. Please be more specific: {e.options}")
    except wikipedia.exceptions.HTTPTimeoutError:
        speak("Wikipedia service is currently unavailable.")
    except Exception as e:
        speak("I encountered an error while fetching the data.")
        print(e)

# Function to authenticate and fetch Google Calendar events
def authenticate_google_account():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_calendar_events():
    creds = authenticate_google_account()
    service = build('calendar', 'v3', credentials=creds)
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    events_result = service.events().list(calendarId='primary', timeMin=now,
                                           maxResults=10, singleEvents=True,
                                           orderBy='startTime').execute()
    events = events_result.get('items', [])
    if not events:
        speak('No upcoming events found.')
        return
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        speak(f"Upcoming event: {event['summary']} at {start}")

# Function to fetch weather data
def get_weather():
    api_key = "your_api_key"
    city = "your_city"
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
    response = requests.get(url)
    weather_data = response.json()
    if weather_data["cod"] == 200:
        weather_desc = weather_data["weather"][0]["description"]
        temp = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        speak(f"The current weather in {city} is {weather_desc}. Temperature is {temp}°C with {humidity}% humidity.")
    else:
        speak("Sorry, I couldn't fetch the weather information.")

# Function to send an email
def send_email(subject, body, to_email):
    sender_email = "your_email@gmail.com"
    password = "your_email_password"
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = to_email
    message["Subject"] = subject
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, text)
        server.close()
        speak(f"Email sent to {to_email}")
    except Exception as e:
        speak(f"Failed to send email: {str(e)}")

# Function for task reminders
def add_reminder(task, time_str):
    reminders.append((task, time_str))
    schedule.every().day.at(time_str).do(lambda: speak(f"Reminder: {task}"))

def run_reminders():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Function to control home automation devices (IoT)
def control_light(command):
    if "turn on the light" in command:
        GPIO.output(17, GPIO.HIGH)
        speak("The light is now on.")
    elif "turn off the light" in command:
        GPIO.output(17, GPIO.LOW)
        speak("The light is now off.")

# Function to open apps and websites
def open_app_or_website(command):
    if 'open' in command:
        if 'app' in command:
            app_name = command.replace('open app', '').strip()
            if app_name:
                speak(f"Opening {app_name}.")
                os.system(f"start {app_name}")  # For Windows
            else:
                speak("Which app would you like me to open?")
        elif 'website' in command:
            website_name = command.replace('open website', '').strip()
            if website_name:
                speak(f"Opening {website_name} website.")
                webbrowser.open(f"http://{website_name}")  # Open in default browser
            else:
                speak("Please specify the website.")
        else:
            speak("Sorry, I can only open apps or websites.")
    else:
        speak("Please specify what you want to open. You can say 'Open app [app name]' or 'Open website [website name]'.")

# Function to handle commands
def handle_command(command):
    if 'hello' in command or 'hi' in command:
        speak("Hello Mr. Sasank, how can I assist you today?")
    
    elif 'time' in command:
        current_time = get_time()
        speak(f"The current time is {current_time}.")
    
    elif 'date' in command:
        current_date = datetime.datetime.now().strftime("%A, %d %B %Y")
        speak(f"Today's date is {current_date}.")
    
    elif 'open' in command:
        open_app_or_website(command)
    
    elif 'wikipedia' in command:
        query = command.replace('wikipedia', '').strip()
        search_wikipedia(query)
    
    elif 'weather' in command:
        get_weather()
    
    elif 'calendar' in command:
        get_calendar_events()
    
    elif 'email' in command:
        speak("Please tell me the recipient's email.")
        recipient_email = listen()
        speak("Please tell me the subject.")
        subject = listen()
        speak("What would you like to say in the email?")
        body = listen()
        send_email(subject, body, recipient_email)
    
    elif 'reminder' in command:
        speak("What task would you like to set a reminder for?")
        task = listen()
        speak("At what time?")
        time_str = listen()
        add_reminder(task, time_str)
    
    elif 'light' in command:
        control_light(command)
    
    elif 'exit' in command or 'quit' in command:
        speak("Goodbye Mr. Sasank. Have a nice day!")
        exit()

# Main function
def run_assistant():
    speak("Hello Mr. Sasank, I am your assistant. How can I help you today?")
    
    while True:
        command = listen()

        if command:
            handle_command(command)

# Start the assistant
if __name__ == "__main__":
    run_assistant()
