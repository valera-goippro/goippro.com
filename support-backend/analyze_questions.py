"""GoIPPro Support — Question Analyzer
Reads logged questions, groups by topic, finds gaps in knowledge base.
Run monthly or on-demand: python3 analyze_questions.py
"""
import json
import os
import glob
from collections import Counter
from datetime import datetime

LOG_DIR = "/var/log/goippro-support"
KB_DIR = "/home/administrator/shared/goippro/knowledge_base"
REPORT_DIR = "/home/administrator/shared/goippro"

def load_questions():
    """Load all logged questions."""
    questions = []
    for fpath in sorted(glob.glob(os.path.join(LOG_DIR, "questions_*.jsonl"))):
        with open(fpath, "r", encoding="utf-8") as f:
            for line in f:
                try:
                    questions.append(json.loads(line.strip()))
                except:
                    pass
    return questions

def analyze(questions):
    """Analyze questions for patterns."""
    if not questions:
        return "No questions logged yet."
    
    # Language distribution
    lang_counts = Counter(q.get("language", "unknown") for q in questions)
    
    # Common keywords
    words = Counter()
    for q in questions:
        msg = q.get("question", "").lower()
        for w in msg.split():
            if len(w) > 3:
                words[w] += 1
    
    # Questions that might indicate KB gaps (contain "?" and longer questions)
    potential_gaps = []
    for q in questions:
        msg = q.get("question", "")
        ans_preview = q.get("answer_preview", "")
        if "don't know" in ans_preview.lower() or "don't have" in ans_preview.lower() or "contact support" in ans_preview.lower():
            potential_gaps.append(msg)
    
    # Build report
    report = []
    report.append(f"# GoIPPro Support — Question Analysis Report")
    report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    report.append(f"Total questions: {len(questions)}")
    report.append(f"")
    report.append(f"## Language Distribution")
    for lang, count in lang_counts.most_common():
        report.append(f"- {lang}: {count} ({100*count//len(questions)}%)")
    report.append(f"")
    report.append(f"## Top Keywords")
    for word, count in words.most_common(20):
        report.append(f"- {word}: {count}")
    report.append(f"")
    report.append(f"## Potential Knowledge Base Gaps ({len(potential_gaps)} questions)")
    for gap in potential_gaps[:20]:
        report.append(f"- {gap}")
    report.append(f"")
    report.append(f"## Recommendations")
    if potential_gaps:
        report.append(f"- {len(potential_gaps)} questions resulted in 'I don't know' — review and add to KB")
    report.append(f"- Most popular language: {lang_counts.most_common(1)[0][0] if lang_counts else 'N/A'}")
    report.append(f"- Consider adding KB content for top keywords not well covered")
    
    return "\n".join(report)

if __name__ == "__main__":
    questions = load_questions()
    report = analyze(questions)
    
    report_path = os.path.join(REPORT_DIR, "support_analysis_report.md")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report)
    
    print(report)
    print(f"\nReport saved to {report_path}")
