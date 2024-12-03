import os
import subprocess

def run_cleaning():
    """Run the cleaning script."""
    print("Running the cleaning script...")
    subprocess.run(["python", "app/clean_5.py"])

def create_database():
    """Run the database creation script."""
    print("Creating the database...")
    subprocess.run(["python", "app/create_db.py"])

def insert_data():
    """Run the data insertion script."""
    print("Inserting data into the database...")
    subprocess.run(["python", "app/insert.py"])

def view_data():
    """Run the data selection script."""
    print("Viewing data from the database...")
    subprocess.run(["python", "app/select.py"])

def main_menu():
    """Main menu for the application."""
    while True:
        print("\nMain Menu:")
        print("1. Clean data")
        print("2. Create database")
        print("3. Insert data into database")
        print("4. View data from database")
        print("5. Exit")
        choice = input("Select an option: ")

        if choice == "1":
            run_cleaning()
        elif choice == "2":
            create_database()
        elif choice == "3":
            insert_data()
        elif choice == "4":
            view_data()
        elif choice == "5":
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main_menu()
