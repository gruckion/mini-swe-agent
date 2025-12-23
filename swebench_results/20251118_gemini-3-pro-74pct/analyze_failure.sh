#!/bin/bash
# Analyze a single trajectory file and output failure analysis

INSTANCE_ID=$1
TRAJ_FILE="trajs/${INSTANCE_ID}/${INSTANCE_ID}.traj.json"

if [ ! -f "$TRAJ_FILE" ]; then
    echo "ERROR: File not found: $TRAJ_FILE"
    exit 1
fi

echo "# Failure Analysis: ${INSTANCE_ID}"
echo ""
echo "## Basic Info"
echo '```'
jq -r '{exit_status: .info.exit_status, api_calls: .info.model_stats.api_calls, cost: .info.model_stats.instance_cost}' "$TRAJ_FILE" 2>/dev/null || echo "Could not parse basic info"
echo '```'
echo ""

echo "## Token Usage"
MAX_TOKENS=$(jq '[.messages[].extra.response.usage.prompt_tokens // 0] | max' "$TRAJ_FILE" 2>/dev/null || echo "0")
echo "- Max prompt tokens: $MAX_TOKENS"
echo ""

echo "## Files Modified in Submission"
echo '```'
jq -r '.info.submission // "NO SUBMISSION"' "$TRAJ_FILE" 2>/dev/null | grep "^diff --git" | sed 's/diff --git a\//- /' | sed 's/ b\/.*//' || echo "No files modified"
echo '```'
echo ""

echo "## Rule Violation Check"
SUBMISSION=$(jq -r '.info.submission // ""' "$TRAJ_FILE" 2>/dev/null)

# Check for test file modifications
TEST_MODS=$(echo "$SUBMISSION" | grep -E "test_.*\.py|tests/.*\.py" | head -3)
if [ -n "$TEST_MODS" ]; then
    echo "### ❌ TEST FILES MODIFIED"
    echo '```'
    echo "$TEST_MODS"
    echo '```'
fi

# Check for config file modifications
CONFIG_MODS=$(echo "$SUBMISSION" | grep -E "pyproject\.toml|setup\.cfg|setup\.py|requirements" | head -3)
if [ -n "$CONFIG_MODS" ]; then
    echo "### ❌ CONFIG FILES MODIFIED"
    echo '```'
    echo "$CONFIG_MODS"
    echo '```'
fi

# Check if submission is empty
if [ -z "$SUBMISSION" ] || [ "$SUBMISSION" == "" ]; then
    echo "### ❌ EMPTY SUBMISSION"
fi

echo ""
echo "## Agent Reasoning About Tests"
echo '```'
jq -r '.messages[] | select(.role == "assistant") | .content' "$TRAJ_FILE" 2>/dev/null | grep -i "update.*test\|modify.*test\|change.*test\|fix.*test\|edit.*test" | head -5 || echo "No test-related reasoning found"
echo '```'
echo ""

echo "## Submission Diff (first 100 lines)"
echo '```diff'
jq -r '.info.submission // "NO SUBMISSION"' "$TRAJ_FILE" 2>/dev/null | head -100
echo '```'
