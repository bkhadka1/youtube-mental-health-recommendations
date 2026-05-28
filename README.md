# Algorithmic Pathways to Mental Health Content: How YouTube's Recommendation System Shapes Adolescent Exposure Patterns

**Author:** Bikash Khadka  
**Status:** Preprint — https://doi.org/10.5281/zenodo.20278934  
**Contact:** bcash2233@gmail.com

---

## Overview

This project investigates how YouTube's recommendation algorithm shapes what adolescents encounter when searching for mental health content. Using a mixed-methods approach combining algorithmic walkthroughs (qualitative) with YouTube Data API analysis (quantitative), we identify systematic patterns in how the platform routes users toward or away from professional mental health resources.

---

## Key Findings

- **Dual-Axis Framework:** Content pathway quality depends on two factors — search term framing (negative/clinical vs. positive/wellness) and starting channel type (established ecosystem vs. random). These two axes predict user outcomes across all six tested journeys.
- **Professional Content Suppression:** Professional mental health content comprises 24.4% of available videos but appears at <10% in typical recommendation pathways — despite achieving 32.5% higher engagement rates than peer content.
- **Teen Content Gap:** Teen-specific mental health searches yield the lowest professional content availability (8%), lowest engagement rates, and lowest view counts of any category tested.
- **Algorithmic Escalation:** Negative search framing combined with random channel entry produces progressive content darkening — from general advice to crisis content over 90 videos — with minimal professional intervention.

---

## Data

- **Algorithmic Walkthroughs:** 6 journeys, 200+ manually coded videos across different search queries
- **API Dataset:** 525 videos collected via YouTube Data API v3 across 12 mental health search terms
- **Analysis Period:** January 2026

> **Note:** Raw video data and manual coding sheets are not included in this repository to respect content creator privacy. Processed summary statistics and analysis outputs are provided.

---

## Repository Structure

```
youtube-mental-health-recommendations/
├── README.md
├── .gitignore
├── requirements.txt
├── code/
│   ├── collection/
│   │   ├── collect_youtube_data.py
│   │   └── test_youtube_api.py
│   ├── analysis/
│   │   ├── identify_ecosystem.py
│   │   ├── analyze_by_search_term.py
│   │   ├── analyze_professional_vs_peer.py
│   │   ├── classify_by_title.py
│   │   ├── explore_data.py
│   │   ├── network_analysis.py
│   │   └── bert_sentiment_analysis.py
│   └── paper/
│       ├── 01_journey_trajectory_analysis.py
│       ├── 02_content_creator_analysis.py
│       ├── 03_qualitative_examples.py
│       └── 04_paper_statistics.py
├── data/
│   └── processed/
│       ├── established_ecosystem.json
│       └── professional_vs_peer_analysis.json
├── figures/
│   ├── established_ecosystem.png
│   ├── fig1_harmful_trajectories.png
│   ├── fig2_dual_axis_framework.png
│   ├── fig3_content_distribution.png
│   ├── fig4_journey1_deepdive.png
│   ├── fig5_creator_evolution.png
│   ├── fig6_sentiment_resource_matrix.png
│   ├── fig7_target_audience.png
│   ├── professional_vs_peer.png
│   ├── search_term_analysis.png
│   ├── bert_sentiment_results.png
│   └── network_analysis_results.png
├── paper/
│   ├── drafts/
│   │   └── bikash_khadka_research_draft.pdf
│   ├── paper_statistics.md
│   ├── qualitative_examples.md
│   └── table1_journey_summary.csv
└── docs/
    ├── research_proposal_outline.md
    ├── comprehensive_journey_analysis.md
    ├── journey_summaries.md
    └── api_data_summary.md
```

---

## Methods

### Phase 1: Algorithmic Walkthroughs

Six systematic journeys through YouTube's recommendation system, each starting from a different mental health search query in fresh incognito browser sessions. Videos were manually coded for content type, sentiment, creator credentials, target audience, resource quality, and potential harm.

| Journey | Search Query | Videos | Key Pattern |
|---------|-------------|--------|-------------|
| 1 | "mental health" | 90 | Escalation to crisis content |
| 2 | "feeling depressed" | 20 | Content-type loop (films) |
| 3 | "therapy for teens" | 30 | Audience mismatch (parent-focused) |
| 4 | "anxiety relief" | 20 | Single-source professional loop |
| 5 | "teen depression" | 20 | Topic drift (attachment theory) |
| 6 | "mental wellness" | 30 | Positive content maintained |

### Phase 2: API Data Collection

525 videos collected via YouTube Data API v3 across 12 search terms to validate qualitative findings at scale. Analysis focused on channel ecosystem mapping, professional vs. peer content distribution, and engagement metrics.

---

## Tools & Technologies

- **Python** — pandas, matplotlib, seaborn, NumPy
- **YouTube Data API v3** — data collection and video metadata retrieval
- **Content Classification** — keyword-based title/description classification (see `classify_by_title.py`)
- **Manual Coding** — structured coding scheme applied across all 6 journeys

> **Note on transformer-based classification (`bert_sentiment_analysis.py`):**
> A DistilBERT zero-shot sentiment pipeline (SST-2 weights) was evaluated as a potential classifier for the "potentially harmful" coding dimension. It was not used in the paper's analysis. The model conflates *topic negativity* with *sentiment negativity* — titles like "Signs Your Teen Needs Therapy" were flagged as negative because they contain clinical language, while genuinely harmful peer-confessional titles were sometimes rated positive due to hopeful framing ("Overcoming..."). The SST-2 training corpus (movie reviews) is too distant from mental health discourse for zero-shot inference to be reliable here. The script is retained in the repository as a documented baseline and starting point for future fine-tuning on the manual coding labels. See `bert_sentiment_analysis.py` for the full failure analysis and a proposed fine-tuning roadmap.

---

## Setup

```bash
# Clone the repository
git clone https://github.com/bkhadka1/youtube-mental-health-recommendations.git
cd youtube-mental-health-recommendations

# Install dependencies
pip install -r requirements.txt

# For data collection (requires YouTube API key)
# Add your API key to config/config.py (not tracked by git)
```

---

## Target Venues

- ICWSM 2027 (International Conference on Web and Social Media)
- CHI 2027 (ACM Conference on Human Factors in Computing Systems)
- FAccT 2027 (ACM Conference on Fairness, Accountability, and Transparency)

---

## Citation

If you use this work, please cite:

> Khadka, B. (2026). *Algorithmic Pathways to Mental Health Content: How YouTube's Recommendation System Shapes Adolescent Exposure Patterns.* Zenodo. https://doi.org/10.5281/zenodo.20278934

---

## License

This project is for academic research purposes. Please contact the author for reuse permissions.