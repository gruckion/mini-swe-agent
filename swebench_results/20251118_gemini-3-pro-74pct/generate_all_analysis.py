#!/usr/bin/env python3
"""Generate detailed analysis for all 95 no-rule-violation failures."""

import json
import re
import os

def get_full_analysis(instance_id):
    """Get comprehensive analysis for a single instance."""
    traj_file = f'trajs/{instance_id}/{instance_id}.traj.json'

    with open(traj_file) as f:
        data = json.load(f)

    messages = data.get('messages', [])
    info = data.get('info', {})

    # 1. Extract problem statement
    problem = ""
    for msg in messages[:5]:
        content = msg.get('content', '')
        if '<pr_description>' in content:
            match = re.search(r'<pr_description>(.*?)</pr_description>', content, re.DOTALL)
            if match:
                problem = match.group(1).strip()
                break

    # 2. Extract the patch
    patch = info.get('submission', '')

    # 3. Get files modified
    files_modified = re.findall(r'^diff --git a/(\S+)', patch, re.MULTILINE) if patch else []

    # 4. Extract key code changes
    key_changes = []
    if patch:
        for match in re.finditer(r'^\+\s*(.+)$', patch, re.MULTILINE):
            line = match.group(1).strip()
            if line and not line.startswith('+') and len(line) > 10:
                if any(kw in line for kw in ['def ', 'class ', 'if ', 'return ', 'raise ', 'try:', 'except', 'elif', 'else:']):
                    key_changes.append(line[:100])

    # 5. Find agent's core reasoning about the fix
    fix_thoughts = []
    for msg in messages:
        if msg.get('role') == 'assistant':
            content = msg.get('content', '')
            thought_match = re.search(r'THOUGHT:(.+?)(?:```|$)', content, re.DOTALL)
            if thought_match:
                thought = thought_match.group(1).strip()
                if any(kw in thought.lower() for kw in ['fix', 'the issue', 'the problem', 'solution', 'i will change', 'i need to modify']):
                    if len(thought) > 50:
                        fix_thoughts.append(thought[:500])

    # 6. Find test failure messages
    test_failures = []
    for msg in messages:
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            if 'FAILED' in content or 'AssertionError' in content or 'Error' in content:
                lines = content.split('\n')
                for i, line in enumerate(lines):
                    if 'FAILED' in line or 'AssertionError' in line or 'Error' in line:
                        context = '\n'.join(lines[max(0, i-1):min(len(lines), i+4)])
                        if len(context) > 20 and context not in test_failures:
                            test_failures.append(context[:300])
                            if len(test_failures) >= 2:
                                break

    # 7. Determine the root cause
    root_cause = determine_root_cause(problem, patch, fix_thoughts, test_failures, files_modified, key_changes)

    return {
        'instance_id': instance_id,
        'problem': problem[:1000],
        'patch': patch[:1500] if patch else "NO PATCH",
        'files_modified': files_modified,
        'key_changes': key_changes[:5],
        'fix_thoughts': fix_thoughts[:2],
        'test_failures': test_failures[:2],
        'root_cause': root_cause,
        'cost': info.get('model_stats', {}).get('instance_cost', 0),
        'api_calls': info.get('model_stats', {}).get('api_calls', 0)
    }

def determine_root_cause(problem, patch, fix_thoughts, test_failures, files_modified, key_changes):
    """Determine the specific root cause of the failure."""

    # Check for specific patterns
    if not patch or len(patch) < 20:
        return {
            'category': 'NO_PATCH',
            'reason': 'Agent did not submit a valid patch'
        }

    if len(files_modified) > 4:
        return {
            'category': 'OVER_ENGINEERING',
            'reason': f'Modified too many files ({len(files_modified)}), likely scope creep'
        }

    # Check if agent understood the problem
    problem_lower = problem.lower()
    patch_lower = patch.lower()

    # Pattern: Agent added wrong type of fix
    if 'raise' in str(key_changes) and 'error' not in problem_lower:
        return {
            'category': 'WRONG_FIX_TYPE',
            'reason': 'Added error raising when problem required different behavior'
        }

    # Pattern: Try-except that swallows errors
    if 'try:' in str(key_changes) and 'except' in str(key_changes):
        if 'pass' in patch_lower or 'return none' in patch_lower.replace(' ', ''):
            return {
                'category': 'SWALLOWED_ERROR',
                'reason': 'Added try-except that silently swallows errors instead of proper handling'
            }

    # Check test failures for hints
    if test_failures:
        failure_text = ' '.join(test_failures).lower()
        if 'assertequal' in failure_text or 'not equal' in failure_text or '!=' in failure_text:
            return {
                'category': 'WRONG_OUTPUT',
                'reason': 'Fix produces incorrect output value - logic error in implementation'
            }
        if 'attributeerror' in failure_text:
            return {
                'category': 'API_MISUSE',
                'reason': 'Used wrong attribute or method name'
            }
        if 'typeerror' in failure_text:
            return {
                'category': 'TYPE_ERROR',
                'reason': 'Fix has type mismatch - wrong argument types or return type'
            }
        if 'keyerror' in failure_text:
            return {
                'category': 'MISSING_KEY',
                'reason': 'Fix misses handling for certain keys or cases'
            }

    # Default: incomplete fix
    return {
        'category': 'INCOMPLETE_FIX',
        'reason': 'Fix addresses the issue partially but misses edge cases or requirements'
    }

def main():
    # Read list of instances
    with open('no_rule_violation_instances.txt') as f:
        instances = [line.strip() for line in f if line.strip()]

    print("# Detailed Root Cause Analysis: 95 Incorrect Fix Logic Failures")
    print()
    print("This report analyzes each failure to identify exactly why the agent's fix was incorrect.")
    print()

    # Categorize
    categories = {}

    for instance_id in instances:
        try:
            analysis = get_full_analysis(instance_id)

            cat = analysis['root_cause']['category']
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(analysis)

        except Exception as e:
            print(f"Error analyzing {instance_id}: {e}")

    # Print summary
    print("## Summary")
    print()
    print("| Category | Count | Description |")
    print("|----------|-------|-------------|")
    for cat in sorted(categories.keys(), key=lambda x: -len(categories[x])):
        count = len(categories[cat])
        reason = categories[cat][0]['root_cause']['reason'][:50]
        print(f"| {cat} | {count} | {reason}... |")

    print()
    print("---")
    print()

    # Print detailed analysis for each
    print("## Detailed Analysis")
    print()

    for instance_id in instances:
        try:
            analysis = get_full_analysis(instance_id)

            print(f"### {analysis['instance_id']}")
            print()
            print(f"**Category:** {analysis['root_cause']['category']}")
            print()
            print(f"**Root Cause:** {analysis['root_cause']['reason']}")
            print()
            print("**Problem Summary:**")
            # Get first few lines of problem
            prob_lines = analysis['problem'].split('\n')[:5]
            print('> ' + '\n> '.join(prob_lines))
            print()
            print(f"**Files Modified:** `{', '.join(analysis['files_modified'][:3])}`")
            print()
            if analysis['key_changes']:
                print("**Key Code Changes:**")
                for change in analysis['key_changes'][:3]:
                    print(f"- `{change}`")
                print()
            if analysis['fix_thoughts']:
                print("**Agent's Reasoning:**")
                print(f"> {analysis['fix_thoughts'][0][:300]}...")
                print()
            if analysis['test_failures']:
                print("**Test Failure:**")
                print(f"```\n{analysis['test_failures'][0][:200]}\n```")
                print()
            print(f"**Cost:** ${analysis['cost']:.2f} | **API Calls:** {analysis['api_calls']}")
            print()
            print("---")
            print()

        except Exception as e:
            print(f"Error: {instance_id}: {e}")
            print()

if __name__ == '__main__':
    main()
