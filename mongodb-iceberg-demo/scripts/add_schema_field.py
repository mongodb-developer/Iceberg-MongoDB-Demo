from common import get_collection, utcnow

ORDER_ID = "ORD-LIVE-002"


def main():
    client, coll = get_collection()
    try:
        coll.delete_one({"_id": ORDER_ID})
        doc = {
            "_id": ORDER_ID,
            "customerId": "C-9999",
            "region": "CA",
            "product": "MacBook Pro",
            "quantity": 1,
            "amount": 3499.00,
            "status": "REVIEW",
            "fraudScore": 0.92,
            "orderDate": utcnow(),
        }
        coll.insert_one(doc)
        print(f"Inserted {ORDER_ID} with NEW FIELD fraudScore=0.92")
        print("Use sql/05_validate_schema.sql to validate Iceberg schema evolution.")
    finally:
        client.close()


if __name__ == "__main__":
    main()
