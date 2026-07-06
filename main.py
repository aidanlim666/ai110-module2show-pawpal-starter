from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Aidan", available_minutes=120, day_start="08:00")

pet1 = Pet(name="Pet1", species="cat")
pet2 = Pet(name="Pet2", species="dog")

owner.add_pet(pet1)
owner.add_pet(pet2)

# pet1's tasks — added out of chronological order on purpose
pet1.add_task(Task(title="Enrichment toy", duration_minutes=20, priority="low",    category="enrichment"))
pet1.add_task(Task(title="Evening meds",   duration_minutes=5,  priority="high",   category="meds",       fixed_time="18:00", completed=True))
pet1.add_task(Task(title="Morning meds",   duration_minutes=5,  priority="high",   category="meds",       fixed_time="08:00"))
pet1.add_task(Task(title="Feeding",        duration_minutes=10, priority="high",   category="feeding"))

# pet2's tasks — also added out of chronological order
pet2.add_task(Task(title="Play session", duration_minutes=20, priority="low",    category="enrichment"))
pet2.add_task(Task(title="Breakfast",    duration_minutes=10, priority="high",   category="feeding",    fixed_time="09:00"))
pet2.add_task(Task(title="Grooming",     duration_minutes=25, priority="medium", category="grooming",   completed=True))
pet2.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   category="walk",      fixed_time="08:00"))


scheduler = Scheduler()

print("TASKS SORTED BY TIME")
for pet in owner.pets:
    print(f"\n{pet.name}:")
    for t in scheduler.sort_by_time(pet.get_tasks()):
        when = t.fixed_time or "flexible"
        print(f"  {when:<9} {t.title} ({t.duration_minutes} min)")
print("-" * 50)

print("\nFILTERED TASKS")
print("Pet1 only:", [t.title for t in owner.get_tasks(pet_name="Pet1")])
print("Completed:", [t.title for t in owner.get_tasks(completed=True)])
print("Not completed:", [t.title for t in owner.get_tasks(completed=False)])
print("-" * 50)

print("\nTODAY'S SCHEDULE")

schedules = []
for pet in owner.pets:
    schedule = scheduler.schedule_day(pet, owner)
    schedules.append(schedule)
    print()
    print(schedule.get_summary())
    print()
    print(schedule.explain())
    print("-" * 50)

print("\nCONFLICT CHECK")
conflict_warnings = scheduler.check_conflicts(schedules)
if conflict_warnings:
    for warning in conflict_warnings:
        print(f"  WARNING: {warning}")
else:
    print("  No conflicts detected.")
print("-" * 50)
