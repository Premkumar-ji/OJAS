import pywhatkit as pyw
import speech_recognition as sr
from datetime import datetime, timedelta
from database import create_database, get_phone_number


def listen_input(prompt):
    """
    Captures voice input and converts it into text.
    """
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print(prompt)
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            print("Listening...")
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language='en-IN')
            print(f"You said: {text}")
            return text
        except sr.UnknownValueError:
            print("Sorry, I could not understand. Please try again.")
            return listen_input(prompt)
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None


def send_whatsapp_message():
    """
    Sends a WhatsApp message using the fetched phone number.
    """
    try:
        recipient_name = listen_input("Say the recipient's name:")
        message_content = listen_input("Say the message you want to send:")

        # Fetch the phone number from the database
        if recipient_name:
            phone_number = get_phone_number(recipient_name)
            if phone_number:
                # Schedule the message 2 minutes from now
                now = datetime.now()
                send_time = now + timedelta(minutes=2)

                # Send the message using pywhatkit
                pyw.sendwhatmsg(phone_number, message_content, send_time.hour, send_time.minute, 10)
                print(f"Message to {recipient_name} scheduled successfully!")
            else:
                print("Recipient name not found in the database.")
        else:
            print("No name was recognized. Exiting.")
    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # Ensure the database is created before running the script
    create_database()
    send_whatsapp_message()
