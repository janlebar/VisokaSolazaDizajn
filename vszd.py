import icalendar
from datetime import datetime

# Corrected path to the .ics file
# ics_file_path = "urnik-SAMO-FD.ics"

# # Open the .ics file using the correct path
# with open(path_to_ics_file) as f:
#     calendar = icalendar.Calendar.from_ical(f.read())

# # Process the calendar events
# for event in calendar.walk('VEVENT'):
#     print(event.get("SUMMARY"))



def convert_ics_to_html(ics_file_path):
    # Open the .ics file
    with open(ics_file_path, 'rb') as file:
        cal = icalendar.Calendar.from_ical(file.read())

    # Start building HTML output
    html_output = "<html><head><title>iCalendar Events</title></head><body>"
    html_output += "<h1>iCalendar Events</h1>"
    html_output += "<table border='1'>"
    html_output += "<tr><th>Date</th><th>Time</th><th>Subject</th><th>Type</th><th>Professor</th><th>Location</th></tr>"

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
            start_time_str = start_time.strftime("%Y-%m-%d")
            start_time_time = start_time.strftime("%H:%M")
            end_time_time = end_time.strftime("%H:%M")

            # Extract additional details from the description if available
            description_str = str(description)
            type_index = description_str.find("Predmet:")
            type_str = description_str[type_index:].split("\n")[0].split(":")[1].strip()

            professor_index = description_str.find("Izvajalci:")
            professor_str = description_str[professor_index:].split("\n")[0].split(":")[1].strip()

            # Add event details to HTML output
            html_output += "<tr>"
            html_output += f"<td>{start_time_str}</td>"
            html_output += f"<td>{start_time_time} - {end_time_time}</td>"
            html_output += f"<td>{summary}</td>"
            html_output += f"<td>{type_str}</td>"
            html_output += f"<td>{professor_str}</td>"
            html_output += f"<td>{location}</td>"
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


