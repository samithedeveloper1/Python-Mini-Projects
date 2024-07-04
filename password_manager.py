from cryptography.fernet import Fernet, InvalidToken

def write_key():
    """
    Generates a key and saves it into a file named `key.key`
    """
    key = Fernet.generate_key()
    with open("key.key", "wb") as key_file:
        key_file.write(key)

def load_key():
    """
    Loads the key from the `key.key` file
    """
    try:
        with open("key.key", "rb") as key_file:
            key = key_file.read()
        return key
    except FileNotFoundError:
        print("Key not found. Generating a new key.")
        write_key()
        return load_key()

# Load or generate the key
key = load_key()
fer = Fernet(key)

def view():
    """
    View the stored account names and their passwords
    """
    try:
        with open('password.txt', 'r') as f:
            for line in f.readlines():
                data = line.rstrip()
                try:
                    user, passw = data.split("|")
                    print("User:", user, "| Password:", fer.decrypt(passw.encode()).decode())
                except InvalidToken:
                    print(f"Cannot decrypt password for user: {user}. Invalid token.")
    except FileNotFoundError:
        print("No passwords found. Please add a password first.")

def add():
    """
    Add a new account name and password
    """
    name = input('Account Name: ')
    pwd = input("Password: ")

    with open('password.txt', 'a') as f:
        f.write(name + " | " + fer.encrypt(pwd.encode()).decode() + "\n")

# Main loop
while True:
    mode = input("Would you like to add a new password or view existing ones (view, add), press q to quit? ").lower()
    if mode == "q":
        break
    elif mode == "view":
        view()
    elif mode == "add":
        add()
    else:
        print("Invalid mode")
        continue
