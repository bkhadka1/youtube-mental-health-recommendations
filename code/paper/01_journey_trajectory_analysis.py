"""
Journey Trajectory Analysis
Analyzes how YouTube's algorithm shapes content exposure across different starting queries
Author: Bikash
Date: January 31, 2026
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import os

# Set style for publication-quality figures
sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.4)
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
print("YOUTUBE ALGORITHM JOURNEY ANALYSIS")
print("="*70)
print(f"📊 Figures directory: {FIGURES_DIR}")
print(f"📄 Paper directory: {PAPER_DIR}")

# Load data
df = pd.read_csv(DATA_PATH)
print(f"\n✅ Loaded {len(df)} videos across {df['journey_number'].nunique()} journeys")

# Journey metadata
journey_info = {
    1: {'query': 'depression help', 'framing': 'positive', 'type': 'help-seeking'},
    2: {'query': 'i hate my life', 'framing': 'negative', 'type': 'distress'},
    3: {'query': 'anxiety coping strategies', 'framing': 'positive', 'type': 'skill-seeking'},
    4: {'query': 'why am i depressed', 'framing': 'neutral', 'type': 'understanding'},
    5: {'query': 'random start', 'framing': 'neutral', 'type': 'random'},
    6: {'query': 'teen mental health', 'framing': 'neutral', 'type': 'teen-specific'}
}

# Color palette
journey_colors = {
    1: '#e74c3c',  # Red - most concerning
    2: '#9b59b6',  # Purple
    3: '#3498db',  # Blue - most helpful
    4: '#2ecc71',  # Green
    5: '#f39c12',  # Orange
    6: '#1abc9c'   # Teal
}

print("\n" + "="*70)
print("JOURNEY SUMMARY STATISTICS")
print("="*70)

for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    print(f"\nJourney {journey_num}: '{journey_info[journey_num]['query']}'")
    print(f"  Total videos: {len(j_data)}")
    print(f"  Harmful content: {(j_data['potentially_harmful'] == 'yes').sum()} ({(j_data['potentially_harmful'] == 'yes').sum()/len(j_data)*100:.1f}%)")
    print(f"  Negative sentiment: {(j_data['sentiment'] == 'negative').sum()} ({(j_data['sentiment'] == 'negative').sum()/len(j_data)*100:.1f}%)")
    print(f"  Professional content: {(j_data['has_professional'] == 'yes').sum()} ({(j_data['has_professional'] == 'yes').sum()/len(j_data)*100:.1f}%)")
    print(f"  No resources: {(j_data['resource_quality'] == 'no_resources').sum()} ({(j_data['resource_quality'] == 'no_resources').sum()/len(j_data)*100:.1f}%)")

# ============================================================================
# FIGURE 1: HARMFUL CONTENT TRAJECTORY BY JOURNEY
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 1: Harmful Content Trajectories")
print("="*70)

fig, ax = plt.subplots(figsize=(14, 8))

for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num].sort_values('position_in_journey')
    
    # Create bins for smoothing (every 5 videos)
    max_pos = j_data['position_in_journey'].max()
    if max_pos >= 10:
        bin_size = 5
        bins = np.arange(0, max_pos + bin_size, bin_size)
        j_data['position_bin'] = pd.cut(j_data['position_in_journey'], 
                                        bins=bins, 
                                        labels=bins[:-1] + bin_size/2, 
                                        include_lowest=True)
        
        # Calculate harmful % per bin
        harmful_by_position = j_data.groupby('position_bin', observed=True).apply(
            lambda x: (x['potentially_harmful'] == 'yes').sum() / len(x) * 100,
            include_groups=False
        )
        
        ax.plot(harmful_by_position.index.astype(float), 
               harmful_by_position.values,
               marker='o', 
               linewidth=3, 
               markersize=8,
               label=f"J{journey_num}: {journey_info[journey_num]['query']}", 
               color=journey_colors[journey_num])

ax.set_xlabel('Video Position in Journey', fontsize=14, fontweight='bold')
ax.set_ylabel('Potentially Harmful Content (%)', fontsize=14, fontweight='bold')
ax.set_title('Algorithmic Divergence: Harmful Content Trajectories by Starting Query', 
            fontsize=16, fontweight='bold', pad=20)
ax.legend(loc='best', fontsize=10, framealpha=0.9)
ax.grid(True, alpha=0.3)
ax.set_ylim(-5, 50)

# Add annotation for Journey 1
ax.annotate('Journey 1: "depression help"\nShows highest harmful content',
           xy=(40, 30), xytext=(60, 40),
           arrowprops=dict(arrowstyle='->', color='red', lw=2),
           fontsize=11, color='red', fontweight='bold',
           bbox=dict(boxstyle='round,pad=0.5', facecolor='white', edgecolor='red', alpha=0.8))

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig1_harmful_trajectories.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig1_harmful_trajectories.png')}")

# ============================================================================
# FIGURE 2: DUAL-AXIS FRAMEWORK VALIDATION
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 2: Dual-Axis Framework")
print("="*70)

fig, axes = plt.subplots(1, 2, figsize=(16, 6))

# Left panel: Harmful content by journey
harmful_by_journey = df.groupby('journey_number').apply(
    lambda x: (x['potentially_harmful'] == 'yes').sum() / len(x) * 100,
    include_groups=False
)

bars = axes[0].bar(range(1, 7), harmful_by_journey.values,
                   color=[journey_colors[i] for i in range(1, 7)],
                   alpha=0.8, edgecolor='black', linewidth=1.5)
axes[0].set_xlabel('Journey Number', fontsize=12, fontweight='bold')
axes[0].set_ylabel('Potentially Harmful Content (%)', fontsize=12, fontweight='bold')
axes[0].set_title('Harmful Content by Journey', fontsize=14, fontweight='bold')
axes[0].set_xticks(range(1, 7))
axes[0].set_xticklabels([f"J{i}\n{journey_info[i]['query'][:15]}..." for i in range(1, 7)], 
                        fontsize=9, rotation=45, ha='right')

# Add value labels
for i, bar in enumerate(bars):
    height = bar.get_height()
    axes[0].text(bar.get_x() + bar.get_width()/2., height + 1,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=10)

# Right panel: Professional content by journey
prof_by_journey = df.groupby('journey_number').apply(
    lambda x: (x['has_professional'] == 'yes').sum() / len(x) * 100,
    include_groups=False
)

bars2 = axes[1].bar(range(1, 7), prof_by_journey.values,
                    color=[journey_colors[i] for i in range(1, 7)],
                    alpha=0.8, edgecolor='black', linewidth=1.5)
axes[1].set_xlabel('Journey Number', fontsize=12, fontweight='bold')
axes[1].set_ylabel('Professional Content (%)', fontsize=12, fontweight='bold')
axes[1].set_title('Professional Content Distribution', fontsize=14, fontweight='bold')
axes[1].set_xticks(range(1, 7))
axes[1].set_xticklabels([f"J{i}\n{journey_info[i]['query'][:15]}..." for i in range(1, 7)], 
                        fontsize=9, rotation=45, ha='right')

# Add value labels
for i, bar in enumerate(bars2):
    height = bar.get_height()
    axes[1].text(bar.get_x() + bar.get_width()/2., height + 2,
                f'{height:.1f}%', ha='center', va='bottom', 
                fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig2_dual_axis_framework.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig2_dual_axis_framework.png')}")

# ============================================================================
# FIGURE 3: CONTENT TYPE DISTRIBUTION ACROSS JOURNEYS
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 3: Content Type Distribution")
print("="*70)

fig, ax = plt.subplots(figsize=(14, 8))

# Calculate content type percentages by journey
content_by_journey = df.groupby(['journey_number', 'content_type']).size().unstack(fill_value=0)
content_pct = content_by_journey.div(content_by_journey.sum(axis=1), axis=0) * 100

# Reorder columns for better visualization
column_order = ['professional_advice', 'educational', 'peer_support', 'harmful', 'commercial']
content_pct = content_pct[[col for col in column_order if col in content_pct.columns]]

# Create stacked bar chart
content_pct.plot(kind='bar', stacked=True, ax=ax, 
                color=['#2ecc71', '#3498db', '#f39c12', '#e74c3c', '#95a5a6'],
                alpha=0.85, width=0.7, edgecolor='black', linewidth=0.5)

ax.set_xlabel('Journey Number', fontsize=12, fontweight='bold')
ax.set_ylabel('Content Distribution (%)', fontsize=12, fontweight='bold')
ax.set_title('Content Type Distribution Across Algorithmic Journeys', 
            fontsize=14, fontweight='bold', pad=20)
ax.set_xticklabels([f"Journey {i}\n'{journey_info[i]['query']}'" for i in range(1, 7)], 
                   rotation=45, ha='right', fontsize=10)
ax.legend(title='Content Type', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize=10)
ax.set_ylim(0, 100)
ax.grid(True, alpha=0.3, axis='y')

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig3_content_distribution.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig3_content_distribution.png')}")

# ============================================================================
# FIGURE 4: JOURNEY 1 DEEP DIVE (90 videos)
# ============================================================================
print("\n" + "="*70)
print("CREATING FIGURE 4: Journey 1 Deep Dive")
print("="*70)

j1_data = df[df['journey_number'] == 1].sort_values('position_in_journey')

fig, ax = plt.subplots(figsize=(16, 8))

# Create 10-video bins
bins = np.arange(0, 91, 10)
j1_data['bin'] = pd.cut(j1_data['position_in_journey'], 
                        bins=bins, 
                        labels=[f"{b+1}-{min(b+10, 90)}" for b in bins[:-1]], 
                        include_lowest=True)

# Calculate metrics per bin
harmful_per_bin = j1_data.groupby('bin', observed=True).apply(
    lambda x: (x['potentially_harmful'] == 'yes').sum() / len(x) * 100,
    include_groups=False
)
negative_per_bin = j1_data.groupby('bin', observed=True).apply(
    lambda x: (x['sentiment'] == 'negative').sum() / len(x) * 100,
    include_groups=False
)
no_resources_per_bin = j1_data.groupby('bin', observed=True).apply(
    lambda x: (x['resource_quality'] == 'no_resources').sum() / len(x) * 100,
    include_groups=False
)
peer_content_per_bin = j1_data.groupby('bin', observed=True).apply(
    lambda x: (x['creator_type'] == 'peer_creator').sum() / len(x) * 100,
    include_groups=False
)

x_pos = np.arange(len(harmful_per_bin))
width = 0.2

bars1 = ax.bar(x_pos - 1.5*width, harmful_per_bin.values, width, 
              label='Potentially Harmful', color='#e74c3c', alpha=0.9, edgecolor='black')
bars2 = ax.bar(x_pos - 0.5*width, negative_per_bin.values, width, 
              label='Negative Sentiment', color='#9b59b6', alpha=0.9, edgecolor='black')
bars3 = ax.bar(x_pos + 0.5*width, no_resources_per_bin.values, width, 
              label='No Resources', color='#95a5a6', alpha=0.9, edgecolor='black')
bars4 = ax.bar(x_pos + 1.5*width, peer_content_per_bin.values, width, 
              label='Peer-Created', color='#f39c12', alpha=0.9, edgecolor='black')

ax.set_xlabel('Video Position Range in Journey', fontsize=12, fontweight='bold')
ax.set_ylabel('Percentage (%)', fontsize=12, fontweight='bold')
ax.set_title('Journey 1 ("depression help") Escalation: 90-Video Deep Dive', 
            fontsize=16, fontweight='bold', pad=20)
ax.set_xticks(x_pos)
ax.set_xticklabels(harmful_per_bin.index, rotation=45, ha='right')
ax.legend(loc='upper left', fontsize=11, framealpha=0.9)
ax.grid(True, alpha=0.3, axis='y')
ax.set_ylim(0, 100)

# Add trend line for harmful content
z = np.polyfit(x_pos, harmful_per_bin.values, 1)
p = np.poly1d(z)
ax.plot(x_pos, p(x_pos), "r--", linewidth=3, alpha=0.7, 
       label=f'Harmful Trend (slope: {z[0]:.2f}%/10 videos)')
ax.legend(loc='upper left', fontsize=10, framealpha=0.9)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, 'fig4_journey1_deepdive.png'), dpi=300, bbox_inches='tight')
print(f"✅ Saved: {os.path.join(FIGURES_DIR, 'fig4_journey1_deepdive.png')}")

# ============================================================================
# SUMMARY STATISTICS FOR PAPER
# ============================================================================
print("\n" + "="*70)
print("SUMMARY STATISTICS FOR PAPER")
print("="*70)

print("\n📊 OVERALL STATISTICS:")
print(f"Total videos analyzed: {len(df)}")
print(f"Potentially harmful: {(df['potentially_harmful'] == 'yes').sum()} ({(df['potentially_harmful'] == 'yes').sum()/len(df)*100:.1f}%)")
print(f"Negative sentiment: {(df['sentiment'] == 'negative').sum()} ({(df['sentiment'] == 'negative').sum()/len(df)*100:.1f}%)")
print(f"Professional content: {(df['has_professional'] == 'yes').sum()} ({(df['has_professional'] == 'yes').sum()/len(df)*100:.1f}%)")
print(f"No resources provided: {(df['resource_quality'] == 'no_resources').sum()} ({(df['resource_quality'] == 'no_resources').sum()/len(df)*100:.1f}%)")

print("\n🎯 KEY COMPARISONS:")
print(f"\nJourney 1 vs Journey 3:")
j1_harmful = (df[df['journey_number'] == 1]['potentially_harmful'] == 'yes').sum() / len(df[df['journey_number'] == 1]) * 100
j3_harmful = (df[df['journey_number'] == 3]['potentially_harmful'] == 'yes').sum() / len(df[df['journey_number'] == 3]) * 100
print(f"  Journey 1 harmful: {j1_harmful:.1f}%")
print(f"  Journey 3 harmful: {j3_harmful:.1f}%")
if j3_harmful > 0:
    print(f"  Journey 1 is {j1_harmful/j3_harmful:.1f}x more harmful")
else:
    print(f"  Journey 1 has harmful content, Journey 3 has NONE")

print("\n✅ ALL FIGURES CREATED SUCCESSFULLY!")
print(f"Figures directory: {FIGURES_DIR}")
print("\nFigures created:")
print("  1. fig1_harmful_trajectories.png")
print("  2. fig2_dual_axis_framework.png")
print("  3. fig3_content_distribution.png")
print("  4. fig4_journey1_deepdive.png")