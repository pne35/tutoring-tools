from clients import (
    add_client, add_session, view_clients, load_clients,
    earnings_summary, mark_session_paid, view_weak_topics
)


def main():
    while True:
        print("""
=== Tutoring Tools ===
1. Add Client
2. View Clients
3. Log Session
4. Earnings Summary
5. Mark Session as Paid
6. View Weak Topics
7. Exit
""")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_client()
        elif choice == "2":
            clients = load_clients()
            view_clients(clients)
        elif choice == "3":
            add_session()
        elif choice == "4":
            earnings_summary()
        elif choice == "5":
            mark_session_paid()
        elif choice == "6":
            view_weak_topics()
        elif choice == "7":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


if __name__ == "__main__":
    main()