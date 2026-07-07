# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

In my initial UML design, I created 6 classes. Task is the core data object, holding all attributes a task should have, including title, duration, priority, category, start time (optional), and recurrence info. Pet describes a pet, holding the animal/s name, species, and a list of Task objects that are associated with it. Owner describes the human, continaing a list of Pet objects, name, and total availble mins/day. DailySchedule holds an ordered list of ScheduledEntery objects, any tasks that were skipped, and total duration. ScheduledEntry describes an entry, pairing a Task with a start and end time, along with reason. Scheduler has no data of its own, its job is to calculate a DailySchedule based on the owner's available minutes and a Pet (which itself contains Tasks).


**b. Design changes**

Yes, the design changed after reviewing. For example, added day_start attribute to Owner, so that we can set a wake up time, and we can know when the day starts, so that the scheduler can produce concrete clock times.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

- What constraints does your scheduler consider (for example: time, priority, preferences)?
- How did you decide which constraints mattered most?

**b. Tradeoffs**

One tradeoff my scheduler makes is checking for conflicts after tasks have been scheduled instead of checking them at the same time. This tradeoff is reasonable because it is possible that a person wants to schedule 2 tasks at the same time (maybe they have a helper, or maybe they could multitask), and give them a warning later just as a heads up, not as a restriction.

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

I used AI to brainstorm, add efficiency, and implement my code. I often brainstormed with AI, asking first with "Plan Mode" to get a general picture on what it thinks is the best approach, then tweaked it as needed, adding in new attributes such as priority. I also used it to debug. Some prompts that were helpful included giving the AI exact instructions, such as telling it certain methods and attributes I wanted a new class to have, rather than just allowing it to make up its own mind.


**b. Judgment and verification**

I didn't accept the AI's suggestion to disallow scheduling tasks at the same time. The AI may not have had the full context, and suggested scheduling so that tasks had to be at seperate times, but after seeing the next instruction on the project page ("Ask your AI coding assistant for a "lightweight" conflict detection strategy that returns a warning message rather than crashing the program."), I told the AI to brainstorm again using the abovementioned lightweight conflict detection strategy.

---

## 4. Testing and Verification

**a. What you tested**

I tested task basics, sorting correctness, recurrence logic, and conflict detections. These tests are important because they are the core features of this project.


**b. Confidence**

I am 8/10 confident that the scheduler works correctly, as I have tested many times, and also allowed Claude to make more tests, ensuring high quality. If I had more time, I would have tested the functionality of inputing zero or negative time for available minutes.
=
---

## 5. Reflection

**a. What went well**

I think this was a good project that allowed me to improve my coding skills with AI as a development partner, and allowed me to utilize it in a way that improved quality, not detoriated it (as in vibecoding)

**b. What you would improve**

I would make the graphical user interface better, with more contrasting colors, and easier to see buttons and fonts. 

**c. Key takeaway**

I learned that AI is a powerful design partner indeed, but tests must be thoroughly written to check it and allow it to iterate over itself many times.