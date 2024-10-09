import sqlite3
import os

# Connect to (or create) a database named "computer.db"
conn = sqlite3.connect("computer.db")
cursor = conn.cursor()

# Create the sys_command table if it does not exist
cursor.execute("""
CREATE TABLE IF NOT EXISTS sys_command (
    id INTEGER PRIMARY KEY, 
    name VARCHAR(100) UNIQUE, 
    path VARCHAR(1000)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS websites (
    id INTEGER PRIMARY KEY, 
    name VARCHAR(100) UNIQUE, 
    url VARCHAR(1000) UNIQUE
)
""")

# List of directories to search for system and user-installed apps (excluding core services)
app_dirs = [
    "/Applications",                  # User-installed Applications
    "/System/Applications",           # System Applications
]

# Function to add applications to the sys_command table
def add_applications(cursor, app_dirs):
    for dir_path in app_dirs:
        dir_path = os.path.expanduser(dir_path)  # Expand "~" to the home directory

        if os.path.exists(dir_path):
            for app in os.listdir(dir_path):
                if app.endswith(".app"):  # Only process .app files
                    app_name = app.replace(".app", "").lower()  # Remove the .app extension, store in lowercase
                    app_path = os.path.join(dir_path, app)  # Get the full path

                    # Insert the app name and path into the sys_command table
                    query = "INSERT OR IGNORE INTO sys_command (name, path) VALUES (?, ?)"
                    cursor.execute(query, (app_name, app_path))
def add_websites(cursor):
    websites = [
        ('google', 'https://www.google.com'),
        ('youtube', 'https://www.youtube.com'),
        ('facebook', 'https://www.facebook.com'),
        ('twitter', 'https://www.twitter.com'),
        ('instagram', 'https://www.instagram.com'),
        ('linkedin', 'https://www.linkedin.com'),
        ('reddit', 'https://www.reddit.com'),
        ('wikipedia', 'https://www.wikipedia.org'),
        ('amazon', 'https://www.amazon.com'),
        ('ebay', 'https://www.ebay.com'),
        ('github','https://github.com/'),
        ('stackoverflow','https://stackoverflow.com/')
    ]

    query = "INSERT OR IGNORE INTO websites (name, url) VALUES (?, ?)"
    cursor.executemany(query, websites)
# Function to remove duplicates from sys_command table
def remove_duplicates_from_sys_command(cursor):
    # Create a temporary table to hold unique entries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temp_sys_command (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            path VARCHAR(1000)
        )
    """)

    # Insert unique entries into the temporary table
    cursor.execute("""
        INSERT INTO temp_sys_command (name, path)
        SELECT DISTINCT name, path
        FROM sys_command
    """)

    # Drop the original sys_command table
    cursor.execute("DROP TABLE sys_command")

    # Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE temp_sys_command RENAME TO sys_command")

# Function to remove duplicates from websites table
def remove_duplicates_from_websites(cursor):
    # Create a temporary table to hold unique entries
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS temp_websites (
            id INTEGER PRIMARY KEY,
            name VARCHAR(100) UNIQUE,
            url VARCHAR(1000) UNIQUE
        )
    """)

    # Insert unique entries into the temporary table
    cursor.execute("""
        INSERT INTO temp_websites (name, url)
        SELECT DISTINCT name, url
        FROM websites
    """)

    # Drop the original websites table
    cursor.execute("DROP TABLE websites")

    # Rename the temporary table to the original table name
    cursor.execute("ALTER TABLE temp_websites RENAME TO websites")

# Call the functions to add applications and websites
add_applications(cursor,app_dirs)  # Pass cursor to the function
add_websites(cursor)       # Pass cursor to the function

# Call the functions to remove duplicates
remove_duplicates_from_sys_command(cursor)  # Pass cursor
remove_duplicates_from_websites(cursor)      # Pass cursor

# Commit the changes and close the connection
conn.commit()
conn.close()