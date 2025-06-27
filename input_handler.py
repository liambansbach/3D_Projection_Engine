class InputHandler:
    def __init__(self):
        self.held_keys = set()
        self.pressed_once = set()

    def key_press(self, key: str):
        if key not in self.held_keys:
            self.pressed_once.add(key)
        self.held_keys.add(key)

    def key_release(self, key: str):
        self.held_keys.discard(key)

    def is_held(self, key: str):
        return key in self.held_keys

    def was_pressed_once(self, key: str):
        return key in self.pressed_once

    def end_frame(self):
        self.pressed_once.clear()