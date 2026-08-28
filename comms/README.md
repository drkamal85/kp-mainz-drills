# comms

`motion-snapshot.json` is written nightly (03:00 UTC) by the **Motion Snapshot** Action.

The Mentor chat reads this file instead of calling `api.usemotion.com` directly
(that host is not allowlisted in the sandbox).

Requires repo secret **MOTION_API_KEY**.
