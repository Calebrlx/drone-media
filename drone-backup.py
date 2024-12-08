import os
import shutil
from datetime import datetime
from tqdm import tqdm

# Paths and configurations
SD_CARD_PATH = "/mnt/DroneMedia/DCIM/DJI_001"
DESTINATION_PATH = os.path.expanduser("~/drone-media/")
TELEMETRY_FOLDER = os.path.join(DESTINATION_PATH, "telemetry")

# Ensure necessary folders exist
os.makedirs(TELEMETRY_FOLDER, exist_ok=True)

def copy_files():
    """Copy files from SD card to the appropriate folders."""
    # Create a new folder for today’s date
    date_folder_name = datetime.now().strftime("%m-%d-%y")
    date_folder_path = os.path.join(DESTINATION_PATH, date_folder_name)
    photos_folder = os.path.join(date_folder_path, "photos")
    os.makedirs(photos_folder, exist_ok=True)

    # Check if the SD card is mounted
    if not os.path.exists(SD_CARD_PATH):
        print("SD card not found. Make sure it is connected and mounted correctly.")
        return

    # Walk through SD card files and copy them
    for root, dirs, files in os.walk(SD_CARD_PATH):
        for file in tqdm(files, desc="Processing files", unit="file"):
            if file.startswith("._"):
                # Skip macOS metadata files
                print(f"Skipped macOS metadata file: {file}")
                continue
            
            file_path = os.path.join(root, file)
            if file.lower().endswith((".srt", ".lrt")):
                # Telemetry data
                shutil.copy(file_path, TELEMETRY_FOLDER)
                print(f"Copied telemetry file: {file}")
            elif file.lower().endswith((".dng", ".jpg")):
                # Photos
                shutil.copy(file_path, photos_folder)
                print(f"Copied photo file: {file}")
            elif file.lower().endswith(".mp4"):
                # Videos
                shutil.copy(file_path, date_folder_path)
                print(f"Copied video file: {file}")
            else:
                print(f"Skipped unsupported file: {file}")

def clear_sd_card():
    """Clear all data from the SD card after confirming it was copied."""
    if not os.path.exists(SD_CARD_PATH):
        print("SD card not found. Make sure it is connected and mounted correctly.")
        return

    for root, dirs, files in os.walk(SD_CARD_PATH):
        for file in tqdm(files, desc="Deleting files", unit="file"):
            if file.startswith("._"):
                # Skip macOS metadata files
                continue
            file_path = os.path.join(root, file)
            os.remove(file_path)
            print(f"Deleted file: {file_path}")
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            shutil.rmtree(dir_path)
            print(f"Deleted directory: {dir_path}")

def main():
    print("Starting file transfer...")
    copy_files()
    # Uncomment the following for post-transfer cleanup
    # print("File transfer complete. Verifying before clearing SD card...")
    # confirmation = input("Do you want to clear the SD card? (yes/no): ").strip().lower()
    # if confirmation == "yes":
    #     clear_sd_card()
    #     print("SD card cleared.")
    # else:
    #     print("SD card not cleared.")

if __name__ == "__main__":
    main()


# import os
# import shutil
# from datetime import datetime

# # Paths and configurations
# SD_CARD_PATH = "/mnt/DroneMedia/DCIM/DJI_001"
# DESTINATION_PATH = os.path.expanduser("~/drone-media/")
# TELEMETRY_FOLDER = os.path.join(DESTINATION_PATH, "telemetry")

# # Ensure necessary folders exist
# os.makedirs(TELEMETRY_FOLDER, exist_ok=True)

# def copy_files():
#     """Copy files from SD card to the appropriate folders."""
#     # Create a new folder for today’s date
#     date_folder_name = datetime.now().strftime("%m-%d-%y")
#     date_folder_path = os.path.join(DESTINATION_PATH, date_folder_name)
#     photos_folder = os.path.join(date_folder_path, "photos")
#     os.makedirs(photos_folder, exist_ok=True)

#     # Check if the SD card is mounted
#     if not os.path.exists(SD_CARD_PATH):
#         print("SD card not found. Make sure it is connected and mounted correctly.")
#         return

#     # Walk through SD card files and copy them
#     for root, dirs, files in os.walk(SD_CARD_PATH):
#         for file in files:
#             file_path = os.path.join(root, file)
#             if file.lower().endswith((".srt", ".lrt")):
#                 # Telemetry data
#                 shutil.copy(file_path, TELEMETRY_FOLDER)
#                 print(f"Copied telemetry file: {file}")
#             elif file.lower().endswith((".dng", ".jpg")):
#                 # Photos
#                 shutil.copy(file_path, photos_folder)
#                 print(f"Copied photo file: {file}")
#             elif file.lower().endswith(".mp4"):
#                 # Videos
#                 shutil.copy(file_path, date_folder_path)
#                 print(f"Copied video file: {file}")
#             else:
#                 print(f"Skipped unsupported file: {file}")

# def clear_sd_card():
#     """Clear all data from the SD card after confirming it was copied."""
#     if not os.path.exists(SD_CARD_PATH):
#         print("SD card not found. Make sure it is connected and mounted correctly.")
#         return

#     for root, dirs, files in os.walk(SD_CARD_PATH):
#         for file in files:
#             file_path = os.path.join(root, file)
#             os.remove(file_path)
#             print(f"Deleted file: {file_path}")
#         for dir in dirs:
#             dir_path = os.path.join(root, dir)
#             shutil.rmtree(dir_path)
#             print(f"Deleted directory: {dir_path}")

# def main():
#     print("Starting file transfer...")
#     copy_files()
#     # print("File transfer complete. Verifying before clearing SD card...")

#     ## Verify SD card is safe to clear (implement checksum comparisons)
#     # confirmation = input("Do you want to clear the SD card? (yes/no): ").strip().lower()
#     # if confirmation == "yes":
#     #     clear_sd_card()
#     #     print("SD card cleared.")
#     # else:
#     #     print("SD card not cleared.")

# if __name__ == "__main__":
#     main()
