# Failure Report: django__django-13195

**Labels:** `no-rule-violation`, `incorrect-fix-logic`

## Summary
Incorrect fix logic - changes don't pass original test suite

## Evidence

### Basic Info
- API Calls: 27
- Cost: $0.3780686
- Max Tokens: 23078

### Files Modified
```
- django/contrib/messages/storage/cookie.py
- django/contrib/sessions/middleware.py
- django/http/response.py
```

### Agent Reasoning About Tests
However, the task instructions say: "Your task is specifically to make changes to non-test files in the current directory in order to fix the issue described in the PR description in a way that is general and consistent with the codebase."
The instructions say "MODIFY: Regular source code files in /testbed".
I need to update the reproduction script to test the new arguments.
THOUGHT: I see `tests/responses/test_cookie.py`. I should not modify tests, but I should check if my changes break them.
And `docs/ref/request-response.txt` which I should probably not modify as per instructions "MODIFY: Regular source code files". Usually documentation is not required unless specified, but "Regular source code files" usually excludes docs. But if I change the signature, docs are outdated. However, the instructions say "MODIFY: Regular source code files in /testbed". Docs are usually text files. I'll skip docs.

## Conclusion
**Failure Type:** Incorrect fix logic - changes don't pass original test suite
