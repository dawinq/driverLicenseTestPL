import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import pandas as pd
import os

class VideoPlayerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Video Player App")

        # Video Player Variables
        self.video_path = ""
        self.cap = None
        self.current_frame = None
        self.total_frames = 0
        self.current_frame_number = 0

        # Question Data Variables
        self.questions_df = None
        self.current_question_index = 0
        self.media_folder = ""

        # UI Components
        self.video_canvas = tk.Canvas(root, width=1024, height=576)
        self.video_canvas.grid(row=0, column=0, columnspan=3, pady=10)

        self.btn_play = tk.Button(root, text="Play", command=self.play_video)
        self.btn_play.grid(row=1, column=0, padx=10, pady=10)

        self.btn_replay = tk.Button(root, text="Replay", command=self.replay_video)
        self.btn_replay.grid(row=1, column=1, padx=10, pady=10)

        self.btn_previous = tk.Button(root, text="Previous", command=self.previous_question)
        self.btn_previous.grid(row=2, column=0, padx=10, pady=10)

        self.lbl_question_number = tk.Label(root, text="0 / 0")
        self.lbl_question_number.grid(row=2, column=1, padx=10, pady=10)

        self.btn_next = tk.Button(root, text="Next", command=self.next_question)
        self.btn_next.grid(row=2, column=2, padx=10, pady=10)

        self.load_questions_from_excel_button = tk.Button(root, text="Load Questions", command=self.load_questions_from_excel_dialog)
        self.load_questions_from_excel_button.grid(row=3, column=0, padx=10, pady=10)

        self.load_media_folder_button = tk.Button(root, text="Load Media Folder", command=self.load_media_folder_dialog)
        self.load_media_folder_button.grid(row=3, column=1, columnspan=2, padx=10, pady=10)

        # Question Label
        self.question_label = tk.Label(root, text="Your Question Here", font=("Arial", 14))
        self.question_label.grid(row=4, column=0, columnspan=3, pady=10)

        # Response Labels
        self.response_label_a = tk.Label(root, text="Response A")
        self.response_label_a.grid(row=5, column=0, padx=10, pady=5)

        self.response_label_b = tk.Label(root, text="Response B")
        self.response_label_b.grid(row=5, column=1, padx=10, pady=5)

        self.response_label_c = tk.Label(root, text="Response C")
        self.response_label_c.grid(row=5, column=2, padx=10, pady=5)

        # Right Answer Label
        self.right_answer_label = tk.Label(root, text="Right Answer: ", font=("Arial", 12))
        self.right_answer_label.grid(row=6, column=0, columnspan=3, pady=5)

    def play_video(self):
        if self.cap:
            ret, frame = self.cap.read()
            if ret:
                self.current_frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
                self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
                self.root.after(10, self.play_video)

    def replay_video(self):
        if self.cap:
            self.cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            self.show_frame()

    def show_frame(self):
        ret, frame = self.cap.read()
        if ret:
            self.current_frame_number = int(self.cap.get(cv2.CAP_PROP_POS_FRAMES))
            self.lbl_question_number.config(text=f"{self.current_frame_number} / {self.total_frames}")
            self.current_frame = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.video_canvas.create_image(0, 0, anchor=tk.NW, image=self.current_frame)
        else:
            messagebox.showinfo("End of Video", "End of video reached.")

    def load_and_play_video(self, video_path):
        self.cap = cv2.VideoCapture(video_path)
        self.total_frames = int(self.cap.get(cv2.CAP_PROP_FRAME_COUNT))
        self.play_video()

    def load_and_display_image(self, image_path):
        image = Image.open(image_path)
        image = image.resize((1024, 576), Image.ANTIALIAS)
        photo_image = ImageTk.PhotoImage(image=image)
        self.video_canvas.create_image(0, 0, anchor=tk.NW, image=photo_image)
        self.root.update_idletasks()  # Update the canvas immediately to display the image

    def next_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            self.current_question_index = (self.current_question_index + 1) % self.total_questions
            self.show_question()

    def previous_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            self.current_question_index = (self.current_question_index - 1) % self.total_questions
            self.show_question()

    def load_media_folder_dialog(self):
        media_folder = filedialog.askdirectory()
        if media_folder:
            # Update the path to media folder
            self.media_folder = media_folder
            # Reload the current question to display media for the selected question
            self.show_question()

    def load_questions_from_excel_dialog(self):
        excel_path = filedialog.askopenfilename(filetypes=[("Excel files", "*.xlsx")])
        if excel_path:
            self.load_questions_from_excel(excel_path)

    def load_questions_from_excel(self, excel_path):
        try:
            self.questions_df = pd.read_excel(excel_path)
            self.total_questions = len(self.questions_df)
            self.show_question()
        except Exception as e:
            messagebox.showerror("Error", f"Error loading questions: {str(e)}")

    def show_question(self):
        if self.questions_df is not None and not self.questions_df.empty:
            question_data = self.questions_df.iloc[self.current_question_index]
            question_text = question_data['Pytanie ENG']
            response_a = question_data['Odpowiedź ENG A']
            response_b = question_data['Odpowiedź ENG B']
            response_c = question_data['Odpowiedź ENG A']
            right_answer = question_data['Poprawna odp']
            media_file_name = question_data['Media']
            question_number = question_data['Lp.']

            # Update UI elements with question data
            self.question_label.config(text=question_text)

            # Include labels for responses
            self.response_label_a.config(text=f"A: {response_a}")
            self.response_label_b.config(text=f"B: {response_b}")
            self.response_label_c.config(text=f"C: {response_c}")

            self.right_answer_label.config(text=f"Right Answer: {right_answer}")

            # Load and display media file (if exists)
            if media_file_name and not pd.isna(media_file_name):
                media_file_path = os.path.join(self.media_folder, media_file_name)
                if media_file_name.lower().endswith(".wmv"):
                    self.load_and_play_video(media_file_path)
                elif media_file_name.lower().endswith((".jpg", ".jpeg")):
                    self.load_and_display_image(media_file_path)
                else:
                    messagebox.showinfo("Information", "Unsupported media file type.")
            else:
                messagebox.showinfo("Information", "No media file required for this question.")

            # Display question number
            max_question_number = self.questions_df['Lp.'].max()
            self.lbl_question_number.config(text=f"{question_number} / {max_question_number}")
        else:
            messagebox.showinfo("Information", "No questions loaded.")

    def set_bottom_layout(self):
        # Move the previous button, the question number label, and the next button to the bottom
        self.btn_previous.grid(row=7, column=0, padx=10, pady=10)
        self.lbl_question_number.grid(row=7, column=1, padx=10, pady=10)
        self.btn_next.grid(row=7, column=2, padx=10, pady=10)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoPlayerApp(root)
    app.set_bottom_layout()
    root.mainloop()

