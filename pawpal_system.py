from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Task:
    title: str
    duration_minutes: int
    priority: str                      # "low" | "medium" | "high"
    category: str                      # "walk" | "feeding" | "meds" | "grooming" | "enrichment"
    fixed_time: Optional[str] = None   # e.g. "08:00" — None means flexible
    is_recurring: bool = False
    frequency: str = "daily"           # "daily" | "weekly"

    def priority_value(self) -> int:
        """Convert priority label to integer for sorting (high=3, medium=2, low=1)."""
        pass

    def is_fixed_time(self) -> bool:
        """Return True if this task has a required start time."""
        pass

    def fits_in(self, available_minutes: int) -> bool:
        """Return True if duration_minutes <= available_minutes."""
        pass


@dataclass
class Pet:
    name: str
    species: str                       # "dog" | "cat" | "other"
    tasks: list[Task] = field(default_factory=list)

    def add_task(self, task: Task) -> None:
        """Append a task to this pet's task list."""
        pass

    def remove_task(self, title: str) -> None:
        """Remove the first task whose title matches (case-insensitive)."""
        pass

    def get_tasks(self) -> list[Task]:
        """Return the full list of tasks."""
        pass


@dataclass
class Owner:
    name: str
    available_minutes: int
    pets: list[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet) -> None:
        """Add a pet to this owner's list."""
        pass

    def get_pet(self, name: str) -> Optional[Pet]:
        """Return the pet with the given name, or None if not found."""
        pass


@dataclass
class ScheduledEntry:
    task: Task
    start_time: str    # e.g. "08:00"
    end_time: str      # e.g. "08:30"
    reason: str        # human-readable explanation for why/when this was scheduled


@dataclass
class DailySchedule:
    pet_name: str
    entries: list[ScheduledEntry] = field(default_factory=list)
    skipped_tasks: list[Task] = field(default_factory=list)
    total_duration_minutes: int = 0

    def get_summary(self) -> str:
        """Return a formatted string listing each scheduled entry with times."""
        pass

    def explain(self) -> str:
        """Return a paragraph explaining the overall plan and any skipped tasks."""
        pass


class Scheduler:
    """Stateless scheduling logic. Call schedule_day() to produce a DailySchedule."""

    def schedule_day(self, pet: Pet, available_minutes: int) -> DailySchedule:
        """Build and return a DailySchedule for the given pet within the time budget."""
        pass

    def _sort_by_priority(self, tasks: list[Task]) -> list[Task]:
        """Sort tasks high→low priority; break ties by shorter duration first."""
        pass

    def _place_fixed_tasks(self, tasks: list[Task]) -> list[ScheduledEntry]:
        """Reserve time slots for tasks that have a fixed_time set."""
        pass

    def _fill_remaining(
        self,
        tasks: list[Task],
        fixed_entries: list[ScheduledEntry],
        remaining_minutes: int,
    ) -> list[ScheduledEntry]:
        """Greedily assign flexible tasks to the remaining time budget."""
        pass

    def _build_reason(self, task: Task, position: int) -> str:
        """Generate a human-readable explanation for why this task was scheduled."""
        pass
