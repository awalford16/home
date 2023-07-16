# Activity Planner

## TODO:

- Dont schedule events within 1 hour of other events
- Account for sleep hours with night shifts
- Run as cron job

## Process

A cron job that:

- Pulls from Google Calendar and identify when people are free
- Reads from a list of activities and their duration
- Schedules activities into the calendar for the week
