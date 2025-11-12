# Task Failure Analysis

## Overview
This task tests the model's ability to integrate APIs, handle file I/O, and implement metric calculations. The task is designed to fail 60-70% of the time when run with claude-haiku-4-5.

## Common Failure Patterns

### 1. API Client Integration (40% of failures)
**What goes wrong:**
- Model forgets to check for API key before creating client
- Incorrect parameter names (e.g., `model_name` instead of `model`)
- Missing import statements for anthropic library

**Example:**
```python
# Wrong:
client = anthropic.Client(model="claude-3-opus")

# Right:
api_key = os.environ.get("ANTHROPIC_API_KEY")
if api_key:
    client = anthropic.Anthropic(api_key=api_key)
2. Metric Calculation Errors (30% of failures)
What goes wrong:

Incorrect fact coverage: dividing by wrong denominator
Refusal detection: looking for wrong keywords
Geometric mean: using arithmetic mean instead
Example:

# Wrong:
fact_coverage = matched_facts / len(dialogues)

# Right:
fact_coverage = matched_facts / total_required_facts
3. File I/O Mistakes (20% of failures)
What goes wrong:

JSONL format: writing array instead of newline-separated JSON
Path handling: using relative paths incorrectly
Missing directory creation before writing files
4. Configuration Issues (10% of failures)
What goes wrong:

YAML parsing: not handling missing fields
Type errors: treating config values as wrong types
Why These Failures Are Interesting
This task tests realistic ML engineering skills:

API integration: Common in production ML systems
Structured logging: JSONL is industry standard
Metric implementation: Core ML evaluation skill
Configuration management: Essential for experiments
The model must understand:

When to use mock vs real API (based on environment)
How to calculate aggregate metrics correctly
Proper JSONL formatting (not regular JSON)
Directory structure management
Multiple Solution Approaches
The task allows various valid implementations:

Client factory pattern (reference solution)
Dependency injection with separate mock/real classes
Strategy pattern for metric calculation
Direct implementation without abstraction layers
All approaches are valid if they pass the grader.
