import os
import threading
import asyncio
from bot.painter import painters
from bot.mineclaimer import mine_claimer
from bot.utils import night_sleep, Colors
from bot.notpx import NotPx
from telethon.sync import TelegramClient

# Global event loop variable
loop = asyncio.get_event_loop()

def multithread_starter():
    dirs = os.listdir("sessions/")
    sessions = list(filter(lambda x: x.endswith(".session"), dirs))
    sessions = list(map(lambda x: x.split(".session")[0], sessions))
    
    for session_name in sessions:
        try:
            cli = NotPx("sessions/" + session_name)

            # Schedule the painters and mine_claimer functions in the event loop
            asyncio.run_coroutine_threadsafe(painters(cli, session_name), loop)
            asyncio.run_coroutine_threadsafe(mine_claimer(cli, session_name), loop)

        except Exception as e:
            print("[!] {}Error loading session{} \"{}\", error: {}".format(Colors.RED, Colors.END, session_name, e))

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

def show_sessions():
    sessions = [f for f in os.listdir("sessions/") if f.endswith(".session")]
    if not sessions:
        print("[!] No sessions found.")
        return
    
    print(f"\n{Colors.BLUE}{'='*40}{Colors.END}")
    print(f"{Colors.GREEN}{'Available Sessions:':^40}{Colors.END}")  # Centered title
    print(f"{Colors.BLUE}{'='*40}{Colors.END}")
    
    for session in sessions:
        print(f"{Colors.YELLOW}{session[:-8].upper():^40}{Colors.END}")  # Uppercase and centered session names

    print(f"{Colors.BLUE}{'='*40}{Colors.END}")

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

def display_menu():
    print(f"\n{Colors.BLUE}{'='*40}{Colors.END}")
    print(f"{Colors.GREEN}         NotPx Auto Paint & Claim{Colors.END}")
    print(f"{Colors.BLUE}{'='*40}{Colors.END}")
    print(f"{Colors.YELLOW}1. Add Account{Colors.END}")
    print(f"{Colors.YELLOW}2. Start Mining + Claiming{Colors.END}")
    print(f"{Colors.YELLOW}3. Add API ID and Hash{Colors.END}")
    print(f"{Colors.YELLOW}4. Reset API Credentials{Colors.END}")
    print(f"{Colors.YELLOW}5. Reset Session{Colors.END}")
    print(f"{Colors.YELLOW}6. Show Sessions{Colors.END}")  # New option
    print(f"{Colors.BLUE}{'='*40}{Colors.END}")

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
        display_menu()
        
        option = input(f"\n[!] Enter your choice (1-6): ")  # Updated to 6 options
        
        if option == "1":
            name = input("\nEnter Session name: ")
            if not any(name in i for i in os.listdir("sessions/")):
                api_id, api_hash = load_api_credentials()
                if api_id and api_hash:
                    client = TelegramClient("sessions/" + name, api_id, api_hash).start()
                    client.disconnect()
                    print("[+] Session {} {}saved successfully{}.".format(name, Colors.GREEN, Colors.END))
                else:
                    print("[!] API credentials not found. Please add them first.")
            else:
                print("[x] Session {} {}already exists{}.".format(name, Colors.RED, Colors.END))
                
        elif option == "2":
            multithread_starter()
            break
            
        elif option == "3":
            add_api_credentials()
            
        elif option == "4":
            reset_api_credentials()
            
        elif option == "5":
            reset_session()
            
        elif option == "6":
            show_sessions()  # Call the show_sessions function
            
        else:
            print("[!] Invalid option. Please try again.")

if __name__ == "__main__":
    process()
