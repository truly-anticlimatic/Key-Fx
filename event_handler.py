import keyboard
from pygame import mixer
import config

keyboard_events = {" "}  # Empty list of events
press_sfx = None
release_sfx = None  # Set the sound effect path to none
hook = None  # Set the hook to none

mixer.init()  # Initiate the mixer


def cycle_events(event):
    keyboard_events.pop()
    keyboard_events.add(
        str(event)
    )  # Cycle by adding the event and popping one random event


def handle_event(event):
    global press_sfx, release_sfx
    # This function triggers whenever a key is pressed/released and if the event wasn't already registered

    if (
        not press_sfx or not release_sfx
    ):  # If there isn't any value in one of these two, skip
        return None

    press_sfx.set_volume(config.volume)
    release_sfx.set_volume(
        config.volume
    )  # Set the volume to config.volume each time this is called

    if event.event_type == "down":
        if str(event) in keyboard_events:  # If it was already done, pass
            pass
        else:
            press_sfx.play()
            cycle_events(event)  # Play sound and cycle

    elif event.event_type == "up":
        if (
            str(event) in keyboard_events and mixer.get_busy()
        ):  # If a sound is playing, skip
            pass
        else:
            release_sfx.play()
            cycle_events(event)  # Play sound and cycle


def run(category: str, soundpack: str):
    global hook, press_sfx, release_sfx

    if config.is_running:
        return None  # If the thread is running, exit

    try:
        press_path = config.keyboard_sounds[category][soundpack][0]
        release_path = config.keyboard_sounds[category][soundpack][1]
        # Load the sound paths into a variable since putting it into the sound class will be permanent

        press_sfx = mixer.Sound(press_path)
        release_sfx = mixer.Sound(release_path)

        config.is_running = True  # Set running to true

    except (KeyError, IndexError):
        print(
            f"{soundpack} from {category} could not be found"
        )  # If it couldn't find the sound, pass

    hook = keyboard.hook(lambda event: handle_event(event))  # Hook the hook


def deactivate():
    global hook, press_sfx, release_sfx

    config.is_running = False  # Set the thread flag to false

    if hook is not None:  # If the hook is something other than none...
        keyboard.unhook(hook)
        hook = None  # Unhook and set to none

    press_sfx = None
    release_sfx = None


if __name__ == "__main__":
    run("Switches", "Cherry MX Blue")
    keyboard.wait()
