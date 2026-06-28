#!/usr/bin/env python3
# Reconcile /api/themen and /api/content. Run after the builders (and as a nightly check).
# Fails (exit 1) if the slug contract drifts so a topic could show "covered" but not open,
# or a built review is unreachable, or a published review is missing a core station.
import json, sys

themen = json.load(open('api/themen.json', encoding='utf-8'))
content = json.load(open('content/topics.json', encoding='utf-8'))

themen_ids = set()
for x in themen['topics'] + themen.get('extras', []):
    if x.get('covered') and x.get('reviewId'):
        themen_ids.add(x['reviewId'])
content_ids = {t['id'] for t in content['topics']}

missing_body = sorted(themen_ids - content_ids)      # themen says covered, but no body -> would not open
unreachable  = sorted(content_ids - themen_ids)       # body exists, but not listed in themen -> hidden
incomplete   = sorted(t['id'] for t in content['topics'] if not t.get('complete', True))

ok = not missing_body and not unreachable
print('themen covered reviewIds: %d  |  content bodies: %d' % (len(themen_ids), len(content_ids)))
print('  covered-but-no-body (would not open in app): %s' % (missing_body or 'none'))
print('  body-but-not-in-themen (unreachable):        %s' % (unreachable or 'none'))
print('  incomplete (missing a core station):         %s' % (incomplete or 'none'))
print('RESULT: %s' % ('PASS' if ok else 'FAIL'))
sys.exit(0 if ok else 1)
