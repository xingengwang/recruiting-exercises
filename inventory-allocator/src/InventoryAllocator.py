import collections
from typing import Dict, List

Order = Dict[str, int]


class InventoryAllocator:
    """
    InventoryAllocator allow us to find the cheapest shipment for a order among all the inventory distribution
    """
    def __init__(self, order: Order, warehouses: List[dict]):
        self.order = self.filter_order(order)
        self.inventory_distribution, self.total_inventory = self.compute_inventory(warehouses)

    @staticmethod
    def filter_order(order: Order) -> Order:
        """
        Remove all the item in the given order that has a number that is less than 1
        :param order: Order
        :return:
        order: a order that all item's amount are greater than 0
        """
        delete = [key for key in order if order[key] < 1]
        for key in delete:
            del order[key]
        return order

    @staticmethod
    def compute_inventory(warehouses: List[dict]) -> (Dict[str, list], Dict[str, int]):
        """
        :param warehouses: list of object with warehouse name and inventory amounts
        :return:
        inventory_distribution: a map indicate which item are in which warehouse and the amount in that warehouse
                                i.e. if two warehouses each has 5 apples, the result will be {apple: [(owd, 5), (dm, 5)]}
        total_inventory: accumulative total of all item in all the given warehouses
                         i.e. if two warehouses each has 5 apples, the result will be {apple: 10}
        """
        inventory_distribution = collections.defaultdict(list)
        total_inventory = collections.defaultdict(int)
        for warehouse in warehouses:
            for k, v in warehouse.get('inventory', {}).items():
                inventory_distribution[k].append((warehouse.get('name'), v))
                total_inventory[k] += v
        return inventory_distribution, total_inventory

    @staticmethod
    def format_result(results: dict) -> List[dict]:
        """
        :param results: a dictionary that has the key are warehouse name and values are item's name and amount
        :return: a list of warehouse name to item map
        """
        return [{k: v} for k, v in results.items()]

    def update_order(self, order: Order):
        """
        update the order in the given InventoryAllocator instance
        :param order: a new order
        """
        self.order = self.filter_order(order)

    def update_warehouses(self, warehouses: List[dict]):
        """
        update the warehouses in the given InventoryAllocator instance
        :param warehouses: a new list of warehouses
        """
        self.inventory_distribution, self.total_inventory = self.compute_inventory(warehouses)

    def have_enough_inventory(self, item_name: str, item_quantity: int) -> bool:
        """
        Check if the item form the order are in our inventory and if we have enough quantity in inventory for this item
        :param item_name: the name of the item from the order
        :param item_quantity: the quantity of the item for item_name from the order
        :return: bool
        """
        return item_name in self.total_inventory and self.total_inventory.get(item_name) >= item_quantity

    def get_cheapest_shipment(self):
        """
        Find the cheapest shipment from all the warehouses for the order
        :return: a list of map which key is the warehouse name and value is the list of goods from that warehouse
        """
        if not self.order or not self.total_inventory:
            return []
        results = collections.defaultdict(dict)
        for item_name, item_quantity in self.order.items():
            if not self.have_enough_inventory(item_name, item_quantity):
                return []
            else:
                inventory_list = self.inventory_distribution.get(item_name, ())
                for warehouse_name, item_count in inventory_list:
                    if item_count >= item_quantity:
                        results[warehouse_name][item_name] = item_quantity
                        break
                    else:
                        item_quantity -= item_count
                        results[warehouse_name][item_name] = item_count

        return self.format_result(results)
