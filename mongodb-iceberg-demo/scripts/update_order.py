from common import get_collection

ORDER_ID = "ORD-LIVE-001"


def main():
    client, coll = get_collection()
    try:
        result = coll.update_one(
            {"_id": ORDER_ID},
            {"$set": {"status": "SHIPPED", "amount": 199.00}},
        )
        if result.matched_count == 0:
            raise SystemExit(
                f"{ORDER_ID} does not exist. Run scripts/insert_order.py first."
            )
        print(f"Updated {ORDER_ID}: status=SHIPPED amount=199.00")
    finally:
        client.close()


if __name__ == "__main__":
    main()
