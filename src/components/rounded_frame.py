import tkinter as tk

class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg_color, width=0, height=0, radius=25, **kwargs):
        tk.Canvas.__init__(self, parent, bd=0, highlightthickness=0, bg=parent["bg"])
        self._bg_color = bg_color
        self.radius = radius
        
        # Bind configure event to update the rounded rectangle when the widget is resized
        self.bind('<Configure>', self._on_resize)
        
    def _on_resize(self, event):
        # Clear the canvas
        self.delete("all")
        # Redraw the rounded rectangle with the new size
        self.round_rectangle(0, 0, event.width, event.height, self.radius, fill=self._bg_color)
        
    def round_rectangle(self, x1, y1, x2, y2, radius, **kwargs):
        # Create rounded rectangle using a smooth polygon
        points = [
            x1 + radius, y1,
            x2 - radius, y1,
            x2, y1,
            x2, y1 + radius,
            x2, y2 - radius,
            x2, y2,
            x2 - radius, y2,
            x1 + radius, y2,
            x1, y2,
            x1, y2 - radius,
            x1, y1 + radius,
            x1, y1
        ]
        return self.create_polygon(points, smooth=True, **kwargs)
