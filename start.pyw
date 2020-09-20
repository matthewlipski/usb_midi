import subprocess

# Path to virtual environment Python executable
python_bin = "venv/Scripts/python.exe"

# Path to script
script_file = "usb_midi.pyw"

# Running the script using selected Python executable
subprocess.Popen([python_bin, script_file])
