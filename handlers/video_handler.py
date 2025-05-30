import os
from typing import Optional
from tkinter import Tk, filedialog
import ffmpeg

def select_video_file() -> Optional[str]:
    """Open a file dialog to select a video file."""
    Tk().withdraw()
    while True:
        file_path = filedialog.askopenfilename(
            title="Select Video File",
            filetypes=[("Video Files", "*.mp4 *.mkv *.avi *.mov *.flv"), ("All Files", "*.*")]
        )
        if not file_path:
            return None
        if os.path.isfile(file_path):
            return file_path
        print("Invalid file selection. Please try again.")

def extract_video_metadata(file_path: str):
    """Extract detailed metadata from a video file."""
    try:
        metadata = ffmpeg.probe(file_path)
        streams = metadata.get('streams', [])
        format_info = metadata.get('format', {})

        print("\n--- Format Information ---")
        for key, value in format_info.items():
            print(f"{key}: {value}")

        print("\n--- Streams Information ---")
        for i, stream in enumerate(streams):
            print(f"\nStream #{i}:")
            for key, value in stream.items():
                print(f"  {key}: {value}")

        return metadata

    except ffmpeg.Error as e:
        print(f"Error extracting metadata: {e.stderr.decode()}")
        return None

def video_handler():
    """This is the entry point your main.py will call."""
    file_path = select_video_file()
    if file_path:
        metadata = extract_video_metadata(file_path)
        if metadata:
            print("\nMetadata extraction completed successfully.")
        else:
            print("\nFailed to extract metadata.")
    else:
        print("\nNo video file selected.")
