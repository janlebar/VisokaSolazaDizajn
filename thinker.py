from tkinter import filedialog, Tk
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

# Mapping of month names in Slovenian
month_names_slovenian = {
    1: "januar",
    2: "februar",
    3: "marec",
    4: "april",
    5: "maj",
    6: "junij",
    7: "julij",
    8: "avgust",
    9: "september",
    10: "oktober",
    11: "november",
    12: "december"
}

def convert_ics_to_html(ics_file_path):
    # Open the .ics file
    with open(ics_file_path, 'rb') as file:
        cal = icalendar.Calendar.from_ical(file.read())

    # Start building HTML output
    html_output = "<html><head><title>iCalendar Events</title></head><body>"
    html_output += "<style>table { border-collapse: collapse; } th, td { padding: 8px; border: 1px solid black; }</style>"
    html_output += "<h1>iCalendar Events</h1>"
    html_output += "<table>"
    html_output += "<tr><th>Date</th><th>Time</th><th>Hours</th><th>Subject</th><th>Professor</th><th>Location</th></tr>"

    # List to store events
    events = []

    # Iterate through each event in the calendar
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            location = component.get('location')
            description = component.get('description')
            organizer = component.get('organizer')

            # Format the date and time
            day_in_week = weekday_names_slovenian[start_time.weekday()]  # Get Slovenian day name
            start_time_str = start_time.strftime("%d. %B") + f" {day_in_week}"  # Format date

            start_time_time = start_time.strftime("%H:%M")
            end_time_time = end_time.strftime("%H:%M")

            # Calculate duration of the event in hours
            duration_hours = (end_time - start_time).seconds // 3600

            # Extract additional details from the description if available
            description_str = str(description)
            
            professor_index = description_str.find("Izvajalci:")
            professor_str = description_str[professor_index:].split("\n")[0].split(":")[1].strip()

            # Get color if available
            color = component.get('color')
            if color:
                color_style = f"background-color: {color};"
            else:
                color_style = ""

            # Append event details to the list
            events.append((start_time, summary, start_time_str, start_time_time, end_time_time, duration_hours, professor_str, location, color_style))

    # Sort events by start time
    events.sort(key=lambda x: x[0])
    
    
    # Create a list of all dates in the week
    start_date = events[0][0].date()
    end_date = events[-1][0].date()
    delta = timedelta(days=1)
    week_dates = []
    current_date = start_date
    while current_date <= end_date:
        week_dates.append(current_date)
        current_date += delta

    # Add sorted events to HTML output
    for date in week_dates:
        events_on_date = [event for event in events if event[0].date() == date]
        if events_on_date:
            for event in events_on_date:
                html_output += f"<tr style='{event[8]}'>"
                html_output += f"<td>{event[2]}</td>"
                html_output += f"<td>{event[3]} - {event[4]}</td>"
                html_output += f"<td>{event[5]}</td>"
                html_output += f"<td>{event[1]}</td>"
                html_output += f"<td>{event[6]}</td>"
                html_output += f"<td>{event[7]}</td>"
                html_output += "</tr>"
        else:
            day_in_week = weekday_names_slovenian[date.weekday()]  # Get Slovenian day name
            date_str = date.strftime("%d. %B") + f" {day_in_week}"  # Format date
            html_output += f"<tr style='background-color: lightgray;'>"
            html_output += f"<td>{date_str}</td><td></td><td></td><td></td><td></td>"
            html_output += "</tr>"

    html_output += "</table>"
    html_output += "</body></html>"

    return html_output

def open_file_dialog():
    root = Tk()
    root.withdraw()  # Hide the main window
    file_path = filedialog.askopenfilename(filetypes=[("iCalendar files", "*.ics")])
    if file_path:
        html_output = convert_ics_to_html(file_path)
        with open("calendar_events.html", "w") as html_file:
            html_file.write(html_output)
        print("Conversion completed. HTML file generated.")

if __name__ == "__main__":
    open_file_dialog()
