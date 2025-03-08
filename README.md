# ww2pyfile
For contest
# Event Management System

This is a simple command-line event management system built with Python and SQLite. It allows users to add events, search for events, and view statistics about events and participants.

## Features

- Add new events with date, name, and participants
- Search for events by keyword and/or date
- View statistics about events and participants
- SQLite database for persistent storage

## Requirements

- Python 3.x
- SQLite3

## Usage

To use the program, run the `test.py` file with Python and use the following commands:

Available options:

- `--add <date> <name> [participants...]`: Add a new event
- `--search [keyword] [date]`: Search for events
- `--stats`: Show statistics
- `--help`: Show help message

### Examples

1. Add a new event:
   python test.py --add 2023-05-15 "Birthday Party" John Mary

2. Search for events by keyword:
   python test.py --search "Birthday"

3. Search for events by date:
   python test.py --search 2023-05

4. Search for events by keyword and date:
   python test.py --search "Birthday" 2023-05

5. Show statistics:
   python test.py --stats

## License

This project is licensed under the Apache License 2.0. See the [LICENSE](LICENSE) file for details.
