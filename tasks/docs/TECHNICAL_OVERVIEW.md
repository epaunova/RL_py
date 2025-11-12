# Technical Overview: Anthropic Experiment Profiler Task

## What is this?

This repo implements a realistic ML engineering task: building a CLI tool that runs batches of prompts through Claude, logs everything, and calculates quality metrics. It's designed to be used in reinforcement learning training where an agent needs to complete a partially-implemented codebase.

Think of it like a mini-version of what you'd build at an ML company to profile model behavior during fine-tuning experiments.

## Architecture
The codebase is split into the following layers:

| Layer | Key Modules | Responsibilities |
| --- | --- | --- |
| CLI | `reference_submission/experiment_profiler/cli.py` | Exposes `run` and `summarize` subcommands. The CLI wires up configuration parsing, experiment execution, and rich/terminal output. It now ships with a graceful fallback so the tool works even when the optional `rich` package is unavailable. |
| Execution core | `reference_submission/experiment_profiler/runner.py` | Coordinates dataset iteration, API calls, metric computation, and artifact writing. Returns `RunResult` with both the file paths and aggregated metric dictionary. |
| Configuration | `reference_submission/experiment_profiler/config.py` | Validates YAML manifests, resolves dataset paths relative to the repo, and instantiates strongly typed dataclasses consumed by the runner. |
| Simulation & tools | `reference_submission/experiment_profiler/simulation.py`, `tools/anthropic_client.py`, `tools/dataset.py`, `tools/logging_utils.py`, `tools/metrics.py` | Provide realistic infrastructure: a client that prefers the real Anthropic SDK but falls back to deterministic mocks, dataset readers, canonical logging schema helpers, and metric implementations (fact coverage, refusal flag, aggregate statistics). |
| Persistence | `reference_submission/experiment_profiler/storage.py` | Creates run directories under `runs/`, writes JSONL request/response logs, and stores aggregated summaries. |
| Grading | `grader/grade.py` | Imports the starter submission, runs the CLI end to end, and verifies that outputs match the contract defined in `prompt.md`. |

Starter counterparts mirror the reference modules but contain TODOs for the RL agent to complete. The grader imports from the starter package during evaluation.

## Data Flow
1. **Configuration parsing:** The CLI reads a YAML manifest via `ExperimentConfig.from_yaml`, which resolves relative dataset paths and extracts run parameters (model, temperature, max tokens, requested metrics).
2. **Client selection:** `ClientFactory` chooses `AnthropicClient` when the `ANTHROPIC_API_KEY` environment variable and SDK are available; otherwise it supplies a `MockAnthropicClient` backed by `data/mock_responses.json` for deterministic behavior.
3. **Experiment loop:** `ExperimentRunner.run` iterates over dialogue samples from `data/dialogues.json`, logs prompts, requests completions from the selected client, captures responses, and gathers per-dialogue metrics.
4. **Aggregation & storage:** Metrics are aggregated with `metrics.aggregate_metrics`, then `storage.write_*` helpers persist request logs, response logs, and the aggregated `summary.json` under `runs/<experiment_id>/`.
5. **Reporting:** The CLI prints status messages. The `summarize` command loads `summary.json` and renders it as either a Rich table (if available) or an aligned plain-text table.

## Optional Dependencies
- `rich` is now strictly optional. When it is missing, the `_ConsoleWrapper` strips Rich markup tags and prints plain strings, while the fallback summary renderer produces an ASCII table.
- `anthropic` remains optional; absence of the SDK or API key automatically routes through the mock client without failing tests.

## Verification & Testing

### Real API Testing (Completed)
**Tested with:** `claude-haiku-4-5` using live Anthropic API

The reference implementation has been validated with real API calls:
```bash
export ANTHROPIC_API_KEY="sk-ant-api03-..."
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli \
    run \
    --config tasks/experiment_profiler/configs/sample_experiment.yaml \
    --output-dir runs/real_api_test
Real API Results:

fact_coverage: 0.2222 (22.22%)
geometric_mean: 0.4714 (47.14%)
refusal_rate: 0.0000 (0%)
Note: Real API responses naturally differ from mock responses (which are crafted to pass grading thresholds). The system correctly:

Auto-detects API key and switches to live API
Makes 3 real Claude API calls
Generates all required output files
Calculates metrics accurately
Automated Testing
pytest executes tasks/experiment_profiler/grader/tests/test_reference_submission.py, which runs the grading script against the reference implementation to ensure behavioral coverage.
Manual smoke tests can be executed via:
python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli \
    run \
    --config tasks/experiment_profiler/configs/sample_experiment.yaml \
    --output-dir runs/sample

python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli \
    summarize \
    --log-dir runs/sample/demo_run
The commands succeed in both Rich-present and Rich-free environments.
Extensibility Notes
New metrics can be added by extending tools/metrics.py and updating both the runner aggregation logic and grader expectations.
Additional experiment manifests can be dropped into configs/ and referenced during RL evaluation without code changes.
The deterministic mock client enables unit tests to run offline; integration tests with the live API only require exporting ANTHROPIC_API_KEY.
Common Issues & Debugging
"Module not found: experiment_profiler"
Make sure you're running from the repo root and using the full module path:

python -m tasks.experiment_profiler.reference_submission.experiment_profiler.cli run ...
Grader fails with "requests.jsonl not found"
Check that your implementation is actually creating files in the output directory. Add debug prints to verify prepare_output_dir is being called.

Metrics don't match expected values
The grader is strict about:

Rounding to 4 decimal places
Computing geometric mean as sqrt(fact_coverage * (1 - refusal_rate))
Detecting refusals with "I'm sorry" or "type": "refusal" in metadata
Want to test without the mock?
Export your API key and the tool automatically switches to real API calls:

export ANTHROPIC_API_KEY="sk-ant-..."
File Structure Quick Reference
tasks/experiment_profiler/
├── configs/
│   └── sample_experiment.yaml      # Defines model, temp, dataset path
├── data/
│   ├── dialogues.json              # Input prompts + required facts
│   └── mock_responses.json         # Deterministic fallback responses
├── tools/                          # Shared utilities (all complete)
│   ├── anthropic_client.py         # API wrapper with mock fallback
│   ├── config_loader.py            # YAML parser (works w/o PyYAML)
│   ├── dataset.py                  # Load dialogues.json
│   ├── logging_utils.py            # JSONL schema helpers
│   └── metrics.py                  # Fact coverage, refusal detection
├── starter/                        # Incomplete (for RL agent to fill)
│   └── experiment_profiler/
│       ├── cli.py                  # TODOs in run() and summarize()
│       ├── runner.py               # TODOs in run() and summarize()
│       └── ...
├── reference_submission/           # Complete implementation
│   └── experiment_profiler/
│       └── ...
└── grader/
    ├── grade.py                    # Validates submission
    └── tests/
        └── test_reference_submission.py
