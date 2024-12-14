import pyttsx3
import speech_recognition as sr
from serpapi import GoogleSearch

# Function to capture speech input
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
            print("Sorry, I could not understand.")
            return None
        except sr.RequestError as e:
            print(f"Could not request results; {e}")
            return None
        except sr.WaitTimeoutError:
            print("No input detected within the timeout period.")
            return None


# Function to speak text
def speak_text(text):
    """
    Converts text into voice output.
    """
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()


# Function to search Google using SerpAPI
def search_google(query):
    """
    Fetches results from Google using the SerpAPI search service.
    """
    try:
        print("Performing Google search...")

        # SerpAPI search parameters
        params = {
            "q": query,
            "api_key": "b1a55f2f2b3457a019b36f66b0c90f604a254f9314cdd64c1813c2711af49c0e",  # Using your provided API key
            "engine": "google",
        }

        # Perform search
        search = GoogleSearch(params)
        results = search.get_dict()

        # Handle search results
        if "organic_results" in results and len(results["organic_results"]) > 0:
            first_result = results["organic_results"][0]
            title = first_result.get("title", "No Title Found")
            snippet = first_result.get("snippet", "No Snippet Found")
            url = first_result.get("link", "No URL Found")

            response_text = f"Title: {title}. Snippet: {snippet}. URL: {url}"
            print(response_text)
            return response_text
        else:
            return "No search results found."
    except Exception as e:
        print(f"Error during search: {e}")
        return "An error occurred while searching Google."


# Main driver function
def main():
    """
    Main driver to listen for speech input, query Google, and return results.
    """
    print("Ask me about any topic or person...")
    user_query = listen_input("What would you like to know?")
    if user_query:
        search_response = search_google(user_query)
        speak_text(search_response)
    else:
        print("No input received. Exiting.")
        speak_text("No input received. Exiting.")


# Run the main program
if __name__ == "__main__":
    main()
