import os
import requests
from tqdm import tqdm
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from dotenv import load_dotenv

# Load secrets from .env file
load_dotenv()
FRAMEIO_API_TOKEN = os.getenv("FRAMEIO_API_TOKEN")
FRAMEIO_PROJECT_ID = "44ec8d36-1e54-4f3c-a3dd-ba48a6f3539d"  # From the URL
FRAMEIO_FOLDER_ID = "1274fa0b-2bc7-48ad-94ba-eeb55833cc78"    # From the URL

# Verify secrets
if not FRAMEIO_API_TOKEN:
    raise ValueError("Missing FRAMEIO_API_TOKEN in .env file.")

# Console for TUI
console = Console()

# Headers for API requests
HEADERS = {
    "Authorization": f"Bearer {FRAMEIO_API_TOKEN}",
    "Content-Type": "application/json"
}

def list_videos(folder):
    """List all videos in a given folder."""
    videos = []
    for root, dirs, files in os.walk(folder):
        for file in files:
            if file.lower().endswith(".mp4"):
                videos.append(os.path.join(root, file))
    return videos

def get_upload_url(filename):
    """Get a Frame.io upload URL for the video."""
    url = f"https://api.frame.io/v2/assets/{FRAMEIO_FOLDER_ID}/children"
    payload = {
        "name": filename,
        "type": "file"
    }
    response = requests.post(url, headers=HEADERS, json=payload)
    if response.status_code != 201:  # 201 Created
        console.print(f"[red]Failed to create asset: {response.status_code} {response.text}[/red]")
        raise Exception(f"Failed to create asset: {response.text}")
    return response.json()["upload_url"]

def upload_video(upload_url, file_path):
    """Upload the video to Frame.io using the provided URL."""
    file_size = os.path.getsize(file_path)
    headers = {
        "Content-Length": str(file_size),
        "Content-Type": "application/octet-stream"
    }

    with open(file_path, "rb") as file, tqdm(
        total=file_size, unit="B", unit_scale=True, desc=f"Uploading {os.path.basename(file_path)}"
    ) as progress_bar:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            progress_bar.update(len(chunk))
            response = requests.put(upload_url, headers=headers, data=chunk)
            if not response.ok:
                console.print(f"[red]Upload failed: {response.status_code} {response.text}[/red]")
                response.raise_for_status()

def main():
    console.clear()
    console.print("[bold blue]Welcome to Frame.io Uploader[/bold blue]\n")

    # Prompt for the folder to upload videos from
    folder = Prompt.ask("[green]Enter the folder containing videos to upload[/green]", default="~/drone-media")
    folder = os.path.expanduser(folder)

    # List videos
    videos = list_videos(folder)
    if not videos:
        console.print("[red]No videos found in the specified folder.[/red]")
        return

    # Show a table of videos
    table = Table(title="Videos to Upload")
    table.add_column("Index", justify="right")
    table.add_column("Filename", justify="left")
    for idx, video in enumerate(videos):
        table.add_row(str(idx + 1), os.path.basename(video))
    console.print(table)

    # Confirm upload
    confirm = Prompt.ask("[yellow]Do you want to upload these videos to Frame.io?[/yellow] (yes/no)", choices=["yes", "no"], default="no")
    if confirm != "yes":
        console.print("[red]Upload canceled.[/red]")
        return

    # Upload videos
    for video in videos:
        console.print(f"[cyan]Preparing to upload:[/cyan] {os.path.basename(video)}")
        try:
            upload_url = get_upload_url(os.path.basename(video))
            upload_video(upload_url, video)
            console.print(f"[green]Successfully uploaded:[/green] {os.path.basename(video)}")
        except Exception as e:
            console.print(f"[red]Failed to upload {os.path.basename(video)}: {e}[/red]")

    console.print("[bold green]All uploads complete![/bold green]")

if __name__ == "__main__":
    main()