"""
FusionClaw — Standalone deliberation panel with NaN Builders.

Run a multi-model panel without OpenClaw. Just NaN API + Python.

pip install openai
"""

import json
import concurrent.futures
from openai import OpenAI

# ── Config ──────────────────────────────────────────────────────────
import os
NaN_API_KEY = os.environ.get("NAN_API_KEY", "your-api-key-here")  # Get yours at https://nan.builders
NaN_BASE_URL = "https://api.nan.builders/v1"

client = OpenAI(base_url=NaN_BASE_URL, api_key="NaN_API_KEY")

# ── Models ──────────────────────────────────────────────────────────
PANEL_MODELS = [
    "deepseek-v4-flash",  # Fast reasoning
    "qwen3.6",            # Balanced analysis
    "gemma4",             # Diverse perspective
]
JUDGE_MODEL = "deepseek-v4-flash"

# ── Panelist prompt ─────────────────────────────────────────────────
PANELIST_PROMPT = """You are a panelist in a multi-model deliberation. \
Answer the following question directly and thoroughly.

Question: {question}

Provide your analysis. Be specific, flag uncertainties, and state your confidence level."""

# ── Judge prompt ────────────────────────────────────────────────────
JUDGE_PROMPT = """You are a judge in a multi-model deliberation panel. \
Analyze the responses from multiple AI models and produce a structured comparison.

## Original Question
{question}

## Panelist Responses
{responses}

## Your Task
Produce a structured JSON assessment with:
1. consensus: Points where ALL or MOST panelists agree
2. contradictions: Where panelists disagree (topic + positions)
3. coverage_gaps: Important aspects no panelist addressed
4. unique_insights: Valuable insights from only one panelist
5. confidence_assessment: high/medium/low for each conclusion
6. recommendation: Synthesized best answer with uncertainty flags

Return ONLY valid JSON."""


def run_panelist(model: str, question: str) -> dict:
    """Run a single panelist."""
    resp = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": PANELIST_PROMPT.format(question=question)}],
        max_tokens=2000,
    )
    return {"model": model, "response": resp.choices[0].message.content}


def run_judge(question: str, panelist_results: list[dict]) -> dict:
    """Run the judge on all panelist responses."""
    responses_text = "\n\n".join(
        f"### {r['model']}\n{r['response']}" for r in panelist_results
    )
    resp = client.chat.completions.create(
        model=JUDGE_MODEL,
        messages=[{
            "role": "user",
            "content": JUDGE_PROMPT.format(question=question, responses=responses_text),
        }],
        max_tokens=3000,
    )
    try:
        return json.loads(resp.choices[0].message.content)
    except json.JSONDecodeError:
        return {"raw": resp.choices[0].message.content}


def deliberate(question: str) -> dict:
    """Run a full deliberation panel."""
    # 1. Spawn panelists in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(PANEL_MODELS)) as pool:
        futures = [pool.submit(run_panelist, m, question) for m in PANEL_MODELS]
        panelist_results = [f.result() for f in futures]

    # 2. Judge synthesizes
    judge_result = run_judge(question, panelist_results)

    return {
        "question": question,
        "panelists": panelist_results,
        "judge": judge_result,
    }


# ── Example ─────────────────────────────────────────────────────────
if __name__ == "__main__":
    result = deliberate(
        "Should a startup with 5 engineers use microservices or a monolith?"
    )

    judge = result["judge"]

    print("=" * 60)
    print("CONSENSUS:")
    for c in judge.get("consensus", []):
        print(f"  • {c}")

    print("\nCONTRADICTIONS:")
    for c in judge.get("contradictions", []):
        print(f"  ⚠ {c.get('topic', '?')}")
        for pos in c.get("positions", []):
            print(f"    - {pos.get('model', '?')}: {pos.get('position', '?')}")

    print("\nUNIQUE INSIGHTS:")
    for u in judge.get("unique_insights", []):
        print(f"  💡 {u.get('model', '?')}: {u.get('insight', '?')}")

    print("\nRECOMMENDATION:")
    print(f"  {judge.get('recommendation', 'N/A')}")
    print("=" * 60)