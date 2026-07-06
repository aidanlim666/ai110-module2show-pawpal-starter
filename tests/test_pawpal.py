from datetime import date

from pawpal_system import Task, Pet, Owner, Scheduler


def test_mark_complete_changes_status():
    task = Task(title="Morning walk", duration_minutes=30, priority="high", category="walk")
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_add_task_increases_pet_task_count():
    pet = Pet(name="Mochi", species="cat")
    assert len(pet.get_tasks()) == 0
    pet.add_task(Task(title="Feeding", duration_minutes=10, priority="high", category="feeding"))
    assert len(pet.get_tasks()) == 1
    pet.add_task(Task(title="Enrichment toy", duration_minutes=20, priority="low", category="enrichment"))
    assert len(pet.get_tasks()) == 2


def test_sort_by_time_returns_chronological_order():
    scheduler = Scheduler()
    tasks = [
        Task(title="Evening walk", duration_minutes=30, priority="medium", category="walk", fixed_time="18:00"),
        Task(title="Breakfast", duration_minutes=10, priority="high", category="feeding", fixed_time="08:00"),
        Task(title="Enrichment toy", duration_minutes=15, priority="low", category="enrichment"),
        Task(title="Meds", duration_minutes=5, priority="high", category="meds", fixed_time="12:00"),
    ]

    ordered = scheduler.sort_by_time(tasks)

    assert [t.title for t in ordered] == ["Breakfast", "Meds", "Evening walk", "Enrichment toy"]


def test_recurring_daily_task_creates_task_for_next_day():
    task = Task(
        title="Morning walk",
        duration_minutes=30,
        priority="high",
        category="walk",
        is_recurring=True,
        frequency="daily",
        due_date=date(2026, 7, 6),
    )

    next_task = task.mark_complete()

    assert task.completed is True
    assert next_task is not None
    assert next_task.completed is False
    assert next_task.due_date == date(2026, 7, 7)
    assert next_task.title == "Morning walk"


def test_scheduler_flags_duplicate_fixed_times_as_conflict():
    pet = Pet(name="Mochi", species="cat")
    pet.add_task(Task(title="Feeding", duration_minutes=15, priority="high", category="feeding", fixed_time="08:00"))
    pet.add_task(Task(title="Meds", duration_minutes=10, priority="high", category="meds", fixed_time="08:00"))
    owner = Owner(name="Alex", available_minutes=120)
    owner.add_pet(pet)

    schedule = Scheduler().schedule_day(pet, owner)

    skipped_titles = {t.title for t in schedule.skipped_tasks}
    assert skipped_titles == {"Feeding", "Meds"}
    assert not any(e.task.title in skipped_titles for e in schedule.entries)


def test_check_conflicts_flags_overlapping_times_across_pets():
    dog = Pet(name="Rex", species="dog")
    dog.add_task(Task(title="Walk", duration_minutes=30, priority="high", category="walk", fixed_time="09:00"))
    cat = Pet(name="Mochi", species="cat")
    cat.add_task(Task(title="Feeding", duration_minutes=15, priority="high", category="feeding", fixed_time="09:00"))
    owner = Owner(name="Alex", available_minutes=120)
    owner.add_pet(dog)
    owner.add_pet(cat)

    scheduler = Scheduler()
    dog_schedule = scheduler.schedule_day(dog, owner)
    cat_schedule = scheduler.schedule_day(cat, owner)

    warnings = scheduler.check_conflicts([dog_schedule, cat_schedule])

    assert len(warnings) == 1
    assert "Walk" in warnings[0]
    assert "Feeding" in warnings[0]
