import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
from PIL import Image, ImageTk
import pandas as pd
import os

class MediaPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Media Player App")
        self.playing_media = False
        self.canvas_cleared = False

        # Media Player Variables
        self.media_path = ""
        self.cap = None
        self.current_media = None
        self.total_frames = 0
        self.current_frame_number = 0

        # Image Player Variables
        self.image_path = ""
        self.image_references = {}
        self.current_image = None

        # Question Data Variables
        self.questions_df = None
        self.current_question_index = 0
        self.media_folder = ""

        # Fixed height for the canvas
        self.canvas_height = 576

        # UI Components
        self.media_canvas = tk.Canvas(root, width=1024, height=self.canvas_height)
        self.media_canvas.grid(row=0, column=0, columnspan=4, pady=10)

        self.btn_play = tk.Button(root, text="Play", command=self.play_media)
        self.btn_play.grid(row=1, column=0, padx=10, pady=10)

        self.btn_replay = tk.Button(root, text="Replay", command=self.replay_media)
        self.btn_replay.grid(row=1, column=1, padx=10, pady=10)

        self.btn_previous = tk.Button(root, text="Previous", command=self.previous_question)
        self.btn_previous.grid(row=2, column=0, padx=10, pady=10)

        self.btn_next = tk.Button(root, text="Next", command=self.next_question)
        self.btn_next.grid(row=2, column=1, padx=10, pady=10)

        self.load_questions_from_excel_button = tk.Button(root, text="Load Questions", command=self.load_questions_from_excel_dialog)
        self.load_questions_from_excel_button.grid(row=3, column=0, padx=10, pady=10, columnspan=2)

        self.load_media_folder_button = tk.Button(root, text="Load Media Folder", command=self.load_media_folder_dialog)
        self.load_media_folder_button.grid(row=3, column=2, padx=10, pady=10, columnspan=2)

        self.entry_question_number = tk.Entry(root, state=tk.NORMAL)
        self.entry_question_number.grid(row=4, column=0, padx=10, pady=10, columnspan=2)
        self.entry_question_number.bind("<Return>", self.jump_to_question)

        self.lbl_question_info = tk.Label(root, text="/ 0")
        self.lbl_question_info.grid(row=4, column=2, padx=10, pady=10, columnspan=2)

        # Question Label
        self.question_label = tk.Label(root, text="Your Question Here", font=("Arial", 14), wraplength=800)
        self.question_label.grid(row=5, column=0, columnspan=4, pady=10)

        # Response Labels
        self.response_label_a = tk.Label(root, text="Response A", wraplength=250)
        self.response_label_a.grid(row=6, column=0, padx=10, pady=5)

        self.response_label_b = tk.Label(root, text="Response B", wraplength=250)
        self.response_label_b.grid(row=6, column=1, padx=10, pady=5)

        self.response_label_c = tk.Label(root, text="Response C", wraplength=250)
        self.response_label_c.grid(row=6, column=2, padx=10, pady=5)

        # Right Answer Label
        self.right_answer_label = tk.Label(root, text="Right Answer: ", font=("Arial", 12), wraplength=800)
        self.right_answer_label.grid(row=7, column=0, columnspan=4, pady=5)

    def play_media(self):
        if self.cap and not self.playing_media:
            self.playing_media = True
            self.play_media_frame()

    def play_media_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.entry_question_number.delete(0, tk.END)  # Clear the entry box when playing
            self.current_media = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))

            if not self.canvas_cleared:
                self.media_canvas.delete("all")
                self.canvas_cleared = True

            self.media_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_media)
            self.root.after(10, self.play_media_frame)
        else:
            self.cap.release()
            self.playing_media = False

    def replay_media(self):
        if self.cap and not self.playing_media:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.play_media()

    def load_and_play_media(self, media_path):
        if self.cap:
            self.cap.release()
        self.cap = cv2.VideoCapture(media_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        self.play_media()

    def load_and_display_image(self, image_path):
        if self.cap and self.playing_media:
            self.cap.release()
            self.playing_media = False

        image = Image.open(image_path)
        image = image.resize((1024, self.canvas_height))
        photo_image = ImageTk.PhotoImage(image=image)

        self.image_references[image_path] = photo_image

        self.media_canvas.delete("all")
        self.media_canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        self.root.update_idletasks()

    def previous_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            self.current_question_index = (self.current_question_index - 1) % self.total_questions
            self.show_question()

    def next_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            self.current_question_index = (self.current_question_index + 1) % self.total_questions
            self.show_question()

    def jump_to_question(self, event):
        try:
            target_question = int(self.entry_question_number.get())
            if 1 <= target_question <= self.total_questions:
                self.current_question_index = target_question - 1
            else:
                self.current_question_index = 0
            self.show_question()
        except ValueError:
            self.entry_question_number.delete(0, tk.END)
            self.entry_question_number.insert(0, str(self.current_question_index + 1))

    def load_media_folder_dialog(self):
        media_folder = filedialog.askdirectory()
        if media_folder:
            self.media_folder = media_folder
            self.show_question()

    def load_questions_from_excel_dialog(self):
        excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if excel_path:
            self.load_questions_from_excel(excel_path)

    def load_questions_from_excel(self, excel_path):
        try:
            self.questions_df = pd.read_excel(excel_path)
            self.total_questions = len(self.questions_df)
            self.lbl_question_info.config(text=f"/ {self.total_questions}")
            self.show_question()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading questions: {str(e)}")

    def show_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            question_data = self.questions_df.iloc[self.current_question_index]
            question_text = question_data['Pytanie ENG']
            response_a = question_data['Odpowiedź ENG A']
            response_b = question_data['Odpowiedź ENG B']
            response_c = question_data['Odpowiedź ENG C']
            right_answer = question_data['Poprawna odp']
            media_file_name = question_data['Media']

            self.question_label.config(text=question_text)
            self.response_label_a.config(text=f"A: {response_a}")
            self.response_label_b.config(text=f"B: {response_b}")
            self.response_label_c.config(text=f"C: {response_c}")
            self.right_answer_label.config(text=f"Right Answer: {right_answer}")

            self.canvas_cleared = False

            if media_file_name and not pd.isna(media_file_name):
                media_file_path = os.path.join(self.media_folder, media_file_name)
                if media_file_name.lower().endswith((".jpg", ".jpeg")):
                    self.load_and_display_image(media_file_path)
                elif media_file_name.lower().endswith((".wmv", ".mp4")):
                    self.load_and_play_media(media_file_path)
                else:
                    messagebox.showinfo("Information", "Unsupported media file type.")
            else:
                messagebox.showinfo("Information", "No media file required for this question.")

            self.entry_question_number.delete(0, tk.END)
            self.entry_question_number.insert(0, str(self.current_question_index + 1))
        else:
            messagebox.showinfo("Information", "No questions loaded.")

if __name__ == "__main__":
    root = tk.Tk()
    app = MediaPlayerApp(root)
    root.mainloop()
