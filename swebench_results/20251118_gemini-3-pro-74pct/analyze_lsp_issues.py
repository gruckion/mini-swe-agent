#!/usr/bin/env python3
"""
Analyze SWE-bench failures for LSP-detectable issues.

Categories of LSP-detectable issues:
1. Undefined symbols/variables
2. Signature mismatches (wrong args)
3. Type errors
4. Wrong/missing imports
5. Wrong member access (attribute doesn't exist)
6. Syntax errors
"""

import json
import os
import re
import glob
from collections import defaultdict

def extract_submission(traj_file):
    """Extract the submission diff from a trajectory file."""
    try:
        with open(traj_file) as f:
            data = json.load(f)
        return data.get('info', {}).get('submission', '')
    except:
        return ''

def analyze_diff_for_lsp_issues(diff, instance_id):
    """
    Analyze a diff for potential LSP-detectable issues.
    Returns a dict with issue categories and evidence.
    """
    issues = {
        'undefined_symbol': [],
        'signature_mismatch': [],
        'type_error': [],
        'import_issue': [],
        'attribute_error': [],
        'syntax_error': [],
        'other': []
    }

    if not diff:
        return {'empty_submission': True}

    # Split into added lines (+ prefix)
    added_lines = []
    current_file = None
    for line in diff.split('\n'):
        if line.startswith('diff --git'):
            match = re.search(r'a/(.+?) b/', line)
            if match:
                current_file = match.group(1)
        elif line.startswith('+') and not line.startswith('+++'):
            added_lines.append((current_file, line[1:]))  # Remove + prefix

    for file_path, line in added_lines:
        # Skip test files and config files
        if file_path and ('test' in file_path.lower() or file_path.endswith(('.toml', '.cfg', '.ini'))):
            continue

        # Check for potential undefined symbols
        # Look for variables used before definition, typos, etc.

        # Check for common patterns that indicate issues:

        # 1. Calling methods that might not exist
        method_calls = re.findall(r'\.(\w+)\s*\(', line)

        # 2. Using variables that look like typos (uncommon patterns)
        # This is heuristic - real LSP would know the scope

        # 3. Import issues - importing from wrong module
        import_match = re.search(r'from\s+(\S+)\s+import|import\s+(\S+)', line)
        if import_match:
            # Check if this looks like a potentially wrong import
            pass

        # 4. Check for obvious syntax issues
        # Unmatched brackets, invalid Python, etc.
        try:
            # Try to compile the line as an expression
            # This won't catch everything but catches obvious issues
            pass
        except:
            issues['syntax_error'].append(line)

    return issues

def analyze_trajectory_for_repair_loops(traj_file):
    """
    Analyze a trajectory for signs of repair loops caused by LSP-detectable issues.

    Look for patterns like:
    - Agent makes change
    - Error occurs (NameError, AttributeError, TypeError, ImportError)
    - Agent tries to fix
    """
    try:
        with open(traj_file) as f:
            data = json.load(f)
    except:
        return None

    messages = data.get('messages', [])

    # Track error patterns in the trajectory
    error_patterns = {
        'NameError': [],      # Undefined symbol
        'AttributeError': [], # Wrong member access
        'TypeError': [],      # Signature mismatch / type error
        'ImportError': [],    # Import issues
        'ModuleNotFoundError': [],
        'SyntaxError': [],
        'IndentationError': [],
    }

    repair_indicators = []
    step_count = 0
    first_error_step = None

    for i, msg in enumerate(messages):
        if msg.get('role') == 'user':
            content = msg.get('content', '')

            # Look for error outputs
            for error_type in error_patterns.keys():
                if error_type in content:
                    error_patterns[error_type].append(i)
                    if first_error_step is None:
                        first_error_step = i

            # Look for common error messages
            if 'Traceback' in content:
                repair_indicators.append(('traceback', i))
            if 'Error' in content and 'returncode' in content:
                repair_indicators.append(('error_return', i))

    # Calculate metrics
    total_messages = len(messages)
    info = data.get('info', {})

    return {
        'instance_id': os.path.basename(traj_file).replace('.traj.json', ''),
        'total_messages': total_messages,
        'api_calls': info.get('model_stats', {}).get('api_calls', 0),
        'cost': info.get('model_stats', {}).get('instance_cost', 0),
        'first_error_step': first_error_step,
        'error_patterns': {k: len(v) for k, v in error_patterns.items() if v},
        'total_errors': sum(len(v) for v in error_patterns.values()),
        'repair_indicators': len(repair_indicators),
        'steps_after_first_error': total_messages - first_error_step if first_error_step else 0,
    }

def main():
    traj_dir = 'trajs'

    # Get all failed instances
    failed_instances = []
    with open('RESULTS.md') as f:
        content = f.read()
        # Extract failed instance IDs
        in_failed_section = False
        for line in content.split('\n'):
            if '❌ Failed' in line:
                in_failed_section = True
            elif '✅ Passed' in line or '</details>' in line:
                in_failed_section = False
            elif in_failed_section and line.startswith('- ['):
                match = re.search(r'\[([^\]]+)\]', line)
                if match:
                    failed_instances.append(match.group(1))

    print(f"Analyzing {len(failed_instances)} failed instances...")
    print()

    # Analyze each failure
    results = []
    lsp_detectable_count = 0

    for instance_id in failed_instances:
        traj_file = f'{traj_dir}/{instance_id}/{instance_id}.traj.json'
        if not os.path.exists(traj_file):
            continue

        analysis = analyze_trajectory_for_repair_loops(traj_file)
        if analysis:
            results.append(analysis)

            # Count LSP-detectable issues
            if analysis['error_patterns']:
                lsp_detectable_count += 1

    # Summary statistics
    print("=" * 60)
    print("LSP-DETECTABLE ERROR ANALYSIS")
    print("=" * 60)
    print()

    # Count by error type
    error_type_counts = defaultdict(int)
    for r in results:
        for error_type, count in r['error_patterns'].items():
            if count > 0:
                error_type_counts[error_type] += 1

    print("Failures with LSP-detectable errors:")
    print(f"  Total: {lsp_detectable_count} / {len(results)} ({100*lsp_detectable_count/len(results):.1f}%)")
    print()
    print("By error type:")
    for error_type, count in sorted(error_type_counts.items(), key=lambda x: -x[1]):
        print(f"  {error_type}: {count} instances")
    print()

    # Analyze repair loop cost
    with_errors = [r for r in results if r['total_errors'] > 0]
    without_errors = [r for r in results if r['total_errors'] == 0]

    if with_errors:
        avg_steps_after_error = sum(r['steps_after_first_error'] for r in with_errors) / len(with_errors)
        avg_cost_with_errors = sum(r['cost'] for r in with_errors) / len(with_errors)
        avg_calls_with_errors = sum(r['api_calls'] for r in with_errors) / len(with_errors)
        print(f"Failures WITH LSP-detectable errors ({len(with_errors)}):")
        print(f"  Avg steps after first error: {avg_steps_after_error:.1f}")
        print(f"  Avg cost: ${avg_cost_with_errors:.2f}")
        print(f"  Avg API calls: {avg_calls_with_errors:.1f}")
        print()

    if without_errors:
        avg_cost_without_errors = sum(r['cost'] for r in without_errors) / len(without_errors)
        avg_calls_without_errors = sum(r['api_calls'] for r in without_errors) / len(without_errors)
        print(f"Failures WITHOUT LSP-detectable errors ({len(without_errors)}):")
        print(f"  Avg cost: ${avg_cost_without_errors:.2f}")
        print(f"  Avg API calls: {avg_calls_without_errors:.1f}")
        print()

    # Output detailed results
    print("=" * 60)
    print("INSTANCES WITH MOST REPAIR LOOPS")
    print("=" * 60)

    sorted_by_errors = sorted(results, key=lambda x: x['total_errors'], reverse=True)[:20]
    for r in sorted_by_errors:
        if r['total_errors'] > 0:
            print(f"\n{r['instance_id']}:")
            print(f"  Errors: {r['error_patterns']}")
            print(f"  Steps after first error: {r['steps_after_first_error']}")
            print(f"  Cost: ${r['cost']:.2f}, API calls: {r['api_calls']}")

if __name__ == '__main__':
    main()
