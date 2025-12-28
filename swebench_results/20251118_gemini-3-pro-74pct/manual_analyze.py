#!/usr/bin/env python3
"""Manual deep analysis of each failure."""

import json
import re
import os
import sys

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

    # 3. Find all error messages and test failures
    errors = []
    for msg in messages:
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            # Look for errors
            for error_type in ['Error', 'FAILED', 'assert']:
                if error_type in content:
                    # Get relevant context
                    lines = content.split('\n')
                    for i, line in enumerate(lines):
                        if error_type in line:
                            context = lines[max(0, i-2):min(len(lines), i+5)]
                            err_text = '\n'.join(context)
                            if err_text not in errors and len(err_text) > 20:
                                errors.append(err_text[:400])
                    break

    # 4. Extract agent's understanding of the fix
    fix_reasoning = []
    for msg in messages:
        if msg.get('role') == 'assistant':
            content = msg.get('content', '')
            thought_match = re.search(r'THOUGHT:(.+?)```', content, re.DOTALL)
            if thought_match:
                thought = thought_match.group(1).strip()
                if any(kw in thought.lower() for kw in ['fix', 'issue', 'problem', 'solution', 'change', 'modify']):
                    if thought[:300] not in fix_reasoning:
                        fix_reasoning.append(thought[:300])

    print(f"{'='*70}")
    print(f"INSTANCE: {instance_id}")
    print(f"{'='*70}")
    print()
    print("## PROBLEM STATEMENT")
    print(problem[:1500])
    print()
    print("## AGENT'S REASONING (key thoughts)")
    for i, r in enumerate(fix_reasoning[:3]):
        print(f"\n[Thought {i+1}]")
        print(r)
    print()
    print("## PATCH SUBMITTED")
    print(patch[:2000] if patch else "NO PATCH")
    print()
    print("## ERRORS/FAILURES ENCOUNTERED")
    for i, e in enumerate(errors[:3]):
        print(f"\n[Error {i+1}]")
        print(e)
    print()
    print(f"Cost: ${info.get('model_stats', {}).get('instance_cost', 0):.2f}")
    print(f"API calls: {info.get('model_stats', {}).get('api_calls', 0)}")

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python manual_analyze.py <instance_id>")
        sys.exit(1)

    get_full_analysis(sys.argv[1])
