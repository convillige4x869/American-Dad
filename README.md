# American Dad Intro Loop

A minimal 4:3 Pygame window that plays the supplied video and streams its audio
continuously on loop. It also includes a Floor Clip practice mode using the
provided bedroom and dinner frames.

## Run it

From this folder:

```powershell
python -m pip install -r requirements.txt
python american_dad_speedrun.py
```

The player reads the MP4 directly from your Pictures folder using PyAV and
renders each frame in Pygame. Choose Floor Clip from the menu, then hold Space
to alternate the two bedroom frames automatically. Build enough speed
to trigger the dinner-frame teleport. The same glitch is hidden in Play Intro:
when the bedroom moment arrives, spam Space on rhythm to jump ahead to the
dinner scene. Each floor frame also triggers its matching short audio slice,
creating the stutter/glitch effect. Press Enter to restart and Escape to return
to the menu. The newspaper skip works the same way later in the intro: Space
cycles frames 479–481 and enough speed cuts to frame 560.
