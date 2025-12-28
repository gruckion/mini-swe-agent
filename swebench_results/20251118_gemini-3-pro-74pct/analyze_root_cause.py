#!/usr/bin/env python3
"""Analyze a trajectory to identify root cause of failure."""

import json
import re
import sys

def extract_problem_statement(messages):
    """Extract the problem statement from first message."""
    if messages and messages[0].get('role') == 'user':
        content = messages[0].get('content', '')
        # Look for problem statement section
        match = re.search(r'<problem_statement>(.*?)</problem_statement>', content, re.DOTALL)
        if match:
            return match.group(1).strip()[:2000]
        # Fallback: first 2000 chars
        return content[:2000]
    return "No problem statement found"

def extract_final_patch(data):
    """Extract the final patch/diff from info."""
    info = data.get('info', {})
    return info.get('submission', '')[:3000]

def extract_test_output(messages):
    """Extract test failure output from messages."""
    test_outputs = []
    for msg in reversed(messages):
        if msg.get('role') == 'user':
            content = msg.get('content', '')
            # Look for test failures
            if 'FAILED' in content or 'Error' in content or 'error' in content:
                # Extract relevant portion
                lines = content.split('\n')
                relevant = []
                capture = False
                for line in lines:
                    if 'FAILED' in line or 'Error' in line or 'assert' in line.lower():
                        capture = True
                    if capture:
                        relevant.append(line)
                    if len(relevant) > 30:
                        break
                if relevant:
                    test_outputs.append('\n'.join(relevant[:30]))
                    if len(test_outputs) >= 2:
                        break
    return '\n---\n'.join(test_outputs) if test_outputs else "No test output found"

def extract_agent_reasoning(messages):
    """Extract key reasoning from agent about their fix."""
    reasoning = []
    for msg in messages:
        if msg.get('role') == 'assistant':
            content = msg.get('content', '')
            # Look for reasoning about the fix
            if any(kw in content.lower() for kw in ['fix', 'solution', 'the issue', 'the problem', 'i will', 'i need to']):
                # Get first 500 chars of this reasoning
                snippet = content[:500]
                if snippet not in reasoning:
                    reasoning.append(snippet)
                if len(reasoning) >= 3:
                    break
    return '\n---\n'.join(reasoning) if reasoning else "No reasoning found"

def analyze_trajectory(instance_id):
    """Analyze a single trajectory."""
    traj_file = f'trajs/{instance_id}/{instance_id}.traj.json'

    try:
        with open(traj_file) as f:
            data = json.load(f)
    except Exception as e:
        return f"Error loading trajectory: {e}"

    messages = data.get('messages', [])

    result = {
        'instance_id': instance_id,
        'problem_statement': extract_problem_statement(messages),
        'final_patch': extract_final_patch(data),
        'test_output': extract_test_output(messages),
        'agent_reasoning': extract_agent_reasoning(messages)
    }

    return result

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python analyze_root_cause.py <instance_id>")
        sys.exit(1)

    instance_id = sys.argv[1]
    result = analyze_trajectory(instance_id)

    if isinstance(result, str):
        print(result)
    else:
        print(f"=" * 70)
        print(f"INSTANCE: {result['instance_id']}")
        print(f"=" * 70)
        print(f"\n### PROBLEM STATEMENT ###\n{result['problem_statement']}")
        print(f"\n### AGENT REASONING ###\n{result['agent_reasoning']}")
        print(f"\n### FINAL PATCH ###\n{result['final_patch'][:1500]}")
        print(f"\n### TEST OUTPUT ###\n{result['test_output']}")
