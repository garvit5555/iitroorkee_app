# 🎓 IIT Roorkee AI Assistant

An innovative and intelligent voice-enabled AI assistant designed to help students of IIT Roorkee clarify their doubts and stay informed about institute-related matters. This system provides a humanized natural language voice interface, making information easily accessible and fostering a positive environment where student queries are promptly addressed.

## ✨ Features

-   **📱 Voice-enabled Phone Service**: Students can call a dedicated mobile number to interact with the AI assistant using natural voice commands.
-   **🤖 Advanced AI Responses**: Powered by the Groq LLM (Gemma2-9b-it), the assistant provides accurate, helpful, and human-like responses based on the institute's data.
-   **🎙️ Speech Recognition & Text-to-Speech**: Utilizes advanced speech recognition models for understanding student queries and gTTS for generating natural-sounding voice replies.
-   **💻 Intuitive Web Interface (Streamlit)**: A user-friendly web application for direct text-based interaction and an option to request an outbound call from the AI assistant.
-   **📚 Comprehensive Knowledge Base**: The AI is trained on a sample dataset covering various aspects of IIT Roorkee, ensuring relevant and contextual answers.
-   **🔄 Real-time Query Processing**: Provides instant answers, reducing waiting times for students' doubts to be clarified.
-   **🌐 24/7 Availability**: Always accessible to students, regardless of office hours.
-   **📞 Outbound Call Feature**: Users can request a call from the AI assistant through the Streamlit app, making the service proactive and convenient.

## 🚀 Tech Stack Used

The project is built using a combination of modern technologies to deliver a robust and interactive AI assistant:

-   **Frontend**: Streamlit
-   **Voice Processing**: Twilio (for handling incoming and outgoing calls, TwiML generation)
-   **AI Model**: Groq (specifically the `Gemma2-9b-it` model for efficient and high-quality language understanding and generation)
-   **Speech Recognition**: Google Speech Recognition (integrated via `speech_recognition` library)
-   **Text-to-Speech**: gTTS (Google Text-to-Speech for converting AI responses into natural voice)
-   **Web Framework**: Flask (for handling Twilio webhooks)
-   **Tunneling**: Pyngrok (to expose local Flask server to the internet for Twilio callbacks)
-   **Data Management**: Pandas (for loading and managing the CSV-based knowledge base)
-   **Environment Variables**: Python-decouple (for secure management of API keys and credentials, though currently hardcoded for demonstration as per user request).

## 🛠️ Setup and Run Instructions

Follow these steps to set up and run the IIT Roorkee AI Assistant on your local machine.

### Prerequisites

-   Python 3.8+
-   A Twilio Account with a purchased phone number.
-   A Groq API Key.
-   An ngrok Authtoken (for exposing your local server).

### Steps

1.  **Clone the repository**:
    ```bash
    git clone <repository-url> # Replace with your repository URL
    cd iit-roorkee-ai-assistant
    ```

2.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Update API Keys**:
    Open `app.py` and replace the placeholder credentials with your actual API keys and Twilio phone number:
    ```python
    GROQ_API_KEY = "YOUR_GROQ_API_KEY_HERE"
    TWILIO_ACCOUNT_SID = "YOUR_TWILIO_ACCOUNT_SID_HERE"
    TWILIO_AUTH_TOKEN = "YOUR_TWILIO_AUTH_TOKEN_HERE"
    TWILIO_PHONE_NUMBER = "YOUR_TWILIO_PHONE_NUMBER_HERE"
    ```
    Similarly, update your ngrok authtoken in `ngrok_setup.py`:
    ```python
    ngrok.set_auth_token("YOUR_NGROK_AUTHTOKEN_HERE")
    ```

4.  **Run the Twilio Webhook Handler (Flask App)**:
    Open your first terminal and run the Flask server:
    ```bash
    python twilio_handler.py
    ```

5.  **Start Ngrok Tunnel**:
    Open a second terminal and run the ngrok setup script to get a public URL. This URL is crucial for Twilio to send webhook requests to your local server:
    ```bash
    python ngrok_setup.py
    ```
    You will see a "Ngrok Public URL" in the output. **Copy this URL**, it will look something like `https://xxxx-xx-xx-xx-xx.ngrok-free.app`.

6.  **Configure Twilio Webhook**:
    -   Go to your [Twilio Console](https://console.twilio.com/).
    -   Navigate to "Phone Numbers" -> "Manage" -> "Active numbers".
    -   Click on your purchased Twilio phone number.
    -   Scroll down to the "Voice Configuration" section.
    -   Under "A CALL COMES IN", select "Webhook" for "Configure with".
    -   In the "URL" field, paste your copied ngrok URL and append `/answer` to it (e.g., `https://xxxx-xx-xx-xx-xx.ngrok-free.app/answer`).
    -   Ensure the HTTP method is set to `HTTP POST`.
    -   Save your changes.

7.  **Run the Streamlit Application**:
    Open a third terminal and start the Streamlit web interface:
    ```bash
    python -m streamlit run app.py
    ```

## 📸 Screenshots

### Chat Interface
This interface allows users to type their questions and receive text-based AI responses.

![Chat Interface Screenshot](/Users/garvi/Downloads/mydecision.ai/chat_interface.png)

### Request a Call Feature
Users can enter their phone number to receive an outbound call from the AI assistant. Once connected, they can ask their questions verbally.

![Request a Call Screenshot](/Users/garvi/Downloads/mydecision.ai/request_call.png)

## 📚 Sample Dataset Used

The AI assistant's knowledge base is simulated using a CSV file (`data/iit_roorkee_data.csv`). This dataset contains various questions and answers related to IIT Roorkee. You can expand this dataset to improve the AI's knowledge.

**Example data (`data/iit_roorkee_data.csv` snippet):**

```csv
category,question,answer
academics,What are the admission requirements for BTech at IIT Roorkee?,Admission to BTech programs at IIT Roorkee is through the JEE Advanced examination. Candidates must clear JEE Main first and then qualify in JEE Advanced with a good rank.
academics,What is the academic calendar for the current semester?,The academic calendar includes regular classes from July to November (Autumn) and January to April (Spring). Mid-semester exams are conducted in September and March while end-semester exams are in November and April.
facilities,What facilities are available in the hostels?,IIT Roorkee hostels provide furnished rooms single/double occupancy rooms with 24/7 internet connectivity Wi-Fi mess facilities common room with TV indoor games facilities gym and laundry services.
```

## 🤝 Contributing

Feel free to contribute to this project by:
1.  Adding more data to the knowledge base (`data/iit_roorkee_data.csv`).
2.  Improving the AI response quality.
3.  Adding new features or enhancing existing ones.
4.  Fixing bugs.

## 📄 License

This project is licensed under the MIT License.
