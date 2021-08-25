## Video Capture Scheduling

This is a command line tool to create calendar events ( as .ics files ) to schedule automated recording for the Tools On Air software: Just:In.

<br/>

### Assumptions:
---

- JustIn will capture the video based on the event date, time.
- Naming the recorded file based on the event title.
- Each capture channel ( video feed ) to be recorded is a calendar.

<br/>

### Instructions:
---

- Run this script to create the proper .ics files.
- Import .ics files to the correct Just:In calendar.
- Verify the default capture format is set.
- Let Just:In do the rest of the work.

<br/>

### System Info:
---

- Created for and tested on Mac OS.
- Tested with Python 3.9.
- Be sure to set the environmental variable 'TIMEZONE'.<br>
Timezone options can be found on [wikipedia](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones).
