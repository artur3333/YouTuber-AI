import os
import subprocess
import threading
import tkinter as tk
from tkinter import ttk

process_is_running = False
process_thread = None
proc = None


def run_process(video_id: str, tts_type: str, platform: str, line_callback: callable = None): # run process
    def run_process():
        global process_is_running
        global proc
        process_is_running = True
        try:
            curr_env = os.environ.copy()
            
            command = ['python', 'main.py', "--video_id", video_id, "--tts_type", tts_type, "--platform", platform]
            if debug_var.get():
                command.append("--debug")
            
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True, env=curr_env)
            
            while process_is_running:
                line = proc.stdout.readline()
                if not line and proc.poll() is not None:
                    break

                decoded_line = line.decode("utf-8", "replace")
                if line_callback is not None:
                    line_callback(decoded_line)
                print(f">> {decoded_line.rstrip()}")
                
            proc.stdout.close()
            proc.stderr.close()
            print("Process finished.")
        except KeyboardInterrupt:
            pass
        except Exception as e:
            print(f"Error: {e}")
        finally:
            process_is_running = False

    global process_thread
    process_thread = threading.Thread(target=run_process)
    process_thread.start()


def stop_process(): # stop process
    global process_is_running, proc, process_thread
    if not process_is_running or proc is None:
        print("Process is not running.")
        return
    
    process_is_running = False
    
    def terminate_process():
        global proc
        try:
            if proc and proc.poll() is None:
                proc.terminate()
            process_thread.join()
            print("Process terminated.")
        except Exception as e:
            print(f"Error: {e}")
    
    threading.Thread(target=terminate_process).start()


class RunGUI: # run GUI
    def __init__(self, debug: bool = False):
        self.debug = debug
        root = tk.Tk()
        root.title("Streamer-AI")
        root.geometry("500x600")
        root.resizable(width=False,height=False)
        root.iconbitmap("icon.ico")

        frame = ttk.Frame(root)
        frame.pack(fill=tk.BOTH, expand=False)

        video_id_label = ttk.Label(frame, text="Stream ID (YouTube)")
        video_id_label.grid(row=0, column=0, padx=5, pady=5)
        video_id_entry = ttk.Entry(frame)
        video_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tts_type_label = ttk.Label(frame, text="TTS Type")
        tts_type_label.grid(row=1, column=0, padx=5, pady=5)
        tts_type_dropdown = ttk.Combobox(frame, values=["openai", "pyttsx3"])
        tts_type_dropdown.current(0)
        tts_type_dropdown.grid(row=1, column=1, padx=5, pady=5)

        platform_label = ttk.Label(frame, text="Platform")
        platform_label.grid(row=2, column=0, padx=5, pady=5)
        platform_dropdown = ttk.Combobox(frame, values=["youtube", "twitch"])
        platform_dropdown.current(0)
        platform_dropdown.grid(row=2, column=1, padx=5, pady=5)

        global debug_var
        debug_var = tk.BooleanVar()
        debug_checkbox = ttk.Checkbutton(frame, text="Enable Debug Mode", variable=debug_var)
        debug_checkbox.grid(row=3, column=0, padx=5, pady=5)

        run_button = ttk.Button(frame, text="Run",
                                command=lambda: run_process(video_id_entry.get(), tts_type_dropdown.get(), platform_dropdown.get(),
                                                            lambda line: (console.insert(tk.END, line), console.yview_moveto(1))))
        run_button.grid(row=4, column=0, padx=5, pady=5)
        stop_button = ttk.Button(frame, text="Stop", command=stop_process)
        stop_button.grid(row=4, column=1, padx=5, pady=5)

        console = tk.Text(frame, height=25, width=60)
        console.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

        self.root = root

    def run(self): # run
        self.log_d("Run")
        self.root.mainloop()

    def log_d(self, message):
        if self.debug:
            print(message)


if __name__ == "__main__":
    RunGUI().run()
