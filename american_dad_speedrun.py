"""Play the American Dad intro continuously in a Pygame window."""
from pathlib import Path
import sys

import av
import numpy as np
import pygame


ROOT = Path(getattr(sys, "_MEIPASS", Path(__file__).parent))
VIDEO = ROOT / "American Dad Intro - For Speedruns.mp4"
WINDOW_SIZE = (800, 600)  # 4:3
ASSETS = ROOT / "assets"


def load_audio_bytes() -> bytes:
    container = av.open(str(VIDEO))
    stream = container.streams.audio[0]
    resampler = av.audio.resampler.AudioResampler(format="s16", layout="stereo", rate=44100)
    audio = bytearray()
    try:
        for frame in container.decode(stream):
            for converted in resampler.resample(frame):
                audio.extend(converted.to_ndarray().tobytes())
        for converted in resampler.resample(None):
            audio.extend(converted.to_ndarray().tobytes())
    finally:
        container.close()
    return bytes(audio)


def make_keyboard_click() -> pygame.mixer.Sound:
    """Create a tiny mechanical key-click without needing an extra asset file."""
    rate = 44100
    length = int(rate * 0.012)
    time = np.arange(length, dtype=np.float32) / rate
    tone = np.sin(2 * np.pi * 1450 * time) * np.exp(-time * 300)
    noise = np.random.default_rng(7).normal(0, 0.18, length) * np.exp(-time * 420)
    sample = np.clip((tone * 0.38 + noise) * 32767, -32768, 32767).astype(np.int16)
    stereo = np.column_stack((sample, sample)).ravel()
    return pygame.mixer.Sound(buffer=stereo.tobytes())


def fit_image(screen: pygame.Surface, image: pygame.Surface) -> None:
    scale = min(screen.get_width() / image.get_width(), screen.get_height() / image.get_height())
    size = (int(image.get_width() * scale), int(image.get_height() * scale))
    image = pygame.transform.smoothscale(image, size)
    screen.fill((0, 0, 0))
    screen.blit(image, image.get_rect(center=screen.get_rect().center))


def floor_clip(screen: pygame.Surface, clock: pygame.time.Clock) -> None:
    frames = [
        pygame.image.load(ASSETS / "floor_clip_82.png").convert(),
        pygame.image.load(ASSETS / "floor_clip_83.png").convert(),
    ]
    success = pygame.image.load(ASSETS / "floor_clip_success.png").convert()
    frame_index = 0
    speed = 0.0
    last_press = -1.0
    clipped = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return
                if event.key == pygame.K_RETURN:
                    frame_index = 0
                    speed = 0.0
                    last_press = -1.0
                    clipped = False
                if event.key == pygame.K_SPACE and not clipped:
                    now = pygame.time.get_ticks() / 1000
                    gap = now - last_press
                    if 0.045 <= gap <= 0.24:
                        speed += 1.0
                    else:
                        speed = max(0.0, speed - 1.5)
                    last_press = now
                    frame_index = 1 - frame_index
                    if speed >= 18:
                        clipped = True

        fit_image(screen, success if clipped else frames[frame_index])
        pygame.display.flip()
        clock.tick(60)


def main() -> None:
    pygame.mixer.pre_init(44100, -16, 2, 1024)
    pygame.init()
    screen = pygame.display.set_mode(WINDOW_SIZE, pygame.SCALED)
    pygame.display.set_caption("American Dad Intro")
    clock = pygame.time.Clock()
    title_font = pygame.font.Font(None, 64)
    button_font = pygame.font.Font(None, 34)
    play_button = pygame.Rect(250, 315, 300, 58)
    quit_button = pygame.Rect(250, 465, 300, 58)
    playing = False
    finished = False
    run_start = None
    final_time = 0.0
    timer_font = pygame.font.Font(None, 30)
    audio = None
    keyboard_click = make_keyboard_click()
    audio_data = b""
    bytes_per_second = 44100 * 2 * 2
    floor_audio = []
    newspaper_audio = []
    family_audio = []
    floor_frames = [
        pygame.image.load(ASSETS / "floor_clip_82.png").convert(),
        pygame.image.load(ASSETS / "floor_clip_83.png").convert(),
    ]
    newspaper_frames = [
        pygame.image.load(ASSETS / "newspaper_479.png").convert(),
        pygame.image.load(ASSETS / "newspaper_480.png").convert(),
        pygame.image.load(ASSETS / "newspaper_481.png").convert(),
    ]
    family_frames = [
        pygame.image.load(ASSETS / "family_287.png").convert(),
        pygame.image.load(ASSETS / "family_288.png").convert(),
        pygame.image.load(ASSETS / "family_289.png").convert(),
    ]
    car_frames = [
        pygame.image.load(ASSETS / "car_640.png").convert(),
        pygame.image.load(ASSETS / "car_641.png").convert(),
        pygame.image.load(ASSETS / "car_642.png").convert(),
    ]
    video_start = 0.0
    clip_speed = 0.0
    last_space = -1.0
    clip_used = False
    just_jumped = False
    restart_requested = False
    floor_active = False
    floor_frame = 0
    newspaper_active = False
    newspaper_frame = 0
    newspaper_speed = 0.0
    last_newspaper = -1.0
    newspaper_used = False
    family_active = False
    family_frame = 0
    family_speed = 0.0
    last_family = -1.0
    family_used = False
    car_active = False
    car_frame = 0
    car_speed = 0.0
    last_car = -1.0
    car_used = False

    while True:
        if not playing:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    playing = True
                    finished = False
                    final_time = 0.0
                    run_start = pygame.time.get_ticks() / 1000
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if play_button.collidepoint(event.pos):
                        playing = True
                        finished = False
                        final_time = 0.0
                        run_start = pygame.time.get_ticks() / 1000
                    elif quit_button.collidepoint(event.pos):
                        pygame.quit()
                        return

            screen.fill((19, 38, 69))
            pygame.draw.rect(screen, (44, 91, 145), (0, 0, 800, 245))
            pygame.draw.circle(screen, (248, 198, 69), (400, 178), 92)
            subtitle = button_font.render("INTRO PLAYER", True, (248, 198, 69))
            screen.blit(subtitle, subtitle.get_rect(center=(400, 160)))
            if finished:
                result = button_font.render(f"FINISHED TIME  {final_time:06.2f}", True, (255, 255, 255))
                screen.blit(result, result.get_rect(center=(400, 235)))
            menu_title = "RUN COMPLETE" if finished else "AMERICAN DAD"
            menu_action = "RESTART RUN" if finished else "START RUN"
            title = title_font.render(menu_title, True, (255, 255, 255))
            screen.blit(title, title.get_rect(center=(400, 100)))
            for button, label in ((play_button, menu_action), (quit_button, "QUIT")):
                pygame.draw.rect(screen, (238, 176, 52), button, border_radius=8)
                text = button_font.render(label, True, (19, 38, 69))
                screen.blit(text, text.get_rect(center=button.center))
            pygame.display.flip()
            clock.tick(60)
            if not playing:
                continue

            audio_data = load_audio_bytes()
            audio = pygame.mixer.Sound(buffer=audio_data)
            floor_audio = [
                pygame.mixer.Sound(buffer=audio_data[int(2.70 * bytes_per_second):int(2.84 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(2.73 * bytes_per_second):int(2.87 * bytes_per_second)]),
            ]
            newspaper_audio = [
                pygame.mixer.Sound(buffer=audio_data[int(15.96 * bytes_per_second):int(16.10 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(15.99 * bytes_per_second):int(16.13 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(16.02 * bytes_per_second):int(16.16 * bytes_per_second)]),
            ]
            family_audio = [
                pygame.mixer.Sound(buffer=audio_data[int(9.56 * bytes_per_second):int(9.70 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(9.59 * bytes_per_second):int(9.73 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(9.62 * bytes_per_second):int(9.76 * bytes_per_second)]),
            ]
            car_audio = [
                pygame.mixer.Sound(buffer=audio_data[int(21.33 * bytes_per_second):int(21.47 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(21.36 * bytes_per_second):int(21.50 * bytes_per_second)]),
                pygame.mixer.Sound(buffer=audio_data[int(21.39 * bytes_per_second):int(21.53 * bytes_per_second)]),
            ]
            audio.play(loops=-1)

        container = av.open(str(VIDEO))
        stream = container.streams.video[0]
        stream.thread_type = "AUTO"
        fps = float(stream.average_rate) if stream.average_rate else 30.0
        if video_start:
            container.seek(int(video_start / float(stream.time_base)), stream=stream, backward=True)

        try:
            for frame in container.decode(stream):
                frame_time = float(frame.pts * frame.time_base) if frame.pts is not None else 0.0
                if video_start and frame_time < video_start:
                    continue
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        container.close()
                        pygame.mixer.stop()
                        pygame.quit()
                        return
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                        run_start = pygame.time.get_ticks() / 1000
                        video_start = 0.0
                        clip_speed = 0.0
                        last_space = -1.0
                        clip_used = False
                        floor_active = False
                        floor_frame = 0
                        newspaper_active = False
                        newspaper_frame = 0
                        newspaper_speed = 0.0
                        last_newspaper = -1.0
                        newspaper_used = False
                        family_active = False
                        family_frame = 0
                        family_speed = 0.0
                        last_family = -1.0
                        family_used = False
                        car_active = False
                        car_frame = 0
                        car_speed = 0.0
                        last_car = -1.0
                        car_used = False
                        restart_requested = True
                        break
                now = pygame.time.get_ticks() / 1000
                holding_space = pygame.key.get_pressed()[pygame.K_SPACE]
                floor_window = 82 / fps
                floor_input_ready = floor_window <= frame_time <= floor_window + 0.20
                if holding_space and not clip_used and (floor_active or floor_input_ready) and now - last_space >= 0.01:
                    if not floor_active:
                        audio.stop()
                    floor_active = True
                    floor_frame = 1 - floor_frame
                    floor_audio[floor_frame].play()
                    keyboard_click.play()
                    clip_speed += 1.0
                    last_space = now
                    if clip_speed >= 12:
                        video_start = 9.3
                        clip_used = True
                        just_jumped = True
                        audio.stop()
                        audio = pygame.mixer.Sound(buffer=audio_data[int(9.3 * bytes_per_second):])
                        audio.play(loops=-1)
                elif holding_space and not newspaper_used and 15.4 <= frame_time <= 17.2 and now - last_newspaper >= 0.01:
                    if not newspaper_active:
                        audio.stop()
                    newspaper_active = True
                    newspaper_frame = (newspaper_frame + 1) % 3
                    newspaper_audio[newspaper_frame].play()
                    keyboard_click.play()
                    newspaper_speed += 1.0
                    last_newspaper = now
                    if newspaper_speed >= 10:
                        video_start = 18.67
                        newspaper_used = True
                        just_jumped = True
                        audio.stop()
                        audio = pygame.mixer.Sound(buffer=audio_data[int(18.67 * bytes_per_second):])
                        audio.play(loops=-1)
                elif holding_space and not family_used and 9.45 <= frame_time <= 10.15 and now - last_family >= 0.01:
                    if not family_active:
                        audio.stop()
                    family_active = True
                    family_frame = (family_frame + 1) % 3
                    family_audio[family_frame].play()
                    keyboard_click.play()
                    family_speed += 1.0
                    last_family = now
                    if family_speed >= 10:
                        video_start = 12.27
                        family_used = True
                        just_jumped = True
                        audio.stop()
                        audio = pygame.mixer.Sound(buffer=audio_data[int(12.27 * bytes_per_second):])
                        audio.play(loops=-1)
                elif holding_space and not car_used and 21.20 <= frame_time <= 21.85 and now - last_car >= 0.01:
                    if not car_active:
                        audio.stop()
                    car_active = True
                    car_frame = (car_frame + 1) % 3
                    car_audio[car_frame].play()
                    keyboard_click.play()
                    car_speed += 1.0
                    last_car = now
                    if car_speed >= 10:
                        video_start = 25.63
                        car_used = True
                        just_jumped = True
                        audio.stop()
                        audio = pygame.mixer.Sound(buffer=audio_data[int(25.63 * bytes_per_second):])
                        audio.play(loops=-1)
                if just_jumped or restart_requested:
                    break

                pixels = frame.to_ndarray(format="rgb24")
                image = pygame.surfarray.make_surface(np.swapaxes(pixels, 0, 1))
                if floor_active and not clip_used:
                    display_image = floor_frames[floor_frame]
                elif newspaper_active and not newspaper_used:
                    display_image = newspaper_frames[newspaper_frame]
                elif family_active and not family_used:
                    display_image = family_frames[family_frame]
                elif car_active and not car_used:
                    display_image = car_frames[car_frame]
                else:
                    display_image = image
                fit_image(screen, display_image)
                elapsed = pygame.time.get_ticks() / 1000 - (run_start or pygame.time.get_ticks() / 1000)
                timer = timer_font.render(f"TIME  {elapsed:06.2f}", True, (255, 255, 255))
                shadow = timer_font.render(f"TIME  {elapsed:06.2f}", True, (0, 0, 0))
                screen.blit(shadow, (17, 17))
                screen.blit(timer, (15, 15))
                pygame.display.flip()
                clock.tick(fps)
        finally:
            container.close()
        if restart_requested:
            restart_requested = False
            if audio is not None:
                audio.stop()
                audio = pygame.mixer.Sound(buffer=audio_data)
                audio.play(loops=-1)
            continue
        if not just_jumped:
            final_time = pygame.time.get_ticks() / 1000 - (run_start or pygame.time.get_ticks() / 1000)
            if audio is not None:
                audio.stop()
            playing = False
            finished = True
            video_start = 0.0
            clip_speed = 0.0
            last_space = -1.0
            clip_used = False
            floor_active = False
            floor_frame = 0
            newspaper_active = False
            newspaper_frame = 0
            newspaper_speed = 0.0
            last_newspaper = -1.0
            newspaper_used = False
            family_active = False
            family_frame = 0
            family_speed = 0.0
            last_family = -1.0
            family_used = False
            car_active = False
            car_frame = 0
            car_speed = 0.0
            last_car = -1.0
            car_used = False
        else:
            just_jumped = False



if __name__ == "__main__":
    main()
