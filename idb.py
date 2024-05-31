import os
import sqlite3
import datetime
import hashlib
import signal
import sys
import time
import argparse

# Function to check if a file has an image or video extension
def is_image_or_video(filename):
    image_extensions = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    video_extensions = ('.mp4', '.avi', '.mov', '.mkv', '.wmv')
    _, ext = os.path.splitext(filename.lower())
    return ext in image_extensions or ext in video_extensions

# Function to create table if it doesn't exist
def create_table_if_not_exists(conn):
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS media_files
                 (id INTEGER PRIMARY KEY, file_name TEXT UNIQUE, file_size INTEGER, created_at TEXT, modified_at TEXT, file_hash TEXT)''')
    c.execute('''CREATE INDEX IF NOT EXISTS idx_file_hash ON media_files (file_hash)''')

# Function to calculate file hash
def calculate_file_hash(file_path):
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while True:
            chunk = f.read(4096)
            if not chunk:
                break
            hasher.update(chunk)
    return hasher.hexdigest()

# Function to scan directory tree and add entries to SQLite database
def scan_and_insert(directory, db_file, print_duplicates_only):
    inserted_count = [0]
    ignored_count = [0]
    processed_files_count = [0]
    start_time = time.time()

    def signal_handler(sig, frame):
        print("\nExiting...")
        print("Inserted files:", inserted_count[0])
        print("Ignored files:", ignored_count[0])
        print("Processed files per minute:", processed_files_count[0] / ((time.time() - start_time) / 60))
        sys.exit(0)

    # Register signal handler for Ctrl-C
    signal.signal(signal.SIGINT, signal_handler)
    
    conn = sqlite3.connect(db_file)
    
    # Create table if it doesn't exist and add indexes
    create_table_if_not_exists(conn)

    c = conn.cursor()

    # Traverse directory tree
    for root, dirs, files in os.walk(directory):
        print("Entering directory:", root)  # Print directory name

        for file in files:
            if time.time() - start_time >= 60:  # Print stats approximately every minute
                print("Processed files in the last minute:", processed_files_count[0])
                processed_files_count[0] = 0  # Reset count
                start_time = time.time()  # Reset timer

            if is_image_or_video(file):
                file_path = os.path.join(root, file)
                file_name = os.path.relpath(file_path, directory)
                file_stat = os.stat(file_path)
                file_size = file_stat.st_size

                # Check if file already exists in database
                c.execute("SELECT COUNT(*) FROM media_files WHERE file_name = ? AND file_size = ?", (file_name, file_size))
                if c.fetchone()[0] > 0:
                    print("Duplicate found:", file_name)  # Print duplicate info
                    ignored_count[0] += 1
                elif not print_duplicates_only:
                    created_at = datetime.datetime.fromtimestamp(file_stat.st_cityme).isoformat()
                    modified_at = datetime.datetime.fromtimestamp(file_stat.st_mtime).isoformat()
                    file_hash = calculate_file_hash(file_path)
                    
                    try:
                        c.execute("INSERT INTO media_files (file_name, file_size, created_at, modified_at, file_hash) VALUES (?, ?, ?, ?, ?)",
                                  (file_name, file_size, created_at, modified_at, file_hash))
                        inserted_count[0] += 1
                    except sqlite3.IntegrityError:
                        print("Insert failed due to IntegrityError, likely a duplicate not caught by the initial check.")

                processed_files_count[0] += 1

                # Commit changes every 50 inserts
                if inserted_count[0] % 50 == 0 and not print_duplicates_only:
                    conn.commit()
    
    # Commit any remaining changes
    if not print_duplicates_only:
        conn.commit()
    conn.close()

    # Final printout
    print("Inserted files:", inserted_count[0])
    print("Ignored files:", ignored_count[0])
    print("Processed files per minute:", processed_files_count[0] / ((time.time() - start_time) / 60))

def main():
    parser = argparse.ArgumentParser(description="Scan directory and manage media files in SQLite database.")
    parser.add_argument("directory", help="Directory to scan")
    parser.add_argument("db_file", help="SQLite database file path")
    parser.add_argument("--print-duplicates", action="store_true", help="Print duplicates without inserting")

    args = parser.parse_args()

    scan_and_insert(args.directory, args.db_file, args.print_duplicates)

if __name__ == "__main__":
    main()
