from pyngrok import ngrok, conf
import time
import sys

try:
    ngrok.set_auth_token(your_ngrok_auth_token)
    
    ngrok.kill()

    conf.get_default().region = 'us'
    
    public_url = ngrok.connect(5000, "http")
    print(f"\nNgrok Public URL: {public_url}")
    print("\nNgrok tunnel established successfully!")
    print("Use this URL in your Twilio webhook configuration:")
    print(f"{public_url}/answer")
    print("\nPress Ctrl+C to exit")

    while True:
        time.sleep(1)

except Exception as e:
    print(f"\nAn error occurred: {str(e)}")
    print("\nIf you haven't authenticated ngrok, please:")
    print("1. Visit https://dashboard.ngrok.com/signup to create a free account")
    print("2. Get your authtoken from https://dashboard.ngrok.com/get-started/your-authtoken")
    print("3. Update the ngrok.set_auth_token() line in this script with your token")
    sys.exit(1)

finally:
    try:
        ngrok.kill()
    except:
        pass 