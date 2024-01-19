import tkinter as tk
from psutil import net_io_counters
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns  # Import Seaborn
import time

# Variables for use in the size() function.
KB = float(1024)
MB = float(KB ** 2)  # 1,048,576
GB = float(KB ** 3)  # 1,073,741,824
TB = float(KB ** 4)  # 1,099,511,627,776

# Constants
WINDOW_SIZE = (500, 650)  # Increase window size
WINDOW_RESIZEABLE = False  # If the window is resizeable or not.
REFRESH_DELAY = 1000  # Window update delay in ms.
GRAPH_DURATION = 10  # Duration for which speed is shown on the graph in seconds.

# Variables
start_time = time.time()
last_upload, last_download, upload_speed, down_speed = 0, 0, 0, 0
total_upload, total_download = 0, 0  # Track total upload and total download
speed_history = {'upload': [], 'download': []}
time_axis = []

# Initializing
window = tk.Tk()

window.title("Realtime Network Speed Monitor")  # Setting the window title.
window.geometry(f"{WINDOW_SIZE[0]}x{WINDOW_SIZE[1]}")  # Setting the window size.
window.resizable(width=WINDOW_RESIZEABLE, height=WINDOW_RESIZEABLE)  # We now lock the window.

# Styling
font_bold = "Quicksand 14 bold"  # Increase font size
font_normal = "Quicksand 12"  # Keep normal font size
font_italic = "Quicksand 11 italic"  # Keep italic font size

# Dark background and white text
window.tk_setPalette(background="#1e1e1e", foreground="white")

# Seaborn style for matplotlib
sns.set(style="darkgrid", palette="pastel")

# Function to update labels and graph
def update():
    global last_upload, last_download, upload_speed, down_speed, total_upload, total_download, start_time
    counter = net_io_counters()

    upload = counter.bytes_sent
    download = counter.bytes_recv
    total = upload + download

    if last_upload > 0:
        if upload < last_upload:
            upload_speed = 0
        else:
            upload_speed = (upload - last_upload) / MB  # Convert to Megabytes per second

    if last_download > 0:
        if download < last_download:
            down_speed = 0
        else:
            down_speed = (download - last_download) / MB  # Convert to Megabytes per second

    last_upload = upload
    last_download = download

    total_upload += upload_speed
    total_download += down_speed

    label_total_upload.config(text=f"Total Upload: {total_upload:.2f} MB")
    label_total_download.config(text=f"Total Download: {total_download:.2f} MB")
    label_current_upload.config(text=f"Upload Speed: {upload_speed:.2f} Mbps")
    label_current_download.config(text=f"Download Speed: {down_speed:.2f} Mbps")

    elapsed_time = time.time() - start_time
    time_axis.append(elapsed_time)

    speed_history['upload'].append(upload_speed)
    speed_history['download'].append(down_speed)

    update_graph()

    window.after(REFRESH_DELAY, update)  # reschedule event in refresh delay

# Function to update the graph using Seaborn
def update_seaborn_graph():
    plt.clf()  # Clear the current plot
    plt.plot(time_axis[-int(GRAPH_DURATION / REFRESH_DELAY):], speed_history['upload'][-int(GRAPH_DURATION / REFRESH_DELAY):], label='Upload Speed', marker='o')
    plt.plot(time_axis[-int(GRAPH_DURATION / REFRESH_DELAY):], speed_history['download'][-int(GRAPH_DURATION / REFRESH_DELAY):], label='Download Speed', marker='o')
    plt.title('Upload and Download Speed Over Time')
    plt.xlabel('Elapsed Time (s)')
    plt.ylabel('Speed (Mbps)')
    plt.legend()
    plt.tight_layout()

# Function to update the graph
def update_graph():
    ax.clear()
    ax.plot(time_axis, speed_history['upload'], label='Upload Speed', marker='o')
    ax.plot(time_axis, speed_history['download'], label='Download Speed', marker='o')
    ax.legend()
    ax.set_xlim(max(0, time_axis[-1] - GRAPH_DURATION), time_axis[-1] + 1)  # Set x-axis limit based on elapsed time
    canvas.draw()

    update_seaborn_graph()  # Update the Seaborn graph

# Creating a custom theme
window.tk_setPalette(background="#1e1e1e", foreground="white")

# Frame for total upload and download labels
total_labels_frame = tk.Frame(window, bg="#1e1e1e", bd=5)
total_labels_frame.place(relx=0.5, rely=0.1, relwidth=0.95, anchor="n")

# Labels for total upload and download
label_total_upload = tk.Label(total_labels_frame, text="", font=font_normal, bg="#1e1e1e", fg="white")
label_total_download = tk.Label(total_labels_frame, text="", font=font_normal, bg="#1e1e1e", fg="white")

# Frame for better layout control
label_frame = tk.Frame(window, bg="#1e1e1e", bd=5)
label_frame.place(relx=0.5, rely=0.2, relwidth=0.95, anchor="n")

# Labels for current upload and download
label_current_upload = tk.Label(label_frame, text="", font=font_normal, bg="#1e1e1e", fg="white")
label_current_download = tk.Label(label_frame, text="", font=font_normal, bg="#1e1e1e", fg="white")

# Updating Labels
window.after(REFRESH_DELAY, update)

# Packing Labels
label_total_upload.pack(pady=5)
label_total_download.pack(pady=5)
label_current_upload.pack(pady=5)
label_current_download.pack(pady=5)

# Attribution
attribution = tk.Label(window, text="~ IrfanArshad ~", font=font_italic, bg="#1e1e1e", fg="white")
attribution.place(relx=0.5, rely=1.0, anchor="s")  # Place at the bottom of the window

# Matplotlib Graph
fig, ax = plt.subplots(figsize=(6, 3), dpi=80)  # Increase graph size
canvas = FigureCanvasTkAgg(fig, master=label_frame)
widget = canvas.get_tk_widget()
widget.pack()

window.mainloop()