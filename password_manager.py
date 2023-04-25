import os
import json
import bcrypt
from cryptography.fernet import Fernet


# Authentication
MASTER_PASSWORD = b"password123"
PASSWORD_HASH = bcrypt.hashpw(MASTER_PASSWORD, bcrypt.gensalt())

# Main
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

        # Encryption
        key_path = os.path.join(usb_path, "key.txt")
        if os.path.exists(key_path):
            with open(key_path, "rb") as key_file:
                key = key_file.read()
        else:
            key = Fernet.generate_key()
            with open(key_path, "wb") as key_file:
                key_file.write(key)

        fernet = Fernet(key)

        # Check if the password file exists on the USB drive
        password_file_path = os.path.join(usb_path, "passwords.bin")
        if os.path.exists(password_file_path):
            with open(password_file_path, "rb") as password_file:
                password_data_encrypted = password_file.read()
                try:
                    password_data_decrypted = fernet.decrypt(password_data_encrypted)
                    password_data = json.loads(password_data_decrypted)
                except Exception as e:
                    print("Error decrypting password file:", str(e))
                    return
        else:
            password_data = {}

        # Main menu
        while True:
            print("_" * 60)
            print(" ")
            print("1. View all passwords")
            print("2. Add a new password")
            print("3. Edit an existing password")
            print("4. Delete an existing password")
            print("5. Exit")

            choice = input("Please enter your choice: ")

            if choice == "1":
                view_passwords(password_data)
            elif choice == "2":
                add_password(password_data)
                save_passwords(password_data, password_file_path, fernet)
            elif choice == "3":
                edit_password(password_data)
                save_passwords(password_data, password_file_path, fernet)
            elif choice == "4":
                delete_passwords(password_data)
                save_passwords(password_data, password_file_path, fernet)
            elif choice =="5":
                save_passwords(password_data, password_file_path, fernet)
                break
            else:
                print("Invalid choice.")

    else:
        print("Incorrect password.")
        return False


def view_passwords(password_data):
    # Check if there are any saved passwords
    if not password_data:
        print("_" * 60)
        print(" ")
        print("No saved passwords.")
        return

    # Print out the saved passwords
    for key, value in password_data.items():
        print("_" * 60)
        print(key + ": " + value)

def add_password(password_data):
    # Ask for the new password and website
    print(" ")
    new_website = input("Please enter the website: ")
    new_password = input("Please enter the password: ")

    # Add the new password to the password data dictionary
    password_data[new_website] = new_password

    print("Password added successfully.")


def edit_password(password_data):
    # Check if there are any saved passwords
    if not password_data:
        print("No saved passwords.")
        return

    # Print out the saved passwords
    for key, value in password_data.items():
        print("_" * 60)
        print(key + ": " + value)
    # Ask for the website to edit
    print("_" * 60)
    print(" ")
    website_to_edit = input("Please enter the website to edit: ")

    # Check if the website exists in the password data
    if website_to_edit not in password_data:
        print("Website not found.")
        return

    # Ask for the new password
    new_password = input("Please enter the new password: ")

    # Update the password for the website
    password_data[website_to_edit] = new_password

    print("Password updated successfully.")


def delete_passwords(password_data):
    # Check if there are any saved passwords
    if not password_data:
        print("No saved passwords.")
        return

    # Print out the current saved passwords for reference
    view_passwords(password_data)

    # Ask for the website to delete
    print("_" * 60)
    print(" ")
    website_to_delete = input("Please enter the website to delete: ")

    # Check if the website exists in the password data
    if website_to_delete in password_data:
        # Delete the password for the website
        del password_data[website_to_delete]
        print(" ")
        print("Website", website_to_delete, "and password deleted successfully.")
    else:
        print(" ")
        print("Website not found in saved passwords.")



def save_passwords(password_data, password_file_path, fernet):
    # Encrypt the password data
    password_data_encrypted = fernet.encrypt(json.dumps(password_data).encode())

    # Save the password data to the file
    with open(password_file_path, "wb") as password_file:
        password_file.write(password_data_encrypted)

    print(" ")
    print("Passwords saved successfully.")

if __name__ == "__main__":
    main()
