import pandas as pd
import glob
import os
from datetime import datetime

# Find most recent data file
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
files = glob.glob(os.path.join(data_dir, 'youtube_mental_health_*.csv'))

if not files:
    print("❌ No data files found! Run collect_youtube_data.py first.")
    exit()

latest_file = max(files, key=os.path.getctime)

print(f"📂 Loading: {os.path.basename(latest_file)}\n")

# Load data
df = pd.read_csv(latest_file)

print("=" * 70)
print("DATASET OVERVIEW")
print("=" * 70)
print(f"Total videos: {len(df)}")
print(f"Unique channels: {df['channel_name'].nunique()}")
print(f"Date range: {df['published_at'].min()} to {df['published_at'].max()}")

print(f"\n📊 Search terms distribution:")
print(df['search_term'].value_counts())

print(f"\n\n📈 View count statistics:")
print(df['view_count'].describe())

print(f"\n\n🏆 Top 10 most viewed videos:")
top_videos = df.nlargest(10, 'view_count')[['title', 'channel_name', 'view_count']]
for idx, row in top_videos.iterrows():
    print(f"\n{row['title']}")
    print(f"  Channel: {row['channel_name']}")
    print(f"  Views: {row['view_count']:,}")

print(f"\n\n👥 Top 10 channels by video count:")
print(df['channel_name'].value_counts().head(10))

print(f"\n\n💬 Engagement statistics:")
print(f"Total likes: {df['like_count'].sum():,}")
print(f"Total comments: {df['comment_count'].sum():,}")
print(f"Avg likes per video: {df['like_count'].mean():,.0f}")
print(f"Avg comments per video: {df['comment_count'].mean():,.0f}")

# Calculate engagement rate
df['engagement_rate'] = (df['like_count'] + df['comment_count']) / df['view_count'] * 100
print(f"\nAverage engagement rate: {df['engagement_rate'].mean():.2f}%")

print("\n" + "=" * 70)
print(f"✅ Data exploration complete!")
print("=" * 70)