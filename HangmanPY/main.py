from src.hangman import main_menu, print_help
import sys

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] in ("--help", "-h"):
        print_help()
        sys.exit(0)

    main_menu()
