from app.parser import parse_log_line


def read_logs(file_path):
    events = []

    with open(file_path, "r") as file:
        for line in file:
            line = line.strip()

            if not line:
                continue

            event = parse_log_line(line)

            if event:
                events.append(event)

    return events

if __name__ == "__main__":
    events = read_logs("data/raw/sample.log")

    for event in events:
        print(event)