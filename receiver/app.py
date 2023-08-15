from dotenv import load_dotenv

from api.v1.receiver import main

if __name__ == "__main__":
    load_dotenv()
    main()
