from googleapiclient.discovery import build
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import YOUTUBE_API_KEY

def test_youtube_api():
    """Test YouTube API connection"""
    print("=" * 60)
    print("Testing YouTube Data API v3 Connection")
    print("=" * 60)
    
    try:
        # Build YouTube service
        youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)
        print("✅ YouTube service built successfully\n")
        
        # Test search
        print("🔍 Testing search for 'mental health'...")
        request = youtube.search().list(
            part="snippet",
            q="mental health",
            type="video",
            maxResults=5,
            relevanceLanguage="en"
        )
        response = request.execute()
        
        print(f"✅ Search successful! Found {len(response['items'])} videos:\n")
        
        for idx, item in enumerate(response['items'], 1):
            title = item['snippet']['title']
            channel = item['snippet']['channelTitle']
            print(f"{idx}. {title}")
            print(f"   Channel: {channel}\n")
        
        print("=" * 60)
        print("✅ API IS WORKING PERFECTLY!")
        print("=" * 60)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API key is correct in config.py")
        print("2. Make sure YouTube Data API v3 is enabled")
        print("3. Wait a few minutes if you just created the key")

if __name__ == "__main__":
    test_youtube_api()