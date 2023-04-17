import os
import json
import bcrypt


# Authentication
MASTER_PASSWORD = b"password123"
PASSWORD_HASH = bcrypt.hashpw(MASTER_PASSWORD, bcrypt.gensalt())


def main():
    # User guess for the password
    password_attempt = input("Please enter the master password: ")

    # Do they match?
    if bcrypt.checkpw(password_attempt.encode(), PASSWORD_HASH):
        print("Access granted")
        print("_" * 60)

        # USB path
        usb_path = input("Please enter the path of the USB drive: ")

        # Check if the USB drive is available
        if not os.path.exists(usb_path):
            print("USB drive not found.")
            return

        # Check if the password file exists on the USB drive
        password_file_path = os.path.join(usb_path, "passwords.json")
        if os.path.exists(password_file_path):
            with open(password_file_path, "r") as password_file:
                password_data = json.load(password_file)
        else:
            password_data = {}

        # Main menu
        while True:
            print("1. View all passwords")
            print("2. Add a new password")
            print("3. Quit")

            choice = input("Please enter your choice: ")

            if choice == "1":
                view_passwords(password_data)
            elif choice == "2":
                add_password(password_data)
                save_passwords(password_data, password_file_path)
            elif choice == "3":
                save_passwords(password_data, password_file_path)
                break
            else:
                print("Invalid choice.")

    else:
        print("Incorrect password.")
        return False


def view_passwords(password_data):
    # Check if there are any saved passwords
    if not password_data:
        print("No saved passwords.")
        return

    # Print out the saved passwords
    for key, value in password_data.items():
        print(key + ": " + value)


def add_password(password_data):
    # Ask for the new password and website
    new_website = input("Please enter the website: ")
    new_password = input("Please enter the password: ")

    # Add the new password to the password data dictionary
    password_data[new_website] = new_password

    print("Password added successfully.")


def save_passwords(password_data, password_file_path):
    # Save the password data to the file
    with open(password_file_path, "w") as password_file:
        json.dump(password_data, password_file)

    print("Passwords saved successfully.")


if __name__ == "__main__":
    main()
