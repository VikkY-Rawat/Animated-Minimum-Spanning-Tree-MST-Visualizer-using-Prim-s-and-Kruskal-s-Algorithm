import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random, time, threading

# --- Main Window ---
root = tk.Tk()
root.title("Animated MST Visualizer (Prim’s & Kruskal’s)")
root.geometry("950x800")
root.configure(bg="#e8f2ff")

# --- Global Variables ---
G = None
pos = None
running = False

# --- Create Connected Random Graph ---
def create_connected_graph():
    global G, pos
    G = nx.Graph()
    n = 6
    for i in range(n):
        G.add_node(i)
    for i in range(1, n):
        G.add_edge(i - 1, i, weight=random.randint(2, 20))
    for _ in range(random.randint(2, 4)):
        u, v = random.sample(range(n), 2)
        if not G.has_edge(u, v):
            G.add_edge(u, v, weight=random.randint(2, 20))
    pos = nx.spring_layout(G, seed=42)
    draw_graph(G, title="Connected Random Graph Generated")
    update_status("✅ New graph generated successfully!")

# --- Draw Graph Function ---
def draw_graph(graph, mst_edges=None, highlight_edge=None, title="Graph"):
    plt.clf()
    weights = nx.get_edge_attributes(graph, 'weight')
    nx.draw(graph, pos, with_labels=True, node_color="#a3c4f3",
            node_size=800, font_weight="bold", font_size=10)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=weights, font_size=9)
    all_edges = list(graph.edges())

    if mst_edges:
        nx.draw_networkx_edges(graph, pos, edgelist=mst_edges, width=3, edge_color='red')

    if highlight_edge:
        nx.draw_networkx_edges(graph, pos, edgelist=[highlight_edge], width=4, edge_color='orange')

    plt.title(title, fontsize=12, color='green')
    canvas.draw()

# --- Update Status Box ---
def update_status(message):
    status_text.configure(state="normal")
    status_text.insert(tk.END, message + "\n")
    status_text.see(tk.END)
    status_text.configure(state="disabled")

# --- Animation Controller ---
def animate_mst(edges_list, algo_name):
    mst_edges = []
    total_weight = 0
    for (u, v, w) in edges_list:
        if not running:
            return
        draw_graph(G, mst_edges, highlight_edge=(u, v),
                   title=f"{algo_name} — Adding Edge ({u}, {v}) = {w}")
        update_status(f"🔸 Adding edge ({u}, {v}) with weight {w}")
        time.sleep(1.2)
        mst_edges.append((u, v))
        total_weight += w
        draw_graph(G, mst_edges, title=f"{algo_name} — Current MST Weight = {total_weight}")
        time.sleep(1)

    update_status(f"✅ {algo_name} Completed! Total MST Weight = {total_weight}")

# --- Run Algorithm ---
def run_algorithm():
    global running
    running = True
    selected_algo = algo_choice.get()
    if selected_algo not in ["Prim’s Algorithm", "Kruskal’s Algorithm"]:
        messagebox.showwarning("Warning", "Please select an algorithm first!")
        return

    update_status(f"\n▶ Running {selected_algo}...")
    threading.Thread(target=run_selected_algorithm, args=(selected_algo,), daemon=True).start()

def run_selected_algorithm(selected_algo):
    if selected_algo == "Prim’s Algorithm":
        mst = nx.minimum_spanning_tree(G, algorithm='prim')
    else:
        mst = nx.minimum_spanning_tree(G, algorithm='kruskal')

    edges_with_weights = [(u, v, G.edges[u, v]['weight']) for u, v in mst.edges()]
    animate_mst(edges_with_weights, selected_algo)

# --- Stop Animation ---
def stop_animation():
    global running
    running = False
    update_status("🛑 Animation stopped by user.")

# --- Matplotlib Figure ---
fig = plt.figure(figsize=(7, 6))
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(pady=30)

# --- Controls Frame ---
control_frame = tk.Frame(root, bg="#e8f2ff")
control_frame.pack(pady=10)

# --- Dropdown & Buttons ---
tk.Label(control_frame, text="Select Algorithm:", font=("Arial", 11, "bold"), bg="#e8f2ff").grid(row=0, column=0, padx=10)
algo_choice = ttk.Combobox(control_frame, values=["Prim’s Algorithm", "Kruskal’s Algorithm"],
                           width=25, state="readonly", font=("Arial", 10))
algo_choice.grid(row=0, column=1, padx=10)
algo_choice.set("Select Algorithm")

ttk.Button(control_frame, text="Generate Graph", command=create_connected_graph).grid(row=0, column=2, padx=10)
ttk.Button(control_frame, text="Run Algorithm", command=run_algorithm).grid(row=0, column=3, padx=10)
ttk.Button(control_frame, text="Stop", command=stop_animation).grid(row=0, column=4, padx=10)

# --- Status / Log Box ---
tk.Label(root, text="Algorithm Steps:", font=("Arial", 11, "bold"), bg="#e8f2ff").pack()
status_text = tk.Text(root, height=8, width=90, state="disabled", bg="#f5faff", fg="black", font=("Consolas", 10))
status_text.pack(pady=10)

# --- Initialize Graph ---
create_connected_graph()

# --- Run App ---
root.mainloop()
