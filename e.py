import tkinter as tk
import random

# Constants
WIDTH = 600
HEIGHT = 400
BAR_WIDTH = 20
NUM_BARS = WIDTH // BAR_WIDTH
DELAY = 50  # milliseconds

# Initialize window
root = tk.Tk()
root.title("Sorting Algorithm Visualizer - Mac Friendly")

canvas = tk.Canvas(root, width=WIDTH, height=HEIGHT, bg="white")
canvas.pack()

# Random array
array = [random.randint(10, 100) for _ in range(NUM_BARS)]
original_array = array[:]

# Algorithm Selection
algorithm = tk.StringVar(value="Bubble")

def draw_bars(arr, highlight=None):
    canvas.delete("all")
    for i, val in enumerate(arr):
        x0 = i * BAR_WIDTH
        y0 = HEIGHT - (val * 3)  # scale to fit canvas height
        x1 = x0 + BAR_WIDTH
        y1 = HEIGHT
        color = "red" if highlight and i in highlight else "skyblue"
        canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="black")
    root.update_idletasks()

# Global indices for sorting state
i = j = min_index = 0
insertion_key = None
inserting = False

def start_sort():
    global i, j, min_index, insertion_key, inserting, count_sort_index, count_sort_array
    i = j = min_index = 0
    insertion_key = None
    inserting = False
    count_sort_index = 0
    count_sort_array = []
    algo = algorithm.get()
    if algo == "Bubble":
        bubble_sort_step()
    elif algo == "Insertion":
        insertion_sort_step()
    elif algo == "Selection":
        selection_sort_step()
    elif algo == "Count":
        count_sort_prepare()

def reset_sort():
    global array, i, j, min_index, insertion_key, inserting
    array = original_array[:]
    i = j = min_index = 0
    insertion_key = None
    inserting = False
    draw_bars(array)

def bubble_sort_step():
    global i, j, array
    if i < len(array):
        if j < len(array) - i - 1:
            draw_bars(array, highlight=(j, j + 1))
            if array[j] > array[j + 1]:
                array[j], array[j + 1] = array[j + 1], array[j]
            j += 1
            root.after(DELAY, bubble_sort_step)
        else:
            j = 0
            i += 1
            root.after(DELAY, bubble_sort_step)
    else:
        draw_bars(array)

def insertion_sort_step():
    global i, j, insertion_key, inserting, array
    if i < len(array):
        if not inserting:
            insertion_key = array[i]
            j = i - 1
            inserting = True
        if j >= 0 and array[j] > insertion_key:
            draw_bars(array, highlight=(j, j + 1))
            array[j + 1] = array[j]
            j -= 1
            root.after(DELAY, insertion_sort_step)
        else:
            array[j + 1] = insertion_key
            i += 1
            inserting = False
            root.after(DELAY, insertion_sort_step)
    else:
        draw_bars(array)

def selection_sort_step():
    global i, j, min_index, array
    if i < len(array) - 1:
        if j < len(array):
            draw_bars(array, highlight=(i, j))
            if array[j] < array[min_index]:
                min_index = j
            j += 1
            root.after(DELAY, selection_sort_step)
        else:
            array[i], array[min_index] = array[min_index], array[i]
            i += 1
            j = i + 1
            min_index = i
            root.after(DELAY, selection_sort_step)
    else:
        draw_bars(array)

# Count Sort Variables
count_sort_array = []
count_sort_index = 0

def count_sort_prepare():
    global count_sort_array
    max_val = max(array)
    count = [0] * (max_val + 1)

    for num in array:
        count[num] += 1

    count_sort_array = []
    for val, freq in enumerate(count):
        count_sort_array.extend([val] * freq)

    root.after(DELAY, count_sort_step)

def count_sort_step():
    global count_sort_index, array, count_sort_array
    if count_sort_index < len(array):
        array[count_sort_index] = count_sort_array[count_sort_index]
        draw_bars(array, highlight=(count_sort_index,))
        count_sort_index += 1
        root.after(DELAY, count_sort_step)
    else:
        draw_bars(array)

# UI Elements
algo_frame = tk.Frame(root)
tk.Label(algo_frame, text="Select Algorithm:").pack(side="left", padx=5)
for algo_name in ["Bubble", "Insertion", "Selection", "Count"]:
    tk.Radiobutton(algo_frame, text=algo_name, variable=algorithm, value=algo_name).pack(side="left")
algo_frame.pack(pady=5)

tk.Button(root, text="Start Sorting", command=start_sort).pack(pady=5)
tk.Button(root, text="Reset", command=reset_sort).pack()

draw_bars(array)

root.mainloop()