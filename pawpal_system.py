from __future__ import annotations
from dataclasses import dataclass, field
from datetime import date as _date
from typing import Optional


# ---------------------------------------------------------------------------
# Time utilities
# ---------------------------------------------------------------------------

def _time_to_min(t: str) -> int:
    """Convert 'HH:MM' to minutes since midnight."""
    h, m = map(int, t.split(":"))
    return h * 60 + m


def _min_to_time(minutes: int) -> str:
    """Convert minutes since midnight to 'HH:MM'."""
    h, m = divmod(minutes, 60)
    return f"{h:02d}:{m:02d}"


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                      # "low" | "medium" | "high"
    category: str                      # "walk" | "feeding" | "meds" | "grooming" | "enrichment"
    fixed_time: Optional[str] = None   # e.g. "08:00" — None means flexible
    is_recurring: bool = False
    frequency: str = "daily"           # "daily" | "weekly"
    completed: bool = False

    def mark_complete(self) -> None:
        """Mark this task as done."""
        self.completed = True

    def priority_value(self) -> int:
        """Return numeric priority: high=3, medium=2, low=1."""
        return {"high": 3, "medium": 2, "low": 1}.get(self.priority, 0)

    def is_fixed_time(self) -> bool:
        """Return True if this task must start at a specific time."""
        return self.fixed_time is not None

    def fits_in(self, available_minutes: int) -> bool:
        """Return True if this task's duration fits within the given budget."""
        return self.duration_minutes <= available_minutes


@dataclass
class Pet:
    name: str
    species: str                       # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        self.tasks.append(task)

    def remove_task(self, title: str) -> None:
        """Remove all tasks whose title matches (case-insensitive)."""
        self.tasks = [t for t in self.tasks if t.title.lower() != title.lower()]

    def get_tasks(self) -> list[Task]:
        """Return a copy of the task list."""
        return list(self.tasks)


@dataclass
class Owner:
    name: str
    available_minutes: int
    day_start: str = "08:00"           # when the care day begins, e.g. "08:00"
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        self.pets.append(pet)

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        for pet in self.pets:
            if pet.name.lower() == name.lower():
                return pet
        return None


@dataclass
class ScheduledEntry:
    task: Task
    start_time: str    # e.g. "08:00"
    end_time: str      # e.g. "08:30"
    reason: str        # human-readable explanation for why/when this was scheduled


@dataclass
class DailySchedule:
    pet_name: str
    owner_name: str
    date: str                          # e.g. "2026-07-06"
    entries: list[ScheduledEntry] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_duration_minutes: int = 0

    def add_entry(self, entry: ScheduledEntry) -> None:
        """Append an entry and keep total_duration_minutes in sync."""
        self.entries.append(entry)
        self.total_duration_minutes += entry.task.duration_minutes

    def get_summary(self) -> str:
        """Return a formatted timetable string for display."""
        if not self.entries:
            return f"No tasks scheduled for {self.pet_name} on {self.date}."
        lines = [f"Daily plan for {self.pet_name} ({self.owner_name}) — {self.date}:"]
        for e in self.entries:
            lines.append(
                f"  {e.start_time}–{e.end_time}  {e.task.title}"
                f" ({e.task.duration_minutes} min) [{e.task.priority}]"
            )
        lines.append(f"Total: {self.total_duration_minutes} min")
        return "\n".join(lines)

    def explain(self) -> str:
        """Return a plain-English explanation of the plan including any skipped tasks."""
        lines = [f"Reasoning for {self.pet_name}'s schedule on {self.date}:"]
        for e in self.entries:
            lines.append(f"  • {e.task.title}: {e.reason}")
        if self.skipped_tasks:
            names = ", ".join(t.title for t in self.skipped_tasks)
            lines.append(f"Skipped (time ran out or conflict): {names}")
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Scheduler
# ---------------------------------------------------------------------------

class Scheduler:
    """Stateless scheduling logic. Call schedule_day() to produce a DailySchedule."""

    def schedule_day(self, pet: Pet, owner: Owner) -> DailySchedule:
        """Build and return a DailySchedule for the pet within the owner's time budget."""
        tasks = pet.get_tasks()
        fixed = [t for t in tasks if t.is_fixed_time()]
        flexible = [t for t in tasks if not t.is_fixed_time()]

        fixed_entries = self._place_fixed_tasks(fixed, owner.day_start)

        # Remove conflicting fixed-time tasks and surface them as skipped
        conflicts = self._detect_conflicts(fixed_entries)
        conflict_titles = {title for pair in conflicts for title in pair}
        fixed_entries = [e for e in fixed_entries if e.task.title not in conflict_titles]
        conflict_tasks = [t for t in fixed if t.title in conflict_titles]

        fixed_time_used = sum(e.task.duration_minutes for e in fixed_entries)
        remaining = owner.available_minutes - fixed_time_used

        sorted_flexible = self._sort_by_priority(flexible)
        flexible_entries = self._fill_remaining(
            sorted_flexible, fixed_entries, remaining, owner.day_start
        )

        all_entries = sorted(
            fixed_entries + flexible_entries,
            key=lambda e: _time_to_min(e.start_time),
        )

        scheduled_titles = {e.task.title for e in all_entries}
        skipped = conflict_tasks + [t for t in tasks if t.title not in scheduled_titles]

        schedule = DailySchedule(
            pet_name=pet.name,
            owner_name=owner.name,
            date=str(_date.today()),
        )
        for entry in all_entries:
            schedule.add_entry(entry)
        schedule.skipped_tasks = skipped
        return schedule

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks highest-priority first; shorter duration breaks ties."""
        # Primary: highest priority first. Tie-break: shorter task first.
        return sorted(tasks, key=lambda t: (-t.priority_value(), t.duration_minutes))

    def _place_fixed_tasks(self, tasks: list[Task], day_start: str) -> list[ScheduledEntry]:
        """Create entries for tasks that have a required start time."""
        entries = []
        for i, task in enumerate(tasks):
            start_min = _time_to_min(task.fixed_time)
            entries.append(ScheduledEntry(
                task=task,
                start_time=_min_to_time(start_min),
                end_time=_min_to_time(start_min + task.duration_minutes),
                reason=self._build_reason(task, i + 1),
            ))
        return entries

    def _fill_remaining(
        self,
        tasks: list[Task],
        fixed_entries: list[ScheduledEntry],
        remaining_minutes: int,
        day_start: str,
    ) -> list[ScheduledEntry]:
        """Greedily fill remaining time with flexible tasks, jumping over fixed windows."""
        # Build sorted list of occupied (start, end) windows to navigate around
        occupied = sorted(
            (_time_to_min(e.start_time), _time_to_min(e.end_time))
            for e in fixed_entries
        )

        entries: list[ScheduledEntry] = []
        cursor = _time_to_min(day_start)
        budget_left = remaining_minutes

        for task in tasks:
            if not task.fits_in(budget_left):
                continue

            # Advance cursor forward until it clears all overlapping fixed windows
            moved = True
            while moved:
                moved = False
                for occ_start, occ_end in occupied:
                    if cursor < occ_end and cursor + task.duration_minutes > occ_start:
                        cursor = occ_end
                        moved = True
                        break

            position = len(fixed_entries) + len(entries) + 1
            entries.append(ScheduledEntry(
                task=task,
                start_time=_min_to_time(cursor),
                end_time=_min_to_time(cursor + task.duration_minutes),
                reason=self._build_reason(task, position),
            ))
            cursor += task.duration_minutes
            budget_left -= task.duration_minutes

        return entries

    def _detect_conflicts(self, entries: list[ScheduledEntry]) -> list[tuple[str, str]]:
        """Return (title_a, title_b) pairs whose time windows overlap."""
        conflicts = []
        for i, a in enumerate(entries):
            for b in entries[i + 1:]:
                a_start, a_end = _time_to_min(a.start_time), _time_to_min(a.end_time)
                b_start, b_end = _time_to_min(b.start_time), _time_to_min(b.end_time)
                if a_start < b_end and b_start < a_end:
                    conflicts.append((a.task.title, b.task.title))
        return conflicts

    def _build_reason(self, task: Task, position: int) -> str:
        """Build a human-readable explanation for why a task was scheduled at its slot."""
        parts = [f"#{position}", f"priority: {task.priority}"]
        if task.is_fixed_time():
            parts.append(f"fixed at {task.fixed_time}")
        else:
            parts.append("flexible — fit into available time")
        parts.append(f"category: {task.category}")
        return ", ".join(parts)
