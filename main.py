

import time
import sys
import os
import requests
import json

# --- UPDATE LOGIC ---
# IMPORTANT: You need to install the 'requests' library for this to work.
# Run 'pip install requests' in your terminal.

# Define the current version of the script
VERSION = "1.0.0"
# Define the URL for the version file on GitHub
# You'll need to change this URL to point to your specific repository.
# The file should contain only the version number, e.g., "1.1"
GITHUB_VERSION_URL = "https://raw.githubusercontent.com/bablerpaul/IMAZER/refs/heads/main/latest_version.txt"
GITHUB_REPO_URL = "https://github.com/bablerpaul/IMAZER"

def check_for_updates():
    """Checks for a new version of the script on GitHub."""
    print("Checking for updates...")
    try:
        response = requests.get(GITHUB_VERSION_URL, timeout=5)
        response.raise_for_status()  # Raise an exception for bad status codes
        latest_version = response.text.strip()
        
        # Simple version comparison
        if latest_version != VERSION:
            print(f"\n--- A new version ({latest_version}) is available! ---")
            print(f"Your current version is {VERSION}.")
            print(f"Please download the latest version from: {GITHUB_REPO_URL}")
        else:
            print("You are running the latest version.")
            
    except requests.exceptions.RequestException as e:
        print(f"Could not check for updates. Error: {e}")
    print("-" * 35)

# --- END OF UPDATE LOGIC ---


# ANSI color codes
MIDNIGHT_BLUE = "\033[38;5;21m"
DRAGON_RED = "\033[38;5;124m"
RESET = "\033[0m"

# Clear screen function
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Animation frames with moving legs
frames = [
    DRAGON_RED + r"""
                 _.-- ,.--.
               .'   .'    /
               | @      |'..--------._
             /     \._/            '.
             /  .-.-                 \
           (  /    \                  \
           \\      '.                 | #
            \\       \ -.           /
             :\       |   )._____.'  \
                      |   / \  |  \   )
                      |   |./' :__ \.-'
                      '--'
""" + RESET,

    DRAGON_RED + r"""
                 _.-- ,.--.
               .'   .'    /
               | @      |'..--------._
             /     \._/            '.
             /  .-.-                 \
           (  /    \                  \
           \\      '.                 | #
            \\       \ -.           _/
             :\       |   )._____.-'   \
               "      |   / \  |  \   )
                      |   |./' :__ \.-'
                      '--'
""" + RESET,

    DRAGON_RED + r"""
                 _.-- ,.--.
               .'   .'    /
               | @      |'..--------._
             /     \._/            '.
             /  .-.-                 \
           (  /    \                  \
           \\      '.                 | #
            \\       \ -.           /
             :\       |   )._____.'  \
                      |   / \  |  \   )
                      |   |./' :__ \.-'
                      '--'
""" + RESET
]

# Manual ASCII text with royal styling
text = MIDNIGHT_BLUE + r"""
  ██╗███╗   ███╗ █████╗ ███████╗███████╗██████╗ 
  ██║████╗ ████║██╔══██╗╚══███╔╝██╔════╝██╔══██╗
  ██║██╔████╔██║███████║ ███╔╝  █████╗  ██████╔╝
  ██║██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ██╔══██╗
  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗██║  ██║
  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                version 1.0
""" + RESET

# Menu display function
def display_menu():
    clear_screen()
    print("\n" + text)
    print(f"{MIDNIGHT_BLUE}  {'*' * 35}{RESET}")
    print(f"{MIDNIGHT_BLUE}  >>For Image,PDF Details<<{RESET}")
    print(f"{MIDNIGHT_BLUE}  What do you need? {RESET}")
    print(f"{MIDNIGHT_BLUE}  1. Image analyzer {RESET}")
    print(f"{MIDNIGHT_BLUE}  2. PDF analyzer{RESET}")
    print(f"{MIDNIGHT_BLUE}  3. video analyzer{RESET}")
    print(f"{MIDNIGHT_BLUE}  4. audio analyzer{RESET}")
    print(f"{MIDNIGHT_BLUE}  5. exit from tool{RESET}")
    print(f"{MIDNIGHT_BLUE}  {'*' * 35}{RESET}")
    print("\n")

# Main program loop
# The update check will happen before the first menu display
check_for_updates()

while True:
    display_menu()
    n = input("Enter your choice: ")

    if n == "1":
        print("Image analyzer tool launching.....")
        try:
            from handlers.image_handler import image_handler
            image_handler()
        except ImportError:
            print("Error: Could not import 'image_handler'. Make sure the 'handlers' directory and files are in the correct location.")
        input("\nPress Enter to return to main menu...")

    elif n == "2":
        print("PDF analyzer tool launching...")
        try:
            from handlers.pdf_handler import PDF_Handler
            pdf_path = input("Enter PDF file path: ")
            if pdf_path:
                handler = PDF_Handler(pdf_path)
                handler.analyze()
                handler.print_results()
            else:
                print("No PDF file selected.")
        except ImportError:
            print("Error: Could not import 'PDF_Handler'. Make sure the 'handlers' directory and files are in the correct location.")
        except Exception as e:
            print(f"An error occurred: {e}")
        input("\nPress Enter to return to main menu...")

    elif n == "3":
        print("Video analyzer tool launching...")
        try:
            from handlers.video_handler import video_handler
            video_handler()
        except ImportError:
            print("Error: Could not import 'video_handler'. Make sure the 'handlers' directory and files are in the correct location.")
        input("\nPress Enter to return to main menu...")

    elif n == "4":
        print("Audio analyzer tool launching...")
        try:
            from handlers.audio_handler import audio_handler
            audio_path = input("Enter audio file path: ")
            if audio_path:
                result = audio_handler(audio_path)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                print("No audio file selected.")
        except ImportError:
            print("Error: Could not import 'audio_handler'. Make sure the 'handlers' directory and files are in the correct location.")
        except Exception as e:
            print(f"An error occurred: {e}")
        input("\nPress Enter to return to main menu...")

    elif n == "5":
        print("Exited successfully, have a good day!")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
        time.sleep(1.5)
