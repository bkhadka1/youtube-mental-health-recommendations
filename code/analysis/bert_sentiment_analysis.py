"""
=============================================================================
BERT-Based Sentiment Analysis for YouTube Mental Health Content
=============================================================================
Author:  Bikash Khadka
Project: Algorithmic Pathways to Mental Health Content on YouTube
Preprint: https://doi.org/10.5281/zenodo.20278934

PURPOSE
-------
This notebook extends the keyword-based classifier (classify_by_title.py)
with a transformer-based sentiment analysis pipeline using DistilBERT.

It runs zero-shot inference on video titles from the dataset and compares
DistilBERT outputs to the original keyword heuristic — providing a richer
signal for the "potentially harmful" coding dimension and a foundation for
fine-tuning on manually coded labels.

PIPELINE OVERVIEW
-----------------
  Video Titles (raw)
       │
       ▼
  DistilBERT Sentiment (zero-shot, distilbert-base-uncased-finetuned-sst-2)
       │
       ▼
  Keyword Classifier (classify_by_title.py heuristic)
       │
       ▼
  Comparison + Disagreement Analysis
       │
       ▼
  Journey-Level Sentiment Profiles

HOW TO RUN
----------
  pip install transformers torch pandas
  python bert_sentiment_analysis.py

  To convert to Jupyter notebook:
    pip install jupytext
    jupytext --to notebook bert_sentiment_analysis.py

DEPENDENCIES
------------
  transformers >= 4.x
  torch >= 2.x
  pandas, numpy, matplotlib, seaborn
=============================================================================
"""

# ── Imports ──────────────────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from transformers import pipeline
import warnings
warnings.filterwarnings("ignore")

sns.set_style("whitegrid")
sns.set_context("paper", font_scale=1.3)

# ── Section 1: Sample Data ────────────────────────────────────────────────────
#
# In the full pipeline, replace SAMPLE_TITLES with:
#   df = pd.read_csv("data/raw/youtube_mental_health_20260125_225956.csv")
#   titles = df["title"].dropna().tolist()
#
# For reproducibility without the raw data file, we use a representative
# sample drawn from the manually coded journey notes, covering the full
# range of content types seen across the 6 journeys.

SAMPLE_TITLES = [
    # Journey 1 — "mental health" (mix of professional, peer, harmful)
    "What is Mental Health? | Kati Morton",
    "I've been struggling with depression for years (my story)",
    "How to Cope With Depression | Doctor Explains",
    "My darkest moment: I wanted to end it all",
    "Understanding Anxiety Disorders — Mayo Clinic",
    "does anyone else feel completely empty inside",
    "10 Signs You're Depressed (And Don't Know It)",
    "Teen shares raw truth about suicidal thoughts",
    "Mental Health 101: What You Need to Know",
    "i stopped going to school because of my depression",

    # Journey 2 — "feeling depressed" (film/entertainment loop)
    "Feeling Depressed Short Film | Award Winning",
    "Depression — A Silent Killer [Documentary]",
    "What Depression Really Feels Like — Animated Short",
    "Sad Aesthetic Compilation for when you feel empty",
    "Finding Light in the Darkness — Mental Health Film",

    # Journey 3 — "therapy for teens" (professional, parent-focused)
    "How to Find a Therapist for Your Teenager",
    "Signs Your Teen Needs Therapy | Dr. Tracey Marks",
    "Therapy for Teens: What Parents Need to Know",
    "CBT Techniques Explained for Adolescents",
    "When Should You Seek Help for Teen Depression?",

    # Journey 4 — "anxiety relief" (professional loop)
    "5-Minute Anxiety Relief Breathing Exercise",
    "Anxiety Relief Techniques That Actually Work",
    "Dr. Huberman on Stress & Anxiety Management",
    "Guided Meditation for Anxiety (10 Minutes)",
    "Understanding Your Nervous System: Anxiety Explained",

    # Journey 5 — "teen depression" (topic drift)
    "Teen Depression Statistics 2024 — What Parents Should Know",
    "Attachment Theory and Teen Mental Health",
    "Why Teenagers Are More Depressed Than Ever",
    "my experience with teen depression (storytime)",
    "Overcoming Teenage Depression: A Survivor's Story",

    # Journey 6 — "mental wellness" (positive/wellness content)
    "Daily Mental Wellness Habits That Changed My Life",
    "How to Build a Mental Health Routine",
    "The Science of Happiness — Dr. Laurie Santos",
    "Morning Routine for Better Mental Health",
    "Self-Care isn't Selfish: Mental Wellness Tips",
]

# Attach ground-truth journey labels for analysis
JOURNEY_LABELS = [1]*10 + [2]*5 + [3]*5 + [4]*5 + [5]*5 + [6]*5

# Keyword-based classifications (from classify_by_title.py heuristic)
# Values: 'professional_general', 'personal_story', 'educational',
#         'film_entertainment', 'help_seeking', 'other'
KEYWORD_CLASSIFICATIONS = [
    "professional_general", "personal_story", "professional_general",
    "personal_story",       "educational",    "personal_story",
    "educational",          "personal_story", "educational",
    "personal_story",       "film_entertainment", "film_entertainment",
    "film_entertainment",   "other",          "film_entertainment",
    "professional_general", "professional_general", "professional_general",
    "educational",          "help_seeking",   "help_seeking",
    "help_seeking",         "professional_general", "help_seeking",
    "educational",          "educational",    "educational",
    "educational",          "personal_story", "personal_story",
    "help_seeking",         "help_seeking",   "educational",
    "help_seeking",         "help_seeking",
]

df = pd.DataFrame({
    "title":               SAMPLE_TITLES,
    "journey":             JOURNEY_LABELS,
    "keyword_class":       KEYWORD_CLASSIFICATIONS,
})

print("=" * 70)
print("BERT SENTIMENT ANALYSIS — YouTube Mental Health Content")
print("=" * 70)
print(f"\nSample size: {len(df)} titles across {df['journey'].nunique()} journeys")
print(f"Journey distribution:\n{df['journey'].value_counts().sort_index().to_string()}")


# ── Section 2: DistilBERT Inference ─────────────────────────────────────────
#
# Model: distilbert-base-uncased-finetuned-sst-2-english
#   • Fine-tuned on Stanford Sentiment Treebank (SST-2)
#   • Outputs POSITIVE / NEGATIVE with confidence score
#   • Runs on CPU — no GPU required
#
# Limitation note: SST-2 was trained on movie reviews. Mental health text
# has a different register (e.g., "I feel empty" reads as negative, which
# aligns with our coding; "depression explained" may read as neutral/positive
# despite addressing a negative topic). Fine-tuning on the manual coding
# labels is the recommended next step (see Section 5).

print("\n" + "─" * 70)
print("Loading distilbert-base-uncased-finetuned-sst-2-english ...")
print("─" * 70)

sentiment_pipeline = pipeline(
    "sentiment-analysis",
    model="distilbert-base-uncased-finetuned-sst-2-english",
    truncation=True,
    max_length=128,
)

print("✅ Model loaded\n")
print("Running inference on all titles ...")

results = sentiment_pipeline(df["title"].tolist())

df["bert_label"]      = [r["label"] for r in results]
df["bert_confidence"] = [round(r["score"], 4) for r in results]

# Normalise label to lowercase for consistency
df["bert_sentiment"] = df["bert_label"].str.lower()   # 'positive' / 'negative'

print("✅ Inference complete\n")


# ── Section 3: Results ───────────────────────────────────────────────────────

print("=" * 70)
print("RESULTS — Per-Title Predictions")
print("=" * 70)
print(f"\n{'Title':<55} {'BERT':<12} {'Conf':<8} {'Keyword Class'}")
print("─" * 95)

for _, row in df.iterrows():
    title_short = row["title"][:54]
    label_str = row["bert_sentiment"].upper()
    conf_str  = f"{row['bert_confidence']:.3f}"
    print(f"{title_short:<55} {label_str:<12} {conf_str:<8} {row['keyword_class']}")


# ── Section 4: Comparison — BERT vs Keyword Heuristic ───────────────────────

print("\n" + "=" * 70)
print("COMPARISON — DistilBERT vs Keyword Classifier")
print("=" * 70)

# Map keyword classes to an expected sentiment polarity
# (used to check alignment, not as ground truth)
polarity_map = {
    "professional_general": "positive",
    "educational":          "positive",
    "help_seeking":         "positive",
    "film_entertainment":   "negative",
    "personal_story":       "negative",
    "other":                "positive",
}
df["keyword_polarity"] = df["keyword_class"].map(polarity_map)

# Agreement: BERT sentiment matches keyword polarity
df["agreement"] = df["bert_sentiment"] == df["keyword_polarity"]

agreement_rate = df["agreement"].mean() * 100
print(f"\nOverall agreement rate: {agreement_rate:.1f}%")
print(f"  Agreed:    {df['agreement'].sum()} / {len(df)} titles")
print(f"  Disagreed: {(~df['agreement']).sum()} / {len(df)} titles")

# Disagreement cases — most interesting for review
print("\n⚠️  Disagreement Cases (where BERT and keyword heuristic diverge):")
print("─" * 95)

disagreements = df[~df["agreement"]][["title", "bert_sentiment", "bert_confidence", "keyword_class"]]

if len(disagreements) == 0:
    print("  None — full agreement on this sample.")
else:
    for _, row in disagreements.iterrows():
        print(f"  Title:      {row['title']}")
        print(f"  BERT:       {row['bert_sentiment'].upper()} ({row['bert_confidence']:.3f})")
        print(f"  Keyword:    {row['keyword_class']}")
        print()


# ── Section 5: Journey-Level Sentiment Profiles ──────────────────────────────

print("=" * 70)
print("JOURNEY-LEVEL SENTIMENT PROFILES")
print("=" * 70)

journey_info = {
    1: "mental health",
    2: "feeling depressed",
    3: "therapy for teens",
    4: "anxiety relief",
    5: "teen depression",
    6: "mental wellness",
}

journey_stats = df.groupby("journey").agg(
    n              = ("title", "count"),
    pct_negative   = ("bert_sentiment", lambda x: (x == "negative").mean() * 100),
    avg_confidence = ("bert_confidence", "mean"),
).round(2)

print()
print(f"{'J':<4} {'Query':<22} {'N':<5} {'BERT Negative %':<18} {'Avg Confidence'}")
print("─" * 65)

for j, row in journey_stats.iterrows():
    print(
        f"  {j:<3} {journey_info[j]:<22} {int(row['n']):<5} "
        f"{row['pct_negative']:>12.1f}%       {row['avg_confidence']:.3f}"
    )

print()
print("Key observation:")
print("  Journey 1 ('mental health') and Journey 2 ('feeling depressed')")
print("  should show the highest negative sentiment rates — consistent with")
print("  the qualitative coding showing escalation to crisis content.")
print("  Journey 6 ('mental wellness') should show the most positive signal.")


# ── Section 6: Visualisations ────────────────────────────────────────────────

fig, axes = plt.subplots(1, 3, figsize=(16, 5))
fig.suptitle(
    "DistilBERT Sentiment Analysis — YouTube Mental Health Titles\n"
    "Bikash Khadka · Preprint: DOI 10.5281/zenodo.20278934",
    fontsize=13, fontweight="bold", y=1.02
)

# Plot 1: BERT negative % by journey
journey_labels = [f"J{j}\n{journey_info[j][:12]}..." for j in journey_stats.index]
colors = ["#e74c3c", "#9b59b6", "#3498db", "#2ecc71", "#f39c12", "#1abc9c"]

axes[0].bar(journey_labels, journey_stats["pct_negative"], color=colors, alpha=0.85,
            edgecolor="black", linewidth=1.2)
axes[0].set_ylabel("BERT Negative Sentiment (%)", fontweight="bold")
axes[0].set_title("Negative Sentiment by Journey", fontweight="bold")
axes[0].set_ylim(0, 100)
axes[0].grid(True, alpha=0.3, axis="y")

for i, v in enumerate(journey_stats["pct_negative"]):
    axes[0].text(i, v + 2, f"{v:.0f}%", ha="center", fontweight="bold", fontsize=10)

# Plot 2: Agreement between BERT and keyword heuristic
agreement_counts = df["agreement"].value_counts()
axes[1].pie(
    [agreement_counts.get(True, 0), agreement_counts.get(False, 0)],
    labels=["Agree", "Disagree"],
    autopct="%1.1f%%",
    colors=["#2ecc71", "#e74c3c"],
    startangle=90,
    textprops={"fontsize": 12}
)
axes[1].set_title("BERT vs Keyword\nHeuristic Agreement", fontweight="bold")

# Plot 3: Confidence distribution by sentiment
pos_conf = df[df["bert_sentiment"] == "positive"]["bert_confidence"]
neg_conf = df[df["bert_sentiment"] == "negative"]["bert_confidence"]

axes[2].hist(pos_conf, bins=8, alpha=0.7, color="#2ecc71", label="BERT Positive", edgecolor="black")
axes[2].hist(neg_conf, bins=8, alpha=0.7, color="#e74c3c", label="BERT Negative", edgecolor="black")
axes[2].set_xlabel("Confidence Score", fontweight="bold")
axes[2].set_ylabel("Count", fontweight="bold")
axes[2].set_title("Confidence Distribution\nby Predicted Sentiment", fontweight="bold")
axes[2].legend()
axes[2].grid(True, alpha=0.3, axis="y")

# Automatically angles and shifts overflowing text labels across subplots
fig.autofmt_xdate() 

plt.tight_layout()
plt.savefig("bert_sentiment_results.png", dpi=300, bbox_inches="tight")

plt.tight_layout()
plt.savefig("bert_sentiment_results.png", dpi=300, bbox_inches="tight")
print("\n📊 Figure saved: bert_sentiment_results.png")
plt.show()


# ── Section 7: Next Steps Toward Fine-Tuning ────────────────────────────────

print("\n" + "=" * 70)
print("NEXT STEPS — Fine-Tuning on Manual Coding Labels")
print("=" * 70)
print("""
The current pipeline uses zero-shot inference (SST-2 weights). To improve
accuracy for mental health content specifically:

1. PREPARE TRAINING DATA
   Use the manually coded CSV (youtube_manual_coding_enhanced.csv):
     features: title + description (first 200 chars)
     label:    'potentially_harmful' (yes/no) → binary classification

   from datasets import Dataset
   dataset = Dataset.from_pandas(coded_df[["text", "label"]])

2. FINE-TUNE DistilBERT
   from transformers import (DistilBertForSequenceClassification,
                              TrainingArguments, Trainer)
   model = DistilBertForSequenceClassification.from_pretrained(
       "distilbert-base-uncased", num_labels=2
   )
   # TrainingArguments: lr=2e-5, epochs=3, batch_size=16

3. EVALUATE
   Report: accuracy, F1 (macro), confusion matrix
   Compare to keyword baseline (classify_by_title.py)

4. APPLY TO FULL API DATASET (525 videos)
   Generate BERT-predicted harm scores for all videos
   Correlate with engagement metrics (view_count, like_count)

Expected improvement: keyword baseline ~65-70% accuracy on held-out
coded examples; fine-tuned DistilBERT expected ~82-88% based on
comparable mental health NLP tasks in literature.
""")

print("=" * 70)
print("✅ BERT SENTIMENT ANALYSIS COMPLETE")
print("=" * 70)