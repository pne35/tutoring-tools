import json
from pathlib import Path
from datetime import datetime

CLIENTS_FILE = Path(__file__).parent / "Data" / "clients.json"


def load_clients(file_path=CLIENTS_FILE):
    """Load clients from the JSON data file."""
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Could not find clients file: {file_path}")
    except json.JSONDecodeError as error:
        raise ValueError(f"Clients file contains invalid JSON: {file_path}") from error

    return data.get("clients", [])


def save_clients(clients, file_path=CLIENTS_FILE):
    """Save clients to the JSON data file."""
    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    data = {"clients": clients}
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)


def get_next_client_id(clients):
    """Return the next available client ID."""
    if not clients:
        return 1
    return max(client.get("id", 0) for client in clients) + 1


def find_client(clients, client_id):
    """Find and return a client by ID, or None if not found."""
    for client in clients:
        if client.get("id") == client_id:
            return client
    return None


def client_balance(client):
    """Calculate total amount owed for unpaid sessions."""
    rate = client.get("rate", 0)
    total = 0
    for session in client.get("sessions", []):
        if not session.get("paid", False):
            total += rate * session.get("duration", 0)
    return total


def view_clients(clients):
    """Print a summary of all clients."""
    if not clients:
        print("No clients found.")
        return

    print(f"\n{'ID':<5} {'Name':<20} {'Rate':<12} {'Sessions':<10} {'Owed'}")
    print("-" * 55)
    for client in clients:
        sessions = client.get("sessions", [])
        balance = client_balance(client)
        joint = " (joint)" if client.get("joint_session") else ""
        print(
            f"{client['id']:<5} {client['name']:<20} "
            f"£{client['rate']:<11} {len(sessions):<10} £{balance:.2f}{joint}"
        )


def add_client(file_path=CLIENTS_FILE):
    """Prompt for client details, add to data file, and return the new client."""
    clients = load_clients(file_path)

    name = input("Client name: ").strip()
    rate = float(input("Hourly rate (£): ").strip())
    contact = input("Contact info (email/phone): ").strip()
    notes = input("Notes (press Enter to skip): ").strip()
    joint_input = input("Joint session? (y/n): ").strip().lower()
    joint_session = joint_input == "y"

    client = {
        "id": get_next_client_id(clients),
        "name": name,
        "rate": rate,
        "contact": contact,
        "notes": notes,
        "joint_session": joint_session,
        "sessions": [],
        "weak_topics": [],
    }

    clients.append(client)
    save_clients(clients, file_path)
    print(f"\n✅ Client '{name}' added with ID {client['id']}.")
    return client


def add_session(file_path=CLIENTS_FILE):
    """Prompt for session details, log against a client, and save."""
    clients = load_clients(file_path)

    if not clients:
        print("No clients found. Add a client first.")
        return

    print("\nClients:")
    view_clients(clients)

    try:
        client_id = int(input("\nEnter client ID to log session for: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    client = find_client(clients, client_id)
    if client is None:
        print(f"No client found with ID {client_id}.")
        return

    date = input("Date (YYYY-MM-DD): ").strip()
    duration = float(input("Duration in hours (e.g. 1 or 1.5): ").strip())
    topic = input("Topic covered: ").strip()

    weak_input = input("Weak topics identified (comma-separated, or Enter to skip): ").strip()
    weak_topics = [t.strip() for t in weak_input.split(",") if t.strip()] if weak_input else []

    paid_input = input("Paid? (y/n): ").strip().lower()
    paid = paid_input == "y"

    session = {
        "date": date,
        "duration": duration,
        "topic": topic,
        "weak_topics": weak_topics,
        "paid": paid,
    }

    # Merge new weak topics into the client-level list (no duplicates)
    existing_weak = client.setdefault("weak_topics", [])
    for t in weak_topics:
        if t not in existing_weak:
            existing_weak.append(t)

    client.setdefault("sessions", []).append(session)
    save_clients(clients, file_path)
    print(f"\n✅ Session logged for {client['name']} on {date}.")
    if weak_topics:
        print(f"   Weak topics recorded: {', '.join(weak_topics)}")
    return session


def mark_session_paid(file_path=CLIENTS_FILE):
    """Mark a session as paid for a client."""
    clients = load_clients(file_path)

    if not clients:
        print("No clients found.")
        return

    view_clients(clients)

    try:
        client_id = int(input("\nEnter client ID: ").strip())
    except ValueError:
        print("Invalid ID.")
        return

    client = find_client(clients, client_id)
    if client is None:
        print("No client found with that ID.")
        return

    sessions = client.get("sessions", [])
    unpaid = [(i, s) for i, s in enumerate(sessions) if not s.get("paid", False)]

    if not unpaid:
        print(f"No unpaid sessions for {client['name']}.")
        return

    print(f"\nUnpaid sessions for {client['name']}:")
    for i, session in unpaid:
        amount = client["rate"] * session.get("duration", 0)
        print(f"  [{i}] {session['date']} — {session['topic']} — £{amount:.2f}")

    try:
        index = int(input("\nEnter session number to mark as paid: ").strip())
    except ValueError:
        print("Invalid input.")
        return

    if index not in [i for i, _ in unpaid]:
        print("Invalid session number.")
        return

    client["sessions"][index]["paid"] = True
    save_clients(clients, file_path)
    print(f"✅ Session marked as paid.")


def earnings_summary(file_path=CLIENTS_FILE):
    """Print weekly and monthly earnings summary."""
    clients = load_clients(file_path)

    now = datetime.now()
    current_week = now.isocalendar().week
    current_month = now.month
    current_year = now.year

    weekly_earned = 0
    weekly_owed = 0
    monthly_earned = 0
    monthly_owed = 0
    total_owed = 0

    for client in clients:
        rate = client.get("rate", 0)
        is_joint = client.get("joint_session", False)

        for session in client.get("sessions", []):
            try:
                date = datetime.strptime(session["date"], "%Y-%m-%d")
            except ValueError:
                continue
            
            amount = rate * session.get("duration", 0)
            paid = session.get("paid", False)

            if date.isocalendar().week == current_week and date.year == current_year:
                if paid:
                    weekly_earned += amount
                else:
                    weekly_owed += amount

            if date.month == current_month and date.year == current_year:
                if paid:
                    monthly_earned += amount
                else:
                    monthly_owed += amount

            if not paid:
                total_owed += amount

    print(f"\n{'='*35}")
    print(f"  EARNINGS SUMMARY")
    print(f"{'='*35}")
    print(f"  This week:   £{weekly_earned:.2f} earned  |  £{weekly_owed:.2f} owed")
    print(f"  This month:  £{monthly_earned:.2f} earned  |  £{monthly_owed:.2f} owed")
    print(f"  Total owed:  £{total_owed:.2f}")
    print(f"{'='*35}\n")


def view_weak_topics(file_path=CLIENTS_FILE):
    """Print weak topics for all clients."""
    clients = load_clients(file_path)

    if not clients:
        print("No clients found.")
        return

    print(f"\n{'='*45}")
    print(f"  WEAK TOPICS BY CLIENT")
    print(f"{'='*45}")
    for client in clients:
        weak = client.get("weak_topics", [])
        topics_str = ", ".join(weak) if weak else "None recorded"
        print(f"  {client['name']:<20} {topics_str}")
    print(f"{'='*45}\n")