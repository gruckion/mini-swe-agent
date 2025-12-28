#!/usr/bin/env python3
"""Final comprehensive root cause analysis with specific failure reasons."""

import json
import re
import os

def analyze_failure(instance_id):
    """Analyze a single failure in detail."""
    traj_file = f'trajs/{instance_id}/{instance_id}.traj.json'

    with open(traj_file) as f:
        data = json.load(f)

    messages = data.get('messages', [])
    info = data.get('info', {})
    patch = info.get('submission', '')

    # Extract problem statement
    problem = ""
    for msg in messages[:5]:
        content = msg.get('content', '')
        if '<pr_description>' in content:
            match = re.search(r'<pr_description>(.*?)</pr_description>', content, re.DOTALL)
            if match:
                problem = match.group(1).strip()[:800]
                break

    # Get files modified
    files = re.findall(r'^diff --git a/(\S+)', patch, re.MULTILINE) if patch else []

    # Get key changes
    changes = []
    if patch:
        for match in re.finditer(r'^([+-])(.+)$', patch, re.MULTILINE):
            sign, line = match.groups()
            if line.strip() and not line.startswith(sign) and len(line) > 5:
                changes.append((sign, line.strip()[:80]))

    # Get errors from trajectory
    errors = []
    for msg in messages:
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            for err_type in ['Error', 'FAILED', 'AssertionError']:
                if err_type in content:
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if err_type in line and 'Traceback' not in line:
                            err_context = line[:150]
                            if err_context not in errors:
                                errors.append(err_context)

    # Determine specific root cause
    root_cause = analyze_root_cause(problem, patch, changes, errors, files)

    return {
        'instance_id': instance_id,
        'problem_summary': problem[:300],
        'files_modified': files,
        'num_additions': len([c for c in changes if c[0] == '+']),
        'num_deletions': len([c for c in changes if c[0] == '-']),
        'errors': errors[:3],
        'root_cause': root_cause,
        'cost': info.get('model_stats', {}).get('instance_cost', 0)
    }

def analyze_root_cause(problem, patch, changes, errors, files):
    """Determine specific root cause based on evidence."""

    if not patch:
        return ("NO_PATCH_SUBMITTED", "Agent failed to produce a patch")

    # Check for over-engineering
    if len(files) > 4:
        return ("SCOPE_CREEP", f"Modified {len(files)} files when focused fix needed")

    # Check changes for patterns
    additions = [c[1] for c in changes if c[0] == '+']
    deletions = [c[1] for c in changes if c[0] == '-']

    # Check errors
    error_text = ' '.join(errors).lower()

    if 'assertionerror' in error_text or 'assert' in error_text:
        if '==' in error_text or 'equal' in error_text:
            return ("WRONG_VALUE", "Fix outputs incorrect value - test assertion failed")
        return ("BEHAVIOR_MISMATCH", "Fix behavior doesn't match expected test behavior")

    if 'attributeerror' in error_text:
        return ("WRONG_API", "Used incorrect attribute or method name")

    if 'typeerror' in error_text:
        return ("TYPE_MISMATCH", "Incorrect types - wrong argument or return type")

    if 'nameerror' in error_text:
        return ("UNDEFINED_NAME", "Referenced undefined variable or function")

    if 'keyerror' in error_text:
        return ("MISSING_KEY", "Fix doesn't handle all required dictionary keys")

    if 'indexerror' in error_text:
        return ("INDEX_ERROR", "Array/list index out of bounds")

    if 'syntaxerror' in error_text or 'indentationerror' in error_text:
        return ("SYNTAX_ERROR", "Fix has syntax errors")

    # Analyze based on patch patterns
    if any('try:' in a for a in additions) and any('except' in a for a in additions):
        if any('pass' in a.lower() for a in additions) or any('return None' in a for a in additions):
            return ("SWALLOWED_ERROR", "Try-except silences error instead of proper handling")
        return ("ERROR_HANDLING", "Added error handling but may catch wrong exception types")

    if any('raise' in a for a in additions):
        return ("ADDED_EXCEPTION", "Added exception raising - may be too aggressive")

    # Check if fix is minimal but still wrong
    if len(additions) < 5 and len(deletions) < 3:
        return ("SUBTLE_LOGIC_ERROR", "Small change but logic is incorrect")

    # Default
    return ("INCOMPLETE_FIX", "Fix is incomplete - doesn't handle all cases")

def main():
    # Read instances
    with open('no_rule_violation_instances.txt') as f:
        instances = [line.strip() for line in f if line.strip()]

    results = []
    categories = {}

    for instance_id in instances:
        try:
            result = analyze_failure(instance_id)
            results.append(result)

            cat = result['root_cause'][0]
            if cat not in categories:
                categories[cat] = []
            categories[cat].append(result)
        except Exception as e:
            print(f"Error: {instance_id}: {e}")

    # Print summary
    print("# Final Root Cause Analysis: 95 Incorrect Fix Logic Failures")
    print()
    print("## Category Summary")
    print()
    print("| Root Cause | Count | % | Description |")
    print("|------------|-------|---|-------------|")
    total = len(results)
    for cat in sorted(categories.keys(), key=lambda x: -len(categories[x])):
        items = categories[cat]
        count = len(items)
        pct = 100 * count / total
        desc = items[0]['root_cause'][1][:40]
        print(f"| {cat} | {count} | {pct:.1f}% | {desc}... |")

    print()
    print("## Detailed Breakdown")
    print()

    for cat in sorted(categories.keys(), key=lambda x: -len(categories[x])):
        items = categories[cat]
        print(f"### {cat} ({len(items)} instances)")
        print()
        print(f"**Description:** {items[0]['root_cause'][1]}")
        print()
        print("**Instances:**")
        for item in items:
            print(f"- `{item['instance_id']}` - {item['num_additions']}+ {item['num_deletions']}- lines, ${item['cost']:.2f}")
        print()

    # Generate per-instance report
    print("---")
    print()
    print("## Per-Instance Analysis")
    print()

    for r in results:
        print(f"### {r['instance_id']}")
        print()
        print(f"**Root Cause:** {r['root_cause'][0]} - {r['root_cause'][1]}")
        print()
        print(f"**Files:** `{', '.join(r['files_modified'][:2])}`")
        print()
        print(f"**Changes:** +{r['num_additions']} -{r['num_deletions']} lines")
        print()
        if r['errors']:
            print("**Errors:**")
            for e in r['errors'][:2]:
                print(f"- `{e[:80]}...`")
            print()
        print(f"**Problem:** {r['problem_summary'][:150]}...")
        print()
        print("---")
        print()

if __name__ == '__main__':
    main()
