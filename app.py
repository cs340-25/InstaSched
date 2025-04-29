'''
from flask import Flask, render_template, request
import json
import random
from datetime import datetime, timedelta
from flask import Response, session


app = Flask(__name__)

def load_wellness_activities():
    """Load wellness activities from the JSON file."""
    with open('wellness_activities.json', 'r') as f:
        return json.load(f)


def generate_schedule(start_time, end_time, busy_periods, activities):
    
    Generate a schedule by:
    1. Calculating free periods between the user's start/end time and busy periods.
    2. Filling those free periods with wellness activities that fit.
    
    # Convert times to datetime objects
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time_dt = datetime.strptime(end_time, "%H:%M")
    schedule = []

    # Calculate free periods
    free_periods = []
    if busy_periods:
        # Sort busy periods by start time
        busy_periods.sort(key=lambda x: datetime.strptime(x['start'], "%H:%M"))
        # Free time before the first busy period
        first_busy_start = datetime.strptime(busy_periods[0]['start'], "%H:%M")
        if current_time < first_busy_start:
            free_periods.append({"start": current_time.strftime("%H:%M"), "end": busy_periods[0]['start']})
        # Free periods between busy periods
        for i in range(len(busy_periods) - 1):
            prev_end = datetime.strptime(busy_periods[i]['end'], "%H:%M")
            next_start = datetime.strptime(busy_periods[i+1]['start'], "%H:%M")
            if prev_end < next_start:
                free_periods.append({"start": prev_end.strftime("%H:%M"), "end": next_start.strftime("%H:%M")})
        # Free time after the last busy period
        last_end = datetime.strptime(busy_periods[-1]['end'], "%H:%M")
        if last_end < end_time_dt:
            free_periods.append({"start": last_end.strftime("%H:%M"), "end": end_time})
    else:
        # If no busy periods, the entire day is free.
        free_periods.append({"start": start_time, "end": end_time})

    # Fill each free period with wellness activities
    for period in free_periods:
        period_start = datetime.strptime(period["start"], "%H:%M")
        period_end = datetime.strptime(period["end"], "%H:%M")
        free_duration = int((period_end - period_start).total_seconds() // 60)  # in minutes

        current = period_start
        while free_duration > 0 and activities:
            # Find an activity that fits in the remaining free time
            for activity in activities:
                duration = activity["duration"]
                if duration <= free_duration:
                    schedule.append({
                        "activity": activity["name"],
                        "start": current.strftime("%H:%M"),
                        "end": (current + timedelta(minutes=duration)).strftime("%H:%M")
                    })
                    current += timedelta(minutes=duration)
                    free_duration -= duration
                    # Break to try scheduling the next slot
                    break
            else:
                # If no activity fits, exit the loop for this period.
                break

    return schedule


def generate_schedule(start_time, end_time, busy_periods, activities):
    # Convert times to datetime objects for manipulation.
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time_dt = datetime.strptime(end_time, "%H:%M")
    schedule = []

    # Determine free periods.
    free_periods = []
    if busy_periods:
        busy_periods.sort(key=lambda x: datetime.strptime(x['start'], "%H:%M"))
        first_busy_start = datetime.strptime(busy_periods[0]['start'], "%H:%M")
        if current_time < first_busy_start:
            free_periods.append({
                "start": current_time.strftime("%H:%M"),
                "end": busy_periods[0]['start']
            })
        for i in range(len(busy_periods) - 1):
            prev_end = datetime.strptime(busy_periods[i]['end'], "%H:%M")
            next_start = datetime.strptime(busy_periods[i+1]['start'], "%H:%M")
            if prev_end < next_start:
                free_periods.append({
                    "start": prev_end.strftime("%H:%M"),
                    "end": next_start.strftime("%H:%M")
                })
        last_end = datetime.strptime(busy_periods[-1]['end'], "%H:%M")
        if last_end < end_time_dt:
            free_periods.append({
                "start": last_end.strftime("%H:%M"),
                "end": end_time
            })
    else:
        free_periods.append({
            "start": start_time,
            "end": end_time
        })

    # Fill each free period with wellness activities.
    for period in free_periods:
        period_start = datetime.strptime(period["start"], "%H:%M")
        period_end = datetime.strptime(period["end"], "%H:%M")
        free_duration = int((period_end - period_start).total_seconds() // 60)  # in minutes
        current = period_start

        while free_duration > 0:
            # Filter activities that fit into the remaining free duration.
            possible_activities = [activity for activity in activities if activity["duration"] <= free_duration]
            if not possible_activities:
                break  # Exit if no activity fits.

            # Randomly choose one of the available activities.
            selected_activity = random.choice(possible_activities)

            schedule.append({
                "activity": selected_activity["name"],
                "start": current.strftime("%H:%M"),
                "end": (current + timedelta(minutes=selected_activity["duration"])).strftime("%H:%M")
            })

            # Update the time and remaining duration.
            current += timedelta(minutes=selected_activity["duration"])
            free_duration -= selected_activity["duration"]

    return schedule


def generate_schedule(start_time, end_time, busy_periods, activities):
    # Parse the user’s day window
    current_time = datetime.strptime(start_time, "%H:%M")
    end_time_dt  = datetime.strptime(end_time,   "%H:%M")
    schedule     = []
    used_names   = set()  # track what’s been scheduled

    # Calculate free periods (unchanged)
    free_periods = []
    if busy_periods:
        busy_periods.sort(key=lambda x: datetime.strptime(x['start'], "%H:%M"))
        first_busy = datetime.strptime(busy_periods[0]['start'], "%H:%M")
        if current_time < first_busy:
            free_periods.append({"start": current_time.strftime("%H:%M"), "end": busy_periods[0]['start']})
        for i in range(len(busy_periods)-1):
            prev_end   = datetime.strptime(busy_periods[i]['end'],   "%H:%M")
            next_start = datetime.strptime(busy_periods[i+1]['start'], "%H:%M")
            if prev_end < next_start:
                free_periods.append({"start": prev_end.strftime("%H:%M"), "end": next_start.strftime("%H:%M")})
        last_end = datetime.strptime(busy_periods[-1]['end'], "%H:%M")
        if last_end < end_time_dt:
            free_periods.append({"start": last_end.strftime("%H:%M"), "end": end_time})
    else:
        free_periods.append({"start": start_time, "end": end_time})

    # Fill each free slot
    for period in free_periods:
        slot_start   = datetime.strptime(period["start"], "%H:%M")
        slot_end     = datetime.strptime(period["end"],   "%H:%M")
        free_minutes = int((slot_end - slot_start).total_seconds() // 60)
        current      = slot_start

        while free_minutes > 0:
            # find all activities that fit & haven’t been used yet
            candidates = [
                act for act in activities
                if act["duration"] <= free_minutes
                and act["name"] not in used_names
            ]
            if not candidates:
                # no new activity fits → we’re done with this slot
                break

            choice = random.choice(candidates)
            used_names.add(choice["name"])

            schedule.append({
                "activity": choice["name"],
                "start": current.strftime("%H:%M"),
                "end":   (current + timedelta(minutes=choice["duration"])).strftime("%H:%M")
            })

            # move forward in time
            current      += timedelta(minutes=choice["duration"])
            free_minutes -= choice["duration"]

    return schedule


@app.route("/", methods=["GET", "POST"])
def index():
    schedule = None
    if request.method == "POST":
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        busy_input = request.form.get("busy_periods")  # e.g., "09:00-10:00, 13:00-14:00"
        busy_periods = []
        if busy_input:
            entries = busy_input.split(',')
            for entry in entries:
                times = entry.strip().split('-')
                if len(times) == 2:
                    busy_periods.append({"start": times[0].strip(), "end": times[1].strip()})
        activities = load_wellness_activities()
        schedule = generate_schedule(start_time, end_time, busy_periods, activities)
    return render_template("index.html", schedule=schedule)

if __name__ == "__main__":
    app.run(debug=True)
'''

import os
import json
import random
from datetime import datetime, timedelta
from flask import Flask, render_template, request, session, redirect, url_for, Response
from ics import Calendar, Event

app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'dev-secret-key')


def load_wellness_activities():
    with open('wellness_activities.json') as f:
        return json.load(f)


def calculate_free_periods(start_time, end_time, busy_periods):
    current = datetime.strptime(start_time, "%H:%M")
    end_dt = datetime.strptime(end_time, "%H:%M")
    free = []
    if busy_periods:
        busy_periods.sort(key=lambda x: datetime.strptime(x['start'], "%H:%M"))
        # before first busy
        first_start = datetime.strptime(busy_periods[0]['start'], "%H:%M")
        if current < first_start:
            free.append({"start": current.strftime("%H:%M"), "end": busy_periods[0]['start']})
        # between busy
        for i in range(len(busy_periods)-1):
            prev_end = datetime.strptime(busy_periods[i]['end'], "%H:%M")
            next_start = datetime.strptime(busy_periods[i+1]['start'], "%H:%M")
            if prev_end < next_start:
                free.append({"start": prev_end.strftime("%H:%M"), "end": next_start.strftime("%H:%M")})
        # after last
        last_end = datetime.strptime(busy_periods[-1]['end'], "%H:%M")
        if last_end < end_dt:
            free.append({"start": last_end.strftime("%H:%M"), "end": end_time})
    else:
        free.append({"start": start_time, "end": end_time})
    return free


def generate_schedule(start_time, end_time, busy_periods, activities):
    free_periods = calculate_free_periods(start_time, end_time, busy_periods)
    schedule = []
    used = set()

    for period in free_periods:
        slot_start = datetime.strptime(period['start'], "%H:%M")
        slot_end = datetime.strptime(period['end'], "%H:%M")
        minutes = int((slot_end - slot_start).total_seconds() // 60)
        current = slot_start

        while minutes > 0:
            candidates = [a for a in activities
                          if a['duration'] <= minutes and a['name'] not in used]
            if not candidates:
                break
            choice = random.choice(candidates)
            used.add(choice['name'])

            schedule.append({
                'activity': choice['name'],
                'start': current.strftime("%H:%M"),
                'end': (current + timedelta(minutes=choice['duration'])).strftime("%H:%M")
            })
            current += timedelta(minutes=choice['duration'])
            minutes -= choice['duration']

    return schedule


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/build', methods=['GET', 'POST'])
def build():
    activities = load_wellness_activities()
    # extract unique tags
    tags = sorted({tag for a in activities for tag in a['tags']})

    if request.method == 'POST':
        start_time = request.form['start_time']
        end_time = request.form['end_time']
        busy_raw = request.form.get('busy_periods', '')
        busy = []
        for item in busy_raw.split(','):
            if '-' in item:
                s, e = item.strip().split('-')
                busy.append({'start': s.strip(), 'end': e.strip()})
        prefs = request.form.getlist('prefs')
        # filter activities by prefs
        if prefs:
            activities = [a for a in activities if any(t in prefs for t in a['tags'])]

        schedule = generate_schedule(start_time, end_time, busy, activities)
        session['last_schedule'] = schedule

        # build chart data
        chart_labels = [s['activity'] for s in schedule]
        chart_data = []
        # sum durations per activity
        from collections import Counter
        dur = Counter()
        for s in schedule:
            start = datetime.strptime(s['start'], "%H:%M")
            end = datetime.strptime(s['end'],   "%H:%M")
            dur[s['activity']] += int((end - start).total_seconds()//60)
        chart_labels = list(dur.keys())
        chart_data = list(dur.values())

        return render_template('schedule.html', schedule=schedule,
                               chart={'labels': chart_labels, 'data': chart_data})

    return render_template('build.html', tags=tags)


@app.route('/library')
def library():
    activities = load_wellness_activities()
    return render_template('library.html', activities=activities)


@app.route('/download.ics')
def download_ics():
    schedule = session.get('last_schedule', [])
    cal = Calendar()
    today = datetime.now().date()
    for slot in schedule:
        start_dt = datetime.combine(today, datetime.strptime(slot['start'], "%H:%M").time())
        end_dt   = datetime.combine(today, datetime.strptime(slot['end'],   "%H:%M").time())
        evt = Event(name=slot['activity'], begin=start_dt, end=end_dt)
        cal.events.add(evt)
   
    return Response(cal.serialize(), mimetype='text/calendar',
                    headers={'Content-Disposition': 'attachment; filename=schedule.ics'})


if __name__ == '__main__':
    app.run(debug=True)