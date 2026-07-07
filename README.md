# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

Paste a sample of your app's CLI or Streamlit output here so a reader can see what a generated plan looks like:

```
# e.g.:
# Daily plan for Biscuit (Golden Retriever):
#   08:00 — Morning walk (30 min) [priority: high]
#   09:00 — Feeding (10 min) [priority: high]
#   ...
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
python3 -m pytest

# Run with coverage:
pytest --cov
```

The tests cover task basics, sorting correctness, recurrence logic, and conflict detections.

Sample test output:

```
# Paste your pytest output here
TODAY'S SCHEDULE

Daily plan for Pet1 (Aidan) — 2026-07-06:
  08:00–08:05  Morning meds (5 min) [high]
  08:05–08:15  Feeding (10 min) [high]
  08:15–08:35  Enrichment toy (20 min) [low]
Total: 35 min

Reasoning for Pet1's schedule on 2026-07-06:
  • Morning meds: #1, priority: high, fixed at 08:00, category: meds
  • Feeding: #2, priority: high, flexible — fit into available time, category: feeding
  • Enrichment toy: #3, priority: low, flexible — fit into available time, category: enrichment
--------------------------------------------------

Daily plan for Pet2 (Aidan) — 2026-07-06:
  08:00–08:30  Morning walk (30 min) [high]
  08:30–08:55  Grooming (25 min) [medium]
  09:00–09:10  Breakfast (10 min) [high]
  09:10–09:30  Play session (20 min) [low]
Total: 85 min

Reasoning for Pet2's schedule on 2026-07-06:
  • Morning walk: #2, priority: high, flexible — fit into available time, category: walk
  • Grooming: #3, priority: medium, flexible — fit into available time, category: grooming
  • Breakfast: #1, priority: high, fixed at 09:00, category: feeding
  • Play session: #4, priority: low, flexible — fit into available time, category: enrichme
```

## 📐 Smarter Scheduling

> Fill in once you've implemented scheduling logic.

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | Scheduler.sort_by_time()| uses _time_to_min() to convert "HH:MM" to an integer key |
| Filtering |  Owner.get_tasks(pet_name = None, completed = None)| Filters tassk across all of an owner's pets, with two optional arguments|
| Conflict handling |  Scheduler.check_conflicts(schedules) | Checks for time conflicts and returns list of warning strings |
| Recurring tasks |  Task.mark_complete(), Task.next_occurrence() | Marks a task as complete, next_occurence advances due_date according to setting "daily" or "weekly" |


## 📸 Demo Walkthrough

Run with:
python3 -m streamlit run app.py

1. Enter owner info.
2. Enter pet info.
3.  Add a fixed-time task (ex. feed breakfast) and set fixed or flexible time, category, duration, priority
4. Add as many tasks as needed.
5. Review the task table.
6. Click "Generate Schedule".

## Features
1. Priority-based scheduling
2. Fixed-time placement
3. Conflict detection as warnings
4. Sorting by time
5. Recurrence options
6. Task filtering
7. Schedule explanations

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->
