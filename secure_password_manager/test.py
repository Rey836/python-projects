from auth import AuthManager

auth = AuthManager()

print("=" * 40)
print("Testing Authentication")
print("=" * 40)

username = input("Username: ")
password = input("Master Password: ")

try:
    auth.register(username, password)
    print("✅ User registered.")

except ValueError:
    print("ℹ️ User already exists.")

try:
    user = auth.login(username, password)

    print("\nLogin Successful!")
    print("------------------------")
    print(f"ID: {user.id}")
    print(f"Username: {user.username}")

except ValueError as e:
    print(e)