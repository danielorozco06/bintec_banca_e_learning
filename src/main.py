"""
Main file for the project
"""
import os
from dotenv import load_dotenv

load_dotenv()


def main() -> None:
    """
    Main function
    """
    print(os.getenv("OPENAI_TOKEN"))


if __name__ == "__main__":
    main()
