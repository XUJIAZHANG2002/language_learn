from pynput import mouse

class MouseTracker:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.running = True

    def on_move(self, x, y):
        self.x = x
        self.y = y

    def on_click(self, x, y, button, pressed):
        if not pressed and button == mouse.Button.right:
            self.running = False
            return False

    def start(self):
        listener = mouse.Listener(
            on_move=self.on_move,
            on_click=self.on_click
        )
        listener.start()
        return listener
