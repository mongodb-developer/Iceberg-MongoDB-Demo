from common import get_collection

ORDER_ID = "ORD-LIVE-001"


def main():
    client, coll = get_collection()
    try:
        result = coll.delete_one({"_id": ORDER_ID})
        print(f"Deleted {result.deleted_count} document(s) for {ORDER_ID}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
