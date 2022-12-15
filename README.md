# AudioTool

This tool is used for recording the sound from the default output of the computer. The motivation for this project was to capture samples/audio faster and to get rid of the naming/file management involved with some of the existing tools I used before. The main purpose for me to use this is to run the recordings through [Demucs](https://github.com/facebookresearch/demucs). Currently only Windows is supported.

## How to use

1. Clone the repo and open CMD in the folder.
2. To begin recording run `python recorder.py`
3. To stop recording hit the `q` button on your keyboard.
4. The recording is now saved as `recording.wav`
5. If you have Demucs correctly installed, you can separate the audiotrack to different instruments by running `demucs recording.wav`

Check Demucs docs for useful flags if you want different ouput formats or sample rates.

## Disclaimer

I do not take any responsibility for how this piece of software is used.