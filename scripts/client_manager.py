import json
import os
import argparse
import re
from datetime import datetime

CLIENTS_FILE = "references/client_ids.json"

def _load_clients():
    """Loads client data from the JSON file."""
    if not os.path.exists(CLIENTS_FILE):
        return []
    with open(CLIENTS_FILE, "r") as f:
        return json.load(f)

def _save_clients(clients):
    """Saves client data to the JSON file."""
    with open(CLIENTS_FILE, "w") as f:
        json.dump(clients, f, indent=2)

def _slugify(name):
    """Converts a client name to a URL-friendly slug."""
    name = name.lower()
    name = re.sub(r"[^a-z0-9\s-]", "", name)
    name = re.sub(r"\s+", "-", name)
    return name

def create_client(client_name):
    """
    Creates a new client ID and registers the client.
    Returns the new client ID string.
    """
    clients = _load_clients()
    base_slug = _slugify(client_name)
    
    # Find a unique sequential code
    sequential_code = 1
    while True:
        client_id = f"{base_slug}-{sequential_code:03d}"
        if not any(c["id"] == client_id for c in clients):
            break
        sequential_code += 1
            
    new_client = {
        "id": client_id,
        "name": client_name,
        "created_at": datetime.now().isoformat()
    }
    clients.append(new_client)
    _save_clients(clients)
    return client_id

def list_clients():
    """Retrieves a list of all registered clients."""
    return _load_clients()

def get_client(identifier):
    """
    Retrieves details for a specific client by its ID or name.
    Identifier can be client_id or client_name.
    """
    clients = _load_clients()
    for client in clients:
        if client["id"] == identifier or client["name"].lower() == identifier.lower():
            return client
    return None

def main():
    parser = argparse.ArgumentParser(description="Manage Mika Automation LLC client IDs.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    create_parser = subparsers.add_parser("create", help="Create a new client ID.")
    create_parser.add_argument("name", type=str, help="Name of the client.")

    list_parser = subparsers.add_parser("list", help="List all clients.")

    get_parser = subparsers.add_parser("get", help="Get client details by ID or name.")
    get_parser.add_argument("--id", type=str, help="Client ID.")
    get_parser.add_argument("--name", type=str, help="Client name.")

    args = parser.parse_args()

    if args.action == "create":
        new_id = create_client(args.name)
        print(new_id)
    elif args.action == "list":
        clients = list_clients()
        print(json.dumps(clients, indent=2))
    elif args.action == "get":
        if args.id:
            client = get_client(args.id)
        elif args.name:
            client = get_client(args.name)
        else:
            print("Error: Must provide --id or --name for 'get' action.", file=sys.stderr)
            sys.exit(1)
        
        if client:
            print(json.dumps(client, indent=2))
        else:
            print(f"Client not found: {args.id or args.name}", file=sys.stderr)
            sys.exit(1)

if __name__ == "__main__":
    # Ensure current working directory is the skill root for file access
    script_dir = os.path.dirname(__file__)
    skill_root = os.path.abspath(os.path.join(script_dir, os.pardir))
    os.chdir(skill_root)
    main()
