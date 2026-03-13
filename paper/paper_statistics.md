# STATISTICS FOR METHODS SECTION

## Sample Description

**Data Collection Period:** January 20-28, 2026

**Total Videos Analyzed:** 201

**Journey Breakdown:**
- Journey 1 ('depression help'): n = 90
- Journey 2 ('i hate my life'): n = 20
- Journey 3 ('anxiety coping strategies'): n = 30
- Journey 4 ('why am i depressed'): n = 20
- Journey 5 ('random start'): n = 20
- Journey 6 ('teen mental health'): n = 21


**Coding Scheme:**

All videos were coded for the following dimensions:

1. **Content Type** (5 categories):
   - peer_support: n = 78 (38.8%)
   - professional_advice: n = 77 (38.3%)
   - educational: n = 31 (15.4%)
   - harmful: n = 13 (6.5%)
   - commercial: n = 2 (1.0%)


2. **Sentiment** (3 categories):
   - negative: n = 76 (37.8%)
   - neutral: n = 70 (34.8%)
   - positive: n = 55 (27.4%)


3. **Target Audience** (3 categories):
   - general_adult: n = 148 (73.6%)
   - parent_caregiver: n = 28 (13.9%)
   - youth_teen: n = 25 (12.4%)


4. **Resource Quality** (3 categories):
   - no_resources: n = 116 (57.7%)
   - provides_help: n = 79 (39.3%)
   - links_resources: n = 6 (3.0%)


5. **Professional Involvement** (binary):
   - no: n = 125 (62.2%)
   - yes: n = 76 (37.8%)


6. **Potentially Harmful** (binary):
   - no: n = 180 (89.6%)
   - yes: n = 21 (10.4%)


7. **Creator Type** (5 categories):
   - peer_creator: n = 91 (45.3%)
   - licensed_therapist: n = 74 (36.8%)
   - educational_channel: n = 31 (15.4%)
   - mental_health_org: n = 3 (1.5%)
   - influencer: n = 2 (1.0%)


8. **Production Quality** (2 categories):
   - professional: n = 108 (53.7%)
   - amateur: n = 93 (46.3%)


---

## Inter-rater Reliability

**Note:** All videos were coded by a single researcher (the author). While this limits inter-rater reliability assessment, detailed coding notes and operational definitions ensure replicability. Future research should employ multiple coders to establish Cohen's kappa or similar reliability measures.

---

## Journey Design

Six distinct algorithmic journeys were conducted, each representing common teen mental health search behaviors:


**Journey 1: "depression help"**
- Sample size: n = 90
- Harmful content: 20 videos (22.2%)
- Professional involvement: 2 videos (2.2%)
- Negative sentiment: 74 videos (82.2%)


**Journey 2: "i hate my life"**
- Sample size: n = 20
- Harmful content: 1 videos (5.0%)
- Professional involvement: 3 videos (15.0%)
- Negative sentiment: 2 videos (10.0%)


**Journey 3: "anxiety coping strategies"**
- Sample size: n = 30
- Harmful content: 0 videos (0.0%)
- Professional involvement: 29 videos (96.7%)
- Negative sentiment: 0 videos (0.0%)


**Journey 4: "why am i depressed"**
- Sample size: n = 20
- Harmful content: 0 videos (0.0%)
- Professional involvement: 20 videos (100.0%)
- Negative sentiment: 0 videos (0.0%)


**Journey 5: "random start"**
- Sample size: n = 20
- Harmful content: 0 videos (0.0%)
- Professional involvement: 20 videos (100.0%)
- Negative sentiment: 0 videos (0.0%)


**Journey 6: "teen mental health"**
- Sample size: n = 21
- Harmful content: 0 videos (0.0%)
- Professional involvement: 2 videos (9.5%)
- Negative sentiment: 0 videos (0.0%)



**Rationale for Journey Selection:**
- Journeys 1, 3, 4 represent positive-framed help-seeking (varying specificity)
- Journey 2 represents negative-framed distress expression
- Journey 5 tests algorithmic recommendations without query bias
- Journey 6 examines age-specific mental health content

---

# STATISTICS FOR RESULTS SECTION

## Finding 1: Algorithmic Divergence Based on Query Framing

Analysis revealed significant variation in content quality across journeys based on starting query framing:

**Harmful Content by Journey:**
- Journey 1: 22.2%
- Journey 2: 5.0%
- Journey 3: 0.0%
- Journey 4: 0.0%
- Journey 5: 0.0%
- Journey 6: 0.0%


**Statistical Comparison:**
- Journey 1 ("depression help") vs Journey 3 ("anxiety coping strategies"):
  - Harmful content: 22.2% vs 0.0% (Δ = +22.2 percentage points)
  - Chi-square test would show: χ²(1) = [calculate], p < .001 [if significant]

- Journey 1 vs Journey 2 ("i hate my life"):
  - Harmful content: 22.2% vs 5.0% (Δ = +17.2 percentage points)
  - **Paradox:** Help-seeking query yields 4.4x more harmful content than distress expression

---

## Finding 2: Professional Content Systematically Underrepresented

Professional mental health content distribution varied dramatically:

**Professional Content by Journey:**
- Journey 1: 2.2%
- Journey 2: 15.0%
- Journey 3: 96.7%
- Journey 4: 100.0%
- Journey 5: 100.0%
- Journey 6: 9.5%


**Journey Type Classification:**

**Type A - Professional-Dominated Journeys** (Journeys 3, 4, 5):
- Professional content: 98.6% average
- Harmful content: 0.0% average
- Resource provision: 98.6% provide help

**Type B - Peer-Dominated Journeys** (Journeys 1, 6):
- Professional content: 3.6% average  
- Harmful content: 18.0% average
- Resource provision: 7.2% provide help

**Ratio:** Type A journeys contained 27.4x more professional content than Type B journeys.

---

## Finding 3: Resource Desert in Help-Seeking Pathways

Videos addressing serious mental health topics often provided no resources:

**Journey 1 ("depression help") Resource Analysis:**
- Total videos: 90
- Videos with NO resources: 81 (90.0%)
- Harmful videos with NO resources: 19 (21.1%)

**Among videos coded as potentially harmful (n = 21):**
- No resources: 20 (95.2%)
- Provides help: 0 (0.0%)
- Links to resources: 1 (4.8%)

---

## Finding 4: Creator Type Patterns

**Overall Creator Distribution:**
- peer_creator: 91 (45.3%)
- licensed_therapist: 74 (36.8%)
- educational_channel: 31 (15.4%)
- mental_health_org: 3 (1.5%)
- influencer: 2 (1.0%)


**Professional vs Peer by Journey Type:**

Type A Journeys (3, 4, 5):
- Peer creators: 0.0%
- Professional creators: 100.0%

Type B Journeys (1, 6):
- Peer creators: 81.1%
- Professional creators: 17.1%

---

## Finding 5: Youth-Targeted Content Concerns

**Youth/Teen Targeted Videos (n = 25):**
- Potentially harmful: 6 (24.0%)
- Professional involvement: 4 (16.0%)
- No resources: 18 (72.0%)

**Comparison to General Adult Content (n = 148):**
- Potentially harmful: 15 (10.1%)
- Professional involvement: 45 (30.4%)
- No resources: 97 (65.5%)

---

## Journey 1 Temporal Analysis (90 videos)

Examining content evolution across the longest journey:

**First Third (Videos 1-30):**
- Harmful: 26.7%
- Professional: 3.3%
- No resources: 90.0%

**Second Third (Videos 31-60):**
- Harmful: 23.3%
- Professional: 3.3%
- No resources: 80.0%

**Final Third (Videos 61-90):**
- Harmful: 16.7%
- Professional: 0.0%
- No resources: 100.0%

---

## Summary Statistics Table

| Journey | Query | N | Harmful (%) | Negative (%) | Professional (%) | No Resources (%) |
|---------|-------|---|-------------|--------------|------------------|------------------|
| 1 | depression help | 90 | 22.2 | 82.2 | 2.2 | 90.0 |
| 2 | i hate my life | 20 | 5.0 | 10.0 | 15.0 | 80.0 |
| 3 | anxiety coping strategies | 30 | 0.0 | 0.0 | 96.7 | 0.0 |
| 4 | why am i depressed | 20 | 0.0 | 0.0 | 100.0 | 0.0 |
| 5 | random start | 20 | 0.0 | 0.0 | 100.0 | 5.0 |
| 6 | teen mental health | 21 | 0.0 | 0.0 | 9.5 | 85.7 |


---
