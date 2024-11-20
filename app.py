import streamlit as st
import requests

# Set your ElevenLabs API key
ELEVENLABS_API_KEY = " "  # Replace with your ElevenLabs API key

# ElevenLabs API URLs
ELEVENLABS_VOICES_URL = "https://api.elevenlabs.io/v1/voices"
ELEVENLABS_TTS_URL_TEMPLATE = "https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"

# Fetch available voices
@st.cache_data
def fetch_voices():
    headers = {"xi-api-key": ELEVENLABS_API_KEY}
    response = requests.get(ELEVENLABS_VOICES_URL, headers=headers)
    if response.status_code == 200:
        voices = response.json().get("voices", [])
        return {voice["name"]: voice["voice_id"] for voice in voices}
    else:
        st.error(f"Error fetching voices: {response.status_code} - {response.text}")
        return {}

# Fetch voices and display options
voices = fetch_voices()
voice_names = list(voices.keys())

st.title("Text-to-Speech with ElevenLabs")

# Input text box
text_input = st.text_area("Enter text to convert to speech:", height=200)

# Voice selection
if voice_names:
    selected_voice = st.selectbox("Select a voice:", voice_names)

# Button to generate audio
if st.button("Generate Speech"):
    if text_input.strip() and selected_voice:
        try:
            # Get the selected voice ID
            voice_id = voices[selected_voice]
            tts_url = ELEVENLABS_TTS_URL_TEMPLATE.format(voice_id=voice_id)

            # API request to ElevenLabs
            headers = {
                "Accept": "audio/mpeg",
                "xi-api-key": ELEVENLABS_API_KEY,
                "Content-Type": "application/json"
            }
            data = {
                "text": text_input,
                "model_id": "eleven_monolingual_v1"  # Default model
            }
            response = requests.post(tts_url, json=data, headers=headers)

            if response.status_code == 200:
                # Save audio to file
                audio_file = "output_audio.mp3"
                with open(audio_file, "wb") as file:
                    file.write(response.content)

                # Play the audio in Streamlit
                st.audio(audio_file, format="audio/mp3")
                st.success("Speech generated successfully!")
            else:
                st.error(f"Error: {response.status_code} - {response.text}")
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter some text and select a voice.")
