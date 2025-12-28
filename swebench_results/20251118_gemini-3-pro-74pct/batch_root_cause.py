#!/usr/bin/env python3
"""Batch analyze all no-rule-violation failures to identify root causes."""

import json
import re
import os
from collections import defaultdict

def extract_problem_statement(messages):
    """Extract problem statement."""
    for msg in messages[:5]:
        content = msg.get('content', '')
        # Look for PR description
        if '<pr_description>' in content:
            match = re.search(r'<pr_description>(.*?)</pr_description>', content, re.DOTALL)
            if match:
                return match.group(1).strip()[:1500]
        if 'problem_statement' in content.lower():
            match = re.search(r'<problem_statement>(.*?)</problem_statement>', content, re.DOTALL)
            if match:
                return match.group(1).strip()[:1500]
    return ""

def extract_patch(data):
    """Extract the submitted patch."""
    return data.get('info', {}).get('submission', '')

def count_files_modified(patch):
    """Count files modified in patch."""
    if not patch:
        return 0
    return len(re.findall(r'^diff --git', patch, re.MULTILINE))

def get_modified_files(patch):
    """Get list of modified files."""
    if not patch:
        return []
    return re.findall(r'^diff --git a/(\S+)', patch, re.MULTILINE)

def analyze_fix_pattern(patch):
    """Analyze what kind of fix was attempted."""
    if not patch:
        return "no_patch"

    patterns = {
        'try_except_added': bool(re.search(r'\+\s*try:', patch)),
        'if_check_added': bool(re.search(r'\+\s*if\s+', patch)),
        'return_added': bool(re.search(r'\+\s*return\s+', patch)),
        'raise_added': bool(re.search(r'\+\s*raise\s+', patch)),
        'import_added': bool(re.search(r'\+\s*(from|import)\s+', patch)),
        'method_added': bool(re.search(r'\+\s*def\s+', patch)),
        'class_added': bool(re.search(r'\+\s*class\s+', patch)),
        'string_change': bool(re.search(r'[-+]\s*["\'].*["\']', patch)),
    }

    active = [k for k, v in patterns.items() if v]
    return ','.join(active) if active else 'simple_edit'

def identify_error_types(messages):
    """Identify what errors occurred during the run."""
    errors = defaultdict(int)
    for msg in messages:
        content = msg.get('content', '')
        for error_type in ['TypeError', 'AttributeError', 'KeyError', 'ValueError',
                          'NameError', 'ImportError', 'IndexError', 'AssertionError',
                          'SyntaxError', 'IndentationError', 'ModuleNotFoundError']:
            if error_type in content:
                errors[error_type] += 1
    return dict(errors)

def categorize_failure(instance_id, data):
    """Categorize a single failure."""
    messages = data.get('messages', [])
    info = data.get('info', {})

    problem = extract_problem_statement(messages)
    patch = extract_patch(data)
    files_modified = get_modified_files(patch)
    fix_pattern = analyze_fix_pattern(patch)
    errors = identify_error_types(messages)

    # Determine likely root cause category
    category = "unknown"

    if not patch or patch.strip() == "":
        category = "no_fix_submitted"
    elif len(files_modified) > 3:
        category = "over_engineered"
    elif errors.get('SyntaxError', 0) > 2 or errors.get('IndentationError', 0) > 2:
        category = "syntax_errors_in_fix"
    elif errors.get('TypeError', 0) > 5 or errors.get('AttributeError', 0) > 5:
        category = "api_misunderstanding"
    elif 'try_except_added' in fix_pattern and errors.get('TypeError', 0) > 0:
        category = "error_handling_wrong"
    elif not errors:
        category = "logic_incorrect"
    else:
        category = "incomplete_fix"

    return {
        'instance_id': instance_id,
        'problem_snippet': problem[:200] + '...' if len(problem) > 200 else problem,
        'files_modified': files_modified,
        'fix_pattern': fix_pattern,
        'errors_encountered': errors,
        'category': category,
        'api_calls': info.get('model_stats', {}).get('api_calls', 0),
        'cost': info.get('model_stats', {}).get('instance_cost', 0)
    }

def main():
    # Read list of no-rule-violation instances
    with open('no_rule_violation_instances.txt') as f:
        instances = [line.strip() for line in f if line.strip()]

    results = []
    categories = defaultdict(list)

    for instance_id in instances:
        traj_file = f'trajs/{instance_id}/{instance_id}.traj.json'
        if not os.path.exists(traj_file):
            continue

        try:
            with open(traj_file) as f:
                data = json.load(f)
            result = categorize_failure(instance_id, data)
            results.append(result)
            categories[result['category']].append(instance_id)
        except Exception as e:
            print(f"Error processing {instance_id}: {e}")

    # Print summary
    print("=" * 70)
    print("ROOT CAUSE CATEGORY SUMMARY")
    print("=" * 70)
    print()

    for cat, instances in sorted(categories.items(), key=lambda x: -len(x[1])):
        print(f"{cat}: {len(instances)} instances")
        for inst in instances[:5]:
            print(f"  - {inst}")
        if len(instances) > 5:
            print(f"  ... and {len(instances) - 5} more")
        print()

    # Print detailed info for each category
    print("=" * 70)
    print("DETAILED FAILURE ANALYSIS")
    print("=" * 70)

    for result in results:
        print(f"\n### {result['instance_id']}")
        print(f"Category: {result['category']}")
        print(f"Fix pattern: {result['fix_pattern']}")
        print(f"Files modified: {', '.join(result['files_modified'][:3])}")
        print(f"Errors: {result['errors_encountered']}")
        print(f"Cost: ${result['cost']:.2f}, API calls: {result['api_calls']}")

if __name__ == '__main__':
    main()
