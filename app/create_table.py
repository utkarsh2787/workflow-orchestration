"""Create all tables after importing model modules.

This script imports every module in `app.models` and logs per-module import
errors. That makes it easier to diagnose circular imports or exceptions raised
during model import. After importing, it runs Base.metadata.create_all.
"""
import os
import pkgutil
import importlib
from app.db.session import Base, engine
from sqlalchemy import inspect


def import_models():
	models_dir = os.path.join(os.path.dirname(__file__), "models")
	if not os.path.isdir(models_dir):
		print("models directory not found:", models_dir)
		return

	for finder, name, ispkg in pkgutil.iter_modules([models_dir]):
		module_name = f"app.models.{name}"
		try:
			importlib.import_module(module_name)
			print(f"Imported {module_name}")
		except Exception as e:
			print(f"Failed to import {module_name}: {e!r}")


def create_tables():
	print("Engine URL:", engine.url)
	import_models()

	try:
		Base.metadata.create_all(bind=engine)
		inspector = inspect(engine)
		tables = inspector.get_table_names()
		if tables:
			print("Created / existing tables:")
			for t in tables:
				print(" -", t)
		else:
			print("No tables found in database after create_all.")
	except Exception as e:
		print("create_all failed:", repr(e))


if __name__ == "__main__":
	create_tables()
