# Guide: Analyzing SWE-bench Trajectory Files

This guide explains how to navigate `.traj.json` files to understand why an SWE-bench run failed.

## File Structure Overview

A trajectory file contains the complete record of an agent's attempt to solve a GitHub issue. The structure is:

```json
{
  "info": {
    "exit_status": "Submitted",
    "submission": "<git diff of changes>",
    "model_stats": { "instance_cost": 0.45, "api_calls": 32 },
    "config": { ... }
  },
  "messages": [
    { "role": "system", "content": "..." },
    { "role": "user", "content": "..." },
    { "role": "assistant", "content": "...", "extra": { "response": { "usage": {...} } } },
    ...
  ]
}
```

## Quick Analysis Commands

### 1. Check the Submission Diff First

See what changes the agent actually made:

```bash
jq -r '.info.submission' instance.traj.json
```

This immediately shows if the agent:
- Modified files it shouldn't have (tests, config files)
- Made incomplete changes
- Changed the wrong files

### 2. Count Messages and Token Usage

```bash
# Number of messages in conversation
jq '.messages | length' instance.traj.json

# Total characters in all messages
jq '[.messages[].content | length] | add' instance.traj.json

# Get token progression (to check for context window issues)
jq '[.messages[].extra.response.usage.prompt_tokens] | map(select(. > 0))' instance.traj.json

# Get maximum tokens used
jq '[.messages[].extra.response.usage.prompt_tokens // 0] | max' instance.traj.json
```

### 3. Extract All Agent Reasoning

```bash
# Get all assistant messages (contains THOUGHT sections)
jq -r '.messages[] | select(.role == "assistant") | .content' instance.traj.json
```

### 4. Extract All Command Outputs

```bash
# Get all user messages (contains command outputs)
jq -r '.messages[] | select(.role == "user") | .content' instance.traj.json | head -500
```

### 5. Find Specific Decision Points

```bash
# Find where agent decided to modify tests
jq -r '.messages[] | select(.role == "assistant") | .content' instance.traj.json | grep -i "update.*test\|modify.*test\|change.*test"

# Find error messages
jq -r '.messages[] | select(.role == "user") | .content' instance.traj.json | grep -i "error\|failed\|exception"

# Find the final submission command
jq -r '.messages[] | select(.role == "assistant") | .content' instance.traj.json | grep -A2 "COMPLETE_TASK"
```

## Step-by-Step Failure Analysis

### Step 1: Check Exit Status and Submission

```bash
# Quick overview
jq '{exit_status: .info.exit_status, api_calls: .info.model_stats.api_calls, cost: .info.model_stats.instance_cost}' instance.traj.json
```

### Step 2: Review the Initial Instructions

The initial instructions define what the agent was told to do (and not do):

```bash
# Get the system prompt
jq -r '.info.config.agent.system_template' instance.traj.json

# Get the instance template (contains task-specific rules)
jq -r '.info.config.agent.instance_template' instance.traj.json
```

Look for constraints like:
- "DO NOT MODIFY: Tests, configuration files"
- "MODIFY: Regular source code files only"

### Step 3: Identify the Problem Type

Common failure patterns:

| Pattern | How to Detect |
|---------|---------------|
| Modified tests | `jq -r '.info.submission'` shows changes to `test_*.py` |
| Modified config | Submission shows changes to `pyproject.toml`, `setup.cfg`, etc. |
| Incomplete fix | Submission is empty or partial |
| Wrong file | Changes made to unrelated files |
| Context overflow | Max tokens approaches model limit |
| Ignored instructions | Search reasoning for rule violations |

### Step 4: Trace the Decision Chain

Find where things went wrong:

```bash
# Extract reasoning with line numbers for context
jq -r '.messages | to_entries[] | select(.value.role == "assistant") | "=== Message \(.key) ===\n\(.value.content)\n"' instance.traj.json
```

Look for:
- When the agent first encountered test failures
- What reasoning led to violating constraints
- Whether it considered alternatives

### Step 5: Check for Context Window Issues

```bash
# Get token counts over time
jq '[.messages[].extra.response.usage | select(. != null) | .prompt_tokens]' instance.traj.json

# Compare max tokens to model's context limit
# Gemini 3 Pro: 1M tokens
# Claude: 200K tokens
# GPT-4: 128K tokens
```

If tokens approach the limit, the agent may have "forgotten" early instructions.

## Example Analysis: astropy__astropy-13033

### What the submission showed:

```bash
jq -r '.info.submission' astropy__astropy-13033.traj.json | head -50
```

Output revealed changes to:
- `astropy/timeseries/core.py` ✅ (allowed)
- `astropy/timeseries/tests/test_sampled.py` ❌ (forbidden)
- `pyproject.toml` ❌ (forbidden)

### Finding the violation:

```bash
jq -r '.messages[] | select(.role == "assistant") | .content' astropy__astropy-13033.traj.json | grep -B2 -A2 "update.*test"
```

Found:
> "So I need to update `astropy/timeseries/tests/test_sampled.py` to match the new error messages."

### Checking if context was the issue:

```bash
jq '[.messages[].extra.response.usage.prompt_tokens // 0] | max' astropy__astropy-13033.traj.json
# Result: 30678 tokens (only 3% of 1M limit)
```

Context was NOT the issue - the agent chose to ignore instructions.

## Common Failure Modes

### 1. Test Modification (Most Common)

**Symptom:** Agent changes test files to match its implementation

**Detection:**
```bash
jq -r '.info.submission' instance.traj.json | grep "test_"
```

**Root Cause:** Agent prioritizes "making tests pass" over "following constraints"

### 2. Configuration File Changes

**Symptom:** Changes to `pyproject.toml`, `setup.cfg`, `requirements.txt`

**Detection:**
```bash
jq -r '.info.submission' instance.traj.json | grep -E "pyproject|setup\.|requirements"
```

**Root Cause:** Agent tries to fix build/environment issues instead of the actual bug

### 3. Incomplete Implementation

**Symptom:** Empty or partial submission

**Detection:**
```bash
jq -r '.info.submission' instance.traj.json | wc -l
```

**Root Cause:** Agent ran out of steps, hit cost limit, or gave up

### 4. Wrong Error Message Format

**Symptom:** Code fix is correct but changes output format

**Detection:** Compare expected test assertions with actual error messages in agent's test runs

**Root Cause:** Agent doesn't check what format existing tests expect

## Automated Analysis Script

Save as `analyze_traj.sh`:

```bash
#!/bin/bash
TRAJ_FILE=$1

echo "=== TRAJECTORY ANALYSIS ==="
echo ""

echo "## Basic Info"
jq '{exit_status: .info.exit_status, api_calls: .info.model_stats.api_calls, cost: .info.model_stats.instance_cost}' "$TRAJ_FILE"
echo ""

echo "## Message Count"
jq '.messages | length' "$TRAJ_FILE"
echo ""

echo "## Max Tokens Used"
jq '[.messages[].extra.response.usage.prompt_tokens // 0] | max' "$TRAJ_FILE"
echo ""

echo "## Files Modified"
jq -r '.info.submission' "$TRAJ_FILE" | grep "^diff --git" | sed 's/diff --git a\///' | sed 's/ b\/.*//'
echo ""

echo "## Potential Rule Violations"
echo "Test files modified:"
jq -r '.info.submission' "$TRAJ_FILE" | grep "test_" | head -5
echo ""
echo "Config files modified:"
jq -r '.info.submission' "$TRAJ_FILE" | grep -E "pyproject|setup\.|requirements" | head -5
echo ""

echo "## Key Decision Points (search for 'test' in reasoning)"
jq -r '.messages[] | select(.role == "assistant") | .content' "$TRAJ_FILE" | grep -i "update.*test\|modify.*test\|change.*test\|fix.*test" | head -10
```

Usage:
```bash
chmod +x analyze_traj.sh
./analyze_traj.sh astropy__astropy-13033.traj.json
```

## Tips for Debugging

1. **Start with the submission diff** - it tells you exactly what the agent changed
2. **Check instructions first** - know what rules the agent was given
3. **Follow the reasoning** - understand WHY the agent made decisions
4. **Look for test failures** - often the trigger for rule violations
5. **Check token counts** - rule out context window issues
6. **Compare to passing cases** - what did successful runs do differently?

## Red Flags to Watch For

- Agent saying "I need to update the tests"
- Agent modifying `pyproject.toml` or `setup.cfg`
- Agent reasoning "my fix is more accurate" when tests fail
- Token count approaching model's context limit
- Agent creating new files instead of editing existing ones
- Agent running tests and then changing test expectations
