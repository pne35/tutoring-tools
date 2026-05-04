from clients import add_client, add_session, view_clients, load_clients


def main():
    while True:
        print("""
=== Tutoring Tools ===
1. Add Client
2. View Clients
3. Log Session
4. Exit
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
            print("Goodbye.")
            break

        else:
            print("Invalid option. Please enter 1, 2, 3 or 4.")


if __name__ == "__main__":
    main()