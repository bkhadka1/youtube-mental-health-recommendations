import pandas as pd
import glob
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
files = glob.glob(os.path.join(data_dir, 'youtube_mental_health_*.csv'))
latest_file = max(files, key=os.path.getctime)

df = pd.read_csv(latest_file)

print("=" * 70)
print("IDENTIFYING THE 'ESTABLISHED ECOSYSTEM'")
print("=" * 70)

# Channels appearing in multiple search terms
channel_search_diversity = df.groupby('channel_name')['search_term'].nunique()
channel_counts = df['channel_name'].value_counts()

# Combine metrics
ecosystem_df = pd.DataFrame({
    'video_count': channel_counts,
    'search_diversity': channel_search_diversity,
    'avg_views': df.groupby('channel_name')['view_count'].mean().round(0),
    'total_views': df.groupby('channel_name')['view_count'].sum().round(0),
    'avg_likes': df.groupby('channel_name')['like_count'].mean().round(0),
})

# Sort by video count
ecosystem_df = ecosystem_df.sort_values('video_count', ascending=False)

print("\n🎯 TOP 20 CHANNELS (by video count in dataset)")
print("=" * 70)
print(f"{'Channel':<30} {'Videos':<8} {'Search Terms':<15} {'Avg Views':<12} {'Total Views':<15}")
print("-" * 70)

for idx, (channel, row) in enumerate(ecosystem_df.head(20).iterrows(), 1):
    print(f"{channel:<30} {int(row['video_count']):<8} {int(row['search_diversity']):<15} "
          f"{int(row['avg_views']):<12,} {int(row['total_views']):<15,}")

# Define "established" as appearing in multiple search terms with multiple videos
# Criteria: 10+ videos AND 5+ different search terms
established = ecosystem_df[
    (ecosystem_df['video_count'] >= 10) & 
    (ecosystem_df['search_diversity'] >= 5)
]

print("\n" + "=" * 70)
print("'ESTABLISHED ECOSYSTEM' DEFINITION:")
print("Criteria: 10+ videos AND appears in 5+ different search terms")
print("=" * 70)

print(f"\n✅ Channels meeting criteria: {len(established)}")
print("\nThe 'Established Ecosystem' Members:")
print("-" * 70)

for idx, (channel, row) in enumerate(established.iterrows(), 1):
    print(f"{idx:2d}. {channel:<30} ({int(row['video_count'])} videos across {int(row['search_diversity'])} terms)")

# Identify professional channels (manual list based on known credentials)
professional_channels = [
    'Therapy in a Nutshell',
    'Dr. Tracey Marks',
    'Dr Julie',
    'The Grateful Therapist',
    'Andrew Huberman',
    'HealthyGamerGG',
    'Dr. Ramani Durvasula',
    'Psych Hub',
    'MedCircle'
]

# Check which professional channels are in established ecosystem
established_professionals = [ch for ch in professional_channels if ch in established.index]

print("\n" + "=" * 70)
print("PROFESSIONAL CHANNELS IN ESTABLISHED ECOSYSTEM:")
print("=" * 70)

for channel in established_professionals:
    if channel in established.index:
        count = int(established.loc[channel, 'video_count'])
        diversity = int(established.loc[channel, 'search_diversity'])
        print(f"✓ {channel:<30} ({count} videos, {diversity} search terms)")

# Save established ecosystem list
established_channels = established.index.tolist()

output_data = {
    'established_ecosystem': established_channels,
    'criteria': {
        'min_videos': 10,
        'min_search_diversity': 5
    },
    'total_channels': len(established_channels),
    'professional_channels_included': established_professionals,
    'stats': {
        'total_videos_from_established': int(df[df['channel_name'].isin(established_channels)].shape[0]),
        'percentage_of_dataset': round(df[df['channel_name'].isin(established_channels)].shape[0] / len(df) * 100, 1)
    }
}

output_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'analysis',
    'established_ecosystem.json'
)
os.makedirs(os.path.dirname(output_file), exist_ok=True)

with open(output_file, 'w') as f:
    json.dump(output_data, f, indent=2)

print(f"\n💾 Saved to: {output_file}")

# Visualization
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# Plot 1: Top 15 channels by video count
top_15 = ecosystem_df.head(15)
axes[0].barh(range(len(top_15)), top_15['video_count'], color='steelblue')
axes[0].set_yticks(range(len(top_15)))
axes[0].set_yticklabels(top_15.index)
axes[0].set_xlabel('Number of Videos')
axes[0].set_title('Top 15 Channels by Video Count', fontsize=14, fontweight='bold')
axes[0].invert_yaxis()

# Plot 2: Established ecosystem - video count vs search diversity
axes[1].scatter(established['search_diversity'], established['video_count'], 
                s=100, alpha=0.6, color='coral')
for channel in established.index[:10]:  # Label top 10
    axes[1].annotate(channel, 
                     (established.loc[channel, 'search_diversity'], 
                      established.loc[channel, 'video_count']),
                     fontsize=8, alpha=0.7)
axes[1].set_xlabel('Search Term Diversity (# of different searches)')
axes[1].set_ylabel('Video Count')
axes[1].set_title('Established Ecosystem: Diversity vs. Volume', fontsize=14, fontweight='bold')
axes[1].grid(True, alpha=0.3)

plt.tight_layout()

fig_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analysis', 'figures')
os.makedirs(fig_path, exist_ok=True)
plt.savefig(os.path.join(fig_path, 'established_ecosystem.png'), dpi=300, bbox_inches='tight')
print(f"📈 Visualization saved to: {fig_path}/established_ecosystem.png")

plt.show()

print("\n" + "=" * 70)
print("✅ Established ecosystem identified and saved!")
print("=" * 70)

# Print key finding
pct = output_data['stats']['percentage_of_dataset']
print(f"\n🔑 KEY FINDING: {len(established_channels)} established channels account for {pct}% of all collected videos")