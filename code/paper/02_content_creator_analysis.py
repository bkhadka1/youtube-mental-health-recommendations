"""
Content Analysis and Creator Patterns
Analyzes creator types, resource quality, and sentiment patterns
Author: Bikash
Date: January 31, 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3)
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'serif'

# ===== PATH CONFIGURATION =====
# Get the directory where THIS script is located (code/paper/)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# Get project root (two levels up from code/paper/)
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# Input data path
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'youtube_manual_coding_enhanced.csv')

# Output directories
FIGURES_DIR = os.path.join(PROJECT_ROOT, 'figures')  # For PNG files
PAPER_DIR = os.path.join(PROJECT_ROOT, 'paper')      # For MD/CSV files

# Create output directories if they don't exist
os.makedirs(FIGURES_DIR, exist_ok=True)
os.makedirs(PAPER_DIR, exist_ok=True)

print("="*70)
print("CONTENT ANALYSIS AND CREATOR PATTERNS")
print("="*70)
print(f"📊 Figures directory: {FIGURES_DIR}")
print(f"📄 Paper directory: {PAPER_DIR}")

df = pd.read_csv(DATA_PATH)
print(f"\n✅ Loaded {len(df)} videos")

# ============================================================================
# FIGURE 5: CREATOR TYPE EVOLUTION ACROSS JOURNEY PROGRESSION
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 5: Creator Type Evolution")
print("="*70)

# Focus on Journey 1 (90 videos - enough for temporal analysis)
j1 = df[df['journey_number'] == 1].sort_values('position_in_journey')

# Create position bins
bins = np.arange(0, 91, 10)
j1['position_bin'] = pd.cut(j1['position_in_journey'], 
                            bins=bins,
                            labels=[f"Videos {b+1}-{min(b+10,90)}" for b in bins[:-1]],
                            include_lowest=True)

# Calculate creator type distribution per bin
creator_by_bin = j1.groupby(['position_bin', 'creator_type']).size().unstack(fill_value=0)
creator_pct = creator_by_bin.div(creator_by_bin.sum(axis=1), axis=0) * 100

fig, ax = plt.subplots(figsize=(14, 8))

# Plot stacked area chart
creator_pct.plot(kind='area', stacked=True, ax=ax, alpha=0.8,
                color={'peer_creator': '#e74c3c',
                      'licensed_therapist': '#2ecc71', 
                      'mental_health_org': '#3498db',
                      'educational_channel': '#f39c12',
                      'influencer': '#9b59b6'})

ax.set_xlabel('Video Position in Journey 1', fontsize=12, fontweight='bold')
ax.set_ylabel('Content Distribution (%)', fontsize=12, fontweight='bold')
ax.set_title('Journey 1: Creator Type Evolution Over 90 Videos\n"depression help" query', 
            fontsize=14, fontweight='bold', pad=20)
ax.legend(title='Creator Type', loc='center left', bbox_to_anchor=(1, 0.5), fontsize=10)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, axis='y')

# Add annotation
ax.annotate('Peer-created content dominates\nthroughout the journey',
           xy=(4, 85), xytext=(2, 70),
           arrowprops=dict(arrowstyle='->', color='red', lw=2),
           fontsize=11, color='red', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='red', alpha=0.9))

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig5_creator_evolution.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig5_creator_evolution.png')}")

# ============================================================================
# FIGURE 6: SENTIMENT × RESOURCE QUALITY MATRIX
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 6: Sentiment × Resource Quality")
print("="*70)

fig, axes = plt.subplots(2, 3, figsize=(18, 10))
fig.suptitle('Sentiment and Resource Quality Across Journeys', 
            fontsize=16, fontweight='bold', y=0.98)

journey_info = {
    1: 'depression help',
    2: 'i hate my life',
    3: 'anxiety coping',
    4: 'why am i depressed',
    5: 'random start',
    6: 'teen mental health'
}

for idx, journey_num in enumerate(range(1, 7)):
    row = idx // 3
    col = idx % 3
    ax = axes[row, col]
    
    j_data = df[df['journey_number'] == journey_num]
    
    # Create crosstab
    crosstab = pd.crosstab(j_data['sentiment'], j_data['resource_quality'], normalize='all') * 100
    
    # Plot heatmap
    sns.heatmap(crosstab, annot=True, fmt='.1f', cmap='RdYlGn_r', 
               ax=ax, cbar_kws={'label': '% of Videos'},
               vmin=0, vmax=50, linewidths=1, linecolor='black')
    
    ax.set_title(f"Journey {journey_num}: '{journey_info[journey_num]}'", 
                fontweight='bold', fontsize=11)
    ax.set_xlabel('Resource Quality', fontsize=10)
    ax.set_ylabel('Sentiment', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig6_sentiment_resource_matrix.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig6_sentiment_resource_matrix.png')}")

# ============================================================================
# FIGURE 7: TARGET AUDIENCE ANALYSIS
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 7: Target Audience Distribution")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left: Target audience by journey
audience_by_journey = df.groupby(['journey_number', 'target_audience']).size().unstack(fill_value=0)
audience_pct = audience_by_journey.div(audience_by_journey.sum(axis=1), axis=0) * 100

audience_pct.plot(kind='bar', stacked=True, ax=axes[0],
                 color={'youth_teen': '#e74c3c', 
                       'general_adult': '#3498db',
                       'parent_caregiver': '#2ecc71'},
                 alpha=0.85, edgecolor='black', linewidth=0.5)

axes[0].set_xlabel('Journey Number', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Target Audience Distribution (%)', fontsize=12, fontweight='bold')
axes[0].set_title('Target Audience Across Journeys', fontsize=14, fontweight='bold')
axes[0].set_xticklabels([f"J{i}" for i in range(1, 7)], rotation=0)
axes[0].legend(title='Target Audience', loc='upper right', fontsize=10)
axes[0].set_ylim(0, 100)

# Right: Youth content × Harmful content
youth_data = df[df['target_audience'] == 'youth_teen']
adult_data = df[df['target_audience'] == 'general_adult']

youth_harmful = (youth_data['potentially_harmful'] == 'yes').sum() / len(youth_data) * 100 if len(youth_data) > 0 else 0
adult_harmful = (adult_data['potentially_harmful'] == 'yes').sum() / len(adult_data) * 100 if len(adult_data) > 0 else 0

bars = axes[1].bar(['Youth/Teen Content', 'General Adult Content'], 
                  [youth_harmful, adult_harmful],
                  color=['#e74c3c', '#3498db'], alpha=0.8, edgecolor='black', linewidth=2)

axes[1].set_ylabel('Potentially Harmful Content (%)', fontsize=12, fontweight='bold')
axes[1].set_title('Harmful Content by Target Audience', fontsize=14, fontweight='bold')
axes[1].set_ylim(0, 30)

# Add value labels
for bar in bars:
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 0.5,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=12)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig7_target_audience.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig7_target_audience.png')}")

# ============================================================================
# STATISTICAL SUMMARY TABLE
# ============================================================================
print("\n" + "="*70)
print("CREATING STATISTICAL SUMMARY TABLE")
print("="*70)

summary_data = []

for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    
    summary_data.append({
        'Journey': journey_num,
        'Query': journey_info[journey_num],
        'N': len(j_data),
        'Harmful (%)': f"{(j_data['potentially_harmful'] == 'yes').sum() / len(j_data) * 100:.1f}",
        'Negative (%)': f"{(j_data['sentiment'] == 'negative').sum() / len(j_data) * 100:.1f}",
        'Professional (%)': f"{(j_data['has_professional'] == 'yes').sum() / len(j_data) * 100:.1f}",
        'No Resources (%)': f"{(j_data['resource_quality'] == 'no_resources').sum() / len(j_data) * 100:.1f}",
        'Peer Content (%)': f"{(j_data['creator_type'] == 'peer_creator').sum() / len(j_data) * 100:.1f}",
        'Youth Target (%)': f"{(j_data['target_audience'] == 'youth_teen').sum() / len(j_data) * 100:.1f}"
    })

summary_df = pd.DataFrame(summary_data)

print("\n" + summary_df.to_string(index=False))

# Save as CSV to paper directory
summary_df.to_csv(os.path.join(PAPER_DIR, 'table1_journey_summary.csv'), index=False)
print(f"\n✅ Saved: {os.path.join(PAPER_DIR, 'table1_journey_summary.csv')}")

# ============================================================================
# DETAILED STATISTICS FOR PAPER
# ============================================================================
print("\n" + "="*70)
print("DETAILED FINDINGS FOR PAPER")
print("="*70)

print("\n🔍 CREATOR TYPE ANALYSIS:")
creator_counts = df['creator_type'].value_counts()
print("\nOverall creator distribution:")
for creator, count in creator_counts.items():
    print(f"  {creator}: {count} ({count/len(df)*100:.1f}%)")

print("\n🎯 PROFESSIONAL VS PEER CONTENT BY JOURNEY:")
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    prof_count = (j_data['creator_type'].isin(['licensed_therapist', 'mental_health_org', 'educational_channel'])).sum()
    peer_count = (j_data['creator_type'] == 'peer_creator').sum()
    print(f"\nJourney {journey_num} ('{journey_info[journey_num]}'):")
    print(f"  Professional: {prof_count} ({prof_count/len(j_data)*100:.1f}%)")
    print(f"  Peer: {peer_count} ({peer_count/len(j_data)*100:.1f}%)")
    if peer_count > 0 and prof_count > 0:
        print(f"  Peer:Professional ratio = {peer_count/prof_count:.2f}:1")
    elif peer_count > 0:
        print(f"  ALL PEER CONTENT")
    else:
        print(f"  ALL PROFESSIONAL CONTENT")

print("\n⚠️  RESOURCE QUALITY CRISIS:")
for journey_num in [1, 6]:  # Focus on worst journeys
    j_data = df[df['journey_number'] == journey_num]
    no_resources = (j_data['resource_quality'] == 'no_resources').sum()
    harmful = (j_data['potentially_harmful'] == 'yes').sum()
    
    # Videos that are harmful AND have no resources
    harmful_no_resources = ((j_data['potentially_harmful'] == 'yes') & 
                           (j_data['resource_quality'] == 'no_resources')).sum()
    
    print(f"\nJourney {journey_num} ('{journey_info[journey_num]}'):")
    print(f"  Videos with no resources: {no_resources} ({no_resources/len(j_data)*100:.1f}%)")
    print(f"  Harmful videos: {harmful} ({harmful/len(j_data)*100:.1f}%)")
    print(f"  Harmful AND no resources: {harmful_no_resources} ({harmful_no_resources/len(j_data)*100:.1f}%)")

print("\n📱 YOUTH-TARGETED CONTENT ANALYSIS:")
youth_videos = df[df['target_audience'] == 'youth_teen']
print(f"\nTotal youth-targeted videos: {len(youth_videos)} ({len(youth_videos)/len(df)*100:.1f}% of all videos)")
print(f"Harmful youth content: {(youth_videos['potentially_harmful'] == 'yes').sum()} ({(youth_videos['potentially_harmful'] == 'yes').sum()/len(youth_videos)*100:.1f}%)")
print(f"Youth content with professional: {(youth_videos['has_professional'] == 'yes').sum()} ({(youth_videos['has_professional'] == 'yes').sum()/len(youth_videos)*100:.1f}%)")

print("\n✅ ALL ANALYSES COMPLETE!")