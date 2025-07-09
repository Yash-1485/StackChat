# authentication/stream.py

from stream_chat import StreamChat
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ.get("STREAM_API_KEY")
api_secret = os.environ.get("STREAM_SECRET_KEY")

if not api_key or not api_secret:
    raise Exception("Stream API key or secret missing")

stream_client = StreamChat(api_key=api_key, api_secret=api_secret)

def upsert_stream_user(user_data):
    try:
        stream_client.upsert_users([user_data])
        return user_data
    except Exception as e:
        print("Stream upsert error:", str(e))

def generate_stream_token(user_id):
    try:
        # print(user_id)
        return stream_client.create_token(str(user_id))
    except Exception as e:
        print("Stream token generation error:", str(e))
