from pymongo import ReplaceOne
from common import get_collection


ORDERS = [
    ("DEMO-0001", "C-1001", "IL", "MongoDB Hoodie", 2, 150.00, "SHIPPED"),
    ("DEMO-0002", "C-1002", "TX", "Running Shoes", 1, 129.99, "PROCESSING"),
    ("DEMO-0003", "C-1003", "CA", "Laptop Stand", 3, 179.97, "SHIPPED"),
    ("DEMO-0004", "C-1004", "NY", "Mechanical Keyboard", 1, 149.00, "PROCESSING"),
    ("DEMO-0005", "C-1005", "IL", "USB-C Dock", 2, 239.98, "SHIPPED"),
    ("DEMO-0006", "C-1006", "TX", "Noise Cancelling Headphones", 1, 349.00, "REVIEW"),
    ("DEMO-0007", "C-1007", "CA", "Webcam", 2, 198.00, "SHIPPED"),
    ("DEMO-0008", "C-1008", "WA", "Monitor Arm", 1, 119.00, "PROCESSING"),
    ("DEMO-0009", "C-1009", "FL", "Portable SSD", 2, 279.98, "SHIPPED"),
    ("DEMO-0010", "C-1010", "NY", "Desk Lamp", 1, 89.00, "PROCESSING"),
    ("DEMO-0011", "C-1011", "IL", "Travel Backpack", 1, 139.00, "SHIPPED"),
    ("DEMO-0012", "C-1012", "TX", "Smart Speaker", 2, 198.00, "PROCESSING"),
]


def main():
    client, coll = get_collection()
    try:
        ops = []
        from common import utcnow
        for order_id, customer_id, region, product, quantity, amount, status in ORDERS:
            doc = {
                "_id": order_id,
                "customerId": customer_id,
                "region": region,
                "product": product,
                "quantity": quantity,
                "amount": amount,
                "status": status,
                "orderDate": utcnow(),
            }
            ops.append(ReplaceOne({"_id": order_id}, doc, upsert=True))

        result = coll.bulk_write(ops, ordered=True)
        print(f"Seed complete: {len(ORDERS)} demo orders ready in {coll.full_name}")
        print(
            f"matched={result.matched_count} modified={result.modified_count} "
            f"upserted={result.upserted_count}"
        )
    finally:
        client.close()


if __name__ == "__main__":
    main()
