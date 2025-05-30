# imazer_logo.py

import time
import sys
import os

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
               .'   .'     /
               | @       |'..--------._
              /      \._/              '.
             /  .-.-                     \
            (  /    \                     \
            \\      '.                  | #
             \\       \   -.           /
              :\       |    )._____.'   \
                       |   /  \  |  \    )
                       |   |./'  :__ \.-'
                       '--'
""" + RESET,

    DRAGON_RED + r"""
                 _.-- ,.--.
               .'   .'     /
               | @       |'..--------._
              /      \._/              '.
             /  .-.-                     \
            (  /    \                     \
            \\      '.                  | #
             \\       \   -.           _/
              :\       |    )._____.-'   \
               "       |   /  \  |  \    )
                       |   |./'  :__ \.-'
                       '--'
""" + RESET,

    DRAGON_RED + r"""
                 _.-- ,.--.
               .'   .'     /
               | @       |'..--------._
              /      \._/              '.
             /  .-.-                     \
            (  /    \                     \
            \\      '.                  | #
             \\       \   -.           /
              :\       |    )._____.'   \
                       |   /  \  |  \    )
                       |   |./'  :__ \.-'
                       '--'
""" + RESET
]

# Animate the elephant
for _ in range(3):  # Repeat animation 3 times
    for frame in frames:
        sys.stdout.write("\033[H\033[J")  # Clear screen
        print("\n" + frame)
        time.sleep(0.2)

# Manual ASCII text with royal styling
text = MIDNIGHT_BLUE + r"""
  ██╗███╗   ███╗ █████╗ ███████╗███████╗██████╗ 
  ██║████╗ ████║██╔══██╗╚══███╔╝██╔════╝██╔══██╗
  ██║██╔████╔██║███████║  ███╔╝ █████╗  ██████╔╝
  ██║██║╚██╔╝██║██╔══██║ ███╔╝  ██╔══╝  ██╔══██╗
  ██║██║ ╚═╝ ██║██║  ██║███████╗███████╗██║  ██║
  ╚═╝╚═╝     ╚═╝╚═╝  ╚═╝╚══════╝╚══════╝╚═╝  ╚═╝
                                                 version 1.0.0 
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
while True:
    display_menu()
    n = input("Enter your choice: ")

    if n == "1":
        print("Image analyzer tool launching.....")
        from handlers.image_handler import image_handler
        image_handler()
        input("\nPress Enter to return to main menu...")

    elif n == "2":
        print("PDF analyzer tool launching...")
        from handlers.pdf_handler import PDF_Handler
        pdf_path = input("Enter PDF file path: ")
        if pdf_path:
            handler = PDF_Handler(pdf_path)
            handler.analyze()
            handler.print_results()
        else:
            print("No PDF file selected.")
        input("\nPress Enter to return to main menu...")

    elif n == "3":
        print("Video analyzer tool launching...")
        from handlers.video_handler import video_handler
        video_handler()
        input("\nPress Enter to return to main menu...")

    elif n == "4":
        print("Audio analyzer tool launching...")
        from handlers.audio_handler import audio_handler
        audio_path = input("Enter audio file path: ")
        if audio_path:
            result = audio_handler(audio_path)
            import json
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print("No audio file selected.")
        input("\nPress Enter to return to main menu...")

    elif n == "5":
        print("Exited successfully, have a good day!")
        break

    else:
        print("Invalid choice. Please enter a number from 1 to 5.")
        time.sleep(1.5)

