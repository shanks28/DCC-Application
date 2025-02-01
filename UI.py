from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QListWidget, QInputDialog, QMessageBox
)
from PyQt5.QtCore import QThread, pyqtSignal
import requests
import sys

SERVER_URL = "http://127.0.0.1:8000/object"

class LoadInventoryThread(QThread):
    inventory_loaded = pyqtSignal(list)

    def run(self):
        try:
            response = requests.get(f"{SERVER_URL}/inventory")
            if response.status_code == 200:
                inventory_data = response.json()
                self.inventory_loaded.emit(inventory_data)
        except Exception as e:
            print(f"Error fetching inventory: {e}")

class RequestThread(QThread):
    result_ready = pyqtSignal(dict)  # Signal to send the result back

    def __init__(self, endpoint, data, method="POST", parent=None):
        super().__init__(parent)
        self.endpoint = endpoint
        self.data = data
        self.method = method.upper()

    def run(self):
        try:
            url = f"{SERVER_URL}/{self.endpoint}"
            if self.method == "POST":
                response = requests.post(url, json=self.data)
            elif self.method == "PUT":
                response = requests.put(url, json=self.data)
            elif self.method == "DELETE":
                response = requests.delete(url, json=self.data)
            else:
                raise ValueError(f"Unsupported HTTP method: {self.method}")

            if response.status_code in (200, 204):
                self.result_ready.emit({"status": "success"})
            else:
                try:
                    error_msg = response.json()
                except Exception:
                    error_msg = response.text
                self.result_ready.emit({"status": "error", "error": error_msg})
        except Exception as e:
            self.result_ready.emit({"status": "error", "error": str(e)})

class InventoryUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory Management")
        self.setGeometry(100, 100, 400, 300)
        self.layout = QVBoxLayout()

        self.inventory_list = QListWidget()
        self.layout.addWidget(self.inventory_list)

        self.refresh_button = QPushButton("Refresh Inventory")
        self.refresh_button.clicked.connect(self.load_inventory)
        self.layout.addWidget(self.refresh_button)

        self.add_button = QPushButton("Add Item")
        self.add_button.clicked.connect(self.add_item)
        self.layout.addWidget(self.add_button)

        self.remove_button = QPushButton("Remove Item")
        self.remove_button.clicked.connect(self.remove_item)
        self.layout.addWidget(self.remove_button)

        self.update_button = QPushButton("Update Quantity")
        self.update_button.clicked.connect(self.update_quantity)
        self.layout.addWidget(self.update_button)

        self.buy_button = QPushButton("Buy Item")
        self.buy_button.clicked.connect(self.buy_item)
        self.layout.addWidget(self.buy_button)

        self.return_button = QPushButton("Return Item")
        self.return_button.clicked.connect(self.return_item)
        self.layout.addWidget(self.return_button)

        self.setLayout(self.layout)
        self.load_inventory()

    def load_inventory(self):
        self.inventory_thread = LoadInventoryThread()
        self.inventory_thread.inventory_loaded.connect(self.update_inventory_list)
        self.inventory_thread.start()

    def update_inventory_list(self, inventory_data):
        self.inventory_list.clear()
        for item in inventory_data:
            self.inventory_list.addItem(f"{item['name']}: {item['quantity']}")

    def send_request(self, endpoint, data, method="POST"):
        self.request_thread = RequestThread(endpoint, data, method)
        self.request_thread.result_ready.connect(self.handle_request_result)
        self.request_thread.start()

    def handle_request_result(self, result):
        if result["status"] == "success":
            self.load_inventory()
        else:
            print("Error:", result.get("error"))

    def add_item(self):
        name, ok = QInputDialog.getText(self, "Add Item", "Enter item name:")
        if ok and name:
            quantity, ok = QInputDialog.getInt(self, "Quantity", "Enter quantity:")
            if ok:
                self.send_request("add-item", {"name": name, "qty": quantity}, method="POST")

    def remove_item(self):
        selected_item = self.inventory_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to remove.")
            return
        name = selected_item.text().split(":")[0]

        self.send_request("remove-item", {"name": name}, method="DELETE")

    def update_quantity(self):
        selected_item = self.inventory_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to update.")
            return
        name = selected_item.text().split(":")[0]
        new_quantity, ok = QInputDialog.getInt(self, "Update Quantity", "Enter new quantity:")
        if ok:

            self.send_request("update-quantity", {"name": name, "new_qty": new_quantity}, method="PUT")

    def buy_item(self):
        selected_item = self.inventory_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to buy.")
            return
        name = selected_item.text().split(":")[0]

        self.send_request("update-quantity", {"name": name, "new_qty": -1}, method="PUT")

    def return_item(self):
        selected_item = self.inventory_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "No Selection", "Please select an item to return.")
            return
        name = selected_item.text().split(":")[0]
        self.send_request("update-quantity", {"name": name, "new_qty": 1}, method="PUT")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = InventoryUI()
    window.show()
    sys.exit(app.exec_())
