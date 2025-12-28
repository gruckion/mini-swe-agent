#!/usr/bin/env python3
"""Deep analysis of each failure to identify specific root cause."""

import json
import re
import os

def extract_problem_summary(messages):
    """Extract a concise problem summary."""
    for msg in messages[:5]:
        content = msg.get('content', '')
        # Look for PR description
        if '<pr_description>' in content:
            match = re.search(r'<pr_description>(.*?)</pr_description>', content, re.DOTALL)
            if match:
                desc = match.group(1).strip()
                # Get first paragraph or up to 500 chars
                lines = desc.split('\n')
                summary = []
                for line in lines:
                    if line.strip():
                        summary.append(line.strip())
                    if len('\n'.join(summary)) > 400:
                        break
                return '\n'.join(summary)[:500]
    return "No problem statement found"

def extract_agent_fix_description(messages):
    """Extract what the agent said they were fixing."""
    for msg in messages:
        if msg.get('role') == 'assistant':
            content = msg.get('content', '')
            # Look for reasoning about fix
            if 'fix' in content.lower() and ('will' in content.lower() or 'need' in content.lower()):
                # Get the THOUGHT section
                thought_match = re.search(r'THOUGHT:(.+?)```', content, re.DOTALL)
                if thought_match:
                    thought = thought_match.group(1).strip()[:400]
                    if 'fix' in thought.lower() or 'issue' in thought.lower() or 'problem' in thought.lower():
                        return thought
    return ""

def extract_patch_summary(patch):
    """Create a human-readable summary of the patch."""
    if not patch:
        return "No patch submitted"

    files = re.findall(r'^diff --git a/(\S+)', patch, re.MULTILINE)

    # Count additions and deletions
    additions = len(re.findall(r'^\+[^+]', patch, re.MULTILINE))
    deletions = len(re.findall(r'^-[^-]', patch, re.MULTILINE))

    # Extract key code changes
    changes = []
    for match in re.finditer(r'^\+\s*(.+)$', patch, re.MULTILINE):
        line = match.group(1).strip()
        if line and not line.startswith('+') and len(line) > 10:
            if any(kw in line for kw in ['def ', 'class ', 'if ', 'return ', 'raise ', 'try:', 'except']):
                changes.append(line[:80])

    return {
        'files': files,
        'additions': additions,
        'deletions': deletions,
        'key_changes': changes[:5]
    }

def extract_test_failure_reason(messages):
    """Extract what specific test assertion failed."""
    for msg in reversed(messages):
        content = msg.get('content', '')
        if msg.get('role') == 'user':
            # Look for assertion errors
            if 'AssertionError' in content or 'assert' in content.lower():
                # Get context around assertion
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'assert' in line.lower() or 'AssertionError' in line:
                        context = lines[max(0, i-2):i+3]
                        return '\n'.join(context)[:300]
            # Look for FAILED tests
            if 'FAILED' in content:
                match = re.search(r'(FAILED.+?)(?:\n\n|\Z)', content, re.DOTALL)
                if match:
                    return match.group(1)[:300]
    return ""

def determine_root_cause(instance_id, data):
    """Analyze and determine the specific root cause."""
    messages = data.get('messages', [])
    info = data.get('info', {})
    patch = info.get('submission', '')

    problem = extract_problem_summary(messages)
    agent_reasoning = extract_agent_fix_description(messages)
    patch_summary = extract_patch_summary(patch)
    test_failure = extract_test_failure_reason(messages)

    # Analyze the gap between problem and fix
    root_cause = "Unknown"
    explanation = ""

    # Check for common patterns
    if not patch or patch.strip() == "":
        root_cause = "NO_FIX_SUBMITTED"
        explanation = "Agent did not submit any code changes"
    elif len(patch_summary.get('files', [])) > 3:
        root_cause = "OVER_ENGINEERED"
        explanation = f"Modified too many files ({len(patch_summary['files'])}), likely diverged from focused fix"
    elif 'test' in str(patch_summary.get('files', [])).lower():
        root_cause = "MODIFIED_TESTS"
        explanation = "Modified test files despite instructions"
    else:
        # Check the nature of the fix vs problem
        if agent_reasoning:
            if 'raise' in agent_reasoning.lower() and 'error' not in problem.lower():
                root_cause = "WRONG_APPROACH"
                explanation = "Added error raising when problem didn't require it"
            elif 'try' in agent_reasoning.lower() and 'except' in agent_reasoning.lower():
                root_cause = "INCOMPLETE_ERROR_HANDLING"
                explanation = "Added try-except but may have caught wrong exception or swallowed error"

        if root_cause == "Unknown":
            if test_failure:
                if 'not equal' in test_failure.lower() or '!=' in test_failure or 'AssertionError' in test_failure:
                    root_cause = "WRONG_OUTPUT_VALUE"
                    explanation = "Fix produces wrong output value, logic error in implementation"
                elif 'attribute' in test_failure.lower():
                    root_cause = "API_MISMATCH"
                    explanation = "Fix uses wrong API/attribute names"
                else:
                    root_cause = "TEST_ASSERTION_FAILED"
                    explanation = "Fix doesn't satisfy test requirements"
            else:
                root_cause = "INCOMPLETE_FIX"
                explanation = "Fix addresses part of the problem but misses edge cases or requirements"

    return {
        'instance_id': instance_id,
        'problem': problem,
        'agent_reasoning': agent_reasoning,
        'patch_files': patch_summary.get('files', []),
        'key_changes': patch_summary.get('key_changes', []),
        'test_failure': test_failure,
        'root_cause': root_cause,
        'explanation': explanation,
        'cost': info.get('model_stats', {}).get('instance_cost', 0)
    }

def main():
    # Read list of instances
    with open('no_rule_violation_instances.txt') as f:
        instances = [line.strip() for line in f if line.strip()]

    results = []
    root_causes = {}

    for instance_id in instances:
        traj_file = f'trajs/{instance_id}/{instance_id}.traj.json'
        if not os.path.exists(traj_file):
            continue

        try:
            with open(traj_file) as f:
                data = json.load(f)
            result = determine_root_cause(instance_id, data)
            results.append(result)

            cause = result['root_cause']
            if cause not in root_causes:
                root_causes[cause] = []
            root_causes[cause].append(result)
        except Exception as e:
            print(f"Error: {instance_id}: {e}")

    # Generate detailed report
    print("# Root Cause Analysis Report")
    print()
    print("## Summary by Root Cause")
    print()
    print("| Root Cause | Count | % |")
    print("|------------|-------|---|")
    for cause in sorted(root_causes.keys(), key=lambda x: -len(root_causes[x])):
        count = len(root_causes[cause])
        pct = 100 * count / len(results)
        print(f"| {cause} | {count} | {pct:.1f}% |")

    print()
    print("## Detailed Analysis by Instance")
    print()

    for result in results:
        print(f"### {result['instance_id']}")
        print()
        print(f"**Root Cause:** {result['root_cause']}")
        print()
        print(f"**Explanation:** {result['explanation']}")
        print()
        print("**Problem:**")
        print(f"> {result['problem'][:300]}...")
        print()
        print(f"**Files Modified:** {', '.join(result['patch_files'][:3])}")
        print()
        if result['key_changes']:
            print("**Key Changes:**")
            for change in result['key_changes'][:3]:
                print(f"- `{change}`")
            print()
        if result['test_failure']:
            print("**Test Failure:**")
            print(f"```\n{result['test_failure'][:200]}\n```")
            print()
        print(f"**Cost:** ${result['cost']:.2f}")
        print()
        print("---")
        print()

if __name__ == '__main__':
    main()
