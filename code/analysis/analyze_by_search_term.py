import pandas as pd
import glob
import os
import matplotlib.pyplot as plt
import seaborn as sns

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 8)

# Load data
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
files = glob.glob(os.path.join(data_dir, 'youtube_mental_health_*.csv'))
latest_file = max(files, key=os.path.getctime)

print(f"Loading: {os.path.basename(latest_file)}")
df = pd.read_csv(latest_file)

print("\n" + "=" * 70)
print("SEARCH TERM ANALYSIS")
print("=" * 70)

# Videos per search term
print("\n📊 Videos Collected Per Search Term:")
term_counts = df['search_term'].value_counts()
print(term_counts)

# Summary stats by search term
print("\n" + "=" * 70)
print("ENGAGEMENT METRICS BY SEARCH TERM")
print("=" * 70)

engagement_stats = df.groupby('search_term').agg({
    'view_count': ['mean', 'median', 'sum'],
    'like_count': ['mean', 'median'],
    'comment_count': ['mean', 'median'],
    'video_id': 'count'
}).round(0)

engagement_stats.columns = ['_'.join(col) for col in engagement_stats.columns]
print(engagement_stats)

# Calculate engagement rate by search term
df['engagement_rate'] = ((df['like_count'] + df['comment_count']) / df['view_count'] * 100).fillna(0)

print("\n" + "=" * 70)
print("AVERAGE ENGAGEMENT RATE BY SEARCH TERM")
print("=" * 70)

for term in df['search_term'].unique():
    term_df = df[df['search_term'] == term]
    avg_engagement = term_df['engagement_rate'].mean()
    print(f"{term:30s}: {avg_engagement:.2f}%")

# Top channels by search term
print("\n" + "=" * 70)
print("TOP 3 CHANNELS BY SEARCH TERM")
print("=" * 70)

for term in sorted(df['search_term'].unique()):
    print(f"\n🔍 '{term}':")
    term_df = df[df['search_term'] == term]
    top_channels = term_df['channel_name'].value_counts().head(3)
    for channel, count in top_channels.items():
        print(f"   {count:2d} videos - {channel}")

# Create visualization
fig, axes = plt.subplots(2, 2, figsize=(15, 10))

# Plot 1: Videos per search term
term_counts.plot(kind='barh', ax=axes[0, 0], color='steelblue')
axes[0, 0].set_title('Videos Collected Per Search Term', fontsize=14, fontweight='bold')
axes[0, 0].set_xlabel('Number of Videos')
axes[0, 0].set_ylabel('Search Term')

# Plot 2: Average views by search term
avg_views = df.groupby('search_term')['view_count'].mean().sort_values()
avg_views.plot(kind='barh', ax=axes[0, 1], color='coral')
axes[0, 1].set_title('Average Views Per Video by Search Term', fontsize=14, fontweight='bold')
axes[0, 1].set_xlabel('Average Views')
axes[0, 1].set_ylabel('Search Term')

# Plot 3: Engagement rate by search term
avg_engagement = df.groupby('search_term')['engagement_rate'].mean().sort_values()
avg_engagement.plot(kind='barh', ax=axes[1, 0], color='lightgreen')
axes[1, 0].set_title('Average Engagement Rate by Search Term', fontsize=14, fontweight='bold')
axes[1, 0].set_xlabel('Engagement Rate (%)')
axes[1, 0].set_ylabel('Search Term')

# Plot 4: Channel diversity by search term
channel_diversity = df.groupby('search_term')['channel_name'].nunique().sort_values()
channel_diversity.plot(kind='barh', ax=axes[1, 1], color='mediumpurple')
axes[1, 1].set_title('Channel Diversity by Search Term', fontsize=14, fontweight='bold')
axes[1, 1].set_xlabel('Number of Unique Channels')
axes[1, 1].set_ylabel('Search Term')

plt.tight_layout()

# Save figure
fig_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analysis', 'figures')
os.makedirs(fig_path, exist_ok=True)
plt.savefig(os.path.join(fig_path, 'search_term_analysis.png'), dpi=300, bbox_inches='tight')
print(f"\n📈 Visualization saved to: {fig_path}/search_term_analysis.png")

plt.show()

print("\n" + "=" * 70)
print("✅ Search term analysis complete!")
print("=" * 70)