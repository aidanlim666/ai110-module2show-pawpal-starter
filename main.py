from pawpal_system import Owner, Pet, Task, Scheduler

owner = Owner(name="Aidan", available_minutes=120, day_start="08:00")

pet1 = Pet(name="Pet1", species="cat")
pet2 = Pet(name="Pet2", species="dog")

owner.add_pet(pet1)
owner.add_pet(pet2)

# pet1's tasks
pet1.add_task(Task(title="Morning meds",   duration_minutes=5,  priority="high",   category="meds",       fixed_time="08:00"))
pet1.add_task(Task(title="Feeding",        duration_minutes=10, priority="high",   category="feeding"))
pet1.add_task(Task(title="Enrichment toy", duration_minutes=20, priority="low",    category="enrichment"))

# pet2's tasks
pet2.add_task(Task(title="Morning walk", duration_minutes=30, priority="high",   category="walk"))
pet2.add_task(Task(title="Breakfast",    duration_minutes=10, priority="high",   category="feeding",    fixed_time="09:00"))
pet2.add_task(Task(title="Grooming",     duration_minutes=25, priority="medium", category="grooming"))
pet2.add_task(Task(title="Play session", duration_minutes=20, priority="low",    category="enrichment"))


scheduler = Scheduler()

print("TODAY'S SCHEDULE")


for pet in owner.pets:
    schedule = scheduler.schedule_day(pet, owner)
    print()
    print(schedule.get_summary())
    print()
    print(schedule.explain())
    print("-" * 50)
