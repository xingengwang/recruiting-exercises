
### Problem

The problem is compute the best way an order can be shipped (called shipments) given inventory across a set of warehouses (called inventory distribution). 
The task is to implement InventoryAllocator class to produce the cheapest shipment.


### How to run the code
The solution that I provide is in python3 and my version is 3.8, please make sure your python version is newer than 3.5 because I use `typing` which is 
the feature from version 3.5, any version below that might run in to syntax error.

1. make sure you have your python version >= 3.5
2. cd into the src folder
3. in your terminal, run `python testInventoryAllocator.py` and all the test case will be run


### File Structure 
There are only one folder here call src which contain all the codes
1. `InventoryAllocator.py` is the source code for this assessment
2. `testInventoryAllocator.py` is the test file for the `InventoryAllocator.py`


### Assumption
I have been told that I can assume that the list of warehouses is pre-sorted based on cost.
We know that shipping from the first warehouse is cheaper from the second one, but we don't know how much cheaper,
this led to a problem, what happen if I want 4 apple but first warehouse only has 3 but the second has 4.
It might be cheaper if we just get one shipment from the second warehouse because then we just need one shipment,
This is true if cost between two warehouse are not that much different, but it is also possible that the second warehouse 
is really far away and the cost are a lot more expensive which mean ship all 3 apple from the first warehouse and just 
ship one apple from the second warehouse could be cheaper that just ship all 4 apple from the second warehouse.

Due to this unknown, I make a assumption in my solution that we always want to get the goods from the cheaper warehouse first.
