import mythic_container
import subprocess
import sys
import os
from telegram.c2_functions.telegram import *

# Start the Python Telegram server
try:
    # Change to the c2_code directory
    os.chdir("/Mythic/telegram/c2_code")
    
    # Install requirements if needed
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
    
    # Start the Telegram server in background
    server_process = subprocess.Popen([sys.executable, "server.py"])
    
    # Start Mythic container service
    mythic_container.mythic_service.start_and_run_forever()
    
except Exception as e:
    print(f"Error starting Telegram C2: {e}")
    sys.exit(1)
