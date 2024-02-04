from datetime import datetime, timedelta
import icalendar

# Mapping of weekday names in Slovenian
weekday_names_slovenian = {
    0: "ponedeljek",
    1: "torek",
    2: "sreda",
    3: "četrtek",
    4: "petek",
    5: "sobota",
    6: "nedelja"
}

def read_ics_file(ics_file_path):
    """Reads the .ics file and returns the calendar object."""
    with open(ics_file_path, 'rb') as file:
        return icalendar.Calendar.from_ical(file.read())

def format_html_header():
    """Formats the HTML header."""
    return "<html><head><title>iCalendar Events</title></head><body>"

def format_html_footer():
    """Formats the HTML footer."""
    return "</body></html>"

def format_event_row(event):
    """Formats an event row in HTML."""
    html_output = f"<tr style='{event[8]}'>"
    html_output += f"<td>{event[2]}</td>"
    html_output += f"<td>{event[3]} - {event[4]}</td>"
    html_output += f"<td>{event[5]}</td>"
    html_output += f"<td>{event[1]}</td>"
    html_output += f"<td>{event[6]}</td>"
    html_output += f"<td>{event[7]}</td>"
    html_output += "</tr>"
    return html_output

def format_empty_row(date):
    """Formats an empty row for dates without events."""
    day_in_week = weekday_names_slovenian[date.weekday()]  
    date_str = date.strftime("%d. %B") + f" {day_in_week}"  
    return f"<tr style='background-color: lightgray;'><td>{date_str}</td><td></td><td></td><td></td><td></td></tr>"

def convert_ics_to_html(ics_file_path):
    """Converts an .ics file to HTML format."""
    cal = read_ics_file(ics_file_path)
    html_output = format_html_header()
    html_output += "<h1>iCalendar Events</h1>"
    html_output += "<table>"
    html_output += "<style>table { border-collapse: collapse; } th, td { padding: 8px; border: 1px solid black; }</style>"
    html_output += "<tr><th>Date</th><th>Time</th><th>Hours</th><th>Subject</th><th>Professor</th><th>Location</th></tr>"

    events = extract_events(cal)

    for date in get_week_dates(events):
        events_on_date = [event for event in events if event[0].date() == date]
        if events_on_date:
            for event in events_on_date:
                html_output += format_event_row(event)
        else:
            html_output += format_empty_row(date)

    html_output += "</table>"
    html_output += format_html_footer()
    return html_output

def extract_events(calendar):
    """Extracts events from the calendar object."""
    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            location = component.get('location')
            description = component.get('description')
            professor_str = extract_professor(description)
            color = component.get('color')
            duration_hours = (end_time - start_time).seconds // 3600
            events.append((start_time, summary, format_date(start_time), start_time.strftime("%H:%M"),
                           end_time.strftime("%H:%M"), duration_hours, professor_str, location, f"background-color: {color};" if color else ""))
    events.sort(key=lambda x: x[0])
    return events

def extract_professor(description):
    """Extracts professor information from the event description."""
    if description:
        professor_index = description.find("Izvajalci:")
        if professor_index != -1:
            return description[professor_index:].split("\n")[0].split(":")[1].strip()
    return ""

def format_date(date_time):
    """Formats the date in Slovenian."""
    day_in_week = weekday_names_slovenian[date_time.weekday()]
    return date_time.strftime("%d. %B") + f" {day_in_week}"

def get_week_dates(events):
    """Creates a list of all dates in the week."""
    start_date = events[0][0].date()
    end_date = events[-1][0].date()
    delta = timedelta(days=1)
    week_dates = []
    current_date = start_date
    while current_date <= end_date:
        week_dates.append(current_date)
        current_date += delta
    return week_dates

if __name__ == "__main__":
    ics_file_path = "urnik-SAMO-FD.ics"
    html_output = convert_ics_to_html(ics_file_path)

    with open("calendar_events.html", "w") as html_file:
        html_file.write(html_output)

    print("Conversion completed. HTML file generated.")
