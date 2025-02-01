# Python Developer Assignment - DCC Integration

## Overview
This assignment tests your ability to integrate Python with a **DCC application** (Maya or Blender). You'll build a **plugin** and a **local server** to manage object transforms and maintain a simple inventory.

## Part 1: DCC Plugin (Maya or Blender) *(Optional, but recommended)*

### Requirements
1. **Interface:**
   - Object selection (choose objects in Maya/Blender).
   - Transform controls (position, rotation, scale).
   - Endpoint dropdown (select which server function to use).
   - Submit button (sends data to the server).

2. **Functionality:**
   - Transform controls update when object transforms change in the DCC.
   - Clicking "Submit" sends selected object's transform data to the server.

---

## Part 2: Local Server (Flask or FastAPI)

### Endpoints
| Endpoint          | Description |
|------------------|-------------|
| `/transform`     | Takes all transforms (position, rotation, scale). |
| `/translation`   | Takes only position. |
| `/rotation`      | Takes only rotation. |
| `/scale`         | Takes only scale. |
| `/file-path`     | Returns the DCC file's path. `/file-path?projectpath=true` returns the project folder path. |
| `/add-item`      | Adds an item to a database (name, quantity). |
| `/remove-item`   | Removes an item from the database (by name). |
| `/update-quantity` | Updates an item's quantity (name, new quantity). |

### Server Behavior
- **10-second delay** for all responses.
- Logs received requests to the terminal.
- Uses correct status codes (`200`, `400`, `404`).

---

## Part 3: Database (SQLite)
- Use **SQLite** to store inventory items and quantities.
- The server updates the database based on `/add-item`, `/remove-item`, and `/update-quantity` requests.

---

## Part 4: PyQt/PySide UI

### Features
- **Inventory Display**: Shows the inventory from the database.
- **Purchase/Return**: Buttons to buy/return items (updates database & DCC plugin display).
- **Responsiveness**: UI should not freeze while waiting for server responses.

---

## Requirements
- **Python proficiency**
- **DCC Python API knowledge** Blender
- **REST API experience** FastAPI
- **SQLite database skills**
- **Git for version control**

---
## System Design
![image](https://github.com/user-attachments/assets/20dc89d7-df33-4abe-86c0-b3fdc394f867)

