i need this whole text in markdown format # Voice Assistant Project

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
