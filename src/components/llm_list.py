import tkinter as tk
import os
from components.rounded_frame import RoundedFrame
#from main import AssessAIGUI


class LLMList(tk.Frame):
    def __init__(self, parent, root, **kwargs):
        super().__init__(parent, bg="#D2E9FC", **kwargs)
        #self.main_gui = AssessAIGUI(root)  # instance of AssessAIGUI
        self.setup_list_area()

    def setup_list_area(self):
        self.grid_columnconfigure(0, weight=1)

        # list container with rounded corners
        self.list_container = RoundedFrame(self, "#FFFFFF", radius=50)
        self.list_container.grid(row=0, column=0, sticky="nsew", padx=(0, 5), pady=(5, 5))
        self.list_container.grid_columnconfigure(0, weight=1)
        self.list_container.grid_rowconfigure(0, weight=1)

        # Frame for LLM list + scrollbar
        self.scrolllist_frame = tk.Frame(self.list_container, bg="white")
        self.scrolllist_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
        self.scrolllist_frame.grid_columnconfigure(0, weight=1)
        self.scrolllist_frame.grid_rowconfigure(0, weight=1)

        # LLM list area
        self.list = tk.Listbox(
            self.scrolllist_frame,
            height=15,
            width=30,
            font=("SF Pro Text", 14),
            bd=0,
            bg="white",
            highlightthickness=0,
            relief="flat"
        )
        self.list.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        # LLM list scrollbar
        self.list_scrollbar = tk.Scrollbar(self.scrolllist_frame, orient="vertical", command=self.list.yview)
        self.list_scrollbar.grid(row=0, column=1, sticky="ns")

        self.list.configure(yscrollcommand=self.list_scrollbar.set)

        # scroll binding
        # self.list_frame.bind("<Configure>", self.update_scroll)
        self.list.bind("<MouseWheel>", self.mouse_scroll)  # bind to mouse
        # selection bind
        self.list.bind("<ButtonRelease-1>", self.model_selected)

        self.write_list(self.get_models())

    def model_selected(self, event):
        selected_model = self.list.curselection()
        if selected_model:
            model_path = self.list.get(selected_model)

            #self.main_gui.show_page("model", model_path)
            return

    def get_models(self):
        folder_list = []
        cwd = os.getcwd()  # current directory
        parent = os.path.dirname(cwd)  # parent directory
        model_dir = os.path.join(parent, "model_files")
        # check if model_files
        for folder in os.listdir(model_dir):  # list all folders in model_files folder
            if os.path.isdir(os.path.join(model_dir, folder)):
                folder_list.append(folder)
        return folder_list

    def write_list(self, list):
        self.list.delete(0, tk.END)  # delete existing entries
        count = 0
        for model in list:
            count += 1
            self.list.insert(count, model)

    def mouse_scroll(self, event):
        if event.delta:
            self.list.yview_scroll(-1 * (event.delta // 120), "units")
        elif event.num == 4:
            self.list.yview_scroll(-1, "units")
        elif event.num == 5:
            self.list.yview_scroll(1, "units")
        return "break"
