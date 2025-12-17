# SWE-bench Results & Trajectory Access

This document explains how to access the benchmark results, trajectory logs, and failure analysis for mini-swe-agent's SWE-bench performance.

## Performance Summary

| Model | Resolution Rate | Total Cost | Avg API Calls | Date |
|-------|----------------|------------|---------------|------|
| **Claude 4.5 Opus** | 74.4% | $360.62 | 38.0 | 2025-11-24 |
| **Gemini 3 Pro Preview** | 74.2% | $229.98 | 40.3 | 2025-11-18 |
| **GPT-5.2 (high reasoning)** | TBD | - | 19.8 | 2025-12-11 |

## S3 Bucket Paths for Trajectories

All trajectories are publicly available in AWS S3:

```
# Claude 4.5 Opus (74.4%)
s3://swe-bench-experiments/bash-only/20251124_mini-v1.16.0_claude-opus-4-5-20251101/

# Gemini 3 Pro Preview (74.2%)
s3://swe-bench-experiments/bash-only/20251118_mini-v1.15.0_gemini-3-pro-preview-20251118/

# GPT-5.2 (unchecked)
s3://swe-bench-experiments/bash-only/20251211_mini-v1.17.2_gpt-5.2-2025-12-11-high/
```

## How to Download Results

### Option 1: AWS CLI Direct Download

```bash
# Install and configure AWS CLI
aws configure

# Download all results for a specific model
aws s3 sync s3://swe-bench-experiments/bash-only/20251118_mini-v1.15.0_gemini-3-pro-preview-20251118/ ./gemini-results/

# Download only trajectories
aws s3 sync s3://swe-bench-experiments/bash-only/20251118_mini-v1.15.0_gemini-3-pro-preview-20251118/trajs/ ./trajs/
```

### Option 2: Using the Experiments Repository

```bash
git clone https://github.com/SWE-bench/experiments
cd experiments
python -m analysis.download_logs bash-only/20251118_mini-v1.15.0_gemini-3-pro-preview-20251118
```

## Downloaded File Structure

```
<submission>/
├── trajs/                    # Trajectory files (.traj)
│   ├── django__django-12345.traj
│   ├── sympy__sympy-67890.traj
│   └── ...
├── logs/                     # Execution logs per instance
│   └── <instance_id>/
│       ├── patch.diff        # Generated patch
│       ├── report.json       # Evaluation report
│       └── test_output.txt   # Test execution output
├── all_preds.jsonl           # All model predictions
└── metadata.yaml             # Run configuration and metadata
```

## Trajectory File Format

Each `.traj` file is JSON containing the full agent conversation:

```json
{
  "trajectory": [
    {
      "role": "user",
      "content": "THOUGHT: ...\n\n```bash\nls -la\n```"
    },
    {
      "role": "assistant",
      "content": "<returncode>0</returncode>\n<output>...</output>"
    }
  ],
  "exit_status": "submitted",
  "result": "...",
  "instance_id": "django__django-12345",
  "model_name": "...",
  "cost": 0.45,
  "n_calls": 25
}
```

## Analyzing Failures

### Finding Failed Instances

1. Visit the [SWE-bench Bash Only Leaderboard](https://www.swebench.com/bash-only.html)
2. Per-instance results show `resolved: true/false` for each test case
3. Filter for failed instances and examine their trajectories

### Common Failure Patterns

When analyzing the ~26% failures, look for:

- **Incorrect diagnosis**: Agent misunderstood the bug
- **Wrong file edited**: Agent modified the wrong location
- **Incomplete fix**: Partial solution that doesn't pass all tests
- **Timeout/cost limit**: Agent ran out of steps or budget
- **Environment issues**: Docker/dependency problems

## Interactive Viewers

- **SWE-bench Results Viewer**: https://www.swebench.com/viewer.html
- **Bash Only Leaderboard**: https://www.swebench.com/bash-only.html
- **Docent Viewer**: Links available on leaderboard for visual trajectory exploration

## Running Your Own Evaluation

```bash
# Run on SWE-bench verified with your model
mini-extra swebench \
    --model google/gemini-3-pro \
    --subset verified \
    --split test \
    --workers 4 \
    -o ./my_results

# Evaluate results with sb-cli (free cloud evaluation)
sb-cli submit swe-bench_verified test \
    --predictions_path ./my_results/preds.json \
    --run_id my-run-id
```

## References

- [SWE-bench Leaderboards](https://www.swebench.com/)
- [SWE-bench/experiments Repository](https://github.com/SWE-bench/experiments)
- [mini-swe-agent Documentation](https://mini-swe-agent.com/latest/usage/swebench/)
- [sb-cli Cloud Evaluation](https://www.swebench.com/sb-cli/)
