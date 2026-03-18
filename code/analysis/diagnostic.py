import pandas as pd

df = pd.read_csv('data/raw/youtube_manual_coding_enhanced.csv')

print("JOURNEY MAPPING IN YOUR CSV:")
print("="*60)

for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    if len(j_data) > 0:
        print(f"\nJourney {journey_num}:")
        print(f"  Total videos: {len(j_data)}")
        print(f"  First video title/notes: {j_data.iloc[0].get('title', j_data.iloc[0].get('notes', 'N/A'))[:100]}...")