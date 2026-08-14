# American Dad Intro Speedrun

A 4:3 Pygame speedrun built around the supplied American Dad intro. The game
plays the intro video with its extracted WAV soundtrack, tracks your run time,
and includes frame-accurate skip glitches.

## Run the Python version

From this folder:

```powershell
python -m pip install -r requirements.txt
python american_dad_speedrun.py
```

The original video and extracted audio must be present beside the script:

- `American Dad Intro - For Speedruns.mp4`
- `American Dad Intro Audio.wav`
- `assets/`

## Controls

- Start Run: begin from the menu
- Restart Run: restart after finishing
- Hold `Space`: activate and build each glitch
- `Enter`: restart the current run
- Close the window: quit

## Glitches

- Floor Skip: cycles frames 82–83 and jumps to about frame 279
- Family Skip: cycles frames 288–290 and jumps to frame 368
- Newspaper Skip: cycles frames 479–481 and jumps to frame 560
- Car Skip: cycles frames 619–620 and jumps to frame 784

Each glitch uses a tight timing window, frame cycling, speed buildup, and a
short keyboard-click effect. When a skip succeeds, the video and WAV soundtrack
seek to the destination point together.

## Windows executable

The compiled executable is available as a GitHub Release asset:

`dist/AmericanDadIntro.exe`

The executable bundles the video, WAV audio, and image assets, so Python is not
required to run it.
