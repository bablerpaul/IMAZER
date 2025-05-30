# FORENSIC TOOL FOR METADATA EXTRACTION
<div align="center">

  <h1>
    <img src="https://img.shields.io/badge/IMAZER-Forensic_Tool-blue?style=for-the-badge&logo=icloud&logoColor=white" alt="IMAZER">
  </h1>

  <img src="https://media.giphy.com/media/rn79UlSTDfDlS/giphy.gif" width="500" alt="Data extraction visualization">

  <h3>
    <img src="https://img.shields.io/badge/JUST_LIKE_THE_BURST!-FF6B6B?style=flat-square&logo=starship&logoColor=white" alt="Tagline">
  </h3>
</div>

## Description
A Python tool to extract metadata from video/image files and save it to JSON format. Supports common formats (MP4, MOV, AVI, JPEG, PNG, etc.) using FFmpeg and ExifTool.

## System Requirements
- **Python**: 3.7+
- **System Dependencies**:
  - `FFmpeg` (for video processing)
  - `Tkinter` (for GUI file dialogs)
  - `exiftool` (for image metadata)

## Installation

### 1. Install System Dependencies
#### Windows
- Download FFmpeg: [ffmpeg.org/download.html](https://ffmpeg.org/download.html)  
  *(Add to PATH during installation)*

#### macOS
```bash
brew install ffmpeg
```

#### Linux (Debian/Ubuntu)
```bash
sudo apt update
sudo apt install ffmpeg python3-tk libimage-exiftool-perl
```

### 2. Install Python Dependencies
```bash
# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/macOS
venv\Scripts\activate    # Windows

# Install packages
pip install -r requirements.txt
```

## Usage
```bash
python metadata_extractor.py
```
1. Select a file using the graphical dialog
2. JSON output will be saved in the same directory as `[filename]_metadata.json`

## Python Requirements
The `requirements.txt` contains:
```
ffmpeg-python==0.2.0
pymediainfo==9.1.0
```

## Troubleshooting
**"FFmpeg not found" errors**  
Verify FFmpeg is in your system PATH:
```bash
ffmpeg -version
```
Reinstall FFmpeg following official guidelines

**Tkinter Issues (Linux)**  
If you see `_tkinter.TclError`:
```bash
sudo apt install python3-tk  # Debian/Ubuntu
```

**Alternative File Dialog (Linux Headless)**  
If Tkinter is unavailable:
```bash
sudo apt install qarma    # Preferred Qt-based
# OR
sudo apt install zenity  # GTK-based
```



## License
MIT
