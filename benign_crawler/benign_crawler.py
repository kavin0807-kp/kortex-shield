import requests, time, random, getpass
BASE_URL = "http://localhost:8080"
try:
    #AUTH=None # Auth is disabled in nginx.conf for easier testing
    # If you re-enable it, uncomment these lines.
    username = input(f"Enter username for {BASE_URL}: "); 
    password = getpass.getpass("Enter password: ");
    AUTH = (username, password)
except Exception as e: print(f"Could not read credentials. Error: {e}"); exit(1)
EMPLOYEE_NAMES=["Alice", "Bob", "Charlie", "David", "Eve"]; DEPARTMENTS=["Engineering", "Marketing", "Sales", "HR"]
REVIEWS=["Great product!", "Could be better.", "Amazing!"]; COMMANDS=["ping google.com", "traceroute 8.8.8.8"]
USER_AGENTS=["Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36","Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"]
def generate_traffic():
    while True:
        try:
            app_choice = random.choice(['app1', 'app2', 'app3', 'refresh'])
            headers = {"User-Agent": random.choice(USER_AGENTS)}
            if app_choice == 'app1':
                params = { 'employee_name': random.choice(EMPLOYEE_NAMES), 'department': random.choice(DEPARTMENTS) }
                r = requests.get(BASE_URL, params=params, headers=headers, auth=AUTH, timeout=5)
                print(f"App1 (GET): {r.url} -> {r.status_code}")
            elif app_choice == 'app2':
                data = { 'review_text': random.choice(REVIEWS), 'rating': random.randint(3, 5) }
                r = requests.post(f"{BASE_URL}/?app=app2", data=data, headers=headers, auth=AUTH, timeout=5)
                print(f"App2 (POST): {r.url} -> {r.status_code}")
            elif app_choice == 'app3':
                data = {'command': random.choice(COMMANDS)}
                r = requests.post(f"{BASE_URL}/?app=app3", data=data, headers=headers, auth=AUTH, timeout=5)
                print(f"App3 (POST): {r.url} -> {r.status_code}")
            elif app_choice == 'refresh':
                r = requests.get(BASE_URL, headers=headers, auth=AUTH, timeout=5)
                print(f"Refresh (GET): {r.url} -> {r.status_code}")
            if r.status_code == 401: print("[!] Authentication failed."); break
        except requests.exceptions.RequestException as e: print(f"ERROR: Could not connect to {BASE_URL}. Is it running?"); break
        time.sleep(random.uniform(1, 3))
if __name__ == "__main__": print(f"[+] Starting traffic generation on {BASE_URL}..."); print("Press Ctrl+C to stop."); generate_traffic()
