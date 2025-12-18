# Failure Report: django__django-15252

**Labels:** `no-rule-violation`, `incorrect-fix-logic`

## Summary
Incorrect fix logic - changes don't pass original test suite

## Evidence

### Basic Info
- API Calls: 22
- Cost: $0.3238773999999999
- Max Tokens: 19716

### Files Modified
```
- django/db/migrations/recorder.py
```

### Agent Reasoning About Tests
I'll modify the reproduction script to test `record_applied`.

## Conclusion
**Failure Type:** Incorrect fix logic - changes don't pass original test suite
