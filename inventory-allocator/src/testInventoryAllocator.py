from InventoryAllocator import InventoryAllocator
import unittest


class TestInventoryAllocatorFilterOrder(unittest.TestCase):
    def test_default_happy_case(self):
        order = {'apple': 1}
        expect = {'apple': 1}
        actual = InventoryAllocator.filter_order(order)
        self.assertEqual(actual, expect)

    def test_contain_invalid_number(self):
        order = {'apple': 1, 'peach': 0}
        expect = {'apple': 1}
        actual = InventoryAllocator.filter_order(order)
        self.assertEqual(actual, expect)

    def test_all_invalid_number(self):
        order = {'apple': -1, 'peach': 0}
        expect = {}
        actual = InventoryAllocator.filter_order(order)
        self.assertEqual(actual, expect)


class TestInventoryAllocatorComputeInventory(unittest.TestCase):
    def test_default_happy_case(self):
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        expect_inventory_distribution = {'apple': [('owd', 1)]}
        expect_total_inventory = {'apple': 1}
        expect = (expect_inventory_distribution, expect_total_inventory)
        actual = InventoryAllocator.compute_inventory(warehouses)
        self.assertEqual(actual, expect)

    def test_multiple_warehouse(self):
        warehouses = [
            {'name': 'owd', 'inventory': {'apple': 5}},
            {'name': 'dm', 'inventory': {'apple': 5}}
        ]
        expect_inventory_distribution = {'apple': [('owd', 5), ('dm', 5)]}
        expect_total_inventory = {'apple': 10}
        expect = (expect_inventory_distribution, expect_total_inventory)
        actual = InventoryAllocator.compute_inventory(warehouses)
        self.assertEqual(actual, expect)

    def test_multiple_goods(self):
        warehouses = [
            {'name': 'owd', 'inventory': {'apple': 5, 'peach': 3}},
            {'name': 'dm', 'inventory': {'apple': 5}}
        ]
        expect_inventory_distribution = {
            'apple': [('owd', 5), ('dm', 5)],
            'peach': [('owd', 3)]
        }
        expect_total_inventory = {'apple': 10, 'peach': 3}
        expect = (expect_inventory_distribution, expect_total_inventory)
        actual = InventoryAllocator.compute_inventory(warehouses)
        self.assertEqual(actual, expect)


class TestInventoryAllocatorHaveEnoughInventory(unittest.TestCase):
    def setUp(self):
        order = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        self.inventoryAllocator = InventoryAllocator(order, warehouses)

    def test_default_happy_case(self):
        self.assertTrue(self.inventoryAllocator.have_enough_inventory('apple', 1))

    def test_item_not_exist(self):
        self.assertFalse(self.inventoryAllocator.have_enough_inventory('peach', 1))

    def test_item_exist_but_not_enough(self):
        self.assertFalse(self.inventoryAllocator.have_enough_inventory('apple', 3))


class TestInventoryAllocatorFormatResult(unittest.TestCase):
    def test_default_happy_case(self):
        expect = [{'owd': {'apple': 1}}]
        raw_result = {'owd': {'apple': 1}}
        actual = InventoryAllocator.format_result(raw_result)
        self.assertEqual(actual, expect)

    def test_empty_case(self):
        expect = []
        raw_result = {}
        actual = InventoryAllocator.format_result(raw_result)
        self.assertEqual(actual, expect)


class TestInventoryAllocatorGetCheapestShipment(unittest.TestCase):
    def setUp(self):
        order = {'apple': 1}
        warehouses = [{'name': 'owd', 'inventory': {'apple': 1}}]
        self.inventoryAllocator = InventoryAllocator(order, warehouses)

    def test_default_happy_case(self):
        expect = [{'owd': {'apple': 1}}]
        self.assertEqual(self.inventoryAllocator.get_cheapest_shipment(), expect)

    def test_not_enough_inventory(self):
        warehouses = [{'name': 'owd', 'inventory': {'apple': 0}}]
        self.inventoryAllocator.update_warehouses(warehouses)
        expect = []
        self.assertEqual(self.inventoryAllocator.get_cheapest_shipment(), expect)

    def test_split_item(self):
        warehouses = [
            {'name': 'owd', 'inventory': {'apple': 5}},
            {'name': 'dm', 'inventory': {'apple': 5}}
        ]
        order = {'apple': 10}
        self.inventoryAllocator.update_warehouses(warehouses)
        self.inventoryAllocator.update_order(order)
        expect = [
            {'owd': {'apple': 5}},
            {'dm': {'apple': 5}}
        ]
        self.assertEqual(self.inventoryAllocator.get_cheapest_shipment(), expect)

    def test_get_from_cheapest_warehouse(self):
        warehouses = [
            {'name': 'owd', 'inventory': {'apple': 5}},
            {'name': 'dm', 'inventory': {'apple': 5}}
        ]
        order = {'apple': 3}
        self.inventoryAllocator.update_warehouses(warehouses)
        self.inventoryAllocator.update_order(order)
        expect = [
            {'owd': {'apple': 3}}
        ]
        self.assertEqual(self.inventoryAllocator.get_cheapest_shipment(), expect)

    def test_invalid_order(self):
        warehouses = [
            {'name': 'owd', 'inventory': {'apple': 5}},
            {'name': 'dm', 'inventory': {'apple': 5}}
        ]
        order = {'apple': 0}
        self.inventoryAllocator.update_warehouses(warehouses)
        self.inventoryAllocator.update_order(order)
        expect = []
        self.assertEqual(self.inventoryAllocator.get_cheapest_shipment(), expect)


if __name__ == '__main__':
    unittest.main()
