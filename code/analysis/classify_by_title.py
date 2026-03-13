import pandas as pd
import glob
import os

# Load data
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
files = glob.glob(os.path.join(data_dir, 'youtube_mental_health_*.csv'))
latest_file = max(files, key=os.path.getctime)

df = pd.read_csv(latest_file)

print("=" * 70)
print("PRELIMINARY CONTENT CLASSIFICATION (By Title Keywords)")
print("=" * 70)

# Simple keyword-based classification
def classify_content_type(title, description):
    """Rough classification based on title/description keywords"""
    text = (str(title) + ' ' + str(description)).lower()
    
    # Professional indicators
    if any(word in text for word in ['dr.', 'dr ', 'doctor', 'therapist', 'psychologist', 'psychiatrist']):
        if any(word in text for word in ['teen', 'adolescent', 'young', 'child', 'parent']):
            return 'professional_parent_focused'
        return 'professional_general'
    
    # Personal story indicators
    if any(phrase in text for phrase in ['my depression', 'my anxiety', 'my story', 'i struggled', 'my journey', 'i was diagnosed']):
        return 'personal_story'
    
    # Film/documentary indicators
    if any(word in text for word in ['film', 'movie', 'documentary', 'short film']):
        return 'film_entertainment'
    
    # Educational indicators
    if any(phrase in text for phrase in ['what is', 'how to', 'understanding', 'explained', 'signs of', 'symptoms']):
        return 'educational'
    
    # Help-seeking indicators
    if any(word in text for word in ['help', 'relief', 'overcome', 'cope', 'manage']):
        return 'help_seeking'
    
    return 'other'

df['content_type_guess'] = df.apply(lambda row: classify_content_type(row['title'], row['description']), axis=1)

print("\n📊 Content Type Distribution (Preliminary):")
print(df['content_type_guess'].value_counts())

print("\n" + "=" * 70)
print("CONTENT TYPES BY SEARCH TERM")
print("=" * 70)

for term in df['search_term'].unique()[:6]:
    print(f"\n🔍 '{term}':")
    term_df = df[df['search_term'] == term]
    print(term_df['content_type_guess'].value_counts().head())

# Most viewed by type
print("\n" + "=" * 70)
print("AVERAGE VIEWS BY CONTENT TYPE")
print("=" * 70)

type_stats = df.groupby('content_type_guess').agg({
    'view_count': ['mean', 'count'],
    'like_count': 'mean',
    'comment_count': 'mean'
}).round(0)

print(type_stats)