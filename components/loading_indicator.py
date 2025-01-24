from components.chat_bubble import ChatBubble

class LoadingIndicator:
    """Manages the loading animation state"""
    def __init__(self, parent, root):
        self.parent = parent
        self.root = root
        self.bubble = None
        self.after_id = None
        
    def start(self):
        """Start loading animation"""
        self.bubble = ChatBubble(self.parent, "", is_user=False)
        self.bubble.pack(anchor="w", padx=20, pady=5, fill="x")
        self._animate()
        
    def stop(self):
        """Stop loading animation and cleanup"""
        if self.bubble:
            self.bubble.destroy()
            self.bubble = None
        if self.after_id:
            self.root.after_cancel(self.after_id)
            self.after_id = None
            
    def _animate(self, dots=0):
        """Animate the loading dots"""
        if self.bubble:
            dots = (dots % 3) + 1
            self.bubble.message.configure(text="Thinking" + "." * dots)
            self.after_id = self.root.after(500, self._animate, dots)