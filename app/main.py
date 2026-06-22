import os
import sys

def get_database_url():
    """Retrieve the database URL from environment variables.
    Raises a clear error if not set.
    """
    try:
        return os.environ["DATABASE_URL"]
    except KeyError:
        sys.stderr.write("Error: DATABASE_URL environment variable not set\n")
        sys.exit(1)

def main():
    db_url = get_database_url()
    # Initialize application with db_url (placeholder for actual init code)
    print(f"Starting application with database URL: {db_url}")
    # ... rest of the application logic ...

if __name__ == "__main__":
    main()
