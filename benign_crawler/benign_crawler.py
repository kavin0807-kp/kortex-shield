import requests
import time
import random
import getpass

BASE_URL = "http://localhost:8080"

try:
    # Authentication is disabled by default in the final nginx.conf for easier cloud testing.
    # If you re-enable it, uncomment these lines.
    username = input(f"Enter username for {BASE_URL}: ")
    password = getpass.getpass("Enter password: ")
    AUTH = (username, password)

except Exception as e:
    print(f"Could not read credentials. Error: {e}")
    exit(1)

EMPLOYEE_NAMES = ["Alice", "Bob", "Charlie", "David", "Eve", "Frank"]
DEPARTMENTS = ["Engineering", "Marketing", "Sales", "HR", "Legal"]
REVIEWS = [
    "This product is amazing, I highly recommend it!", "It's okay, but could be better.",
    "I had a great experience with this.", "Not what I expected."
]
COMMANDS = ["ping google.com", "traceroute 8.8.8.8", "dnslookup github.com", "netstat -a"]
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 1.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36",
]

def generate_traffic():
    while True:
        try:
            app_choice = random.choice(['app1', 'app2', 'app3'])
            user_agent = random.choice(USER_AGENTS)
            headers = {"User-Agent": user_agent}
            
            if app_choice == 'app1':
                params = { 'employee_name': random.choice(EMPLOYEE_NAMES), 'department': random.choice(DEPARTMENTS) }
                response = requests.get(BASE_URL, params=params, headers=headers, auth=AUTH, timeout=5)
                print(f"App1 (GET): {response.url} -> Status: {response.status_code}")
            elif app_choice == 'app2':
                data = { 'review_text': random.choice(REVIEWS), 'rating': random.randint(1, 5) }
                response = requests.post(f"{BASE_URL}/?app=app2", data=data, headers=headers, auth=AUTH, timeout=5)
                print(f"App2 (POST): {response.url} -> Status: {response.status_code}")
            elif app_choice == 'app3':
                data = {'command': random.choice(COMMANDS)}
                response = requests.post(f"{BASE_URL}/?app=app3", data=data, headers=headers, auth=AUTH, timeout=5)
                print(f"App3 (POST): {response.url} -> Status: {response.status_code}")

            if response.status_code not in [200, 401]:
                print(f"WARNING: Received unexpected status {response.status_code}")
            if response.status_code == 401:
                print("[!] Authentication failed. If you enabled auth in nginx.conf, please provide credentials.")
                break
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Could not connect to {BASE_URL}. Is the server running? Details: {e}")
            break

        time.sleep(random.uniform(0.5, 2.5))

if __name__ == "__main__":
    print(f"[+] Starting benign traffic generation on {BASE_URL}...")
    print("Press Ctrl+C to stop.")
    generate_traffic()