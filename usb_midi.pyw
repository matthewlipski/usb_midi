import mido
import os
import pynput
import threading
import win32.lib.win32con as win32con
import win32gui


def setup_config():
    # Lists containing MIDI host/receiver ports
    inports = []
    outports = []

    # Adds each detected host/receiver to the appropriate list
    for name in mido.get_input_names():
        inports.append(mido.open_input(name))
    for name in mido.get_output_names():
        outports.append(mido.open_output(name))

    # Generates a new config.txt file and populates it
    config = open('config.txt', 'w')

    config.write('Connected MIDI Input Devices:\n')
    for inport in inports:
        config.write(inport.name + '\n')

    config.write('\nConnected Audio Output Devices:\n')
    for outport in outports:
        config.write(outport.name + '\n')

    config.write('\nChannel Mode = 0')
    config.close()

    return inports, outports, 0


def read_config():
    # Lists containing MIDI host/receiver ports
    inports = []
    outports = []

    # Adds each active host/receiver found in config.txt to the appropriate list
    config = open('config.txt', 'r')

    line = config.readline()

    while len(line) > 1:
        line = config.readline()
        line = line.rstrip('\n')
        if line in mido.get_input_names() and not line.startswith('#'):
            inports.append(mido.open_input(line))

    line = config.readline()
    while len(line) > 1:
        line = config.readline()
        line = line.rstrip('\n')
        if line in mido.get_output_names() and not line.startswith('#'):
            outports.append(mido.open_output(line))

    # Reads the channel mode from config.txt
    line = config.readline()
    line = line.rstrip('\n')
    mode = int(line[len(line) - 1: len(line)])

    return inports, outports, mode


def process_midi(inport):
    while True:
        # Blocks until a MIDI message is received
        msg = inport.receive()
        print(inport.name, ':', msg)

        # Filters out tempo sync messages which only have a 'time' attribute
        if hasattr(msg, 'channel'):
            channel = msg.channel

            # Sends MIDI message to the appropriate device
            if channel < len(outports) and mode == 0:
                msg.channel = 0
                outports[channel].send(msg)
            else:
                for port in outports:
                    port.send(msg)


def on_press(key):
    if key in show_keys and key not in current_show:
        current_show.append(key)
        if len(show_keys) == len(current_show):
            win32gui.ShowWindow(the_program_to_hide, win32con.SW_SHOW)

    if key in hide_keys and key not in current_hide:
        current_hide.append(key)
        if len(show_keys) == len(current_hide):
            win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)


def on_release(key):
    if key in current_show:
        current_show.remove(key)

    if key in current_hide:
        current_hide.remove(key)


if __name__ == '__main__':
    mido.set_backend('mido.backends.rtmidi/WINDOWS_MM')
    threads = []

    # Checks if config.txt exists, reads it or generates it
    if not os.path.isfile('config.txt'):
        inports, outports, mode = setup_config()
    else:
        inports, outports, mode = read_config()

    print('Active MIDI Input Devices:')
    for inport in inports:
        print(inport.name)
    print()

    print('Active Audio Output Devices:')
    for outport in outports:
        print(outport.name)
    print()

    if len(inports) == 0:
        print('No active MIDI devices found!')
        while True:
            continue

    # Assigns a thread to each MIDI input device so they don't block each other
    for i in range(len(inports)):
        thread = threading.Thread(target=process_midi, args=(inports[i],))
        threads.append(thread)
        threads[i].start()

    # Hides the console window
    the_program_to_hide = win32gui.GetForegroundWindow()
    #win32gui.ShowWindow(the_program_to_hide, win32con.SW_HIDE)

    # Key combination to show window
    show_keys = [pynput.keyboard.Key.ctrl_l, pynput.keyboard.Key.shift_l, pynput.keyboard.Key.f7]
    hide_keys = [pynput.keyboard.Key.ctrl_l, pynput.keyboard.Key.shift_l, pynput.keyboard.Key.f8]
    current_show = []
    current_hide = []

    # Listens for key combination in main thread
    with pynput.keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()
