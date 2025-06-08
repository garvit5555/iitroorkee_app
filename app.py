import streamlit as st
import pandas as pd
from twilio.twiml.voice_response import VoiceResponse, Gather
from twilio.rest import Client
from gtts import gTTS
import speech_recognition as sr
from groq import Groq
import os

GROQ_API_KEY = your_groq_api_key
TWILIO_ACCOUNT_SID = your_Twilio_Account_SID
TWILIO_AUTH_TOKEN = your_Twilio_Auth_token
TWILIO_PHONE_NUMBER = your_Twilio_phone_number

groq_client = Groq(api_key=GROQ_API_KEY)

twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

@st.cache_data
def load_data():
    return pd.read_csv('data/iit_roorkee_data.csv')

def get_ai_response(query, data):
    context = "\n".join([f"Q: {row['question']}\nA: {row['answer']}" for _, row in data.iterrows()])
    
    prompt = f"""You are an AI assistant for IIT Roorkee students. Use the following context to answer the query:

    Context:
    {context}

    Student's Query: {query}

    Please provide a helpful, accurate, and natural response based on the available information."""

    response = groq_client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model="gemma2-9b-it",
        temperature=0.7,
        max_tokens=800
    )
    
    return response.choices[0].message.content

def text_to_speech(text, filename="response.mp3"):
    tts = gTTS(text=text, lang='en')
    tts.save(filename)
    return filename

def handle_incoming_call():
    response = VoiceResponse()
    gather = Gather(input='speech', action='/process_speech', method='POST')
    gather.say("Hello! I'm the IIT Roorkee AI Assistant. How can I help you today?")
    response.append(gather)
    return str(response)

def make_outbound_call(to_number):
    try:
        webhook_url = "https://74ae-2409-40d6-11a-2846-695e-ea85-2c42-b33b.ngrok-free.app/answer"
        
        call = twilio_client.calls.create(
            to=to_number,
            from_=TWILIO_PHONE_NUMBER,
            url=webhook_url,
            method="POST"
        )
        return True, call.sid
    except Exception as e:
        return False, str(e)

def main():
    st.set_page_config(page_title="IIT Roorkee AI Assistant", layout="centered")
    st.title("🎓 IIT Roorkee AI Assistant")
    st.markdown("Welcome to the IIT Roorkee AI Assistant! This system helps students get quick answers to their queries with an innovative voice interface.")

    data = load_data()

    st.sidebar.title("📊 Statistics")
    st.sidebar.markdown("Quick insights into our knowledge base.")
    st.sidebar.metric("Total Knowledge Base Entries", len(data))
    st.sidebar.metric("Categories Covered", len(data['category'].unique()))

    tab1, tab2, tab3 = st.tabs(["💬 Chat Interface", "📱 Request Call", "📚 Knowledge Base"])

    with tab1:
        st.header("Chat with AI Assistant")
        st.markdown("Ask any question about IIT Roorkee and get instant text replies.")
        user_query = st.text_input("Type your question here:", placeholder="e.g., What are the admission requirements for BTech?")
        
        if st.button("Get Answer"):
            if user_query:
                with st.spinner("Getting your answer..."):
                    response = get_ai_response(user_query, data)
                    st.info(response)
            else:
                st.warning("Please type a question to get an answer.")

    with tab2:
        st.header("Request a Call")
        st.markdown("Enter your phone number below. Our AI assistant will call you and answer your questions via voice.")
        
        st.markdown("Enter your phone number in international format (e.g., +91XXXXXXXXXX for India, +1XXXXXXXXXX for USA)")
        phone_number = st.text_input("Your Phone Number:", placeholder="+91XXXXXXXXXX")
        
        if st.button("Request Call"):
            if phone_number:
                with st.spinner("Initiating call..."):
                    success, result = make_outbound_call(phone_number)
                    if success:
                        st.success(f"Call initiated successfully! You will receive a call shortly from {TWILIO_PHONE_NUMBER}")
                        st.write("Once connected, the AI will prompt you to ask your question.")
                    else:
                        st.error(f"Failed to make call: {result}")
            else:
                st.warning("Please enter your phone number to request a call.")

    with tab3:
        st.header("Knowledge Base Overview")
        st.markdown("Explore the data the AI assistant uses to answer your questions.")
        st.dataframe(data, use_container_width=True)

if __name__ == "__main__":
    main() 