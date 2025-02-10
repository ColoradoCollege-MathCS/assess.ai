import tkinter as tk
from components.rounded_frame import RoundedFrame
from components.llm_list import LLMList


class LLMInput(tk.Frame):
    def __init__(self, parent, root, send_callback, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        self.send_callback = send_callback
        self.root = root
        self.setup_input_area()

    def setup_input_area(self):
        self.grid_columnconfigure(0, weight=1)

        # Container frame for title, input, button, and output
        self.container = tk.Frame(self, bg="#D2E9FC")
        self.container.grid(row=0, column=0, sticky="nsew", padx=0, pady=15)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)  # for input frame
        self.container.grid_columnconfigure(1, weight=0)  # for output frame

        # Input + button container
        self.inputbutt_frame = tk.Frame(self.container, bg="#D2E9FC")
        self.inputbutt_frame.grid(row=1, column=0, sticky="ew", padx=(5, 10), pady=(20, 5))
        self.inputbutt_frame.grid_columnconfigure(0, weight=1)
        self.inputbutt_frame.grid_columnconfigure(1, weight=0)

        # Input container with rounded corners
        self.input_container = RoundedFrame(self.inputbutt_frame, "#FFFFFF", radius=50)
        self.input_container.grid(row=0, column=0, sticky="nsew", padx=10, pady=(20, 10))
        self.input_container.grid_columnconfigure(0, weight=1)

        # Output + LLM list container
        self.outputlist_frame = tk.Frame(self.container, bg="#D2E9FC")
        self.outputlist_frame.grid(row=2, column=0, sticky="ew", padx=(5, 10), pady=(20, 5))
        self.outputlist_frame.grid_rowconfigure(0, weight=1)
        self.outputlist_frame.grid_rowconfigure(1, weight=1)
        self.outputlist_frame.columnconfigure(0, weight=1)  # for output box
        self.outputlist_frame.columnconfigure(1, weight=1)  # for list box

        # Output container frame with rounded corners
        self.output_container = RoundedFrame(self.outputlist_frame, "#FFFFFF", radius=50)
        self.output_container.grid(row=1, column=0, sticky="nsew", padx=(20, 5), pady=10)
        self.output_container.grid_rowconfigure(0, weight=1)
        self.output_container.grid_columnconfigure(0, weight=1)

        # LLM list area
        self.LLMList = LLMList(self.outputlist_frame, self.root)
        self.LLMList.grid(row=1, column=1, sticky="nsew", padx=(10, 20), pady=10)
        self.LLMList.grid_rowconfigure(0, weight=1)

        # "Import LLM" string variable
        string = tk.StringVar()
        string.set("Import LLM")

        # "Import LLM" area
        self.import_label = tk.Label(
            self.container,
            textvariable=string,
            bg="#D2E9FC",
            font=("SF Pro Text", 40, "bold"),
            fg="black",
            anchor="w",
            justify="left"
        )
        self.import_label.grid(row=0, column=0, sticky="w", padx=20, pady=(20, 10))

        # Text input area (to input LLM path)
        self.input_text = tk.Text(
            self.input_container,
            height=1,
            width=65,
            font=("SF Pro Text", 14),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )

        self.input_text.tag_configure("center", justify='center')
        self.input_text.insert("1.0", "Insert model path here")  # default text
        self.input_text.tag_add("center", "1.0", "end")
        self.input_text.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)
        self.input_container.grid_rowconfigure(0, weight=1)
        self.input_text.bind("<FocusIn>", self.default)
        self.input_text.bind("<FocusOut>", self.default)

        # "Import" button canvas
        self.import_button = tk.Canvas(
            self.inputbutt_frame,
            width=100,
            height=60,
            bg="#D2E9FC",
            highlightthickness=0,
            cursor="hand2"
        )
        self.import_button.grid(row=0, column=1, sticky="e", padx=(2, 10), pady=20)

        # Draw import button
        padding = 10
        self.rectangle = self.import_button.create_rectangle(
            padding, padding,
            100, 50,
            fill="#0A84FF",
            outline=""
        )

        # Draw "Import" on import button
        self.import_llm = self.import_button.create_text(
            55, 30,
            text="Import",
            fill="white",
            font=("SF Pro Text", 15),
            anchor="center"
        )

        # "Import Status" string variable
        string = tk.StringVar()
        string.set("Import Status")

        # "Import LLM" area
        self.import_status = tk.Label(
            self.outputlist_frame,
            textvariable=string,
            bg="#D2E9FC",
            font=("SF Pro Text", 20),
            fg="black",
            anchor="w",
            justify="left"
        )
        self.import_status.grid(row=0, column=0, sticky="w", padx=20, pady=(5, 5))

        # "LLMs" string variable
        string = tk.StringVar()
        string.set("LLMs")

        # "LLMs" area
        self.llm_listbox = tk.Label(
            self.outputlist_frame,
            textvariable=string,
            bg="#D2E9FC",
            font=("SF Pro Text", 20),
            fg="black",
            anchor="w",
            justify="left"
        )
        self.llm_listbox.grid(row=0, column=1, sticky="w", padx=20, pady=(5, 5))

        # Draw LLM status area
        self.output_text = tk.Text(
            self.output_container,
            height=5,
            width=30,
            font=("SF Pro Text", 14),
            wrap=tk.WORD,
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.output_text.configure(state="disable")
        self.output_text.grid(row=0, column=0, sticky="ew", padx=20, pady=(10, 10))

        self.import_button.bind("<Button-1>", self.handle_import)

    def default(self, event):
        current = self.input_text.get("1.0", tk.END)
        if current == "Insert model path here\n":
            self.input_text.delete("1.0", tk.END)
        elif current == "\n":
            self.input_text.insert("1.0", "Insert model path here")
            self.input_text.tag_add("center", "1.0", "end")

    def handle_import(self, event=None):
        self.disable_output(False)
        self.disable_input(True)

        model_path = self.get_input()
        print("Clicked!")
        if model_path == "Insert model path here":
            self.output_text.insert("1.0", "Please insert model path")
            return
        elif model_path:
            self.clear_input()
            self.send_callback(model_path)
        else:
            self.output_text.insert("1.0", "Please insert model path")
            return

    def disable_input(self, disable):
        if disable:
            self.input_text.configure(state="disable")
            self.import_button.configure(state="disable")
        else:
            self.input_text.configure(state="normal")
            self.import_button.configure(state="normal")

    def disable_output(self, disable):
        if disable:
            self.output_text.configure(state="disable")
        else:
            self.output_text.configure(state="normal")

    def get_input(self):
        return self.input_text.get("1.0", "end-1c").strip()

    def clear_input(self):
        self.input_text.delete("1.0", "end")
        self.input_text.focus()