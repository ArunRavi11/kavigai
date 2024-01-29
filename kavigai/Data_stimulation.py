import csv
from faker import Faker
from datetime import datetime, timedelta
import random

fake = Faker()

def generate_description(event):
    """
    Generate a description based on the given event data.
    """
    description_template = (
        "Join us for an exciting {type} - '{title}' on {date} at {time} in {location}. "
        "Our distinguished speaker, {speaker}, will guide you through {details}. "
        "Don't miss this opportunity to learn and connect with like-minded individuals!"
    )

    # Generate a random location
    location = fake.random_element(elements=('San Francisco', 'New York', 'London', 'Berlin', 'Tokyo'))

    # Check if 'date' field is not empty
    if event['date']:
        try:
            # Try parsing the date with the '%d-%m-%Y' format
            event_date = datetime.strptime(event['date'], '%d-%m-%Y')
        except ValueError:
            # If the first format fails, try parsing with the '%Y-%m-%d' format
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
    else:
        # Provide a default date if 'date' is empty
        event_date = datetime.now()

    # Generate a random time
    event_time = fake.time(pattern='%H:%M:%S')

    description = description_template.format(
        type=event['type'],
        title=event['title'],
        date=event_date.strftime('%Y-%m-%d'),
        time=event_time,
        location=location,
        speaker=event['speaker'],
        details=event['details'] if 'details' in event else '',
    )

    return description, location, event_time  # Return location and time as well

# Load existing data from CSV (assuming 'your_existing_data.csv' exists)
existing_data = []
with open('events.csv', 'r', encoding='utf-8') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        existing_data.append(row)

# Generate additional data to meet the desired count
num_additional_data_points = 10000 - len(existing_data)  # Change 10000 to your desired number
additional_data = []
for i in range(num_additional_data_points):
    event_id = f"event_{i + 1}"
    event_type = fake.random_element(elements=('Conference', 'Workshop', 'Seminar'))
    event_title = fake.sentence()
    event_date = fake.date_between(start_date='-30d', end_date='+30d').strftime('%Y-%m-%d')

    # Generate a random time
    event_time = fake.time(pattern='%H:%M:%S')

    event_speaker = fake.name()
    event_details = fake.paragraph()

    event = {
        'event_id': event_id,
        'type': event_type,
        'title': event_title,
        'date': event_date,
        'time': event_time,
        'speaker': event_speaker,
        'details': event_details,
    }
    additional_data.append(event)

# Combine existing data with additional data
combined_data = existing_data + additional_data

# Generate details for each event in the dataset
details = []
for event in combined_data:
    description, location, event_time = generate_description(event)
    details.append({
        'event_id': event['event_id'],
        'type': event['type'],
        'title': event['title'],
        'date': event['date'],
        'time': event_time,
        'location': location,
        'speaker': event['speaker'],
        'details': event['details'] if 'details' in event else '',
        'description': description,
    })

# Save details to a new CSV file
details_filename = 'event_details.csv'
with open(details_filename, 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = ['event_id', 'type', 'title', 'date', 'time', 'location', 'speaker', 'details', 'description']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(details)

print(f"Event details saved to '{details_filename}'")
