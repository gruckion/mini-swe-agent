#!/bin/bash
# Generate final failure reports from analysis files

for analysis_file in failure_reports/*_analysis.md; do
    base=$(basename "$analysis_file" _analysis.md)
    final_report="failure_reports/${base}.md"

    # Skip if final report already exists
    if [ -f "$final_report" ]; then
        continue
    fi

    # Extract info from analysis
    has_test_mod=$(grep -c "TEST FILES MODIFIED" "$analysis_file" || echo "0")
    has_config_mod=$(grep -c "CONFIG FILES MODIFIED" "$analysis_file" || echo "0")
    has_empty=$(grep -c "EMPTY SUBMISSION" "$analysis_file" || echo "0")

    # Determine labels
    labels=""
    if [ "$has_test_mod" -gt 0 ]; then
        labels="test-modification"
    fi
    if [ "$has_config_mod" -gt 0 ]; then
        if [ -n "$labels" ]; then labels="$labels, "; fi
        labels="${labels}config-modification"
    fi
    if [ "$has_empty" -gt 0 ]; then
        if [ -n "$labels" ]; then labels="$labels, "; fi
        labels="${labels}empty-submission"
    fi
    if [ -z "$labels" ]; then
        labels="no-rule-violation, incorrect-fix-logic"
    fi

    # Determine failure type
    if [ "$has_test_mod" -gt 0 ]; then
        failure_type="Test file modification - agent modified tests to make them pass"
    elif [ "$has_config_mod" -gt 0 ]; then
        failure_type="Config file modification - agent modified configuration files"
    elif [ "$has_empty" -gt 0 ]; then
        failure_type="Empty submission - agent did not produce any changes"
    else
        failure_type="Incorrect fix logic - changes don't pass original test suite"
    fi

    # Get basic info
    api_calls=$(grep -o '"api_calls": [0-9]*' "$analysis_file" | grep -o '[0-9]*' | head -1)
    cost=$(grep -o '"cost": [0-9.]*' "$analysis_file" | grep -o '[0-9.]*' | head -1)
    max_tokens=$(grep "Max prompt tokens:" "$analysis_file" | grep -o '[0-9]*')

    # Get files modified
    files_modified=$(sed -n '/## Files Modified/,/## Rule Violation/p' "$analysis_file" | grep "^- " | head -5)

    # Get agent reasoning about tests
    reasoning=$(sed -n '/## Agent Reasoning/,/## Submission/p' "$analysis_file" | grep -v "^##" | grep -v '```' | head -5)

    # Create final report
    cat > "$final_report" << EOF
# Failure Report: ${base}

**Labels:** \`$(echo $labels | sed 's/, /`, `/g')\`

## Summary
${failure_type}

## Evidence

### Basic Info
- API Calls: ${api_calls:-N/A}
- Cost: \$${cost:-N/A}
- Max Tokens: ${max_tokens:-N/A}

### Files Modified
\`\`\`
${files_modified:-No files modified}
\`\`\`

### Agent Reasoning About Tests
${reasoning:-No specific test reasoning found}

## Conclusion
**Failure Type:** ${failure_type}
EOF

    echo "Generated: $final_report"
done
