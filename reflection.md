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

- Describe one tradeoff your scheduler makes.
- Why is that tradeoff reasonable for this scenario?

---

## 3. AI Collaboration

**a. How you used AI**

- How did you use AI tools during this project (for example: design brainstorming, debugging, refactoring)?
- What kinds of prompts or questions were most helpful?

**b. Judgment and verification**

- Describe one moment where you did not accept an AI suggestion as-is.
- How did you evaluate or verify what the AI suggested?

---

## 4. Testing and Verification

**a. What you tested**

- What behaviors did you test?
- Why were these tests important?

**b. Confidence**

- How confident are you that your scheduler works correctly?
- What edge cases would you test next if you had more time?

---

## 5. Reflection

**a. What went well**

- What part of this project are you most satisfied with?

**b. What you would improve**

- If you had another iteration, what would you improve or redesign?

**c. Key takeaway**

- What is one important thing you learned about designing systems or working with AI on this project?
