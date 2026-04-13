---
name: client-manager
description: Manage client IDs for Mika Automation LLC. Generate unique, human-readable client IDs, list all registered clients, and retrieve client details. Use this skill when: (1) Onboarding a new client, (2) Retrieving a client's ID or details, (3) Listing all current clients.
---

# Client Manager Skill

This skill provides utilities for managing client IDs for Mika Automation LLC. It ensures consistent and unique identifiers for all client-related projects and data.

## Data Structure: `references/client_ids.json`

Client data is stored in `references/client_ids.json` as a JSON array. Each client object has the following structure:

```json
[
  {
    "id": "client-slug-001",
    "name": "Client Name LLC",
    "created_at": "2026-03-27T21:00:00Z"
  }
]
```

## Available Actions (via `scripts/client_manager.py`)

This script provides the core functionality. When using this skill, execute the Python script with the appropriate subcommand and arguments.

### 1. Create a New Client ID

**Purpose:** Generates a new, unique client ID based on the client's name and adds it to the registry.

```bash
scripts/client_manager.py create "Client Name LLC"
```

**Output:** Returns the newly created client ID string.

### 2. List All Clients

**Purpose:** Retrieves a list of all registered clients with their IDs and names.

```bash
scripts/client_manager.py list
```

**Output:** A JSON array of client objects.

### 3. Get Client Details

**Purpose:** Retrieves details for a specific client by its ID or name.

```bash
scripts/client_manager.py get --id "client-slug-001"
# OR
scripts/client_manager.py get --name "Client Name LLC"
```

**Output:** A JSON object of the client, or an error if not found.

---

## Initializing the Skill

Upon first use, initialize `references/client_ids.json` with any existing clients (e.g., Birch Street Law, Mika Automation) by calling the `create` action for each. Ensure `git add -A && git commit` after initialization.
