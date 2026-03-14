"""
API Data Audit - Verify all statistics match your claims
Uses the actual API data file: youtube_mental_health_20260125_225956.csv
"""

import pandas as pd
import json
import os

# ===== PATH CONFIGURATION =====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))

# ACTUAL API data path (525 videos, 12 search terms)
API_DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'youtube_mental_health_20260125_225956.csv')
API_SUMMARY_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'youtube_mental_health_20260125_225956_summary.json')

# Analysis results paths
ECOSYSTEM_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'established_ecosystem.json')
PROF_VS_PEER_PATH = os.path.join(PROJECT_ROOT, 'data', 'processed', 'professional_vs_peer_analysis.json')

print("="*80)
print("API DATA AUDIT - VERIFYING ALL STATISTICS")
print("="*80)

# ============================================================================
# LOAD DATA
# ============================================================================

print("\n📁 LOADING DATA...")

# Load API summary
try:
    with open(API_SUMMARY_PATH, 'r') as f:
        summary = json.load(f)
    print(f"✅ Loaded API summary")
    print(f"   Collection date: {summary['collection_date']}")
    print(f"   Total videos: {summary['total_videos']}")
    print(f"   Search terms: {len(summary['search_terms_used'])}")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find {API_SUMMARY_PATH}")
    summary = None

# Load full API data
try:
    df = pd.read_csv(API_DATA_PATH)
    print(f"✅ Loaded full API data: {len(df)} videos")
except FileNotFoundError:
    print(f"❌ ERROR: Could not find {API_DATA_PATH}")
    print("Available files in data/raw/:")
    import glob
    for f in glob.glob(os.path.join(PROJECT_ROOT, 'data', 'raw', '*.csv')):
        print(f"  • {os.path.basename(f)}")
    exit(1)

print("\n📋 COLUMNS IN API DATA:")
print(df.columns.tolist())

# Load analysis results if they exist
try:
    with open(ECOSYSTEM_PATH, 'r') as f:
        ecosystem_data = json.load(f)
    print(f"\n✅ Loaded ecosystem analysis")
except FileNotFoundError:
    print(f"\n⚠️  Ecosystem analysis not found at: {ECOSYSTEM_PATH}")
    print("   Run: python code/analysis/identify_ecosystem.py")
    ecosystem_data = None

try:
    with open(PROF_VS_PEER_PATH, 'r') as f:
        prof_peer_data = json.load(f)
    print(f"✅ Loaded professional vs peer analysis")
except FileNotFoundError:
    print(f"⚠️  Prof vs peer analysis not found at: {PROF_VS_PEER_PATH}")
    print("   Run: python code/analysis/analyze_professional_vs_peer.py")
    prof_peer_data = None

# ============================================================================
# VERIFY SUMMARY STATISTICS
# ============================================================================

print("\n" + "="*80)
print("BASIC DATASET VERIFICATION")
print("="*80)

print(f"\nFrom summary JSON:")
print(f"  Total videos: {summary['total_videos']}")
print(f"  Avg views: {summary['avg_views']:,}")
print(f"  Unique channels: {summary['unique_channels']}")

print(f"\nFrom actual CSV:")
print(f"  Total rows: {len(df)}")
if 'channel_title' in df.columns:
    print(f"  Unique channels: {df['channel_title'].nunique()}")
if 'search_term' in df.columns:
    print(f"  Unique search terms: {df['search_term'].nunique()}")

# Check if they match
if summary['total_videos'] == len(df):
    print(f"\n✅ Video count matches: {len(df)}")
else:
    print(f"\n⚠️  MISMATCH: Summary says {summary['total_videos']}, CSV has {len(df)}")

# ============================================================================
# YOUR PAPER CLAIMS vs ACTUAL DATA
# ============================================================================

print("\n" + "="*80)
print("YOUR PAPER CLAIMS vs ACTUAL DATA")
print("="*80)

CLAIMS = {
    'total_videos': 525,
    'search_terms': 12,
    'avg_views_claim': 1234890,
    'professional_pct': 24.4,
    'professional_engagement': 4.40,
    'peer_engagement': 3.32,
    'engagement_advantage_pct': 32.5,
}

print(f"\n📊 Total Videos:")
print(f"   Claim: {CLAIMS['total_videos']}")
print(f"   Actual: {len(df)}")
if CLAIMS['total_videos'] == len(df):
    print(f"   ✅ MATCH")
else:
    print(f"   ⚠️  MISMATCH (difference: {len(df) - CLAIMS['total_videos']:+d})")

print(f"\n📊 Average Views:")
print(f"   Claim: {CLAIMS['avg_views_claim']:,}")
print(f"   Actual: {summary['avg_views']:,}")
diff = abs(CLAIMS['avg_views_claim'] - summary['avg_views'])
pct_diff = (diff / CLAIMS['avg_views_claim']) * 100
if pct_diff < 5:
    print(f"   ✅ CLOSE (difference: {diff:,}, {pct_diff:.1f}%)")
else:
    print(f"   ⚠️  SIGNIFICANT DIFFERENCE ({pct_diff:.1f}%)")

# ============================================================================
# ENGAGEMENT STATISTICS
# ============================================================================

print("\n" + "="*80)
print("ENGAGEMENT STATISTICS")
print("="*80)

if 'view_count' in df.columns and 'like_count' in df.columns and 'comment_count' in df.columns:
    # Calculate engagement rate
    df['engagement_rate'] = ((df['like_count'] + df['comment_count']) / df['view_count'] * 100)
    df['engagement_rate'] = df['engagement_rate'].replace([float('inf'), -float('inf')], 0)
    
    total_views = df['view_count'].sum()
    total_likes = df['like_count'].sum()
    total_comments = df['comment_count'].sum()
    avg_engagement = df['engagement_rate'].mean()
    
    print(f"\nTotal Views: {total_views:,}")
    print(f"Total Likes: {total_likes:,}")
    print(f"Total Comments: {total_comments:,}")
    print(f"Average Engagement Rate: {avg_engagement:.2f}%")
    
    # Compare to your claim of 3.58%
    YOUR_CLAIM = 3.58
    if abs(avg_engagement - YOUR_CLAIM) < 0.5:
        print(f"✅ Matches your claim ({YOUR_CLAIM}%)")
    else:
        print(f"⚠️  MISMATCH: Claim {YOUR_CLAIM}%, Actual {avg_engagement:.2f}%")
else:
    print("⚠️  Missing engagement columns")

# ============================================================================
# TOP CHANNELS
# ============================================================================

print("\n" + "="*80)
print("TOP CHANNELS VERIFICATION")
print("="*80)

# Check which channel column exists
if 'channel_title' in df.columns:
    channel_col = 'channel_title'
elif 'channel_name' in df.columns:
    channel_col = 'channel_name'
else:
    print("⚠️  No channel column found")
    channel_col = None

if channel_col:
    top_channels = df[channel_col].value_counts().head(15)
    
    print(f"\nActual top 15 channels (from '{channel_col}' column):")
    for i, (channel, count) in enumerate(top_channels.items(), 1):
        print(f"  {i:2d}. {channel}: {count} videos")
    
    # Calculate ecosystem percentage
    top_8 = top_channels.head(8)
    top_8_total = top_8.sum()
    top_8_pct = (top_8_total / len(df)) * 100
    
    print(f"\nTop 8 channels represent:")
    print(f"  {top_8_total} videos ({top_8_pct:.1f}% of dataset)")
    
    YOUR_CLAIM_PCT = 35.4
    if abs(top_8_pct - YOUR_CLAIM_PCT) < 3:
        print(f"  ✅ Close to your claim ({YOUR_CLAIM_PCT}%)")
    else:
        print(f"  ⚠️  Update claim: actual is {top_8_pct:.1f}%, you claimed {YOUR_CLAIM_PCT}%")
    
    # Your specific channel claims
    YOUR_ECOSYSTEM_CLAIMS = {
        'TEDx Talks': 40,
        'Psych2Go': 34,
        'Therapy in a Nutshell': 31,
        'Dr. Tracey Marks': 27,
        'Dr Julie': 24,
        'The Grateful Therapist': 13,
        'motivationaldoc': 12,
        'Mel Robbins': 10,
        'HealthyGamerGG': 10,
        'Andrew Huberman': 10
    }
    
    print("\n" + "="*80)
    print("COMPARING YOUR CLAIMS TO ACTUAL:")
    print("="*80)
    
    mismatches = []
    for channel, claimed in YOUR_ECOSYSTEM_CLAIMS.items():
        actual = (df[channel_col] == channel).sum()
        match = "✅" if actual == claimed else "⚠️ "
        diff_str = "" if actual == claimed else f" (diff: {actual - claimed:+d})"
        print(f"{match} {channel}: Claimed {claimed}, Actual {actual}{diff_str}")
        
        if actual != claimed:
            mismatches.append({'channel': channel, 'claimed': claimed, 'actual': actual})
    
    if mismatches:
        print(f"\n⚠️  Found {len(mismatches)} mismatches - update your documentation!")
    else:
        print(f"\n✅ All channel counts match your claims!")
else:
    mismatches = []

# ============================================================================
# SEARCH TERM ANALYSIS
# ============================================================================

print("\n" + "="*80)
print("SEARCH TERM ANALYSIS")
print("="*80)

if 'search_term' in df.columns:
    print("\nVideos per search term:")
    for term in summary['search_terms_used']:
        count = (df['search_term'] == term).sum()
        claimed = summary['videos_per_term'].get(term, 'N/A')
        match = "✅" if count == claimed else "⚠️ "
        print(f"  {match} {term}: {count} (claimed: {claimed})")

# ============================================================================
# RECOMMENDATIONS
# ============================================================================

print("\n" + "="*80)
print("NEXT STEPS")
print("="*80)

print("\n1. Run your analysis scripts to generate processed data:")
print("   python code/analysis/identify_ecosystem.py")
print("   python code/analysis/analyze_professional_vs_peer.py")
print("   python code/analysis/analyze_by_search_term.py")

print("\n2. Then re-run this audit to verify all statistics")

print("\n3. Update your paper/documentation with actual numbers")

if mismatches:
    print(f"\n4. ⚠️  FIX {len(mismatches)} channel count discrepancies in your documentation")

print("\n" + "="*80)
print("AUDIT COMPLETE")
print("="*80)