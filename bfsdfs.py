import tkinter as tk
from tkinter import messagebox
import math
import time

# Globals to store node positions and canvas item IDs
positions = {}
node_circles = {}
edge_lines = {}
dfs_parents = {}
dfs_order_index = {}
node_visit_times = {}  # Store visit times for each node during traversal

# Build the graph from input entries
def build_graph():
    verts = [v.strip() for v in vert_entry.get().split(',') if v.strip()]
    edges_raw = edges_entry.get().split(',')
    graph = {v: [] for v in verts}
    for e in edges_raw:
        parts = e.strip().split()
        if len(parts) != 2:
            continue
        u, v = parts
        if u in graph and v in graph:
            graph[u].append(v)
            graph[v].append(u)
    return graph

# Draw the graph on the canvas and store item IDs
def draw_graph(graph):
    global positions, node_circles, edge_lines
    canvas.delete('all')
    positions.clear()
    node_circles.clear()
    edge_lines.clear()
    verts = list(graph.keys())
    n = len(verts)
    if n == 0:
        return
    w = int(canvas['width'])
    h = int(canvas['height'])
    cx, cy = w / 2, h / 2
    rad = min(w, h) / 2 - 40
    # position nodes on circle
    for i, v in enumerate(verts):
        angle = 2 * math.pi * i / n
        x = cx + rad * math.cos(angle)
        y = cy + rad * math.sin(angle)
        positions[v] = (x, y)
    # draw edges and record line IDs
    for u in graph:
        for v in graph[u]:
            if u < v:
                x1, y1 = positions[u]
                x2, y2 = positions[v]
                lid = canvas.create_line(x1, y1, x2, y2)
                edge_lines[(u, v)] = lid
    # draw nodes and record circle IDs
    for v, (x, y) in positions.items():
        r = 15
        cid = canvas.create_oval(x - r, y - r, x + r, y + r, fill='lightblue', tags=v)
        canvas.create_text(x, y, text=v, tags=v)
        node_circles[v] = cid
        canvas.tag_bind(v, "<Button-1>", lambda event, node=v: on_node_click(node))

# Show graph without simulation
def show_graph():
    g = build_graph()
    draw_graph(g)
    output_text.delete(1.0, tk.END)
    timer_label.config(text="")

# Animate traversal: highlight edges and nodes, record visit times
def animate_traversal(order, edges_order, node_color, edge_color):
    global node_visit_times
    node_visit_times.clear()  # Reset times for this traversal

    for v, cid in node_circles.items():
        canvas.itemconfig(cid, fill='lightblue')
    for lid in edge_lines.values():
        canvas.itemconfig(lid, fill='black', width=1)

    start_time = time.time()
    timer_label.config(text=f"Traversal started at: {time.strftime('%H:%M:%S', time.localtime(start_time))}")

    def step(i):
        if i < len(order):
            current_time = time.time()
            v = order[i]
            node_visit_times[v] = current_time  # Save visit time

            if i > 0:
                u, wnode = edges_order[i - 1]
                key = (u, wnode) if (u, wnode) in edge_lines else (wnode, u)
                lid = edge_lines.get(key)
                if lid:
                    canvas.itemconfig(lid, fill=edge_color, width=3)

            cid = node_circles.get(v)
            if cid:
                canvas.itemconfig(cid, fill=node_color)

            root.after(500, step, i + 1)
        else:
            end_time = time.time()
            timer_label.config(
                text=f"Traversal started at: {time.strftime('%H:%M:%S', time.localtime(start_time))}\n"
                     f"Traversal ended at:   {time.strftime('%H:%M:%S', time.localtime(end_time))}"
            )

    root.after(0, step, 0)

# DFS traversal with parent and order tracking
def dfs():
    global dfs_parents, dfs_order_index
    g = build_graph()
    draw_graph(g)
    start = start_entry.get().strip()
    if start not in g:
        messagebox.showerror("Error", f"Start vertex '{start}' not in vertices")
        return
    visited = set()
    order = []
    edges_order = []
    dfs_parents = {start: None}
    dfs_order_index = {}

    def dfs_visit(u):
        visited.add(u)
        dfs_order_index[u] = len(order)
        order.append(u)
        for w in g[u]:
            if w not in visited:
                dfs_parents[w] = u
                edges_order.append((u, w))
                dfs_visit(w)

    dfs_visit(start)
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "DFS Order: " + " ".join(order))
    animate_traversal(order, edges_order, 'orange', 'orange')

# BFS traversal with edge recording
def bfs():
    g = build_graph()
    draw_graph(g)
    start = start_entry.get().strip()
    if start not in g:
        messagebox.showerror("Error", f"Start vertex '{start}' not in vertices")
        return
    visited = set([start])
    queue = [start]
    order = [start]
    edges_order = []
    while queue:
        u = queue.pop(0)
        for w in g[u]:
            if w not in visited:
                visited.add(w)
                queue.append(w)
                order.append(w)
                edges_order.append((u, w))
    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, "BFS Order: " + " ".join(order))
    animate_traversal(order, edges_order, 'green', 'green')

# When a node is clicked, show parent, children, order and visit time
def on_node_click(node):
    parent = dfs_parents.get(node, "None")
    children = [k for k, v in dfs_parents.items() if v == node]
    index = dfs_order_index.get(node, "N/A")
    visit_time = node_visit_times.get(node)

    output_text.delete(1.0, tk.END)
    output_text.insert(tk.END, f"Clicked Node: {node}\n")
    output_text.insert(tk.END, f"Visited at position: {index + 1 if index != 'N/A' else 'N/A'}\n")
    output_text.insert(tk.END, f"Parent: {parent}\n")
    output_text.insert(tk.END, f"Children: {', '.join(children) if children else 'None'}\n")

    if visit_time:
        formatted_time = time.strftime('%H:%M:%S', time.localtime(visit_time))
        output_text.insert(tk.END, f"Visited at time: {formatted_time}")
    else:
        output_text.insert(tk.END, f"Visited at time: Not visited (yet)")

# Main UI setup
root = tk.Tk()
root.title("BFS and DFS Simulator")

# Inputs
tk.Label(root, text="Vertices (comma-separated):").grid(row=0, column=0, sticky='w')
vert_entry = tk.Entry(root, width=40)
vert_entry.grid(row=0, column=1)
vert_entry.insert(0, "A,B,C,D,E,F,G,H,I,J")

tk.Label(root, text="Edges (u v, comma-separated):").grid(row=1, column=0, sticky='w')
edges_entry = tk.Entry(root, width=40)
edges_entry.grid(row=1, column=1)
edges_entry.insert(0, "A B,B C,A D,D E,E F,F G,H I,I J")

tk.Label(root, text="Start Vertex:").grid(row=2, column=0, sticky='w')
start_entry = tk.Entry(root, width=40)
start_entry.grid(row=2, column=1)
start_entry.insert(0, "A")

# Buttons
tk.Button(root, text="Show Graph", command=show_graph).grid(row=3, column=0, pady=5)
tk.Button(root, text="Run BFS", command=bfs).grid(row=3, column=1, pady=5)
tk.Button(root, text="Run DFS", command=dfs).grid(row=3, column=2, pady=5)

# Output and Canvas
output_text = tk.Text(root, height=7, width=60)
output_text.grid(row=4, column=0, columnspan=3, pady=10)

timer_label = tk.Label(root, text="", fg="blue")
timer_label.grid(row=6, column=0, columnspan=3)

canvas = tk.Canvas(root, width=400, height=400, bg='white')
canvas.grid(row=5, column=0, columnspan=3, pady=10)

root.mainloop()
