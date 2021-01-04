import logging
import os
import threading
import time

import dispatcher

LOGGER = logging.getLogger("robot-car-shutdown")

class ShutdownListener(object):
    def __init__(self):
        self.button_pressed_at = 0

        LOGGER.info("Registering shutdown button listener...")
        dispatcher.connect(
            lambda on: self.handle_button_pressed(on),
            signal="/button/green"
        )

        LOGGER.info("Starting shutdown thread...")
        self.thread = threading.Thread(
            target=lambda name: self.shutdown_listener(),
            args=(1,),
            daemon=True
        )

        self.thread.start()

    def handle_button_pressed(self, on):
        if on:
            dispatcher.send(signal="/led/white", on=False)
            self.button_pressed_at = time.time()
        else:
            dispatcher.send(signal="/led/white", on=True)
            self.button_pressed_at = 0

    def shutdown_listener(self):
        while True:
            now = time.time()
            if self.button_pressed_at != 0 and now - self.button_pressed_at > 5:
                LOGGER.info("Button pressed for %ds, intiating shutdown process...", now - self.button_pressed_at)
                try:
                    os.system("/usr/bin/sudo shutdown -h now")
                except Exception as err:
                    LOGGER.error(err)
                dispatcher.send(signal="/system/shutdown")
                break
            time.sleep(1)
