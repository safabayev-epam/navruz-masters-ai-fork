# Audio Processing and Transcription

This project extracts a specific segment from an MP3 file and transcribes its content into text using OpenAI's Whisper API.

## Features
- Cuts a specific portion of an audio file (e.g., 2 minutes).
- Transcribes the extracted audio segment into text.
- Saves the transcription in a text file.

## Requirements
1. Python 3.7 or later
2. FFmpeg installed and added to your system PATH
3. The following Python packages:
   - `pydub`
   - `whisper`
   - `torch`

## Installation

### Step 1: Clone the Repository
```bash
# Clone the repository (if applicable)
git clone https://github.com/your-repo/audio-transcription.git
cd audio-transcription
```

### Step 2: Install Dependencies
Install the required Python packages:
```bash
pip install pydub whisper torch torchvision torchaudio
```

Install FFmpeg (required by `pydub`):
- **Ubuntu/Debian**:
  ```bash
  sudo apt install ffmpeg
  ```
- **MacOS**:
  ```bash
  brew install ffmpeg
  ```
- **Windows**:
  Download FFmpeg from [FFmpeg.org](https://ffmpeg.org/download.html) and add it to your system PATH.

### Step 3: Install CUDA (Optional for GPU Acceleration)
If you have an NVIDIA GPU, install CUDA and PyTorch with GPU support:
```bash
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```
Replace `cu118` with the version matching your installed CUDA Toolkit.

## Usage

### Step 1: Extract Audio Segment
The script extracts a 2-minute segment from an MP3 file:
1. Place your MP3 file in the same directory as the script.
2. Update the file name and time range in the script:
   ```python
   audio = AudioSegment.from_file("your_audio.mp3")
   start_time = 5 * 60 * 1000  # Start time in milliseconds (e.g., 5 minutes)
   end_time = start_time + (2 * 60 * 1000)  # Duration (2 minutes)
   ```
3. Run the script to save the extracted audio as `output_segment.mp3`.

### Step 2: Transcribe Audio
The script uses OpenAI's Whisper API to transcribe the audio:
1. Ensure `output_segment.mp3` exists in the same directory.
2. Run the transcription:
   ```bash
   python get_text_from_audio.py
   ```
3. The transcription is saved in `processed_audio_text.txt`.

## File Structure
```
project-directory/
├── get_text_from_audio.py   # Main script
├── your_audio.mp3           # Original audio file
├── output_segment.mp3       # Extracted audio segment
├── processed_audio_text.txt # Transcription output
└── README.md                # Documentation
```

## Notes
- For higher transcription accuracy, use the larger Whisper models (e.g., `medium`, `large`).
- GPU acceleration significantly speeds up transcription if CUDA is installed.

## License
This project is open-source and available under the MIT License.

## Contact
For questions or issues, feel free to reach out to [your_email@example.com].
