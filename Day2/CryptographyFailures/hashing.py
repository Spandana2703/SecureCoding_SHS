import bcrypt
import os

USER_DATA_FILE = "admin_data.txt"

def hash_passcode(passcode: str) -> bytes:
    return bcrypt.hashpw(passcode.encode('utf-8'), bcrypt.gensalt())


def verify_passcode(stored_hash: bytes, passcode: str) -> bool:
    return bcrypt.checkpw(passcode.encode('utf-8'), stored_hash)


def register_admin():
    print("Admin Registration")
    username = input("Enter a username: ")
    passcode = input("Enter a passcode: ")

    hashed_passcode = hash_passcode(passcode)

    with open(USER_DATA_FILE, 'w') as file:
        file.write(f"{username},{hashed_passcode.decode('utf-8')}\n")

    print("Admin registered successfully!")


def login_admin():
    print("Admin Login")
    
    if not os.path.exists(USER_DATA_FILE):
        print("No admin registered. Please register first.")
        return False

    username = input("Enter your username: ")
    passcode = input("Enter your passcode: ")

    with open(USER_DATA_FILE, 'r') as file:
        admin_data = file.readlines()

   
    attempts = 0
    while attempts < 3:
        for admin in admin_data:
            stored_username, stored_hash = admin.strip().split(',')
            if stored_username == username:
                if verify_passcode(stored_hash.encode('utf-8'), passcode):
                    print("Login successful!")
                    return True
                else:
                    attempts += 1
                    print(f"Invalid passcode. {3 - attempts} attempts left.")
                    break
        if attempts == 3:
            print("You have been locked out due to too many failed attempts.")
            return False
        username = input("Re-enter your username: ")
        passcode = input("Re-enter your passcode: ")
    return False


def main():
    print("Welcome to the Hospital Admin System")
    
    while True:
        choice = input("Choose an option: 1) Register 2) Login 3) Exit: ")

        if choice == '1':
            register_admin()
        elif choice == '2':
            login_admin()
        elif choice == '3':
            print("Exiting system.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

