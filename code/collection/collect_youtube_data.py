from googleapiclient.discovery import build
import pandas as pd
import time
from datetime import datetime
import json
import sys
import os

# Import API key
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import YOUTUBE_API_KEY

# Mental health search terms
SEARCH_TERMS = [
    "depression help",
    "anxiety relief",
    "feeling depressed",
    "mental health",
    "therapy for teens",
    "how to be happy",
    "coping with anxiety",
    "teen mental health",
    "depression support",
    "anxiety support",
    "mental wellness",
    "self care mental health"
]

class YouTubeCollector:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
        self.collected_videos = []
        
    def search_videos(self, query, max_results=50):
        """Search for videos based on query"""
        print(f"\n🔍 Searching for: '{query}'")
        
        try:
            request = self.youtube.search().list(
                part="id,snippet",
                q=query,
                type="video",
                maxResults=max_results,
                relevanceLanguage="en",
                order="relevance",
                safeSearch="none"
            )
            response = request.execute()
            
            print(f"   Found {len(response.get('items', []))} videos")
            return response.get('items', [])
            
        except Exception as e:
            print(f"   ❌ Error searching: {e}")
            return []
    
    def get_video_details(self, video_id):
        """Get detailed statistics for a video"""
        try:
            request = self.youtube.videos().list(
                part="snippet,statistics,contentDetails",
                id=video_id
            )
            response = request.execute()
            return response.get('items', [None])[0]
        except Exception as e:
            print(f"   ⚠️  Could not get details for {video_id}: {e}")
            return None
    
    def collect_for_term(self, search_term, max_videos=50):
        """Collect videos for a specific search term"""
        search_results = self.search_videos(search_term, max_videos)
        
        videos_data = []
        
        for idx, item in enumerate(search_results, 1):
            video_id = item['id']['videoId']
            
            # Get detailed info
            details = self.get_video_details(video_id)
            
            if not details:
                continue
            
            # Extract all relevant data
            video_info = {
                'video_id': video_id,
                'title': details['snippet']['title'],
                'description': details['snippet']['description'],
                'channel_name': details['snippet']['channelTitle'],
                'channel_id': details['snippet']['channelId'],
                'published_at': details['snippet']['publishedAt'],
                'thumbnail_url': details['snippet']['thumbnails']['high']['url'],
                'tags': ', '.join(details['snippet'].get('tags', [])),
                'category_id': details['snippet'].get('categoryId', ''),
                'duration': details['contentDetails']['duration'],
                'view_count': int(details['statistics'].get('viewCount', 0)),
                'like_count': int(details['statistics'].get('likeCount', 0)),
                'comment_count': int(details['statistics'].get('commentCount', 0)),
                'search_term': search_term,
                'collection_date': datetime.now().isoformat(),
                'video_url': f"https://www.youtube.com/watch?v={video_id}"
            }
            
            videos_data.append(video_info)
            
            # Progress update every 10 videos
            if idx % 10 == 0:
                print(f"   Processed {idx}/{len(search_results)} videos")
            
            # Rate limiting
            time.sleep(0.3)
        
        print(f"   ✅ Collected {len(videos_data)} videos for '{search_term}'")
        return videos_data
    
    def collect_all(self, search_terms, videos_per_term=50):
        """Collect videos for all search terms"""
        print("=" * 70)
        print("YouTube Mental Health Content Collection")
        print("=" * 70)
        print(f"Collecting {videos_per_term} videos for each of {len(search_terms)} search terms")
        print(f"Estimated total: {len(search_terms) * videos_per_term} videos")
        print("=" * 70)
        
        all_videos = []
        
        for idx, term in enumerate(search_terms, 1):
            print(f"\n[{idx}/{len(search_terms)}] Processing: {term}")
            
            videos = self.collect_for_term(term, videos_per_term)
            all_videos.extend(videos)
            
            # Pause between searches
            if idx < len(search_terms):
                print("   ⏸️  Pausing 3 seconds before next search...")
                time.sleep(3)
        
        return all_videos
    
    def save_data(self, videos, filename=None):
        """Save collected data to CSV"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"youtube_mental_health_{timestamp}.csv"
        
        df = pd.DataFrame(videos)
        
        output_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'data', 'raw', filename
        )
        
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        df.to_csv(output_path, index=False)
        
        return output_path, df

def main():
    """Main execution function"""
    
    collector = YouTubeCollector(YOUTUBE_API_KEY)
    
    # Start with smaller collection for testing
    print("\n📋 COLLECTION OPTIONS:")
    print("1. Test collection (3 terms, 20 videos each = 60 videos, ~5 mins)")
    print("2. Medium collection (6 terms, 30 videos each = 180 videos, ~15 mins)")
    print("3. Full collection (12 terms, 50 videos each = 600 videos, ~45 mins)")
    
    choice = input("\nEnter your choice (1, 2, or 3): ").strip()
    
    if choice == "1":
        terms = SEARCH_TERMS[:3]
        videos_per_term = 20
    elif choice == "2":
        terms = SEARCH_TERMS[:6]
        videos_per_term = 30
    elif choice == "3":
        terms = SEARCH_TERMS
        videos_per_term = 50
    else:
        print("Invalid choice. Using test collection (option 1).")
        terms = SEARCH_TERMS[:3]
        videos_per_term = 20
    
    print(f"\n✅ Starting collection with {len(terms)} terms, {videos_per_term} videos each")
    input("Press Enter to begin...")
    
    # Collect data
    videos = collector.collect_all(terms, videos_per_term=videos_per_term)
    
    # Save data
    output_path, df = collector.save_data(videos)
    
    # Summary statistics
    print("\n" + "=" * 70)
    print("✅ COLLECTION COMPLETE!")
    print("=" * 70)
    print(f"Total videos collected: {len(videos)}")
    print(f"Saved to: {output_path}")
    print("\n📊 Quick preview:")
    print(df[['title', 'channel_name', 'view_count', 'search_term']].head(10))
    print("\n📈 Videos per search term:")
    print(df.groupby('search_term').size())
    print("=" * 70)
    
    # Save summary
    summary = {
        'collection_date': datetime.now().isoformat(),
        'total_videos': len(videos),
        'search_terms_used': terms,
        'videos_per_term': df.groupby('search_term').size().to_dict(),
        'total_views': int(df['view_count'].sum()),
        'avg_views': int(df['view_count'].mean()),
        'unique_channels': df['channel_name'].nunique(),
        'date_range': {
            'earliest': str(df['published_at'].min()),
            'latest': str(df['published_at'].max())
        }
    }
    
    summary_path = output_path.replace('.csv', '_summary.json')
    with open(summary_path, 'w') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n📄 Summary saved to: {summary_path}")
    print("\n🎉 You now have real research data! Next: manual coding.")

if __name__ == "__main__":
    main()