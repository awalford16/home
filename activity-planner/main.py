from __future__ import print_function

import datetime
import os.path
import random

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = [
    'https://www.googleapis.com/auth/calendar.events'
]

SHARED_CALENDAR="primary"
TIMEZONE="UTC"


def main():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    busy = []

    # Set availability time for next week
    availability_start = datetime.datetime.utcnow()
    one_week_from_now = availability_start + datetime.timedelta(weeks=1)

    api = GoogleAPI()
    events = Events(availability_start, one_week_from_now)
    busy = api.get_calendar_events("shannoncantrill@gmail.com") + api.get_calendar_events("primary") + events.include_activity(20, 6) + events.include_activity(8, 16, True)

    # Determine times where we can do activities
    activities = events.schedule_event(events.get_availbility(busy))

    for activity in activities.keys():
        # print(activity, activities[activity]["start"].strftime("%Y-%m-%d %H:%M:%S"), activities[activity]["end"].strftime("%Y-%m-%d %H:%M:%S"))

        event = {
            "summary": activity,
            "start": {
                "dateTime": activities[activity]["start"].strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": TIMEZONE,
            },
            "end": {
                "dateTime": activities[activity]["end"].strftime("%Y-%m-%dT%H:%M:%S"),
                "timeZone": TIMEZONE,
            }
        }
        api.create_event(SHARED_CALENDAR, event)


class Events:
    def __init__(self, start, end):
        self.start = start
        self.end = end
        self.activities = {
            "tennis": 1,
            "run": 1,
            "swim": 1,
            "yoga": 1,
        }

    def include_activity(self, start_hour, end_hour, only_weekdays=False):
        events = []
        current_date = self.start
        while current_date < self.end:
            if (not only_weekdays) or (only_weekdays and current_date.weekday() < 5):
                events.append({
                    "start": current_date.replace(hour=start_hour, minute=0),
                    "end": current_date.replace(day=(current_date.day+1), hour=end_hour, minute=0),
                })

            current_date += datetime.timedelta(days=1)

        return events

    
    def get_availbility(self, busy):
        availability_slots = []
        sorted_events = sorted(busy, key=lambda x: x["start"])

        previous_event_end = self.start
        for event in sorted_events:
            if event["start"] > previous_event_end:
                availability_slots.append({
                    'start': previous_event_end,
                    'end': event["start"]
                })
            previous_event_end = event["end"]

        # Check if there's availability after the last event
        if previous_event_end < self.end:
            availability_slots.append({
                'start': previous_event_end,
                'end': self.end
            })
        
        return availability_slots

    def schedule_event(self, available):
        activities = {}

        # For each availability slot schedule a random event based on its duration
        for time in available:
            random_activity = random.choice(list(self.activities.keys()))
            
            finish = self.activities[random_activity] + 1

            # Dont schedule activity if it finishes too late
            if (time["start"].hour + finish > 20) or (time["start"].hour + finish > time["end"].hour):
                continue

            activities[random_activity] = {
                "start": time["start"].replace(hour=(time["start"].hour + 1)),
                "end": time["start"].replace(hour=(time["start"].hour + finish)),
            }

        return activities


class GoogleAPI:
    def __init__(self):
        self.creds = None
        # The file token.json stores the user's access and refresh tokens, and is
        # created automatically when the authorization flow completes for the first
        # time.
        if os.path.exists('token.json'):
            self.creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                self.creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(self.creds.to_json())
        
        self.service = build('calendar', 'v3', credentials=self.creds)

    def get_calendars(self):
        page_token = None
        while True:
            calendar_list = self.service.calendarList().list(pageToken=page_token).execute()
            for calendar_list_entry in calendar_list['items']:
                print(calendar_list_entry['summary'])
            page_token = calendar_list.get('nextPageToken')
            if not page_token:
                break

    def get_calendar_events(self, calendar):
        try:
            # Call the Calendar API
            now = datetime.datetime.utcnow().isoformat() + 'Z'  # 'Z' indicates UTC time
            events_result = self.service.events().list(calendarId=calendar, timeMin=now, timeZone='UTC',
                                                maxResults=10, singleEvents=True,
                                                orderBy='startTime').execute()
            events = events_result.get('items', [])

            if not events:
                return []

            # Prints the start and name of the next 10 events
            busy = []
            for event in events:
                busy.append({
                    "start": datetime.datetime.strptime(event['start'].get("dateTime"), "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None),
                    "end": datetime.datetime.strptime(event['end'].get("dateTime"), "%Y-%m-%dT%H:%M:%S%z").replace(tzinfo=None),
                })

        except HttpError as error:
            print('An error occurred: %s' % error)

        return busy

    def create_event(self, calendar, event):
        try:
            event = self.service.events().insert(calendarId=calendar, body=event).execute()
            print("Event created %s at %s" % (event["summary"], event["start"]["dateTime"]))
        except HttpError as error:
            print("An error occured: %s" % error)


if __name__ == '__main__':
    main()