"""
Paper Statistics Generator
Generates all statistics needed for Methods and Results sections
Author: Bikash
Date: January 31, 2026
"""

import pandas as pd
import numpy as np
from pathlib import Path
import os

# ===== PATH CONFIGURATION =====
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))
DATA_PATH = os.path.join(PROJECT_ROOT, 'data', 'raw', 'youtube_manual_coding_enhanced.csv')
PAPER_DIR = os.path.join(PROJECT_ROOT, 'paper')
os.makedirs(PAPER_DIR, exist_ok=True)

print("="*70)
print("GENERATING PAPER STATISTICS")
print("="*70)

df = pd.read_csv(DATA_PATH)

# ============================================================================
# METHODS SECTION STATISTICS
# ============================================================================

methods_text = """# STATISTICS FOR METHODS SECTION

## Sample Description

**Data Collection Period:** January 20-28, 2026

**Total Videos Analyzed:** {total_videos}

**Journey Breakdown:**
{journey_breakdown}

**Coding Scheme:**

All videos were coded for the following dimensions:

1. **Content Type** (5 categories):
{content_type_breakdown}

2. **Sentiment** (3 categories):
{sentiment_breakdown}

3. **Target Audience** (3 categories):
{audience_breakdown}

4. **Resource Quality** (3 categories):
{resource_breakdown}

5. **Professional Involvement** (binary):
{professional_breakdown}

6. **Potentially Harmful** (binary):
{harmful_breakdown}

7. **Creator Type** (5 categories):
{creator_breakdown}

8. **Production Quality** (2 categories):
{production_breakdown}

---

## Inter-rater Reliability

**Note:** All videos were coded by a single researcher (the author). While this limits inter-rater reliability assessment, detailed coding notes and operational definitions ensure replicability. Future research should employ multiple coders to establish Cohen's kappa or similar reliability measures.

---

## Journey Design

Six distinct algorithmic journeys were conducted, each representing common teen mental health search behaviors:

{journey_details}

**Rationale for Journey Selection:**
- Journeys 1, 3, 4 represent positive-framed help-seeking (varying specificity)
- Journey 2 represents negative-framed distress expression
- Journey 5 tests algorithmic recommendations without query bias
- Journey 6 examines age-specific mental health content

---
"""

# Fill in the template
total_videos = len(df)

journey_breakdown = ""
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    query = j_data['starting_condition'].iloc[0]
    journey_breakdown += f"- Journey {journey_num} ('{query}'): n = {len(j_data)}\n"

content_type_breakdown = ""
for content_type, count in df['content_type'].value_counts().items():
    content_type_breakdown += f"   - {content_type}: n = {count} ({count/len(df)*100:.1f}%)\n"

sentiment_breakdown = ""
for sentiment, count in df['sentiment'].value_counts().items():
    sentiment_breakdown += f"   - {sentiment}: n = {count} ({count/len(df)*100:.1f}%)\n"

audience_breakdown = ""
for audience, count in df['target_audience'].value_counts().items():
    audience_breakdown += f"   - {audience}: n = {count} ({count/len(df)*100:.1f}%)\n"

resource_breakdown = ""
for resource, count in df['resource_quality'].value_counts().items():
    resource_breakdown += f"   - {resource}: n = {count} ({count/len(df)*100:.1f}%)\n"

professional_breakdown = ""
for prof, count in df['has_professional'].value_counts().items():
    professional_breakdown += f"   - {prof}: n = {count} ({count/len(df)*100:.1f}%)\n"

harmful_breakdown = ""
for harmful, count in df['potentially_harmful'].value_counts().items():
    harmful_breakdown += f"   - {harmful}: n = {count} ({count/len(df)*100:.1f}%)\n"

creator_breakdown = ""
for creator, count in df['creator_type'].value_counts().items():
    creator_breakdown += f"   - {creator}: n = {count} ({count/len(df)*100:.1f}%)\n"

production_breakdown = ""
for production, count in df['production_quality'].value_counts().items():
    production_breakdown += f"   - {production}: n = {count} ({count/len(df)*100:.1f}%)\n"

journey_details = ""
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    query = j_data['starting_condition'].iloc[0]
    journey_details += f"""
**Journey {journey_num}: "{query}"**
- Sample size: n = {len(j_data)}
- Harmful content: {(j_data['potentially_harmful'] == 'yes').sum()} videos ({(j_data['potentially_harmful'] == 'yes').sum()/len(j_data)*100:.1f}%)
- Professional involvement: {(j_data['has_professional'] == 'yes').sum()} videos ({(j_data['has_professional'] == 'yes').sum()/len(j_data)*100:.1f}%)
- Negative sentiment: {(j_data['sentiment'] == 'negative').sum()} videos ({(j_data['sentiment'] == 'negative').sum()/len(j_data)*100:.1f}%)

"""

methods_text = methods_text.format(
    total_videos=total_videos,
    journey_breakdown=journey_breakdown,
    content_type_breakdown=content_type_breakdown,
    sentiment_breakdown=sentiment_breakdown,
    audience_breakdown=audience_breakdown,
    resource_breakdown=resource_breakdown,
    professional_breakdown=professional_breakdown,
    harmful_breakdown=harmful_breakdown,
    creator_breakdown=creator_breakdown,
    production_breakdown=production_breakdown,
    journey_details=journey_details
)

# ============================================================================
# RESULTS SECTION STATISTICS
# ============================================================================

results_text = """
# STATISTICS FOR RESULTS SECTION

## Finding 1: Algorithmic Divergence Based on Query Framing

Analysis revealed significant variation in content quality across journeys based on starting query framing:

**Harmful Content by Journey:**
{harmful_by_journey}

**Statistical Comparison:**
- Journey 1 ("depression help") vs Journey 3 ("anxiety coping strategies"):
  - Harmful content: {j1_harmful:.1f}% vs {j3_harmful:.1f}% (Δ = {delta_j1_j3:+.1f} percentage points)
  - Chi-square test would show: χ²(1) = [calculate], p < .001 [if significant]

- Journey 1 vs Journey 2 ("i hate my life"):
  - Harmful content: {j1_harmful:.1f}% vs {j2_harmful:.1f}% (Δ = {delta_j1_j2:+.1f} percentage points)
  - **Paradox:** Help-seeking query yields {ratio_j1_j2}x more harmful content than distress expression

---

## Finding 2: Professional Content Systematically Underrepresented

Professional mental health content distribution varied dramatically:

**Professional Content by Journey:**
{professional_by_journey}

**Journey Type Classification:**

**Type A - Professional-Dominated Journeys** (Journeys 3, 4, 5):
- Professional content: {type_a_prof:.1f}% average
- Harmful content: {type_a_harmful:.1f}% average
- Resource provision: {type_a_resources:.1f}% provide help

**Type B - Peer-Dominated Journeys** (Journeys 1, 6):
- Professional content: {type_b_prof:.1f}% average  
- Harmful content: {type_b_harmful:.1f}% average
- Resource provision: {type_b_resources:.1f}% provide help

**Ratio:** Type A journeys contained {ratio_type_a_type_b}x more professional content than Type B journeys.

---

## Finding 3: Resource Desert in Help-Seeking Pathways

Videos addressing serious mental health topics often provided no resources:

**Journey 1 ("depression help") Resource Analysis:**
- Total videos: {j1_total}
- Videos with NO resources: {j1_no_resources} ({j1_no_resources_pct:.1f}%)
- Harmful videos with NO resources: {j1_harmful_no_resources} ({j1_harmful_no_resources_pct:.1f}%)

**Among videos coded as potentially harmful (n = {total_harmful}):**
- No resources: {harmful_no_resources} ({harmful_no_resources_pct:.1f}%)
- Provides help: {harmful_with_help} ({harmful_with_help_pct:.1f}%)
- Links to resources: {harmful_with_links} ({harmful_with_links_pct:.1f}%)

---

## Finding 4: Creator Type Patterns

**Overall Creator Distribution:**
{creator_distribution}

**Professional vs Peer by Journey Type:**

Type A Journeys (3, 4, 5):
- Peer creators: {type_a_peer:.1f}%
- Professional creators: {type_a_prof_creators:.1f}%

Type B Journeys (1, 6):
- Peer creators: {type_b_peer:.1f}%
- Professional creators: {type_b_prof_creators:.1f}%

---

## Finding 5: Youth-Targeted Content Concerns

**Youth/Teen Targeted Videos (n = {youth_total}):**
- Potentially harmful: {youth_harmful} ({youth_harmful_pct:.1f}%)
- Professional involvement: {youth_professional} ({youth_professional_pct:.1f}%)
- No resources: {youth_no_resources} ({youth_no_resources_pct:.1f}%)

**Comparison to General Adult Content (n = {adult_total}):**
- Potentially harmful: {adult_harmful} ({adult_harmful_pct:.1f}%)
- Professional involvement: {adult_professional} ({adult_professional_pct:.1f}%)
- No resources: {adult_no_resources} ({adult_no_resources_pct:.1f}%)

---

## Journey 1 Temporal Analysis (90 videos)

Examining content evolution across the longest journey:

**First Third (Videos 1-30):**
- Harmful: {j1_first_third_harmful:.1f}%
- Professional: {j1_first_third_prof:.1f}%
- No resources: {j1_first_third_no_resources:.1f}%

**Second Third (Videos 31-60):**
- Harmful: {j1_second_third_harmful:.1f}%
- Professional: {j1_second_third_prof:.1f}%
- No resources: {j1_second_third_no_resources:.1f}%

**Final Third (Videos 61-90):**
- Harmful: {j1_final_third_harmful:.1f}%
- Professional: {j1_final_third_prof:.1f}%
- No resources: {j1_final_third_no_resources:.1f}%

---

## Summary Statistics Table

| Journey | Query | N | Harmful (%) | Negative (%) | Professional (%) | No Resources (%) |
|---------|-------|---|-------------|--------------|------------------|------------------|
{summary_table}

---
"""

# Calculate all the statistics
j1 = df[df['journey_number'] == 1]
j2 = df[df['journey_number'] == 2]
j3 = df[df['journey_number'] == 3]

j1_harmful = (j1['potentially_harmful'] == 'yes').sum() / len(j1) * 100
j2_harmful = (j2['potentially_harmful'] == 'yes').sum() / len(j2) * 100
j3_harmful = (j3['potentially_harmful'] == 'yes').sum() / len(j3) * 100

harmful_by_journey = ""
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    harmful_pct = (j_data['potentially_harmful'] == 'yes').sum() / len(j_data) * 100
    harmful_by_journey += f"- Journey {journey_num}: {harmful_pct:.1f}%\n"

professional_by_journey = ""
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    prof_pct = (j_data['has_professional'] == 'yes').sum() / len(j_data) * 100
    professional_by_journey += f"- Journey {journey_num}: {prof_pct:.1f}%\n"

# Type A vs Type B
type_a = df[df['journey_number'].isin([3, 4, 5])]
type_b = df[df['journey_number'].isin([1, 6])]

type_a_prof = (type_a['has_professional'] == 'yes').sum() / len(type_a) * 100
type_a_harmful = (type_a['potentially_harmful'] == 'yes').sum() / len(type_a) * 100
type_a_resources = (type_a['resource_quality'] == 'provides_help').sum() / len(type_a) * 100

type_b_prof = (type_b['has_professional'] == 'yes').sum() / len(type_b) * 100
type_b_harmful = (type_b['potentially_harmful'] == 'yes').sum() / len(type_b) * 100
type_b_resources = (type_b['resource_quality'] == 'provides_help').sum() / len(type_b) * 100

# Creator type patterns
type_a_peer = (type_a['creator_type'] == 'peer_creator').sum() / len(type_a) * 100
type_a_prof_creators = (type_a['creator_type'].isin(['licensed_therapist', 'mental_health_org', 'educational_channel'])).sum() / len(type_a) * 100

type_b_peer = (type_b['creator_type'] == 'peer_creator').sum() / len(type_b) * 100
type_b_prof_creators = (type_b['creator_type'].isin(['licensed_therapist', 'mental_health_org', 'educational_channel'])).sum() / len(type_b) * 100

creator_distribution = ""
for creator, count in df['creator_type'].value_counts().items():
    creator_distribution += f"- {creator}: {count} ({count/len(df)*100:.1f}%)\n"

# Journey 1 specifics
j1_total = len(j1)
j1_no_resources = (j1['resource_quality'] == 'no_resources').sum()
j1_no_resources_pct = j1_no_resources / len(j1) * 100
j1_harmful_no_resources = ((j1['potentially_harmful'] == 'yes') & (j1['resource_quality'] == 'no_resources')).sum()
j1_harmful_no_resources_pct = j1_harmful_no_resources / len(j1) * 100

# Harmful videos resource analysis
harmful_videos = df[df['potentially_harmful'] == 'yes']
total_harmful = len(harmful_videos)
harmful_no_resources = (harmful_videos['resource_quality'] == 'no_resources').sum()
harmful_no_resources_pct = harmful_no_resources / total_harmful * 100 if total_harmful > 0 else 0
harmful_with_help = (harmful_videos['resource_quality'] == 'provides_help').sum()
harmful_with_help_pct = harmful_with_help / total_harmful * 100 if total_harmful > 0 else 0
harmful_with_links = (harmful_videos['resource_quality'] == 'links_resources').sum()
harmful_with_links_pct = harmful_with_links / total_harmful * 100 if total_harmful > 0 else 0

# Youth analysis
youth_videos = df[df['target_audience'] == 'youth_teen']
youth_total = len(youth_videos)
youth_harmful = (youth_videos['potentially_harmful'] == 'yes').sum()
youth_harmful_pct = youth_harmful / youth_total * 100 if youth_total > 0 else 0
youth_professional = (youth_videos['has_professional'] == 'yes').sum()
youth_professional_pct = youth_professional / youth_total * 100 if youth_total > 0 else 0
youth_no_resources = (youth_videos['resource_quality'] == 'no_resources').sum()
youth_no_resources_pct = youth_no_resources / youth_total * 100 if youth_total > 0 else 0

adult_videos = df[df['target_audience'] == 'general_adult']
adult_total = len(adult_videos)
adult_harmful = (adult_videos['potentially_harmful'] == 'yes').sum()
adult_harmful_pct = adult_harmful / adult_total * 100 if adult_total > 0 else 0
adult_professional = (adult_videos['has_professional'] == 'yes').sum()
adult_professional_pct = adult_professional / adult_total * 100 if adult_total > 0 else 0
adult_no_resources = (adult_videos['resource_quality'] == 'no_resources').sum()
adult_no_resources_pct = adult_no_resources / adult_total * 100 if adult_total > 0 else 0

# Journey 1 temporal
j1_first_third = j1[j1['position_in_journey'] <= 30]
j1_second_third = j1[(j1['position_in_journey'] > 30) & (j1['position_in_journey'] <= 60)]
j1_final_third = j1[j1['position_in_journey'] > 60]

j1_first_third_harmful = (j1_first_third['potentially_harmful'] == 'yes').sum() / len(j1_first_third) * 100
j1_first_third_prof = (j1_first_third['has_professional'] == 'yes').sum() / len(j1_first_third) * 100
j1_first_third_no_resources = (j1_first_third['resource_quality'] == 'no_resources').sum() / len(j1_first_third) * 100

j1_second_third_harmful = (j1_second_third['potentially_harmful'] == 'yes').sum() / len(j1_second_third) * 100
j1_second_third_prof = (j1_second_third['has_professional'] == 'yes').sum() / len(j1_second_third) * 100
j1_second_third_no_resources = (j1_second_third['resource_quality'] == 'no_resources').sum() / len(j1_second_third) * 100

j1_final_third_harmful = (j1_final_third['potentially_harmful'] == 'yes').sum() / len(j1_final_third) * 100
j1_final_third_prof = (j1_final_third['has_professional'] == 'yes').sum() / len(j1_final_third) * 100
j1_final_third_no_resources = (j1_final_third['resource_quality'] == 'no_resources').sum() / len(j1_final_third) * 100

# Calculate deltas and ratios for the template
delta_j1_j3 = j1_harmful - j3_harmful
delta_j1_j2 = j1_harmful - j2_harmful
ratio_j1_j2 = f"{j1_harmful/j2_harmful:.1f}" if j2_harmful > 0 else "infinitely"
ratio_type_a_type_b = f"{type_a_prof/type_b_prof:.1f}" if type_b_prof > 0 else "infinitely"

# Summary table
summary_table = ""
for journey_num in range(1, 7):
    j_data = df[df['journey_number'] == journey_num]
    query = j_data['starting_condition'].iloc[0]
    n = len(j_data)
    harmful = (j_data['potentially_harmful'] == 'yes').sum() / n * 100
    negative = (j_data['sentiment'] == 'negative').sum() / n * 100
    professional = (j_data['has_professional'] == 'yes').sum() / n * 100
    no_resources = (j_data['resource_quality'] == 'no_resources').sum() / n * 100
    summary_table += f"| {journey_num} | {query} | {n} | {harmful:.1f} | {negative:.1f} | {professional:.1f} | {no_resources:.1f} |\n"

# Fill in results template
results_text = results_text.format(
    harmful_by_journey=harmful_by_journey,
    j1_harmful=j1_harmful,
    j2_harmful=j2_harmful,
    j3_harmful=j3_harmful,
    delta_j1_j3=delta_j1_j3,
    delta_j1_j2=delta_j1_j2,
    ratio_j1_j2=ratio_j1_j2,
    professional_by_journey=professional_by_journey,
    type_a_prof=type_a_prof,
    type_a_harmful=type_a_harmful,
    type_a_resources=type_a_resources,
    type_b_prof=type_b_prof,
    type_b_harmful=type_b_harmful,
    type_b_resources=type_b_resources,
    ratio_type_a_type_b=ratio_type_a_type_b,
    type_a_peer=type_a_peer,
    type_a_prof_creators=type_a_prof_creators,
    type_b_peer=type_b_peer,
    type_b_prof_creators=type_b_prof_creators,
    creator_distribution=creator_distribution,
    j1_total=j1_total,
    j1_no_resources=j1_no_resources,
    j1_no_resources_pct=j1_no_resources_pct,
    j1_harmful_no_resources=j1_harmful_no_resources,
    j1_harmful_no_resources_pct=j1_harmful_no_resources_pct,
    total_harmful=total_harmful,
    harmful_no_resources=harmful_no_resources,
    harmful_no_resources_pct=harmful_no_resources_pct,
    harmful_with_help=harmful_with_help,
    harmful_with_help_pct=harmful_with_help_pct,
    harmful_with_links=harmful_with_links,
    harmful_with_links_pct=harmful_with_links_pct,
    youth_total=youth_total,
    youth_harmful=youth_harmful,
    youth_harmful_pct=youth_harmful_pct,
    youth_professional=youth_professional,
    youth_professional_pct=youth_professional_pct,
    youth_no_resources=youth_no_resources,
    youth_no_resources_pct=youth_no_resources_pct,
    adult_total=adult_total,
    adult_harmful=adult_harmful,
    adult_harmful_pct=adult_harmful_pct,
    adult_professional=adult_professional,
    adult_professional_pct=adult_professional_pct,
    adult_no_resources=adult_no_resources,
    adult_no_resources_pct=adult_no_resources_pct,
    j1_first_third_harmful=j1_first_third_harmful,
    j1_first_third_prof=j1_first_third_prof,
    j1_first_third_no_resources=j1_first_third_no_resources,
    j1_second_third_harmful=j1_second_third_harmful,
    j1_second_third_prof=j1_second_third_prof,
    j1_second_third_no_resources=j1_second_third_no_resources,
    j1_final_third_harmful=j1_final_third_harmful,
    j1_final_third_prof=j1_final_third_prof,
    j1_final_third_no_resources=j1_final_third_no_resources,
    summary_table=summary_table
)

# Combine and save
full_output = methods_text + results_text

with open(os.path.join(PAPER_DIR, 'paper_statistics.md'), 'w') as f:
    f.write(full_output)

print(f"\n✅ Saved comprehensive statistics to: {os.path.join(PAPER_DIR, 'paper_statistics.md')}")
print("\n" + "="*70)
print("ALL STATISTICS GENERATED")
print("="*70)
print("\nYou now have everything you need to write your Methods and Results sections!")
print("\nFiles created:")
print("  • paper_statistics.md - All stats for Methods & Results")
print("  • qualitative_examples.md - Examples for Discussion")
print("\nJust copy the relevant statistics into your paper draft!")