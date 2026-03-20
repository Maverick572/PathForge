# gap_engine.py  v4.2
# ─────────────────────────────────────────────────────────────────────────────
# Compares extracted resume skills against JD (primary) or O*NET (fallback).
#
# v4.2 changes:
#   [1] extract_skills_from_jd() now uses SKILL_TAXONOMY from skill_extractor
#       as its canonical skill list — same single source of truth as the resume
#       extractor. No more separate _JD_SKILL_KEYWORDS list.
#   [2] Regex pass removed entirely. It was the source of all phantom JD skills
#       ("Chill", "Stay", "Location Mumbai", "Role Overview We" etc).
#       Any regex that matches capitalised words in prose cannot reliably
#       distinguish skills from verbs, adjectives, and section headers.
#   [3] Keyword scan now uses word-boundary lookarounds (same fix as
#       skill_extractor) so "Java" doesn't match inside "JavaScript".
#   [4] "experience with X / proficiency in X" pattern retained but only
#       validates the extracted phrase against SKILL_TAXONOMY — if it's not
#       a known skill, it's discarded.
# ─────────────────────────────────────────────────────────────────────────────

import json
import re
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

# ── Logging ───────────────────────────────────────────────────────────────────

def _log(level: str, fn: str, msg: str) -> None:
    print(f"[gap_engine:{fn}] {level:<5}  {msg}")

def _info(fn, msg):  _log("INFO",  fn, msg)
def _warn(fn, msg):  _log("WARN",  fn, msg)
def _debug(fn, msg): _log("DEBUG", fn, msg)

# ── Config ────────────────────────────────────────────────────────────────────

EMBED_MODEL      = "all-MiniLM-L6-v2"
GAP_THRESHOLD    = 0.50
COURSE_THRESHOLD = 0.35
TOP_K_GAPS       = 15
ONET_ROLE_COL    = "Title"
ONET_SKILL_COL   = "Element Name"

# ── Embedding cache ───────────────────────────────────────────────────────────

class EmbedCache:
    _model  = None
    _cache: dict = {}

    @classmethod
    def model(cls) -> SentenceTransformer:
        if cls._model is None:
            _info("EmbedCache", f"Loading embedding model '{EMBED_MODEL}' (one-time)…")
            cls._model = SentenceTransformer(EMBED_MODEL)
            _info("EmbedCache", "Embedding model loaded and cached")
        return cls._model

    @classmethod
    def embed(cls, texts: list) -> np.ndarray:
        missing = [t for t in texts if t not in cls._cache]
        if missing:
            _debug("EmbedCache", f"Embedding {len(missing)} new texts (cache has {len(cls._cache)})")
            vecs = cls.model().encode(missing, show_progress_bar=False,
                                      normalize_embeddings=True)
            for t, v in zip(missing, vecs):
                cls._cache[t] = v
        return np.stack([cls._cache[t] for t in texts])


# ── JD skill extraction ───────────────────────────────────────────────────────
#
# Strategy (v4.2):
#   Pass 1 — scan the JD text for every skill in SKILL_TAXONOMY using
#             word-boundary regex. This is identical to the resume lexicon
#             scan but over JD text instead. Same list, same boundaries.
#   Pass 2 — "experience with X / proficiency in X" pattern, but only
#             accept X if it appears in SKILL_TAXONOMY. Discards prose.
#
# What was removed:
#   - The old CamelCase regex `[A-Z][a-zA-Z+#\.]+` — grabbed every
#     capitalised word/phrase in the JD including verbs, adjectives,
#     location names, and section headers.
#   - _JD_SKILL_KEYWORDS — a separate hand-maintained list that had already
#     drifted from SKILL_TAXONOMY and was redundant.

# Pattern to catch "experience with X" / "proficiency in X" — X validated
# against taxonomy after extraction so prose doesn't bleed through
_EXPERIENCE_WITH = re.compile(
    r"\b(?:experience|proficiency|familiarity|knowledge|expertise)\s+(?:in|with)\s+"
    r"([\w][\w\s+#./&-]{1,40}?)(?=[,;\n\.]|\s{2}|$)",
    re.IGNORECASE,
)


def extract_skills_from_jd(jd_text: str) -> list[str]:
    """
    Extract skills from a JD using SKILL_TAXONOMY as the single canonical list.

    Both this function and skill_extractor.extract_skills() now use the same
    skill definitions — SKILL_TAXONOMY in skill_extractor.py. No more drift.
    """
    fn = "extract_skills_from_jd"

    # Import here to avoid circular import at module level
    from skill_extractor import SKILL_TAXONOMY, SKILL_INDEX

    _info(fn, f"JD text length: {len(jd_text)} chars")

    # Normalise whitespace — collapse newlines so multi-line bullets don't
    # split skill names across lines (e.g. "Adobe\nXD")
    jd_clean   = " ".join(jd_text.split())
    jd_lower   = jd_clean.lower()
    candidates: set[str] = set()

    # ── Pass 1: scan for every taxonomy skill ────────────────────────────────
    # Use word-boundary lookarounds (not \b) so C++, C#, CI/CD all match.
    # Longest-first so "Google Analytics 4" doesn't get shadowed by
    # "Google Analytics".
    taxonomy_hits: list[str] = []
    skills_by_length = sorted(SKILL_TAXONOMY.keys(), key=len, reverse=True)

    for skill in skills_by_length:
        lc  = skill.lower()
        pat = r"(?<![a-zA-Z0-9])" + re.escape(lc) + r"(?![a-zA-Z0-9])"
        if re.search(pat, jd_lower):
            # Don't add if a longer skill covering this one was already found
            # e.g. "Google Analytics" already added — skip "Google"
            if not any(lc in existing.lower() for existing in candidates):
                candidates.add(skill)
                taxonomy_hits.append(skill)

    _info(fn, f"Pass 1 — taxonomy scan hits ({len(taxonomy_hits)}): {sorted(taxonomy_hits)}")

    # ── Pass 2: "experience with X" pattern — validate against taxonomy ──────
    phrase_hits:     list[str] = []
    phrase_rejected: list[str] = []

    for m in _EXPERIENCE_WITH.finditer(jd_clean):
        phrase = m.group(1).strip()
        lc     = phrase.lower()
        # Only accept if the phrase (or a close match) is in the taxonomy
        canon  = SKILL_INDEX.get(lc)
        if canon and canon not in candidates:
            candidates.add(canon)
            phrase_hits.append(canon)
        else:
            phrase_rejected.append(phrase)

    if phrase_hits:
        _info(fn, f"Pass 2 — 'experience with' pattern added ({len(phrase_hits)}): {phrase_hits}")
    if phrase_rejected:
        _debug(fn, f"Pass 2 — rejected (not in taxonomy) ({len(phrase_rejected)}): {phrase_rejected}")

    result = sorted(candidates)
    _info(fn, f"Final JD skills ({len(result)}): {result}")
    return result


# ── O*NET fallback ────────────────────────────────────────────────────────────

def load_onet_skills(onet_csv: str, role_query: str = None) -> list:
    fn = "load_onet_skills"
    _info(fn, f"Loading O*NET from '{onet_csv}', role_query='{role_query}'")
    if onet_csv.endswith(".xlsx"):
        df = pd.read_excel(onet_csv)
        col_map = {}
        for col in df.columns:
            if "element" in col.lower() and "name" in col.lower():
                col_map[col] = ONET_SKILL_COL
            elif "title" in col.lower():
                col_map[col] = ONET_ROLE_COL
        df = df.rename(columns=col_map)
    else:
        df = pd.read_csv(onet_csv)

    if role_query and ONET_ROLE_COL in df.columns:
        roles     = df[ONET_ROLE_COL].dropna().unique().tolist()
        role_vecs = EmbedCache.embed(roles)
        query_vec = EmbedCache.embed([role_query])
        sims      = cosine_similarity(query_vec, role_vecs)[0]
        best_role = roles[int(np.argmax(sims))]
        best_sim  = round(float(sims[np.argmax(sims)]), 3)
        _info(fn, f"Best O*NET role match: '{best_role}' (sim={best_sim})")
        df = df[df[ONET_ROLE_COL] == best_role]

    skills = df[ONET_SKILL_COL].dropna().unique().tolist()
    _info(fn, f"O*NET returned {len(skills)} skills for role")
    return skills


# ── Core gap computation ──────────────────────────────────────────────────────

def compute_gaps(resume_skills: list, required_skills: list,
                 threshold: float = GAP_THRESHOLD) -> list:
    fn = "compute_gaps"
    _info(fn, f"Resume skills ({len(resume_skills)}): {resume_skills}")
    _info(fn, f"Required skills ({len(required_skills)}): {required_skills}")
    _info(fn, f"Gap threshold: {threshold}")

    if not resume_skills or not required_skills:
        _warn(fn, "Empty resume or required skills — all required treated as gaps with score=0")
        return [{"skill": s, "score": 0.0} for s in required_skills]

    res_vecs   = EmbedCache.embed(resume_skills)
    req_vecs   = EmbedCache.embed(required_skills)
    sim_matrix = cosine_similarity(req_vecs, res_vecs)
    max_sims   = sim_matrix.max(axis=1)

    covered: list[tuple] = []
    gaps:    list[dict]  = []

    for skill, score in zip(required_skills, max_sims):
        score = round(float(score), 4)
        if score < threshold:
            gaps.append({"skill": skill, "score": score})
            _debug(fn, f"  GAP      '{skill}' (max_sim={score} < {threshold})")
        else:
            best_idx = int(sim_matrix[list(required_skills).index(skill)].argmax())
            covered.append((skill, score, resume_skills[best_idx]))
            _debug(fn, f"  COVERED  '{skill}' (sim={score} via '{resume_skills[best_idx]}')")

    gaps_sorted = sorted(gaps, key=lambda x: x["score"])[:TOP_K_GAPS]
    _info(fn, f"Covered: {len(covered)}, Gaps: {len(gaps_sorted)}")
    _info(fn, f"Gap list: {[(g['skill'], g['score']) for g in gaps_sorted]}")
    return gaps_sorted


# ── Course matching ───────────────────────────────────────────────────────────

def match_courses(gaps: list, courses_json: str,
                  threshold: float = COURSE_THRESHOLD) -> list:
    fn = "match_courses"
    courses = json.loads(Path(courses_json).read_text())
    _info(fn, f"Matching {len(gaps)} gaps against {len(courses)} courses (threshold={threshold})")

    if not courses or not gaps:
        _warn(fn, "Empty gaps or courses — returning []")
        return []

    course_skills_lower = [
        {s.lower() for s in c.get("skills_covered", [])} for c in courses
    ]

    course_vecs = []
    for c in courses:
        skill_texts = c.get("skills_covered", [c["title"]])
        vecs        = EmbedCache.embed(skill_texts)
        course_vecs.append(vecs.mean(axis=0))
    course_matrix = np.stack(course_vecs)

    gap_skills = [g["skill"] for g in gaps]
    gap_vecs   = EmbedCache.embed(gap_skills)
    sims       = cosine_similarity(gap_vecs, course_matrix)

    recommendations = []
    used_courses    = set()

    for i, gap in enumerate(gaps):
        gap_lower    = gap["skill"].lower()
        gap_variants = {gap_lower, gap_lower + "s", gap_lower.rstrip("s")}

        exact_idx = next(
            (j for j, skill_set in enumerate(course_skills_lower)
             if gap_variants & skill_set and j not in used_courses),
            None,
        )
        if exact_idx is not None:
            _debug(fn, f"  EXACT '{gap['skill']}' → '{courses[exact_idx]['title']}'")
            recommendations.append({
                "gap_skill":    gap["skill"],
                "course_id":    courses[exact_idx]["id"],
                "course_title": courses[exact_idx]["title"],
                "match_score":  1.0,
            })
            used_courses.add(exact_idx)
            continue

        ranked  = np.argsort(sims[i])[::-1]
        matched = False
        for best_idx in ranked:
            idx        = int(best_idx)
            best_score = float(sims[i][idx])
            if idx in used_courses:
                continue
            if best_score >= threshold:
                _debug(fn, f"  SEMANTIC '{gap['skill']}' → '{courses[idx]['title']}' (sim={round(best_score,3)})")
                recommendations.append({
                    "gap_skill":    gap["skill"],
                    "course_id":    courses[idx]["id"],
                    "course_title": courses[idx]["title"],
                    "match_score":  round(best_score, 4),
                })
                used_courses.add(idx)
                matched = True
            break

        if not matched:
            _warn(fn, f"  NO match for '{gap['skill']}' (best sim={round(float(sims[i].max()),3)} < {threshold})")

    recommendations.sort(key=lambda x: x["match_score"], reverse=True)
    _info(fn, f"Matched {len(recommendations)}/{len(gaps)} gaps to courses")
    return recommendations


# ── Training hints ────────────────────────────────────────────────────────────

def compute_training_hints(gaps: list, extracted_entities: dict) -> dict:
    fn       = "compute_training_hints"
    n_gaps   = len(gaps)
    n_skills = len(extracted_entities.get("SKILL", []))
    n_exp    = len(extracted_entities.get("EXPERIENCE", []))
    n_edu    = len(extracted_entities.get("EDUCATION", []))

    raw = {
        "SKILL":      1.0 + (n_gaps / max(n_skills, 1)),
        "EXPERIENCE": 1.0 + (1.0 / max(n_exp, 1)),
        "EDUCATION":  1.0 + (1.0 / max(n_edu, 1)),
    }
    mean_w  = np.mean(list(raw.values()))
    weights = {k: round(v / mean_w, 4) for k, v in raw.items()}
    weights["O"] = 1.0
    _info(fn, f"Class weights: {weights}")
    return {"class_weights": weights}


# ── Main entry point ──────────────────────────────────────────────────────────

def run_gap_engine(
    extracted_entities: dict,
    onet_csv:           str,
    courses_json:       str,
    jd_text:            str  = None,
    role_query:         str  = None,
    output_path:        str  = "data/gap_report.json",
) -> dict:
    fn            = "run_gap_engine"
    resume_skills = extracted_entities.get("SKILL", [])
    _info(fn, f"Starting — resume skills: {len(resume_skills)}, jd provided: {'yes' if jd_text else 'no'}")

    if jd_text:
        required_skills = extract_skills_from_jd(jd_text)
        source_label    = "JD"
        if len(required_skills) < 5:
            _warn(fn, f"JD yielded only {len(required_skills)} skills — supplementing with O*NET")
            onet_skills     = load_onet_skills(onet_csv, role_query)
            required_skills = list(set(required_skills + onet_skills))
            source_label    = "JD+ONET"
    else:
        _warn(fn, "No JD provided — using O*NET fallback")
        required_skills = load_onet_skills(onet_csv, role_query)
        source_label    = "ONET"

    gaps = compute_gaps(resume_skills, required_skills)
    for g in gaps:
        g["source"] = source_label

    recommendations = match_courses(gaps, courses_json)
    training_hints  = compute_training_hints(gaps, extracted_entities)

    report = {
        "gaps":            gaps,
        "recommendations": recommendations,
        "training_hints":  training_hints,
    }
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    Path(output_path).write_text(json.dumps(report, indent=2))
    _info(fn, f"Gap report written → {output_path} ({len(gaps)} gaps, {len(recommendations)} course matches)")
    return report


# ── CLI ───────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import argparse
    from skill_extractor import extract_skills

    parser = argparse.ArgumentParser()
    parser.add_argument("--resume",  required=True)
    parser.add_argument("--jd",      default=None)
    parser.add_argument("--role",    default=None)
    parser.add_argument("--onet",    default="data/onet_skills.csv")
    parser.add_argument("--courses", default="data/courses.json")
    parser.add_argument("--output",  default="data/gap_report.json")
    args = parser.parse_args()

    resume_text = Path(args.resume).read_text()
    jd_text     = Path(args.jd).read_text() if args.jd else None
    skills      = extract_skills(resume_text)
    entities    = {"SKILL": [s["name"] for s in skills], "EXPERIENCE": [], "EDUCATION": []}
    report      = run_gap_engine(
        extracted_entities=entities,
        jd_text=jd_text,
        role_query=args.role,
        onet_csv=args.onet,
        courses_json=args.courses,
        output_path=args.output,
    )
    print(f"\nTop gaps : {[g['skill'] for g in report['gaps'][:5]]}")
    print(f"Weights  : {report['training_hints']['class_weights']}")