# Experiment Profiler Data Files

This directory contains test data and mock responses for the experiment profiler tool.

## Files

### `dialogues.json`
Contains the test dialogues used for evaluating model responses. Each dialogue has:
- `dialogue_id`: Unique identifier
- `system`: System prompt
- `user`: User prompt
- `required_facts`: List of technical terms/facts expected in responses

This is the ground truth dataset used by both the runner and grader.

### `mock_responses.json`
**Purpose:** Provides deterministic mock responses for testing and grading **without requiring an API key**.

**When used:**
- When `ANTHROPIC_API_KEY` environment variable is not set
- During automated grading (`grader/grade.py`)
- For reproducible testing in CI/CD

**Why it exists:**
Mock responses are carefully crafted to:
- Include all `required_facts` from dialogues.json
- Trigger appropriate refusal detection for safety prompts
- Pass grading thresholds (fact_coverage ≥ 60%, correct refusal rate)

**Real API vs Mock:**
- **Mock responses** (no API key): fact_coverage = 88.89%, refusal_rate = 33.33% ✅ (passes grading)
- **Real API responses** (with API key): Results vary by model (e.g., claude-haiku-4-5 gives 22.22% fact coverage)

The system automatically switches between real API and mocks based on API key presence. Both modes are valid; mocks ensure consistent grading while real API tests actual model behavior.

## Testing

```bash
# Test with mocks (no API key needed)
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli run \
    --config tasks/experiment_profiler/configs/sample_experiment.yaml \
    --output-dir runs/mock_test

# Test with real API
export ANTHROPIC_API_KEY="sk-ant-..."
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli run \
    --config tasks/experiment_profiler/configs/sample_experiment.yaml \
    --output-dir runs/real_api_test
