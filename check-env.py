from dotenv import load_dotenv
import os

load_dotenv()

print("FRAMEIO_API_TOKEN:", os.getenv("FRAMEIO_API_TOKEN"))
print("FRAMEIO_PROJECT_ID:", os.getenv("FRAMEIO_PROJECT_ID"))