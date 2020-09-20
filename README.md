# USB MIDI Tool
A lightweight, background tool which allows for connected MIDI devices to interact with each other over a USB
connection.

To get started, follow the instructions below:

1. Ensure you have the newest version of Python 3 installed on your computer.
2. Run start.pyw. No other installation is required but a config file will be generated the first time the tool is run.
Instructions on editing the config file are found below. Simply re-run start.pyw for your config changes to take effect.
3. Press ctrl+shift+f7 to show the program window and ctrl+shift+f8 to hide it.
4. Disconnected MIDI devices can simply be disabled, but new devices ones will require config.txt to be deleted and
generated again by running start.pyw.

###Editing config.txt:

**To disable a MIDI Device, add a '#' in front of its name:**  

E.g. `Arturia MicroLab 1 -> #Arturia MicroLab 1`.  

Remove the '#' to enable it again. Both actions require a restart of the program.

**Change the channel mode by setting 'mode' to either 0 or 1. The channel modes are:**

**0:** Your MIDI instruments should all be set to channel 1 and channel control is done by the USB MIDI tool software.  

**1:** Your MIDI instruments should each be set to their own channel and channel control is done by the USB MIDI protocol.
Change the MIDI channel of your MIDI controller to control each instrument with either mode.

**Do not edit config.txt in any other way!**
