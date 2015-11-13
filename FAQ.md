alembic.util.CommandError: Target database is not up to date.

After creating a migration, either manually or as `--autogenerate`, you must apply it with `alembic upgrade head`. If you used `db.create_all()` from a shell, you can use `alembic stamp head` to indicate that the current state of the database represents the application of all migrations.
