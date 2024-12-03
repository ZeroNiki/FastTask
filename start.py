# TODO ERROR: fix this shit

import sys
import time
import subprocess
import asyncio
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from src.bot.main import stop_bot

class ScriptReloader(FileSystemEventHandler):
    def __init__(self, script_name):
        self.script_name = script_name
        self.process = None

    async def restart_process(self):
        if self.process:
            print("Terminating current process...")
            self.process.terminate()
            self.process.wait()
            await stop_bot()

        print("Starting...")
        self.process = subprocess.Popen([sys.executable, self.script_name])

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"{self.script_name} has been modified. Restarting...")
            asyncio.run(self.restart_process())


if __name__ == "__main__":
    name = "create.py"
    event_handler = ScriptReloader(name)

    observers = Observer()

    observers.schedule(event_handler, "src/bot", recursive=True)
    observers.schedule(event_handler, "src/api", recursive=True)

    observers.start()


    print("Watching...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observers.stop()

    observers.join()
