import tkinter as tk
from components.rounded_frame import RoundedFrame

class LLMInput(tk.Frame):
    def __init__(self, parent, send_callback, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.send_callback = send_callback
        self.setup_input_area()

    def setup_input_area(self):
        self.grid_columnconfigure(0, weight=1)

        # Container frame for input, button, and output
        self.container = tk.Frame(self, bg="#D2E9FC")
        self.container.grid(row=0, column=0, sticky="ew", padx=20, pady=15)
        self.container.grid_columnconfigure(0, weight=1)

        # Input container with rounded corners
        self.input_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        self.input_container.grid(row=0, column=0, sticky="ew", padx=(0, 10))
        self.input_container.grid_columnconfigure(0, weight=1)

        # Button container frame for button with rounded corners
        #self.button_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        #self.button_container.grid(row=1, column=0, sticky="ew", padx=20, pady=(0,2))

        # Output container frame with rounded corners
        self.output_container = RoundedFrame(self.container, "#FFFFFF", radius=50)
        self.output_container.grid(row=2, column=0, sticky="ew", padx=20, pady=(0,2))
        self.input_container.grid_columnconfigure(0, weight=1)
        # Text input area (to input LLM path)
        self.input_text = tk.Text(
            self.input_container,
            height=3,
            font=("SF Pro Text", 14),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.input_text.insert("1.0", "Type in model path here")# default text
        #self.input_text.pack(fill="both", expand=True, padx=20, pady=2)
        self.input_text.grid(row=0, column=0, sticky="ew", padx=20, pady=2)
        self.input_text.bind("<FocusIn>", self.default)
        self.input_text.bind("<FocusOut>", self.default)

        # "Download" button canvas
        self.download_button = tk.Canvas(
            self.container,
            width=100,
            height=60,
            bg="#D2E9FC",
            highlightthickness=0,
            cursor="hand2"
        )
        self.download_button.grid(row=1, column=0)

        # Draw download button
        padding = 10
        self.rectangle = self.download_button.create_rectangle(
            padding, padding,
            100, 50,
            fill="#0A84FF",
            outline=""
        )

        # Draw "Download LLM" on download button
        self.download_llm = self.download_button.create_text(
            55, 30,
            text="Download",
            fill="white",
            font=("SF Pro Text", 15),
            anchor="center"
        )

        # Draw LLM status area
        self.output_text = tk.Text(
            self.output_container,
            height=5,
            font=("SF Pro Text", 14),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.output_text.configure(state="disable")
        #self.output_text.pack(fill="both", expand=True, padx=20, pady=2)
        self.output_text.grid(row=0, column=0, sticky="ew", padx=20, pady=2)

        self.download_button.bind("<Button-1>", self.handle_download)

    def default(self, event):
        current = self.input_text.get("1.0", tk.END)
        if current == "Type in model path here\n":
            self.input_text.delete("1.0", tk.END)
        elif current == "\n":
            self.input_text.insert("1.0", "Type in model path here")

    def handle_download(self, event = None):
        model_path = self.get_input()
        print ("Clicked!")
        if model_path:
            self.clear_input()
            self.send_callback(model_path)

    def get_input(self):
        return self.input_text.get("1.0", "end-1c").strip()

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.input_text.focus()





