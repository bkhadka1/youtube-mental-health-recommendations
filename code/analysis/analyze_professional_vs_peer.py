import pandas as pd
import glob
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Load data
data_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'raw')
files = glob.glob(os.path.join(data_dir, 'youtube_mental_health_*.csv'))
latest_file = max(files, key=os.path.getctime)

df = pd.read_csv(latest_file)

print("=" * 70)
print("PROFESSIONAL vs PEER CONTENT ANALYSIS")
print("=" * 70)

# Load established ecosystem
ecosystem_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'analysis',
    'established_ecosystem.json'
)

with open(ecosystem_file, 'r') as f:
    ecosystem_data = json.load(f)

# Define professional channels (known licensed professionals)
professional_channels = [
    'Therapy in a Nutshell',
    'Dr. Tracey Marks',
    'Dr Julie',
    'The Grateful Therapist',
    'Andrew Huberman',
    'HealthyGamerGG',
    'Dr. Ramani Durvasula',
    'MedCircle',
    'Psych Hub',
    'Doc Snipes'  # From your Journey 5
]

# Add any professional channels from established ecosystem
for channel in ecosystem_data['professional_channels_included']:
    if channel not in professional_channels:
        professional_channels.append(channel)

# Classify videos
df['is_professional'] = df['channel_name'].isin(professional_channels)
df['is_established'] = df['channel_name'].isin(ecosystem_data['established_ecosystem'])

# Calculate engagement rate
df['engagement_rate'] = ((df['like_count'] + df['comment_count']) / df['view_count'] * 100).fillna(0)

# Overall statistics
print(f"\n📊 OVERALL DATASET BREAKDOWN:")
print("=" * 70)

professional = df[df['is_professional'] == True]
peer = df[df['is_professional'] == False]

print(f"Total videos: {len(df)}")
print(f"\nProfessional videos: {len(professional)} ({len(professional)/len(df)*100:.1f}%)")
print(f"Peer/Other videos: {len(peer)} ({len(peer)/len(df)*100:.1f}%)")

print(f"\nEstablished ecosystem videos: {df['is_established'].sum()} ({df['is_established'].sum()/len(df)*100:.1f}%)")

# Engagement comparison
print("\n" + "=" * 70)
print("ENGAGEMENT METRICS COMPARISON")
print("=" * 70)

print(f"\n{'Metric':<25} {'Professional':<20} {'Peer/Other':<20} {'Difference':<15}")
print("-" * 75)

metrics = {
    'Avg Views': ('view_count', 'mean'),
    'Median Views': ('view_count', 'median'),
    'Avg Likes': ('like_count', 'mean'),
    'Avg Comments': ('comment_count', 'mean'),
    'Avg Engagement Rate': ('engagement_rate', 'mean')
}

for metric_name, (col, func) in metrics.items():
    prof_val = getattr(professional[col], func)()
    peer_val = getattr(peer[col], func)()
    
    if 'Rate' in metric_name:
        diff = prof_val - peer_val
        print(f"{metric_name:<25} {prof_val:>18.2f}% {peer_val:>18.2f}% {diff:>+13.2f}%")
    else:
        diff_pct = ((prof_val - peer_val) / peer_val * 100) if peer_val > 0 else 0
        print(f"{metric_name:<25} {prof_val:>18,.0f} {peer_val:>18,.0f} {diff_pct:>+12.1f}%")

# Professional content by search term
print("\n" + "=" * 70)
print("PROFESSIONAL CONTENT PERCENTAGE BY SEARCH TERM")
print("=" * 70)

for term in sorted(df['search_term'].unique()):
    term_df = df[df['search_term'] == term]
    prof_count = term_df['is_professional'].sum()
    prof_pct = (prof_count / len(term_df)) * 100
    print(f"{term:30s}: {prof_count:3d}/{len(term_df):3d} videos ({prof_pct:5.1f}%)")

# Top professional vs peer channels
print("\n" + "=" * 70)
print("TOP PROFESSIONAL CHANNELS")
print("=" * 70)

prof_channels = professional['channel_name'].value_counts().head(10)
for channel, count in prof_channels.items():
    avg_views = professional[professional['channel_name'] == channel]['view_count'].mean()
    print(f"{channel:<30} {count:3d} videos, {avg_views:>12,.0f} avg views")

print("\n" + "=" * 70)
print("TOP PEER/OTHER CHANNELS")
print("=" * 70)

peer_channels = peer['channel_name'].value_counts().head(10)
for channel, count in peer_channels.items():
    avg_views = peer[peer['channel_name'] == channel]['view_count'].mean()
    print(f"{channel:<30} {count:3d} videos, {avg_views:>12,.0f} avg views")

# Visualization
fig = plt.figure(figsize=(16, 10))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.3)

# Plot 1: Professional vs Peer breakdown
ax1 = fig.add_subplot(gs[0, 0])
categories = ['Professional', 'Peer/Other']
counts = [len(professional), len(peer)]
colors = ['#2ecc71', '#3498db']
ax1.pie(counts, labels=categories, autopct='%1.1f%%', colors=colors, startangle=90)
ax1.set_title('Professional vs Peer Content Distribution', fontsize=14, fontweight='bold')

# Plot 2: Views comparison
ax2 = fig.add_subplot(gs[0, 1])
positions = [1, 2]
data_to_plot = [professional['view_count'].dropna(), peer['view_count'].dropna()]
bp = ax2.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True,
                 showmeans=True, meanline=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax2.set_xticklabels(['Professional', 'Peer/Other'])
ax2.set_ylabel('View Count')
ax2.set_title('View Count Distribution', fontsize=14, fontweight='bold')
ax2.set_yscale('log')
ax2.grid(True, alpha=0.3)

# Plot 3: Engagement rate comparison
ax3 = fig.add_subplot(gs[1, 0])
data_to_plot = [professional['engagement_rate'].dropna(), peer['engagement_rate'].dropna()]
bp = ax3.boxplot(data_to_plot, positions=positions, widths=0.6, patch_artist=True,
                 showmeans=True, meanline=True)
for patch, color in zip(bp['boxes'], colors):
    patch.set_facecolor(color)
ax3.set_xticklabels(['Professional', 'Peer/Other'])
ax3.set_ylabel('Engagement Rate (%)')
ax3.set_title('Engagement Rate Distribution', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# Plot 4: Professional content % by search term
ax4 = fig.add_subplot(gs[1, 1])
prof_by_term = []
terms = []
for term in sorted(df['search_term'].unique()):
    term_df = df[df['search_term'] == term]
    prof_pct = (term_df['is_professional'].sum() / len(term_df)) * 100
    prof_by_term.append(prof_pct)
    terms.append(term)

ax4.barh(terms, prof_by_term, color='#2ecc71')
ax4.set_xlabel('Professional Content (%)')
ax4.set_title('Professional Content % by Search Term', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3, axis='x')

# Plot 5: Top professional channels
ax5 = fig.add_subplot(gs[2, :])
top_prof = professional['channel_name'].value_counts().head(10)
ax5.barh(range(len(top_prof)), top_prof.values, color='#2ecc71')
ax5.set_yticks(range(len(top_prof)))
ax5.set_yticklabels(top_prof.index)
ax5.set_xlabel('Number of Videos')
ax5.set_title('Top 10 Professional Channels', fontsize=14, fontweight='bold')
ax5.invert_yaxis()
ax5.grid(True, alpha=0.3, axis='x')

plt.suptitle('Professional vs Peer Content Analysis', fontsize=16, fontweight='bold', y=0.995)

fig_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'analysis', 'figures')
plt.savefig(os.path.join(fig_path, 'professional_vs_peer.png'), dpi=300, bbox_inches='tight')
print(f"\n📈 Visualization saved to: {fig_path}/professional_vs_peer.png")

plt.show()

# Save analysis results
results = {
    'total_videos': len(df),
    'professional_videos': len(professional),
    'peer_videos': len(peer),
    'professional_percentage': round(len(professional) / len(df) * 100, 1),
    'professional_channels_identified': professional_channels,
    'engagement_comparison': {
        'professional_avg_views': int(professional['view_count'].mean()),
        'peer_avg_views': int(peer['view_count'].mean()),
        'professional_engagement_rate': round(professional['engagement_rate'].mean(), 2),
        'peer_engagement_rate': round(peer['engagement_rate'].mean(), 2)
    },
    'by_search_term': {}
}

for term in df['search_term'].unique():
    term_df = df[df['search_term'] == term]
    results['by_search_term'][term] = {
        'total': len(term_df),
        'professional': int(term_df['is_professional'].sum()),
        'professional_pct': round(term_df['is_professional'].sum() / len(term_df) * 100, 1)
    }

output_file = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    'analysis',
    'professional_vs_peer_analysis.json'
)

with open(output_file, 'w') as f:
    json.dump(results, f, indent=2)

print(f"\n💾 Analysis results saved to: {output_file}")

print("\n" + "=" * 70)
print("✅ Professional vs Peer analysis complete!")
print("=" * 70)

# Key findings
print("\n🔑 KEY FINDINGS:")
print(f"  • {results['professional_percentage']}% of videos are from professional channels")
print(f"  • Professional content averages {results['engagement_comparison']['professional_avg_views']:,} views")
print(f"  • Peer content averages {results['engagement_comparison']['peer_avg_views']:,} views")

if results['engagement_comparison']['peer_engagement_rate'] > results['engagement_comparison']['professional_engagement_rate']:
    print(f"  • Peer content has HIGHER engagement rate ({results['engagement_comparison']['peer_engagement_rate']:.2f}% vs {results['engagement_comparison']['professional_engagement_rate']:.2f}%)")
    print(f"  • This may explain why algorithm surfaces peer over professional content")
else:
    print(f"  • Professional content has HIGHER engagement rate ({results['engagement_comparison']['professional_engagement_rate']:.2f}% vs {results['engagement_comparison']['peer_engagement_rate']:.2f}%)")