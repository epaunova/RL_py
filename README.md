
# ML Profiler: A Realistic Coding Challenge for RL Training

This repo is a complete RL task for training language models on real-world ML engineering work.

## The Challenge

You're given a partially-implemented CLI tool and need to finish it. The tool should:
- Read experiment configs (model, temperature, dataset)
- Execute batches of prompts through Claude's API
- Log everything (requests, responses, metadata)
- Calculate quality metrics (fact coverage, refusal detection)
- Output results in a nice table

**Why this task?** It's based on actual work ML engineers do: building evaluation harnesses for model experiments. Not too simple (requires understanding APIs, file I/O, metrics), not too hard (all the utilities are provided).

## What Makes This Different

Unlike toy coding problems, this task:
- Uses a real API (Anthropic Claude) with proper fallbacks
- Includes a deterministic grader that checks behavior, not code
- Provides professional tooling (config parsing, logging schemas, metrics)
- Has multiple valid solutions (mirrors real engineering)

## Repo Structure

├── requirements.txt # Just 5 dependencies ├── tasks/ │ ├── docs/ │ │ ├── RESULTS.md # Example outputs & metrics explained │ │ └── TECHNICAL_OVERVIEW.md # Architecture & debugging tips │ └── experiment_profiler/ │ ├── README.md # Start here! │ ├── prompt.md # Exact task requirements │ ├── configs/ # Experiment manifests (YAML) │ ├── data/ # Test dialogues + mock responses │ ├── tools/ # Complete utilities (use these!) │ ├── starter/ # Incomplete (you fill TODOs) │ ├── reference_submission/ # Complete (for comparison) │ └── grader/ # Automated testing


**For RL training:** Models start with `starter/` and must complete the TODOs. The grader validates behavior automatically.

## Quick Start (2 minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Test with real API (tested with claude-haiku-4-5)
export ANTHROPIC_API_KEY="sk-ant-your-key-here"
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli run \
    --config tasks/experiment_profiler/configs/sample_experiment.yaml \
    --output-dir runs/test

# Expected output:
# Completed experiment demo_run
# Metrics written to runs/test/demo_run/summary.json

# 3. View results
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli summarize \
    --log-dir runs/test/demo_run
Real API Test Results (with claude-haiku-4-5):

fact_coverage: 0.2222
geometric_mean: 0.4714
refusal_rate: 0.0000
The tool automatically detects your API key and uses real Claude API, or falls back to mock responses for testing/grading.

For RL Training Setup
Give the agent starter/ access - It contains TODOs to complete
Run the grader after each episode - python -m tasks.experiment_profiler.grader.grade
Check the JSON output - "status": "pass" means success!
The task is self-contained - no external API needed during training (uses mock responses).

What Gets Tested?
The grader is strict but fair. It verifies:

Correct files created (requests.jsonl, responses.jsonl, summary.json)
Config values respected (model, temperature, max_tokens)
All dialogues processed in order
Metrics calculated correctly (fact coverage, refusal rate, geometric mean)
CLI commands work (run and summarize)
No style checking, no exact code matching - just behavior validation.

Example Output
When working correctly, the CLI produces:

$ python -m experiment_profiler.cli run --config configs/sample_experiment.yaml --output-dir runs/test

Completed experiment demo_run
Metrics written to runs/test/demo_run/summary.json

$ python -m experiment_profiler.cli summarize --log-dir runs/test/demo_run

    Experiment Metrics
        (demo_run)
┏━━━━━━━━━━━━━━━━┳━━━━━━━━┓
┃ Metric         ┃  Value ┃
┡━━━━━━━━━━━━━━━━╇━━━━━━━━┩
│ fact_coverage  │ 0.8889 │
│ geometric_mean │ 0.7698 │
│ refusal_rate   │ 0.3333 │
└────────────────┴────────┘
Documentation
tasks/experiment_profiler/README.md - Task walkthrough with tips
tasks/experiment_profiler/prompt.md - Exact requirements for models
tasks/docs/RESULTS.md - Real examples with explanations
tasks/docs/TECHNICAL_OVERVIEW.md - Architecture & debugging
