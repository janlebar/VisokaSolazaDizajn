



input_text = '''
KONSTRUKCIJA IN MODELIRANJE II Predavanje Damjana Celcar---03:15
KONSTRUKCIJA IN MODELIRANJE II Predavanje Damjana Celcar---04:00
OBLIKOVANJE PROSTORA Vaje Petra Kocjančič---04:00
OSNOVE VEKTORSKE GRAFIKE IN RAČUNALNIŠKE OBDELAVE SLIK (IZREDNI) Predavanje Domen Lo---03:15
OSNOVE VEKTORSKE GRAFIKE IN RAČUNALNIŠKE OBDELAVE SLIK (IZREDNI) Predavanje Domen Lo---04:00
OSNOVE VEKTORSKE GRAFIKE IN RAČUNALNIŠKE OBDELAVE SLIK Predavanje Domen Lo---04:00
OSNOVE VEKTORSKE GRAFIKE IN RAČUNALNIŠKE OBDELAVE SLIK Predavanje Domen Lo---04:00
'''


lines = input_text.strip().split('\n')
events = {}

for line in lines:
    event_name, time_str = line.rsplit('---', 1)
    hours, minutes = map(int, time_str.split(':'))

    if event_name not in events:
        events[event_name] = {'hours': 0, 'minutes': 0}

    events[event_name]['hours'] += hours
    events[event_name]['minutes'] += minutes

result = {}

for event_name, time in events.items():
    total_minutes = time['hours'] * 60 + time['minutes']
    hours = total_minutes // 60
    minutes = total_minutes % 60
    result[event_name] = f'{hours:02}:{minutes:02}'
    
print (result)