# skill_extractor.py  v4.2
# ─────────────────────────────────────────────────────────────────────────────
# Single source of truth for all skill extraction logic.
#
# Public API:
#   extract_skills(text, jd_skills=None)  → list[dict]
#   load_onet_index(skills_file)          → None  (called once at startup)
#
# Changes in v4.2:
#   [1] Full debug logging throughout every extraction step.
#   [2] _NOISE expanded — generic O*NET cognitive/soft-skill labels added
#       ("science", "mathematics", "reading", "judgment" etc.) that only
#       make sense as part of a multi-word phrase, never as a standalone skill.
#   [3] load_onet_index() has a guard that skips pure-alpha single words
#       under 8 chars not in _SHORT_ALLOWLIST — prevents O*NET entries like
#       "Science", "Reading", "Judgment" from polluting the index.
# ─────────────────────────────────────────────────────────────────────────────

import os
import re
import json
from pathlib import Path

import torch
import numpy as np
import pandas as pd
from torch.utils.data import Dataset, ConcatDataset
from sklearn.model_selection import train_test_split
from transformers import (
    AutoTokenizer,
    AutoModelForTokenClassification,
    TrainingArguments,
    Trainer,
    DataCollatorForTokenClassification,
    pipeline as hf_pipeline,
)
from seqeval.metrics import classification_report, f1_score

# ── Logging ───────────────────────────────────────────────────────────────────

def _log(level: str, fn: str, msg: str) -> None:
    print(f"[skill_extractor:{fn}] {level:<5}  {msg}")

def _info(fn, msg):  _log("INFO",  fn, msg)
def _warn(fn, msg):  _log("WARN",  fn, msg)
def _debug(fn, msg): _log("DEBUG", fn, msg)

# ── Config ────────────────────────────────────────────────────────────────────

BASE_MODEL  = "dslim/bert-base-NER"
OUTPUT_DIR  = "models/skill_extractor"
RESUME_FILE = "data/Resume.csv"
SKILLS_FILE = "data/Skills.xlsx"
TRAIN_JSONL = "data/train.jsonl"
VAL_JSONL   = "data/val.jsonl"
MAX_LEN     = 256
BATCH_SIZE  = 16
EPOCHS      = 3
LR          = 2e-5
VAL_SPLIT   = 0.1

# ── Label schema ──────────────────────────────────────────────────────────────

LABELS   = ["O", "B-SKILL", "I-SKILL", "B-EXPERIENCE", "I-EXPERIENCE", "B-EDUCATION", "I-EDUCATION"]
LABEL2ID = {l: i for i, l in enumerate(LABELS)}
ID2LABEL = {i: l for l, i in LABEL2ID.items()}

# ── Skill taxonomy ────────────────────────────────────────────────────────────

SKILL_TAXONOMY = {
    "Python":           ("Programming",     ["tech", "ml", "data"]),
    "SQL":              ("Database",         ["tech", "data", "finance"]),
    "JavaScript":       ("Programming",     ["tech", "web"]),
    "TypeScript":       ("Programming",     ["tech", "web"]),
    "Java":             ("Programming",     ["tech"]),
    "C++":              ("Programming",     ["tech"]),
    "C#":               ("Programming",     ["tech"]),
    "Go":               ("Programming",     ["tech"]),
    "Rust":             ("Programming",     ["tech"]),
    "Scala":            ("Programming",     ["tech", "data"]),
    "R":                ("Programming",     ["data", "statistics"]),
    "MATLAB":           ("Programming",     ["science"]),
    "VBA":              ("Programming",     ["finance"]),
    "Bash":             ("Tools",           ["tech"]),
    "PHP":              ("Programming",     ["web"]),
    "Ruby":             ("Programming",     ["web"]),
    "Swift":            ("Programming",     ["mobile"]),
    "Kotlin":           ("Programming",     ["mobile"]),
    "HTML":             ("Frontend",        ["web"]),
    "CSS":              ("Frontend",        ["web"]),
    "React":            ("Frontend",        ["web"]),
    "Vue":              ("Frontend",        ["web"]),
    "Angular":          ("Frontend",        ["web"]),
    "Next.js":          ("Frontend",        ["web"]),
    "Node.js":          ("Backend",         ["web"]),
    "jQuery":           ("Frontend",        ["web"]),
    "Bootstrap":        ("Frontend",        ["web"]),
    "Tailwind":         ("Frontend",        ["web"]),
    "Redux":            ("Frontend",        ["web"]),
    "GraphQL":          ("Backend",         ["web"]),
    "REST APIs":        ("Backend",         ["tech"]),
    "WebSockets":       ("Backend",         ["tech"]),
    "FastAPI":          ("Backend",         ["tech", "ml"]),
    "Flask":            ("Backend",         ["tech", "ml"]),
    "Django":           ("Backend",         ["tech"]),
    "Spring Boot":      ("Backend",         ["tech"]),
    "Express":          ("Backend",         ["web"]),
    "JWT":              ("Security",        ["tech"]),
    "OAuth":            ("Security",        ["tech"]),
    "OAuth2":           ("Security",        ["tech"]),
    "Auth0":            ("Security",        ["tech"]),
    "Microservices":    ("Backend",         ["tech"]),
    "gRPC":             ("Backend",         ["tech"]),
    "PyTorch":          ("ML Frameworks",   ["ml"]),
    "TensorFlow":       ("ML Frameworks",   ["ml"]),
    "Keras":            ("ML Frameworks",   ["ml"]),
    "Scikit-learn":     ("ML Libraries",    ["ml", "data"]),
    "XGBoost":          ("ML Libraries",    ["ml", "data"]),
    "LightGBM":         ("ML Libraries",    ["ml", "data"]),
    "CatBoost":         ("ML Libraries",    ["ml", "data"]),
    "Hugging Face":     ("NLP",             ["ml", "nlp"]),
    "BERT":             ("NLP",             ["ml", "nlp"]),
    "GPT":              ("NLP",             ["ml", "nlp"]),
    "LLM":              ("NLP",             ["ml", "nlp"]),
    "NLP":              ("NLP",             ["ml", "nlp"]),
    "Computer Vision":  ("ML",              ["ml"]),
    "OpenCV":           ("ML",              ["ml"]),
    "LangChain":        ("AI Tools",        ["ml", "nlp"]),
    "LlamaIndex":       ("AI Tools",        ["ml", "nlp"]),
    "Machine Learning": ("ML",              ["ml"]),
    "Deep Learning":    ("ML",              ["ml"]),
    "Reinforcement Learning": ("ML",        ["ml"]),
    "Transfer Learning":("ML",              ["ml"]),
    "Feature Engineering": ("ML",           ["ml", "data"]),
    "Model Deployment": ("MLOps",           ["ml"]),
    "Pandas":           ("Data Libraries",  ["data", "ml"]),
    "NumPy":            ("Data Libraries",  ["data", "ml"]),
    "Matplotlib":       ("Visualization",   ["data"]),
    "Seaborn":          ("Visualization",   ["data"]),
    "Plotly":           ("Visualization",   ["data"]),
    "SciPy":            ("Data Libraries",  ["data"]),
    "Kafka":            ("Data Streaming",  ["data", "tech"]),
    "Spark":            ("Big Data",        ["data"]),
    "PySpark":          ("Big Data",        ["data"]),
    "Dask":             ("Big Data",        ["data", "ml"]),
    "Flink":            ("Data Streaming",  ["data"]),
    "Airflow":          ("MLOps",           ["data", "ml"]),
    "dbt":              ("Data Engineering",["data"]),
    "Prefect":          ("Data Engineering",["data"]),
    "Hadoop":           ("Big Data",        ["data"]),
    "Databricks":       ("Data Engineering",["data", "ml"]),
    "Delta Lake":       ("Data Engineering",["data"]),
    "PostgreSQL":       ("Database",        ["tech", "data"]),
    "MySQL":            ("Database",        ["tech"]),
    "SQLite":           ("Database",        ["tech"]),
    "MongoDB":          ("Database",        ["tech"]),
    "Redis":            ("Database",        ["tech"]),
    "Cassandra":        ("Database",        ["tech"]),
    "DynamoDB":         ("Database",        ["tech", "cloud"]),
    "Elasticsearch":    ("Database",        ["tech"]),
    "Neo4j":            ("Database",        ["tech"]),
    "Firestore":        ("Database",        ["tech"]),
    "Snowflake":        ("Data Warehouse",  ["data", "finance"]),
    "BigQuery":         ("Data Warehouse",  ["data"]),
    "Redshift":         ("Data Warehouse",  ["data"]),
    "AWS":              ("Cloud",           ["tech", "ml"]),
    "GCP":              ("Cloud",           ["tech"]),
    "Azure":            ("Cloud",           ["tech"]),
    "EC2":              ("Cloud",           ["tech"]),
    "S3":               ("Cloud",           ["tech"]),
    "Lambda":           ("Cloud",           ["tech"]),
    "SageMaker":        ("Cloud",           ["ml"]),
    "Docker":           ("DevOps",          ["tech", "ml"]),
    "Kubernetes":       ("DevOps",          ["tech", "ml"]),
    "Terraform":        ("DevOps",          ["tech"]),
    "Ansible":          ("DevOps",          ["tech"]),
    "Helm":             ("DevOps",          ["tech"]),
    "Jenkins":          ("DevOps",          ["tech"]),
    "GitHub Actions":   ("DevOps",          ["tech"]),
    "CircleCI":         ("DevOps",          ["tech"]),
    "ArgoCD":           ("DevOps",          ["tech"]),
    "CI/CD":            ("DevOps",          ["tech"]),
    "Nginx":            ("DevOps",          ["tech"]),
    "MLflow":           ("MLOps",           ["ml"]),
    "Kubeflow":         ("MLOps",           ["ml"]),
    "DVC":              ("MLOps",           ["ml"]),
    "Feast":            ("MLOps",           ["ml"]),
    "Tecton":           ("MLOps",           ["ml"]),
    "Pinecone":         ("Vector DB",       ["ml"]),
    "Weaviate":         ("Vector DB",       ["ml"]),
    "Chroma":           ("Vector DB",       ["ml"]),
    "FAISS":            ("Vector DB",       ["ml"]),
    "Git":              ("Tools",           ["tech"]),
    "GitHub":           ("Tools",           ["tech"]),
    "GitLab":           ("Tools",           ["tech"]),
    "Jira":             ("Tools",           ["tech"]),
    "Confluence":       ("Tools",           ["tech"]),
    "Notion":           ("Tools",           ["tech"]),
    "Postman":          ("Tools",           ["tech"]),
    "Jupyter":          ("Tools",           ["data", "ml"]),
    "Linux":            ("Tools",           ["tech"]),
    "Tableau":          ("Visualization",   ["data", "finance", "marketing"]),
    "Power BI":         ("Visualization",   ["data", "finance"]),
    "Looker":           ("Visualization",   ["data", "marketing"]),
    "Metabase":         ("Visualization",   ["data"]),
    "Grafana":          ("Monitoring",      ["tech"]),
    "Datadog":          ("Monitoring",      ["tech"]),
    "Prometheus":       ("Monitoring",      ["tech"]),
    "Pytest":           ("Testing",         ["tech"]),
    "Jest":             ("Testing",         ["web"]),
    "Selenium":         ("Testing",         ["web"]),
    "Cypress":          ("Testing",         ["web"]),
    "DCF":              ("Finance",         ["finance"]),
    "LBO":              ("Finance",         ["finance"]),
    "Financial Modelling": ("Finance",      ["finance"]),
    "Valuation":        ("Finance",         ["finance"]),
    "Due Diligence":    ("Finance",         ["finance"]),
    "Bloomberg Terminal": ("Finance",       ["finance"]),
    "Bloomberg":        ("Finance",         ["finance"]),
    "Capital IQ":       ("Finance",         ["finance"]),
    "FactSet":          ("Finance",         ["finance"]),
    "Comparable Company Analysis": ("Finance", ["finance"]),
    "Precedent Transactions": ("Finance",   ["finance"]),
    "Pitch Books":      ("Finance",         ["finance"]),
    "Credit Analysis":  ("Finance",         ["finance"]),
    "Debt Structuring": ("Finance",         ["finance"]),
    "Portfolio Management": ("Finance",     ["finance"]),
    "Risk Management":  ("Finance",         ["finance"]),
    "Financial Statement Analysis": ("Finance", ["finance"]),
    "IFRS":             ("Accounting",      ["finance"]),
    "Ind AS":           ("Accounting",      ["finance"]),
    "GAAP":             ("Accounting",      ["finance"]),
    "Private Equity":   ("Finance",         ["finance"]),
    "Equity Research":  ("Finance",         ["finance"]),
    "ESG":              ("Finance",         ["finance"]),
    "CFA":              ("Certification",   ["finance"]),
    "FRM":              ("Certification",   ["finance"]),
    "Excel":            ("Tools",           ["finance", "data"]),
    "PowerPoint":       ("Tools",           ["finance"]),
    "SEO":              ("Marketing",       ["marketing"]),
    "SEM":              ("Marketing",       ["marketing"]),
    "Google Ads":       ("Marketing",       ["marketing"]),
    "Meta Ads":         ("Marketing",       ["marketing"]),
    "Facebook Ads":     ("Marketing",       ["marketing"]),
    "Email Marketing":  ("Marketing",       ["marketing"]),
    "Content Strategy": ("Marketing",       ["marketing"]),
    "Social Media Marketing": ("Marketing", ["marketing"]),
    "Performance Marketing": ("Marketing",  ["marketing"]),
    "Growth Marketing": ("Marketing",       ["marketing"]),
    "A/B Testing":      ("Analytics",       ["marketing", "data"]),
    "Google Analytics": ("Analytics",       ["marketing", "data"]),
    "Google Analytics 4": ("Analytics",     ["marketing"]),
    "Mixpanel":         ("Analytics",       ["marketing", "data"]),
    "Amplitude":        ("Analytics",       ["marketing"]),
    "HubSpot":          ("CRM",             ["marketing"]),
    "Salesforce":       ("CRM",             ["marketing", "finance"]),
    "Marketo":          ("CRM",             ["marketing"]),
    "Braze":            ("CRM",             ["marketing"]),
    "Clevertap":        ("CRM",             ["marketing"]),
    "Mailchimp":        ("CRM",             ["marketing"]),
    "SEMrush":          ("Marketing Tools", ["marketing"]),
    "Ahrefs":           ("Marketing Tools", ["marketing"]),
    "AppsFlyer":        ("Marketing Tools", ["marketing"]),
    "Adjust":           ("Marketing Tools", ["marketing"]),
    "App Store Optimisation": ("Marketing", ["marketing"]),
    "ASO":              ("Marketing",       ["marketing"]),
    "Attribution Modelling": ("Analytics",  ["marketing"]),
    "Cohort Analysis":  ("Analytics",       ["marketing", "data"]),
    "Lifecycle Marketing": ("Marketing",    ["marketing"]),
    "Programmatic Advertising": ("Marketing", ["marketing"]),
    "Segment":          ("Data Tools",      ["marketing", "data"]),
    "mParticle":        ("Data Tools",      ["marketing"]),
    "Optimizely":       ("Marketing Tools", ["marketing"]),
    "Figma":            ("Design",          ["design"]),
    "Sketch":           ("Design",          ["design"]),
    "Adobe XD":         ("Design",          ["design"]),
    "Canva":            ("Design",          ["design", "marketing"]),
    "Wireframing":      ("Design",          ["design"]),
    "Prototyping":      ("Design",          ["design"]),
    "User Research":    ("Product",         ["product"]),
    "Product Management": ("Product",       ["product"]),
    "Agile":            ("Practices",       ["tech"]),
    "Scrum":            ("Practices",       ["tech"]),
    "Kanban":           ("Practices",       ["tech"]),
    "System Design":    ("Practices",       ["tech"]),
    "HCI":              ("Design",          ["design", "product"]),
    "InVision":         ("Design",          ["design"]),
    "Zeplin":           ("Design",          ["design"]),
    "Miro":             ("Tools",           ["product", "design"]),
    "Hotjar":           ("Analytics",       ["product", "marketing"]),
    "Dribbble":         ("Design",          ["design"]),
}

# Lowercase lookup: "python" → "Python"
SKILL_INDEX: dict[str, str] = {k.lower(): k for k in SKILL_TAXONOMY}

# Derived keyword list longest-first (prevents substring shadowing)
_SKILL_KEYWORDS: list[str] = sorted(SKILL_TAXONOMY.keys(), key=len, reverse=True)

# Short skills requiring extra context validation before accepting
_SHORT_ALLOWLIST = {
    "sql", "git", "aws", "gcp", "css", "html", "php", "r", "go", "vba", "jwt",
    "dvc", "nlp", "llm", "aso", "esg", "cfa", "frm", "dbt", "api", "hci",
}

# Words that must never be extracted as standalone skills.
# Three categories:
#   1. Single letters and generic verbs/adjectives
#   2. Role/title words that bleed from job descriptions
#   3. Generic O*NET labels that are only meaningful inside a longer phrase
#      ("Computer Science", "Data Science"). As unigrams they're noise.
_NOISE: set[str] = {
    # Single letters
    "a", "b", "c", "d", "e", "f", "g", "h", "i", "j", "k", "l", "m",
    "n", "o", "p", "q", "s", "t", "u", "v", "w", "x", "y", "z",
    # Generic verbs / adjectives from bullet points
    "growth", "scale", "impact", "drive", "lead", "manage", "build",
    "strong", "deep", "broad", "large", "good", "great", "solid",
    "process", "service", "quality", "performance", "operations",
    "support", "planning", "monitoring", "reporting",
    "communication", "training", "review",
    # Role / title words
    "analyst", "manager", "engineer", "developer", "designer",
    "senior", "junior", "head", "director", "associate", "intern", "consultant",
    # Qualification words that aren't skills
    "mba", "phd", "ca", "degree", "bachelor", "master", "preferred",
    # Ambiguous abbreviations (too many false positives as unigrams)
    "rds", "ecs", "eks", "iam", "cdn", "b2b", "b2c", "saas", "fmcg", "sme",
    "roi", "kpi", "okr", "dsp", "cdp",
    # Company names that appear in O*NET / resume context
    "google", "meta", "amazon", "microsoft", "apple",
    # Generic O*NET cognitive/soft-skill labels — only meaningful in a phrase
    "science", "mathematics", "statistics", "technology", "engineering",
    "arts", "commerce", "economics", "biology", "chemistry", "physics",
    "reading", "writing", "speaking", "listening", "learning",
    "judgment", "reasoning", "coordination", "persuasion",
    "negotiation", "instruction", "operation",
}

# ── O*NET vocab index ─────────────────────────────────────────────────────────

_onet_index: dict[str, str] = dict(SKILL_INDEX)  # starts with taxonomy


def load_onet_index(skills_file: str = SKILLS_FILE) -> None:
    """Extend _onet_index with O*NET skills. Called once at server startup."""
    global _onet_index
    fn = "load_onet_index"
    try:
        xlsx = Path(skills_file)
        csv  = Path("data/onet_skills.csv")
        if xlsx.exists():
            _info(fn, f"Loading Skills.xlsx from {skills_file}")
            df  = pd.read_excel(xlsx)
            col = next((c for c in df.columns
                        if "element" in c.lower() and "name" in c.lower()), df.columns[3])
            _info(fn, f"Using column '{col}' ({len(df)} rows)")
        elif csv.exists():
            _info(fn, "Skills.xlsx not found — falling back to onet_skills.csv")
            df, col = pd.read_csv(csv), "Element Name"
        else:
            _warn(fn, "No O*NET file found — index will use taxonomy only")
            return

        added = 0
        for term in df[col].dropna().str.strip().unique():
            if not isinstance(term, str):
                continue
            lc = term.lower().strip()
            if not (2 < len(lc) < 80):
                continue
            if lc in _onet_index or lc in _NOISE:
                continue
            # Guard: skip pure-alpha single words under 8 chars that aren't in
            # the short allowlist. These are O*NET cognitive/soft-skill labels
            # ("Science", "Reading", "Judgment") that match far too broadly as
            # unigrams. Multi-word terms (e.g. "Active Listening") are fine.
            words = lc.split()
            if (len(words) == 1
                    and lc.isalpha()
                    and len(lc) < 8
                    and lc not in _SHORT_ALLOWLIST):
                continue
            _onet_index[lc] = term
            added += 1

        _info(fn, f"O*NET index ready: {len(_onet_index)} terms total ({added} added from file)")

    except Exception as e:
        _warn(fn, f"O*NET load failed: {e} — index will use taxonomy only")


# ── Token helpers ─────────────────────────────────────────────────────────────

def _clean_token(tok: str) -> str:
    """Strip leading/trailing punctuation before ngram assembly."""
    return re.sub(r"^[^\w+#./&-]+|[^\w+#./&-]+$", "", tok)


def _valid_short(term: str, text: str) -> bool:
    """Extra validation for short terms (≤4 chars) — require list context."""
    if term.lower() not in _SHORT_ALLOWLIST:
        return False
    pat = r"(?<![a-zA-Z0-9])" + re.escape(term) + r"(?![a-zA-Z0-9])"
    if not re.search(pat, text, re.IGNORECASE):
        return False
    if len(term) <= 2:
        ctx = r"(skills|languages|tools|stack)[^\n]{0,200}" + re.escape(term.lower())
        sep = r"[,/|•]\s*" + re.escape(term.lower()) + r"\s*[,/|•\n]"
        if not (re.search(ctx, text.lower()) or re.search(sep, text.lower())):
            _debug("_valid_short", f"Rejected short term '{term}' — no list context found")
            return False
    return True


# ── Level inference ───────────────────────────────────────────────────────────

def infer_level(skill: str, text: str) -> str:
    fn    = "infer_level"
    pat   = r"(?<![a-zA-Z0-9])" + re.escape(skill) + r"(?![a-zA-Z0-9])"
    count = len(re.findall(pat, text, re.IGNORECASE))
    idx   = re.search(pat, text, re.IGNORECASE)
    pos   = idx.start() if idx else -1
    ctx   = text[max(0, pos - 400): pos + 400].lower() if pos >= 0 else ""

    level = "beginner"

    if count >= 1 and any(w in ctx for w in [
        "senior", "lead", "expert", "head of", "principal", "architect",
        "5+ year", "6+ year", "7+ year", "8+ year",
    ]):
        level = "advanced"
    elif count >= 1 and any(w in ctx for w in [
        "proficient", "3+ year", "4+ year", "strong", "extensive",
    ]):
        level = "intermediate"
    elif count >= 4:
        level = "advanced"
    elif count >= 2:
        level = "intermediate"
    else:
        yrs = [int(y) for y in re.findall(r"(\d+)\s*\+?\s*year", text.lower()) if int(y) < 30]
        my  = max(yrs, default=0)
        if my >= 4 and count >= 1:
            level = "advanced"
        elif my >= 2 and count >= 1:
            level = "intermediate"
        else:
            m = re.search(
                r"(skills|competencies|expertise|technologies|tools)[^\n]{0,50}\n([\s\S]{0,1000})",
                text.lower(),
            )
            if m and re.search(pat, m.group(2), re.IGNORECASE):
                level = "intermediate"

    _debug(fn, f"'{skill}' → {level} (mentions={count}, ctx_len={len(ctx)})")
    return level


# ── Lexicon scan ──────────────────────────────────────────────────────────────

def _lexicon_scan(text: str, jd_skills: list[str] | None = None) -> list[str]:
    fn    = "_lexicon_scan"
    found: list[str] = []
    seen:  set[str]  = set()
    noise_hits:     list[str] = []
    short_rejected: list[str] = []

    def add(name: str) -> None:
        canon = SKILL_INDEX.get(name.lower(), name)
        lc    = canon.lower()
        if lc in _NOISE:
            noise_hits.append(canon)
            return
        if lc not in seen:
            found.append(canon)
            seen.add(lc)

    raw_tokens = re.split(r"\s+", text.strip())
    tokens     = [_clean_token(t) for t in raw_tokens]
    _debug(fn, f"Tokenised input: {len(tokens)} tokens")

    for i in range(len(tokens)):
        for size in (3, 2, 1):
            chunk = tokens[i: i + size]
            if len(chunk) < size:
                break
            ngram = " ".join(chunk).lower()
            if not ngram or ngram in seen or ngram in _NOISE:
                continue
            if ngram in _onet_index:
                orig = _onet_index[ngram]
                if len(ngram) <= 4 and not _valid_short(ngram, text):
                    short_rejected.append(ngram)
                    continue
                add(orig)
                break

    if jd_skills:
        tl      = text.lower()
        jd_added = []
        for s in jd_skills:
            if s.lower() in seen:
                continue
            pat = r"(?<![a-zA-Z])" + re.escape(s.lower()) + r"(?![a-zA-Z])"
            if re.search(pat, tl):
                add(s)
                jd_added.append(s)
        if jd_added:
            _debug(fn, f"JD-guided additions: {jd_added}")

    if noise_hits:
        _debug(fn, f"Noise-filtered (not added): {sorted(set(noise_hits))}")
    if short_rejected:
        _debug(fn, f"Short-term rejected (no list context): {short_rejected}")

    _info(fn, f"Lexicon scan found {len(found)} skills: {found}")
    return found


def _keyword_regex_scan(text: str, already_seen: set[str]) -> list[str]:
    fn    = "_keyword_regex_scan"
    found: list[str] = []
    tl    = text.lower()

    for kw in _SKILL_KEYWORDS:
        lc = kw.lower()
        if lc in already_seen:
            continue
        if any(lc in f.lower() for f in found):
            continue
        pat = r"(?<![a-zA-Z0-9])" + re.escape(lc) + r"(?![a-zA-Z0-9])"
        if re.search(pat, tl):
            found.append(kw)
            already_seen.add(lc)

    if found:
        _info(fn, f"Keyword regex added {len(found)} skills: {found}")
    else:
        _debug(fn, "Keyword regex scan: nothing new added")
    return found


# ── NER pipeline ──────────────────────────────────────────────────────────────

_NER_PIPELINE: dict[str, object] = {}


def _ner_scan(text: str) -> list[str]:
    fn           = "_ner_scan"
    using_base   = not Path(OUTPUT_DIR).exists()
    active_model = BASE_MODEL if using_base else OUTPUT_DIR

    if using_base:
        _warn(fn, f"Fine-tuned model not found at '{OUTPUT_DIR}' — using base model '{BASE_MODEL}'")
        _warn(fn, "Base model uses CoNLL labels (PER/ORG/LOC/MISC), not SKILL — results will be noisy")
    else:
        _info(fn, f"Using fine-tuned model at '{OUTPUT_DIR}'")

    if active_model not in _NER_PIPELINE:
        _info(fn, f"Loading NER pipeline from {active_model} (one-time)…")
        _NER_PIPELINE[active_model] = hf_pipeline(
            "ner", model=active_model, aggregation_strategy="simple"
        )
        _info(fn, "NER pipeline loaded and cached")

    pipe  = _NER_PIPELINE[active_model]
    trunc = text[:512]
    if len(text) > 512:
        _warn(fn, f"Input truncated from {len(text)} to 512 chars — skills in later sections may be missed")

    results = pipe(trunc)
    _debug(fn, f"Raw NER output ({len(results)} entities): "
               f"{[(r['entity_group'], r['word'], round(r['score'], 3)) for r in results]}")

    skills: list[str] = []
    seen:   set[str]  = set()
    skipped: list[tuple] = []

    for r in results:
        label = r["entity_group"]
        word  = r["word"].strip()
        score = round(r["score"], 3)
        if not word or word.lower() in seen:
            continue
        seen.add(word.lower())

        if label == "SKILL":
            skills.append(word)
            _debug(fn, f"  ACCEPTED  '{word}' (label=SKILL, score={score})")
        elif label in ("MISC", "ORG") and using_base:
            skills.append(word)
            _warn(fn, f"  FALLBACK  '{word}' (label={label}, score={score}) — base model remap, may be noise")
        else:
            skipped.append((word, label, score))

    if skipped:
        _debug(fn, f"NER entities skipped (wrong label): {skipped}")

    _info(fn, f"NER scan produced {len(skills)} skill candidates: {skills}")
    return skills


# ── Public API ────────────────────────────────────────────────────────────────

def extract_skills(text: str, jd_skills: list[str] | None = None) -> list[dict]:
    fn = "extract_skills"
    _info(fn, f"Starting — text length={len(text)}, jd_skills={len(jd_skills) if jd_skills else 0}")

    if not text.strip():
        _warn(fn, "Empty text — returning []")
        return []

    _info(fn, "─── Step 1: lexicon scan")
    lexicon_skills = _lexicon_scan(text, jd_skills)
    seen: set[str] = {s.lower() for s in lexicon_skills}

    _info(fn, "─── Step 2: NER scan")
    ner_skills: list[str] = []
    try:
        raw_ner = _ner_scan(text)
        for s in raw_ner:
            lc = s.lower()
            if lc in seen:
                _debug(fn, f"NER duplicate skipped: '{s}'")
                continue
            if lc in _NOISE:
                _debug(fn, f"NER noise filtered: '{s}'")
                continue
            canon = SKILL_INDEX.get(lc, s)
            if canon != s:
                _debug(fn, f"NER canonicalised: '{s}' → '{canon}'")
            ner_skills.append(canon)
            seen.add(canon.lower())
        _info(fn, f"NER contributed {len(ner_skills)} new skills: {ner_skills}")
    except Exception as e:
        _warn(fn, f"NER scan failed and was skipped: {e}")

    _info(fn, "─── Step 3: keyword regex scan")
    kw_skills = _keyword_regex_scan(text, seen)

    all_skills = lexicon_skills + ner_skills + kw_skills
    _info(fn, f"─── Merge: {len(lexicon_skills)} lexicon + {len(ner_skills)} NER "
              f"+ {len(kw_skills)} regex = {len(all_skills)} total")

    result: list[dict] = []
    for name in all_skills:
        category, _ = SKILL_TAXONOMY.get(name, ("Technical", []))
        result.append({
            "name":     name,
            "level":    infer_level(name, text),
            "category": category,
        })

    _info(fn, f"Final output: {len(result)} skills")
    _info(fn, f"Skills list: {[s['name'] for s in result]}")
    return result


# ── Training helpers ──────────────────────────────────────────────────────────

_TITLE_WORDS = {
    "engineer", "developer", "scientist", "analyst", "architect", "manager",
    "director", "lead", "head", "consultant", "specialist", "associate",
    "intern", "executive", "officer", "president", "vp", "cto", "ceo",
    "designer", "researcher", "administrator", "coordinator",
}

_DEGREE_WORDS = {
    "bachelor", "master", "phd", "doctorate", "b.tech", "m.tech", "b.e",
    "m.e", "b.sc", "m.sc", "mba", "bba", "b.com", "m.com", "be", "me",
    "b.s", "m.s", "bs", "ms", "diploma",
}


def _load_skill_vocab(skills_file: str = SKILLS_FILE) -> set[str]:
    df        = pd.read_excel(skills_file)
    skill_col = next(
        (c for c in df.columns if c.strip().lower() == "element name"),
        df.select_dtypes(include="object").columns[-1],
    )
    vocab = set(df[skill_col].dropna().str.lower().str.strip())
    _info("_load_skill_vocab", f"Loaded {len(vocab)} terms from '{skill_col}'")
    return vocab


def _tag_resume(text: str, skill_vocab: set[str]) -> tuple[list[str], list[str]]:
    words  = text.split()
    labels = ["O"] * len(words)
    i = 0
    while i < len(words):
        clean = _clean_token(words[i]).lower()
        if i + 1 < len(words):
            clean_next = _clean_token(words[i + 1]).lower()
            bigram     = clean + " " + clean_next
            if bigram in skill_vocab:
                labels[i]     = "B-SKILL"
                labels[i + 1] = "I-SKILL"
                i += 2
                continue
        if clean in skill_vocab:
            labels[i] = "B-SKILL"
            i += 1
            continue
        if clean in _TITLE_WORDS:
            labels[i] = "B-EXPERIENCE"
            j = i + 1
            while j < len(words) and j < i + 5:
                w = _clean_token(words[j]).lower()
                if w in ("at", "—", "-") or w.isdigit():
                    labels[j] = "I-EXPERIENCE"
                    j += 1
                else:
                    break
            i = j
            continue
        if clean in _DEGREE_WORDS:
            labels[i] = "B-EDUCATION"
            j = i + 1
            while j < len(words) and j < i + 6:
                w = _clean_token(words[j]).lower()
                if w in ("of", "in", "and", "science", "engineering", "technology",
                         "arts", "commerce", "computer", "information", "marketing",
                         "finance", "economics", "mathematics", "statistics"):
                    labels[j] = "I-EDUCATION"
                    j += 1
                else:
                    break
            i = j
            continue
        i += 1
    return words, labels


class _JsonlNERDataset(Dataset):
    def __init__(self, jsonl_path: str, tokenizer, max_len: int = MAX_LEN):
        self.examples = []
        path = Path(jsonl_path)
        if not path.exists():
            _warn("_JsonlNERDataset", f"{jsonl_path} not found — skipping")
            return
        lines = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        skipped = 0
        for row in lines:
            tokens, str_labels = row["tokens"], row["labels"]
            if any(l not in LABEL2ID for l in str_labels):
                skipped += 1
                continue
            self.examples.append(self._encode(tokens, str_labels, tokenizer, max_len))
        _info("_JsonlNERDataset",
              f"Loaded {len(self.examples)} examples from {jsonl_path} ({skipped} skipped)")

    def _encode(self, tokens, str_labels, tokenizer, max_len):
        enc      = tokenizer(tokens, is_split_into_words=True,
                             truncation=True, max_length=max_len, padding="max_length")
        word_ids = enc.word_ids()
        aligned, prev = [], None
        for wid in word_ids:
            if wid is None:
                aligned.append(-100)
            elif wid != prev:
                aligned.append(LABEL2ID[str_labels[wid]])
            else:
                lbl = str_labels[wid]
                aligned.append(LABEL2ID["I-" + lbl[2:]] if lbl.startswith("B-") else LABEL2ID[lbl])
            prev = wid
        enc["labels"] = aligned
        return {k: torch.tensor(v) for k, v in enc.items()}

    def __len__(self):        return len(self.examples)
    def __getitem__(self, i): return self.examples[i]


class _ResumeNERDataset(Dataset):
    def __init__(self, texts: list[str], tokenizer, skill_vocab: set[str],
                 max_len: int = MAX_LEN):
        self.examples = []
        _info("_ResumeNERDataset", f"Encoding {len(texts)} resumes…")
        for text in texts:
            text = str(text)[:2000]
            words, word_labels = _tag_resume(text, skill_vocab)
            if words:
                self.examples.append(self._encode(words, word_labels, tokenizer, max_len))
        _info("_ResumeNERDataset", f"Encoded {len(self.examples)} examples")

    def _encode(self, tokens, labels, tokenizer, max_len):
        enc      = tokenizer(tokens, is_split_into_words=True,
                             truncation=True, max_length=max_len, padding="max_length")
        word_ids = enc.word_ids()
        aligned, prev = [], None
        for wid in word_ids:
            if wid is None:
                aligned.append(-100)
            elif wid != prev:
                lbl = labels[wid] if wid < len(labels) else "O"
                aligned.append(LABEL2ID[lbl])
            else:
                lbl = labels[wid] if wid < len(labels) else "O"
                aligned.append(LABEL2ID["I-" + lbl[2:]] if lbl.startswith("B-") else LABEL2ID[lbl])
            prev = wid
        enc["labels"] = aligned
        return {k: torch.tensor(v) for k, v in enc.items()}

    def __len__(self):        return len(self.examples)
    def __getitem__(self, i): return self.examples[i]


def _compute_metrics(p):
    preds, label_ids = p
    preds = np.argmax(preds, axis=2)
    true_labels, pred_labels = [], []
    for pred_row, label_row in zip(preds, label_ids):
        tl, pl = [], []
        for pv, lv in zip(pred_row, label_row):
            if lv != -100:
                tl.append(ID2LABEL[lv])
                pl.append(ID2LABEL[pv])
        true_labels.append(tl)
        pred_labels.append(pl)
    return {"f1": f1_score(true_labels, pred_labels),
            "report": classification_report(true_labels, pred_labels)}


# ── Training entry point ──────────────────────────────────────────────────────

def main():
    fn = "main"
    if torch.cuda.is_available():
        _info(fn, f"GPU: {torch.cuda.get_device_name(0)}")
    else:
        _warn(fn, "No GPU — training will be slow on CPU")

    df  = pd.read_csv(RESUME_FILE)
    col = next((c for c in df.columns
                if any(k in c.lower() for k in ["resume_str", "resume", "text"])),
               df.columns[-1])
    _info(fn, f"Using resume column '{col}' ({len(df)} rows)")
    texts       = df[col].dropna().tolist()
    skill_vocab = _load_skill_vocab(SKILLS_FILE)

    train_texts, val_texts = train_test_split(texts, test_size=VAL_SPLIT, random_state=42)
    _info(fn, f"Split: {len(train_texts)} train / {len(val_texts)} val")

    tokenizer = AutoTokenizer.from_pretrained(BASE_MODEL)
    model     = AutoModelForTokenClassification.from_pretrained(
        BASE_MODEL, num_labels=len(LABELS),
        id2label=ID2LABEL, label2id=LABEL2ID, ignore_mismatched_sizes=True,
    )
    _info(fn, f"Model: {BASE_MODEL} with {len(LABELS)} labels: {LABELS}")

    train_ds = ConcatDataset([
        _ResumeNERDataset(train_texts, tokenizer, skill_vocab),
        _JsonlNERDataset(TRAIN_JSONL, tokenizer),
    ])
    val_ds = ConcatDataset([
        _ResumeNERDataset(val_texts, tokenizer, skill_vocab),
        _JsonlNERDataset(VAL_JSONL, tokenizer),
    ])
    _info(fn, f"Dataset sizes — train: {len(train_ds)}, val: {len(val_ds)}")

    args = TrainingArguments(
        output_dir=OUTPUT_DIR, num_train_epochs=EPOCHS,
        per_device_train_batch_size=BATCH_SIZE, per_device_eval_batch_size=BATCH_SIZE,
        learning_rate=LR, weight_decay=0.01, warmup_ratio=0.1,
        eval_strategy="epoch", save_strategy="epoch", save_total_limit=3,
        load_best_model_at_end=True, metric_for_best_model="f1",
        logging_steps=50, fp16=torch.cuda.is_available(), report_to="none",
    )

    Trainer(
        model=model, args=args,
        train_dataset=train_ds, eval_dataset=val_ds,
        tokenizer=tokenizer,
        data_collator=DataCollatorForTokenClassification(tokenizer),
        compute_metrics=_compute_metrics,
    ).train()

    model.save_pretrained(OUTPUT_DIR)
    tokenizer.save_pretrained(OUTPUT_DIR)
    _info(fn, f"Model saved to {OUTPUT_DIR}")


if __name__ == "__main__":
    main()