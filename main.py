import json
import requests
import time
import string
import random

with open('api.json', 'r') as start_file:
    start_data = json.load(start_file)


SCRAPEOPS_API_KEY = start_data.get('api_key', '')

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))

def get_random_user_agent():
    url = 'http://headers.scrapeops.io/v1/user-agents?api_key=' + SCRAPEOPS_API_KEY
    response = requests.get(url)
    json_response = response.json()
    user_agents = json_response.get('result', [])
    if user_agents:
        return user_agents[random.randint(0, len(user_agents) - 1)]
    else:
        return None

def start_process():
    url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    headers = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Linux"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
    }

    data = {
        'partnerUserId': generate_random_string(64)
    }

    session = requests.Session()

    try:
        last_user_agent_change_time = time.time()
        request_count = 0
        is_429_printed = False

        while True:

            current_time = time.time()
            if current_time - last_user_agent_change_time >= 12:
                print("\033[93m[WARNING]\033[0m CHANGING USER AGENT. PLEASE WAIT...")
                random_user_agent = get_random_user_agent()
                if random_user_agent:
                    headers['user-agent'] = random_user_agent
                    print(f"\033[92m[INFO]\033[0m USER AGENT: {random_user_agent}")
                    last_user_agent_change_time = current_time

            response = session.post(url, headers=headers, json=data)
            request_count += 1

            if response.status_code == 200:
                token = response.json().get('token')
                if token:
                    try:
                        with open('codes.txt', 'a') as file:
                            file.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
                            print(f"\033[92m[INFO]\033[0m https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
                    except Exception as error:
                        print(f"\033[91m[ERROR]\033[0m Error writing to file: {str(error)}")
            elif response.status_code == 429:
                if not is_429_printed:
                    print("\033[93m[WARNING]\033[0m 429 ERROR RECEIVED. WAITING...")
                    is_429_printed = True
                    while response.status_code == 429:
                        time.sleep(60)  # Wait for 60 seconds before checking again
                        response = session.post(url, headers=headers, json=data)
                    is_429_printed = False
                else:
                    time.sleep(0)
            else:
                print(f"Request failed, status code: {response.status_code}.")
                print(f"Error message: {response.text}")

            time.sleep(0.5)

    except Exception as error:
        print(f"\033[91m[ERROR]\033[0m An error occurred: {str(error)}")

    finally:
        session.close()

if __name__ == "__main__":
    while True:
        print("1. Start process")
        print("2. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            start_process()
        elif choice == "2":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please enter 1 or 2.")
