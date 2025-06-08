from flask import Flask, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import pandas as pd
from groq import Groq
from gtts import gTTS
import os
import logging
from app import get_ai_response, GROQ_API_KEY

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)

groq_client = Groq(api_key=GROQ_API_KEY)

@app.route("/", methods=['GET'])
def health_check():
    return "Server is running!"

@app.route("/answer", methods=['POST'])
def answer_call():
    try:
        logger.info("Received incoming call")
        resp = VoiceResponse()
        
        gather = Gather(input='speech', action='/process_speech', method='POST', language='en-IN', 
                       speech_timeout='auto', enhanced='true')
        gather.say("Hello! I'm the IIT Roorkee AI Assistant. How can I help you today?")
        resp.append(gather)
        
        resp.redirect('/answer')
        
        logger.info("Successfully created response for incoming call")
        return str(resp)
    except Exception as e:
        logger.error(f"Error in answer_call: {str(e)}")
        resp = VoiceResponse()
        resp.say("Sorry, there was an error processing your call. Please try again later.")
        return str(resp)

@app.route("/process_speech", methods=['POST'])
def process_speech():
    try:
        logger.info("Processing speech")
        logger.debug(f"Request values: {request.values}")
        
        resp = VoiceResponse()
        
        user_speech = request.values.get('SpeechResult', '')
        predefined_question = request.values.get('question', '')
        
        logger.info(f"Speech input: {user_speech}")
        logger.info(f"Predefined question: {predefined_question}")
        
        query = predefined_question if not user_speech else user_speech
        
        if not query:
            logger.warning("No query detected")
            resp.say("I couldn't hear you. Could you please repeat your question?")
            resp.redirect('/answer')
            return str(resp)
        
        data = pd.read_csv('data/iit_roorkee_data.csv')
        
        logger.info(f"Getting AI response for query: {query}")
        ai_response = get_ai_response(query, data)
        logger.info(f"AI response received: {ai_response}")
        
        resp.say(ai_response)
        
        gather = Gather(input='speech', action='/process_speech', method='POST')
        gather.say("Do you have another question? Just ask, or hang up if you're done.")
        resp.append(gather)
        
        logger.info("Successfully processed speech and created response")
        return str(resp)
    except Exception as e:
        logger.error(f"Error in process_speech: {str(e)}")
        resp = VoiceResponse()
        resp.say("Sorry, there was an error processing your request. Please try again later.")
        return str(resp)

if __name__ == "__main__":
    if not os.path.exists('data'):
        os.makedirs('data')
        logger.warning("Created data directory as it was missing")
    
    if not os.path.exists('data/iit_roorkee_data.csv'):
        logger.error("Dataset file is missing!")
    
    logger.info("Starting Flask server...")
    app.run(debug=True, port=5000) 