from dataclasses import dataclass, field
from typing import Dict, List, Optional


class Product:
    """Represents a sellable product in the warehouse."""

    def __init__(self, sku: str, name: str, category: str, unit_price: float, reorder_level: int):
        self.sku = sku
        self.name = name
        self.category = category
        self.unit_price = unit_price
        self.reorder_level = reorder_level
        self.stock_level = 0

    def restock(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Restock quantity must be greater than zero.")
        self.stock_level += quantity

    def sell(self, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Sale quantity must be greater than zero.")
        if quantity > self.stock_level:
            raise ValueError(f"Not enough stock for {self.name}. Available: {self.stock_level}")
        self.stock_level -= quantity

    def is_low_stock(self) -> bool:
        return self.stock_level <= self.reorder_level

    def __repr__(self) -> str:
        return f"Product(sku={self.sku}, name={self.name}, stock={self.stock_level})"


@dataclass
class OrderLine:
    product: Product
    quantity: int

    def subtotal(self) -> float:
        return self.product.unit_price * self.quantity


class Order:
    """Represents a customer order. Subclasses can override fulfillment behaviour."""

    _next_id = 1

    def __init__(self, customer_name: str, priority: str = "normal"):
        self.id = Order._next_id
        Order._next_id += 1
        self.customer_name = customer_name
        self.priority = priority
        self.items: List[OrderLine] = []
        self.status = "pending"

    def add_item(self, product: Product, quantity: int) -> None:
        if quantity <= 0:
            raise ValueError("Order quantity must be greater than zero.")
        self.items.append(OrderLine(product=product, quantity=quantity))

    def total_value(self) -> float:
        return sum(item.subtotal() for item in self.items)

    def fulfill(self) -> None:
        for line in self.items:
            line.product.sell(line.quantity)
        self.status = "fulfilled"

    def __repr__(self) -> str:
        return f"Order(id={self.id}, customer={self.customer_name}, total={self.total_value():.2f}, status={self.status})"


class PriorityOrder(Order):
    """A special order type with expedited handling."""

    def __init__(self, customer_name: str):
        super().__init__(customer_name, priority="high")

    def fulfill(self) -> None:
        print(f"Priority order {self.id} is being processed with express fulfillment.")
        super().fulfill()


class Warehouse:
    """Owns stock, orders and warehouse operational rules."""

    def __init__(self, name: str):
        self.name = name
        self.inventory: Dict[str, Product] = {}
        self.orders: List[Order] = []

    def add_product(self, product: Product) -> None:
        self.inventory[product.sku] = product

    def receive_stock(self, sku: str, quantity: int) -> None:
        product = self.inventory.get(sku)
        if product is None:
            raise KeyError(f"Product with SKU {sku} was not found.")
        product.restock(quantity)

    def create_order(self, customer_name: str, priority: bool = False) -> Order:
        order = PriorityOrder(customer_name) if priority else Order(customer_name)
        self.orders.append(order)
        return order

    def add_item_to_order(self, order: Order, sku: str, quantity: int) -> None:
        product = self.inventory.get(sku)
        if product is None:
            raise KeyError(f"Product with SKU {sku} does not exist.")
        order.add_item(product, quantity)

    def fulfill_order(self, order_id: int) -> None:
        for order in self.orders:
            if order.id == order_id:
                if order.status == "fulfilled":
                    print(f"Order {order_id} has already been fulfilled.")
                    return
                order.fulfill()
                return
        raise ValueError(f"Order {order_id} not found.")

    def low_stock_report(self) -> List[Product]:
        return [product for product in self.inventory.values() if product.is_low_stock()]

    def inventory_summary(self) -> None:
        print(f"\nWarehouse: {self.name}")
        for product in self.inventory.values():
            status = "LOW" if product.is_low_stock() else "OK"
            print(f"- {product.name} [{product.sku}] : {product.stock_level} units | {status}")


class WarehouseManager:
    """High-level controller managing warehouse operations."""

    def __init__(self, warehouse: Warehouse):
        self.warehouse = warehouse

    def receive_shipment(self, sku: str, quantity: int) -> None:
        self.warehouse.receive_stock(sku, quantity)
        print(f"Received {quantity} units for SKU {sku}.")

    def place_order(self, customer_name: str, sku: str, quantity: int, priority: bool = False) -> Order:
        order = self.warehouse.create_order(customer_name, priority=priority)
        self.warehouse.add_item_to_order(order, sku, quantity)
        print(f"Created order {order.id} for {customer_name}.")
        return order

    def run_daily_report(self) -> None:
        print("\nDaily warehouse report")
        self.warehouse.inventory_summary()
        low_stock = self.warehouse.low_stock_report()
        if low_stock:
            print("\nItems requiring replenishment:")
            for item in low_stock:
                print(f"- {item.name} [{item.sku}] needs restocking.")
        else:
            print("\nNo items are currently low on stock.")


if __name__ == "__main__":
    warehouse = Warehouse("North Distribution Hub")
    manager = WarehouseManager(warehouse)

    laptop = Product("LAP-100", "Laptop Pro", "electronics", 1200.00, 10)
    keyboard = Product("KEY-200", "Mechanical Keyboard", "accessories", 95.00, 15)
    monitor = Product("MON-300", "4K Monitor", "electronics", 420.00, 8)

    warehouse.add_product(laptop)
    warehouse.add_product(keyboard)
    warehouse.add_product(monitor)

    manager.receive_shipment("LAP-100", 25)
    manager.receive_shipment("KEY-200", 40)
    manager.receive_shipment("MON-300", 12)

    order = manager.place_order("Apex Retail", "LAP-100", 4, priority=True)
    manager.place_order("Bright Labs", "KEY-200", 8)

    warehouse.fulfill_order(order.id)
    manager.run_daily_report()

    print("\nOrder snapshot:")
    print(order)
