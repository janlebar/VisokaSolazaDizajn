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

    # Iterate through each event in the calendar
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt

            # Format the date and time
            start_time_str = start_time.strftime("%Y-%m-%d %H:%M:%S")
            end_time_str = end_time.strftime("%Y-%m-%d %H:%M:%S")

            # Add event details to HTML output
            html_output += f"<p><strong>Summary:</strong> {summary}</p>"
            html_output += f"<p><strong>Start Time:</strong> {start_time_str}</p>"
            html_output += f"<p><strong>End Time:</strong> {end_time_str}</p>"
            html_output += "<hr>"

    html_output += "</body></html>"

    return html_output

if __name__ == "__main__":
    ics_file_path = "urnik-SAMO-FD.ics"
    html_output = convert_ics_to_html(ics_file_path)

    # Write HTML output to a file
    with open("calendar_events.html", "w") as html_file:
        html_file.write(html_output)

    print("Conversion completed. HTML file generated.")
