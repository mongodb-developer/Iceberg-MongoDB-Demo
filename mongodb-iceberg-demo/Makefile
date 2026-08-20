.PHONY: install seed insert update delete schema reset demo

install:
	python3 -m pip install -r requirements.txt

seed:
	python scripts/seed_orders.py

insert:
	python scripts/insert_order.py

update:
	python scripts/update_order.py

delete:
	python scripts/delete_order.py

schema:
	python scripts/add_schema_field.py

reset:
	python scripts/reset_demo.py

demo:
	python scripts/live_demo.py
