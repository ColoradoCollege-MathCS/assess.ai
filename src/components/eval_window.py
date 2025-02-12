import tkinter as tk
from tkinter import ttk, Toplevel
from PIL import Image, ImageTk
import os

class EvaluationWindow:
    def __init__(self, root):
        self.root = root
        # Images must be stored, or else Tkinter will remove them via Garbage collection
        self.eval_images = []
        
    def show_evaluation(self, eval_name):
        # Create new window
        eval_win = Toplevel(self.root)
        eval_win.title(f"Evaluation: {eval_name}")
        eval_win.geometry("500x500")
        eval_win.configure(bg="#D2E9FC")
        
        # Main container (Used to add scrollbar and Canvas for content)
        main_container = tk.Frame(eval_win, bg="#D2E9FC")
        # Take up all space on window
        main_container.pack(fill="both", expand=True)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_container, bg="#D2E9FC", highlightthickness=0)
        scrollbar = ttk.Scrollbar(main_container, orient="vertical", command=canvas.yview)
        
        # Content frame inside canvas
        content_frame = tk.Frame(canvas, bg="#D2E9FC")
        
        # Links scrollbar to canvas
        canvas.configure(yscrollcommand=scrollbar.set)
        # Set scrollbar to right
        scrollbar.pack(side="right", fill="y")
        canvas.pack(side="left", fill="both", expand=True)
        
        # Create window in canvas for content and bind configuration
        canvas.create_window((canvas.winfo_width()//2, 0), window=content_frame, anchor="n")
        # Adjust scrollbar as content from folder loads
        content_frame.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

        title = tk.Label(content_frame, 
                        text=f"Evaluation Details: {eval_name}", 
                        font=("SF Pro Display", 16, "bold"), # Bold title
                        bg="#D2E9FC")
        title.pack(pady=(20,20))
        
        # Load images and log from folder
        try:
            eval_path = os.path.join(os.path.dirname(os.getcwd()), "eval_files", eval_name)
            # Get and filter files
            files = os.listdir(eval_path)
            image_files = [f for f in files if f.lower().endswith('.png')]
            log_file = 'logs.txt' if 'logs.txt' in files else None
            
            # Display images
            if image_files:
                for img_file in image_files:
                    img_path = os.path.join(eval_path, img_file)
                    try:
                        with Image.open(img_path) as img:
                            display_width = 400
                            ratio = display_width / img.width
                            display_height = int(img.height * ratio)
                            
                            resized_img = img.resize((display_width, display_height))
                            photo = ImageTk.PhotoImage(resized_img)
                            self.eval_images.append(photo)
                            
                            # Render image as a TK label
                            tk.Label(content_frame, image=photo).pack(pady=(0,20))
                    except Exception as e:
                        print(f"Error loading image {img_file}: {str(e)}")
            
            # Display logs.txt
            if log_file:
                try:
                    log_path = os.path.join(eval_path, log_file)
                    
                    # Create log section
                    tk.Label(content_frame,
                            text="Evaluation Logs:",
                            font=("SF Pro Display", 16, "bold"),
                            bg="#D2E9FC").pack(pady=(10,5))
                    
                    log_frame = tk.Frame(content_frame, bg="#D2E9FC")
                    log_frame.pack(fill="both", expand=True, padx=20)
                    
                    log_text = tk.Text(log_frame, height=10, width=60)
                    log_text.pack(pady=(0,20))
                    
                    # Read and display logs
                    with open(log_path, 'r') as f:
                        log_text.insert("1.0", f.read())
                        log_text.configure(state="disabled")
                        
                except Exception as e:
                    print(f"Error reading log file: {str(e)}")

        except Exception as e:
            print(f"Error loading evaluation: {str(e)}")