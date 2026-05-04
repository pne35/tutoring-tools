import json
from pathlib import Path


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


def add_client(file_path=CLIENTS_FILE):
    """Prompt for client details, add to data file, and return the new client."""
    clients = load_clients(file_path)

    name = input("Client name: ").strip()
    rate = float(input("Hourly rate (£): ").strip())
    contact = input("Contact info (email/phone): ").strip()
    notes = input("Notes (press Enter to skip): ").strip()

    client = {
        "id": get_next_client_id(clients),
        "name": name,
        "rate": rate,
        "contact": contact,
        "notes": notes,
        "sessions": [],
    }

    clients.append(client)
    save_clients(clients, file_path)
    print(f"\n✅ Client '{name}' added with ID {client['id']}.")
    return client


def find_client(clients, client_id):
    """Find and return a client by ID, or None if not found."""
    for client in clients:
        if client.get("id") == client_id:
            return client
    return None


def add_session(file_path=CLIENTS_FILE):
    """Prompt for session details, log against a client, and save."""
    clients = load_clients(file_path)

    if not clients:
        print("No clients found. Add a client first.")
        return

    # Show clients so user knows which ID to pick
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
    paid_input = input("Paid? (y/n): ").strip().lower()
    paid = paid_input == "y"

    session = {
        "date": date,
        "duration": duration,
        "topic": topic,
        "paid": paid,
    }

    client.setdefault("sessions", []).append(session)
    save_clients(clients, file_path)
    print(f"\n✅ Session logged for {client['name']} on {date}.")
    return session


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
        print(
            f"{client['id']:<5} {client['name']:<20} "
            f"£{client['rate']:<11} {len(sessions):<10} £{balance:.2f}"
        )