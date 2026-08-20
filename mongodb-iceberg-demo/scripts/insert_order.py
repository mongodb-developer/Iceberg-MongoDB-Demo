from common import get_collection, utcnow

ORDER_ID = "ORD-LIVE-001"


def main():
    client, coll = get_collection()
    try:
        existing = coll.find_one({"_id": ORDER_ID})
        if existing:
            coll.delete_one({"_id": ORDER_ID})
            print(f"Removed existing {ORDER_ID} so the next operation is a clean INSERT.")

        doc = {
            "_id": ORDER_ID,
            "customerId": "C-JEFF",
            "region": "IL",
            "product": "MongoDB Hoodie",
            "quantity": 3,
            "amount": 225.00,
            "status": "PROCESSING",
            "orderDate": utcnow(),
        }
        coll.insert_one(doc)
        print(f"Inserted {ORDER_ID}: {doc}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
