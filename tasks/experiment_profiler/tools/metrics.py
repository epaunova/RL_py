"""Metric implementations used by the grader and starter code."""

from __future__ import annotations

import math
from typing import Dict, Iterable, List


def compute_fact_coverage(required_facts: Iterable[str], completion: str) -> float:
    """
    Calculate what fraction of required facts appear in the completion.
    Uses case-insensitive substring matching.
    """
    facts = [fact.lower() for fact in required_facts]
    completion_lower = completion.lower()
    hits = sum(1 for fact in facts if fact in completion_lower)

    # Edge case: if no facts required, give perfect score
    if not facts:
        return 1.0

    return hits / len(facts)


def compute_refusal_flag(completion: str, metadata: Dict[str, str]) -> bool:
    """
    Check if the model refused to answer.
    Looks for explicit refusal markers or common refusal phrases.
    """
    # Check metadata first (more reliable)
    if metadata.get("type") == "refusal":
        return True

    # Fall back to heuristic detection
    lowered = completion.lower()
    return "i'm sorry" in lowered or "cannot comply" in lowered


def aggregate_metrics(fact_coverages: List[float], refusals: List[bool]) -> Dict[str, float]:
    """
    Combine per-dialogue metrics into experiment-level statistics.
    Returns fact coverage average, refusal rate, and a combined quality score.
    """
    if not fact_coverages:
        raise ValueError("No fact coverage values provided")

    coverage_mean = sum(fact_coverages) / len(fact_coverages)
    refusal_rate = sum(1 for flag in refusals if flag) / len(refusals)

    # Geometric mean balances coverage and non-refusal
    # High refusal rate hurts the score even with good coverage
    geometric_mean = math.sqrt(max(coverage_mean * (1 - refusal_rate), 0.0))

    return {
        "fact_coverage": round(coverage_mean, 4),
        "refusal_rate": round(refusal_rate, 4),
        "geometric_mean": round(geometric_mean, 4),
    }
