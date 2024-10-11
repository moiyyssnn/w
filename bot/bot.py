import os
import threading
import asyncio
from bot.painter import painters
from bot.mineclaimer import mine_claimer
from bot.utils import night_sleep, Colors
from bot.notpx import NotPx
from telethon.sync import TelegramClient

def multithread_starter():
    dirs = os.listdir("sessions/")
    sessions = list(filter(lambda x: x.endswith(".session"), dirs))
    sessions = list(map(lambda x: x.split(".session")[0], sessions))
    
    for session_name in sessions:
        try:
            cli = NotPx("sessions/" + session_name)

            # Define a wrapper function to run the async function in the thread
            def run_painters():
                asyncio.run(painters(cli, session_name))

            def run_mine_claimer():
                asyncio.run(mine_claimer(cli, session_name))

            # Start threads for painters and mine_claimer
            threading.Thread(target=run_painters).start()
            threading.Thread(target=run_mine_claimer).start()
        except Exception as e:
            print("[!] {}Error on load session{} \"{}\", error: {}".format(Colors.RED, Colors.END, session_name, e))

def add_api_credentials():
    api_id = input("Enter API ID: ")
    api_hash = input("Enter API Hash: ")
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.txt')
    with open(env_path, "w") as f:
        f.write(f"API_ID={api_id}\n")
        f.write(f"API_HASH={api_hash}\n")
    print("[+] API credentials saved successfully in env.txt file.")

def reset_api_credentials():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.txt')
    if os.path.exists(env_path):
        os.remove(env_path)
        print("[+] API credentials reset successfully.")
    else:
        print("[!] No env.txt file found. Nothing to reset.")

def reset_session():
    sessions = [f for f in os.listdir("sessions/") if f.endswith(".session")]
    if not sessions:
        print("[!] No sessions found.")
        return
    print("Available sessions:")
    for i, session in enumerate(sessions, 1):
        print(f"{i}. {session[:-8]}")
    choice = input("Enter the number of the session to reset: ")
    try:
        session_to_reset = sessions[int(choice) - 1]
        os.remove(os.path.join("sessions", session_to_reset))
        print(f"[+] Session {session_to_reset[:-8]} reset successfully.")
    except (ValueError, IndexError):
        print("[!] Invalid choice. Please try again.")

def load_api_credentials():
    env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'env.txt')
    if os.path.exists(env_path):
        with open(env_path, 'r') as f:
            lines = f.readlines()
            api_id = None
            api_hash = None
            for line in lines:
                if line.startswith('API_ID='):
                    api_id = line.split('=')[1].strip()
                elif line.startswith('API_HASH='):
                    api_hash = line.split('=')[1].strip()
            return api_id, api_hash
    return None, None

def process():
    if not os.path.exists("sessions"):
        os.mkdir("sessions")
    print(r"""{}
    _   _       _  ______       ______       _   
    | \ | |     | | | ___ \      | ___ \     | |  
    |  \| | ___ | |_| |_/ /_  __ | |_/ / ___ | |_ 
    | . ` |/ _ \| __|  __/\ \/ / | ___ \/ _ \| __|
    | |\  | (_) | |_| |    >  <  | |_/ / (_) | |_ 
    \_| \_/\___/ \__\_|   /_/\_\ \____/ \___/ \__|
                                                
            NotPx Auto Paint & Claim by @savanop - v1.0 {}""".format(Colors.BLUE, Colors.END))
    while True:
        option = input("[!] {}Enter 1{} For Adding Account, {}2{} for start mine + claim, {}3{} for add API ID and Hash, {}4{} to reset API credentials, {}5{} to reset session: ".format(
            Colors.BLUE, Colors.END, Colors.BLUE, Colors.END, Colors.BLUE, Colors.END, Colors.BLUE, Colors.END, Colors.BLUE, Colors.END))
        if option == "1":
            name = input("\nEnter Session name: ")
            if not any(name in i for i in os.listdir("sessions/")):
                api_id, api_hash = load_api_credentials()
                if api_id and api_hash:
                    client = TelegramClient("sessions/" + name, api_id, api_hash).start()
                    client.disconnect()
                    print("[+] Session {} {}saved success{}.".format(name, Colors.GREEN, Colors.END))
                else:
                    print("[!] API credentials not found. Please add them first.")
            else:
                print("[x] Session {} {}already exist{}.".format(name, Colors.RED, Colors.END))
        elif option == "2":
            multithread_starter()
            break
        elif option == "3":
            add_api_credentials()
        elif option == "4":
            reset_api_credentials()
        elif option == "5":
            reset_session()
        else:
            print("[!] Invalid option. Please try again.")
