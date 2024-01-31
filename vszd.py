import icalendar
from datetime import datetime

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

def convert_ics_to_html(ics_file_path):
    # Open the .ics file
    with open(ics_file_path, 'rb') as file:
        cal = icalendar.Calendar.from_ical(file.read())

    # Start building HTML output
    html_output = "<html><head><title>iCalendar Events</title></head><body>"
    html_output += "<style>table { border-collapse: collapse; } th, td { padding: 8px; border: 1px solid black; }</style>"
    html_output += "<h1>iCalendar Events</h1>"
    html_output += "<table>"
    html_output += "<tr><th>Date</th><th>Time</th><th>Subject</th><th>Professor</th><th>Location</th></tr>"

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
            events.append((start_time, summary, start_time_str, start_time_time, end_time_time, professor_str, location, color_style))

    # Sort events by start time
    events.sort(key=lambda x: x[0])

    # Add sorted events to HTML output
    for event in events:
        html_output += f"<tr style='{event[7]}'>"
        html_output += f"<td>{event[2]}</td>"
        html_output += f"<td>{event[3]} - {event[4]}</td>"
        html_output += f"<td>{event[1]}</td>"
        html_output += f"<td>{event[5]}</td>"
        html_output += f"<td>{event[6]}</td>"
        html_output += "</tr>"

    html_output += "</table>"
    html_output += "</body></html>"

    return html_output

if __name__ == "__main__":
    ics_file_path = "urnik-SAMO-FD.ics"
    html_output = convert_ics_to_html(ics_file_path)

    # Write HTML output to a file
    with open("calendar_events.html", "w") as html_file:
        html_file.write(html_output)

    print("Conversion completed. HTML file generated.")




