from tkinter import filedialog, Tk
from datetime import datetime, timedelta
import icalendar
import requests
from tempfile import NamedTemporaryFile

# Preslikava imen dni v slovenščini
weekday_names_slovenian = {
    0: "ponedeljek",
    1: "torek",
    2: "sreda",
    3: "četrtek",
    4: "petek",
    5: "sobota",
    6: "nedelja"
}

# Preslikava imen mesecev v slovenščini
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
    # Odpri datoteko .ics
    with open(ics_file_path, 'rb') as file:
        cal = icalendar.Calendar.from_ical(file.read())

    # Seznam za shranjevanje dogodkov
    events = []

    # Sprehod po vsakem dogodku v koledarju
    for component in cal.walk():
        if component.name == "VEVENT":
            summary = component.get('summary')
            start_time = component.get('dtstart').dt
            end_time = component.get('dtend').dt
            location = component.get('location')
            description = component.get('description')
            organizer = component.get('organizer')

            # Oblikuj datum in čas
            
            day_in_week = weekday_names_slovenian[start_time.weekday()]  # Pridobi slovensko ime dneva
            start_time_str = start_time.strftime("%d. %B") + f" {day_in_week}"  # Oblikuj datum

            start_time_time = start_time.strftime("%H:%M")
            end_time_time = end_time.strftime("%H:%M")

            # Izračunaj trajanje dogodka v urah
            duration_minutes = (end_time - start_time).seconds // 60
            duration_hours = duration_minutes // 45

            # Izvleči dodatne podrobnosti iz opisa, če so na voljo
            description_str = str(description)
            
            professor_index = description_str.find("Izvajalci:")
            professor_str = description_str[professor_index:].split("\n")[0].split(":")[1].strip()

            # Pridobi barvo, če je na voljo
            color = component.get('color')
            if color:
                color_style = f"background-color: white;"
            else:
                color_style = ""

            import locale
            locale.setlocale(locale.LC_TIME, 'ar-EG')
            start_time = component.get('dtstart').dt.strftime('%A, %d. %B')

            # Dodaj podrobnosti dogodka v seznam
            events.append((start_time, summary, start_time_str, start_time_time, end_time_time, duration_hours, professor_str, location, color_style))

    # Razvrsti dogodke po začetnem času
    events.sort(key=lambda x: x[0])

    # Začni graditi izhod HTML
    html_output = "<html><head><title>iCalendar Dogodki</title></head><body>"
    html_output += "<style>table { border-collapse: collapse; } th, td { padding: 8px; border: 1px solid black; }</style>"


    # Izračunaj vsoto duration_hours in pridobi professor_str za vsak edinstveni povzetek
    summary_info = {}
    for event in events:
        summary = event[1]+" --- "+event[6]
        duration_hours = event[5]
        professor_str = event[6]
        if summary in summary_info:
            summary_info[summary][0] += duration_hours
            if professor_str not in summary_info[summary][1]:
                summary_info[summary][1].append(professor_str)
        else:
            summary_info[summary] = [duration_hours, [professor_str]]

    # Dodaj naslov pred mrežo
    html_output += "<div>"
    for summary, info in summary_info.items():
        total_duration = info[0]
        professors = ', '.join(info[1])
        html_output += f"<p><strong>{summary}</strong>: {total_duration} ur, Profesorji: {professors}</p>"
    html_output += "</div>"

    html_output += "<table>"
    html_output += "<tr><th>Datum</th><th>Začetek/Konec</th><th>Ure</th><th>Predmet</th><th>Profesor</th><th>Prostor</th></tr>"

    # Ustvari seznam vseh datumov v tednu
    week_dates = []
    if events:
        start_date = events[0][0].date()
        end_date = events[-1][0].date()
        delta = timedelta(days=1)
        current_date = start_date
        while current_date <= end_date:
            week_dates.append(current_date)
            current_date += delta

    # Dodaj razvrščene dogodke v HTML
    current_month = None
    for date in week_dates:
        events_on_date = [event for event in events if event[0].date() == date]
        if events_on_date:
            for event in events_on_date:
                if date.month != current_month:
                    current_month = date.month
                    month_name = month_names_slovenian[current_month]  # Get Slovenian month name
                    html_output += f"<tr><th colspan='6'>{month_name}</th></tr>"
                day_in_week = weekday_names_slovenian[date.weekday()]  # Get Slovenian day name
                date_str = f" {day_in_week}, " + date.strftime("%d. ") + month_names_slovenian[date.month]  # Oblikuj datum
                html_output += f"<tr style='{event[8]}'>"
                html_output += f"<td>{date_str}</td>"  # Changed to include day and month name
                html_output += f"<td>{event[3]} - {event[4]}</td>"
                html_output += f"<td>{event[5]}</td>"
                html_output += f"<td>{event[1]}</td>"
                html_output += f"<td>{event[6]}</td>"
                html_output += f"<td>{event[7]}</td>"
                html_output += "</tr>"
        else:
            day_in_week = weekday_names_slovenian[date.weekday()]  # Pridobi slovensko ime dneva
            date_str = f" {day_in_week}, " + date.strftime("%d. ") + month_names_slovenian[date.month]  # Oblikuj datum
            html_output += f"<tr style='background-color: lightgray;'>"
            html_output += f"<td>{date_str}</td><td></td><td></td><td></td><td></td>"
            # Add empty cells for location
            html_output += f"<td></td>"
            html_output += "</tr>"


    html_output += "</table>"
    html_output += "</body></html>"

    return html_output

def open_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        with NamedTemporaryFile(delete=False, suffix=".ics") as tmp_file:
            tmp_file.write(response.content)
            tmp_file_path = tmp_file.name
        html_output = convert_ics_to_html(tmp_file_path)
        with open("urnik.html", "w") as html_file:
            html_file.write(html_output)
        print("Conversion completed. HTML file generated.")
    else:
        print("Failed to fetch the iCalendar file from the URL.")

if __name__ == "__main__":
    url = "https://urnik.fd.si/teacher/56/?export=1&types=standard%2Cspecial%2Creservation"
    open_url(url)