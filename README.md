# Voice Assistant Project

## Overview

This is a Python-based voice assistant designed to assist users with a variety of tasks using voice commands. The assistant integrates multiple services, such as checking the weather, sending emails, controlling IoT devices (using Raspberry Pi GPIO), managing reminders, searching Wikipedia, interacting with Google Calendar, and more. This project is built for a Raspberry Pi, but can be modified for other platforms.

## Features

### 1. **Voice Interaction**
   - The assistant listens to voice commands and responds via speech using `pyttsx3`.
   - Recognizes commands such as "hello", "time", "weather", "reminder", etc.

### 2. **Weather Information**
   - Fetches current weather details for a specified city using OpenWeatherMap API.

### 3. **Google Calendar Integration**
   - Retrieves and announces upcoming events from the user's Google Calendar.
   - Requires Google OAuth2 authentication to access the calendar.

### 4. **Email Sending**
   - Sends emails using Gmail's SMTP server.
   - Users can provide recipient, subject, and body of the email through voice commands.

### 5. **Task Reminders**
   - Set daily reminders for tasks that are announced at specified times.
   - Uses the `schedule` library to manage reminders.

### 6. **Raspberry Pi GPIO Control**
   - Control home automation devices like lights using the Raspberry Pi GPIO pins.

### 7. **App & Website Launching**
   - Opens applications or websites based on voice commands.

## Prerequisites

- Python 3.6+ 
- Raspberry Pi (for GPIO control) or other platform (adjust code as needed)
- Necessary APIs for weather, Google Calendar, and email integration (API keys required)

### Dependencies

To run the assistant, you need to install the following Python libraries:

```bash
pip install speechrecognition pyttsx3 wikipedia requests schedule google-api-python-client google-auth-httplib2 RPi.GPIO

## Setup Instructions

Follow these steps to set up and run the Voice Assistant:

1. **Clone the Repository**:  
   First, clone the repository to your local machine.

   ```bash
   git clone https://github.com/yourusername/voice-assistant.git
   cd voice-assistant
Install Dependencies:
Install the required Python libraries using pip. Ensure you have Python 3.6+ installed.

bash
Copy
pip install -r requirements.txt
API Keys and Authentication:

Weather API: Sign up at OpenWeatherMap and get your API Key.

Google Calendar API: Set up the Google Calendar API by following the Quickstart Guide and download the credentials.json file for OAuth2 authentication.

Gmail Setup: If you're using Gmail, you may need to generate an App Password if you have 2FA enabled.

GPIO Setup (For Raspberry Pi only):

Connect your IoT devices (e.g., lights, motors) to the Raspberry Pi's GPIO pins.

Install the RPi.GPIO library if not already installed:

bash
Copy
sudo apt-get install python3-rpi.gpio
Run the Assistant:
After completing the setup, you can start the assistant by running the following command:

bash
Copy
python assistant.py
Give Commands:

Speak into the microphone, and the assistant will respond to your commands.

Examples of commands you can try:

"What is the time?"

"Tell me the weather."

"Set a reminder for meeting at 3 PM."

"Send an email to example@example.com."
