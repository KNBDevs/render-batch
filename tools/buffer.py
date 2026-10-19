import json, os
from datetime import datetime, timezone
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
s = json.load(open(os.path.join(ROOT, "state", "schedule.json")))
now = datetime.now(timezone.utc)
fut = sorted(datetime.fromisoformat(v.replace("Z", "+00:00")) for v in s.values())
fut = [t for t in fut if t > now]
days = sorted({t.date() for t in fut})
run = 0
d = now.date()
from datetime import timedelta
while d + timedelta(days=run) in days or (run == 0 and fut and fut[0].date() == d):
    run += 1
    if run > 60:
        break
print(run)
