# Failure Report: django__django-11087

**Labels:** `no-rule-violation`, `incorrect-fix-logic`

## Summary
Incorrect fix logic - changes don't pass original test suite

## Evidence

### Basic Info
- API Calls: 44
- Cost: $0.9866229999999998
- Max Tokens: 59333

### Files Modified
```
- django/db/models/deletion.py
- update_deletion_debug.py
- update_deletion_final.py
```

### Agent Reasoning About Tests
Let's update `test_gfk.py`.
rm reproduce_issue.py check_parents.py check_only.py update_deletion.py test_parent_link.py test_gfk.py
This confirms that the fix works for the reported issue (assuming no signals) and doesn't break existing tests (which use signals).

## Conclusion
**Failure Type:** Incorrect fix logic - changes don't pass original test suite
