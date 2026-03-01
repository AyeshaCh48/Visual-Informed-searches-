import tkinter as tk
from tkinter import messagebox
import heapq
import math
import random
import time

# --- Colors ---
COLOR_WALL = "#2c3e50"     
COLOR_START = "#27ae60"    
COLOR_GOAL = "#e74c3c"     
COLOR_PATH = "#2ecc71"     
COLOR_VISITED = "#3498db"  
COLOR_FRONTIER = "#f1c40f" 
COLOR_EMPTY = "#ecf0f1"    

class PathfindingApp:
    def __init__(self, root):
        self.root = root

        self.rows = 15 
        self.cols = 15
        self.start_node = (2, 2)
        self.goal_node = (12, 12)
        
        self.grid_rects = {}
        self.text_ids = {} 
        self.walls = set()
        self.algorithm = "A*"
        self.dynamic = tk.BooleanVar(value=False)
        
        self.drawScreen()

    def drawScreen(self):
        self.drawFrame = tk.Frame(self.root, padx=20, pady=20)
        self.drawFrame.pack()

        tk.Label(self.drawFrame, text="Grid Setup", font=("Arial", 12, "bold")).grid(row=0, columnspan=2, pady=10)
        tk.Label(self.drawFrame, text="Rows:").grid(row=1, column=0)
        self.urows = tk.Entry(self.drawFrame); self.urows.insert(0, "15"); self.urows.grid(row=1, column=1)
        tk.Label(self.drawFrame, text="Cols:").grid(row=2, column=0)
        self.ucols = tk.Entry(self.drawFrame); self.ucols.insert(0, "15"); self.ucols.grid(row=2, column=1)
        tk.Label(self.drawFrame, text="Start (r,c):").grid(row=3, column=0); self.ustart = tk.Entry(self.drawFrame); self.ustart.grid(row=3, column=1)
        tk.Label(self.drawFrame, text="Goal (r,c):").grid(row=4, column=0); self.ugoal = tk.Entry(self.drawFrame); self.ugoal.grid(row=4, column=1)

        tk.Button(self.drawFrame, text="Launch Simulation", command=self.run_algo, bg="#3498db", fg="white").grid(row=5, columnspan=2, pady=20)

    def run_algo(self):
        try:
            self.rows = int(self.urows.get()) if self.urows.get() else 15
            self.cols = int(self.ucols.get()) if self.ucols.get() else 15
            if self.ustart.get(): self.start_node = tuple(map(int, self.ustart.get().split(',')))
            if self.ugoal.get(): self.goal_node = tuple(map(int, self.ugoal.get().split(',')))
        except: pass
        self.drawFrame.destroy()
        self.algo_ui()
        self.create_grid()

    def algo_ui(self):
        controls = tk.Frame(self.root, padx=10, pady=5)
        controls.pack(side=tk.TOP, fill=tk.X)

        self.algo_var = tk.StringVar(value="A*")
        tk.OptionMenu(controls, self.algo_var, "A*", "Greedy BFS").pack(side=tk.LEFT, padx=5)
        self.heur_var = tk.StringVar(value="Manhattan")
        tk.OptionMenu(controls, self.heur_var, "Manhattan", "Euclidean").pack(side=tk.LEFT, padx=5)
        tk.Checkbutton(controls, text="Dynamic", variable=self.dynamic).pack(side=tk.LEFT)
        tk.Button(controls, text="Random (30%)", command=self.rand_walls).pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="START", command=self.start_algo, bg="#27ae60", fg="white").pack(side=tk.LEFT, padx=5)
        tk.Button(controls, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)

        legend_frame = tk.Frame(self.root, pady=5)
        legend_frame.pack(side=tk.TOP, fill=tk.X)
        items = [("Start", COLOR_START), ("Goal", COLOR_GOAL), ("In Queue", COLOR_FRONTIER), ("Visited", COLOR_VISITED), ("Path", COLOR_PATH), ("Wall", COLOR_WALL)]
        for text, color in items:
            tk.Label(legend_frame, text=text, bg=color, fg="white" if color == COLOR_WALL else "black", font=("Arial", 8)).pack(side=tk.LEFT, padx=5)

        tk.Label(self.root, text="Cell Text -> Top-Left: g(n) [Path Cost] | Bottom-Right: h(n) [Heuristic]", font=("Arial", 8, "italic"), fg="#555").pack()

        self.stats = tk.Label(self.root, text="Visited: 0 | Cost: 0 | Time: 0ms", font=("Arial", 10, "bold"))
        self.stats.pack(side=tk.BOTTOM, pady=5)

        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="white")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.add_walls)

    def create_grid(self):
        w, h = 600 // self.cols, 600 // self.rows
        for r in range(self.rows):
            for c in range(self.cols):
                x1, y1 = c * w, r * h
                rect = self.canvas.create_rectangle(x1, y1, x1+w, y1+h, fill=COLOR_EMPTY, outline="#ddd")
                self.grid_rects[(r, c)] = rect
                g_txt = self.canvas.create_text(x1+2, y1+2, anchor="nw", font=("Arial", 7), fill="#d35400")
                h_txt = self.canvas.create_text(x1+w-2, y1+h-2, anchor="se", font=("Arial", 7), fill="#8e44ad")
                self.text_ids[(r, c)] = (g_txt, h_txt)
        self.fixed_nodes()

    def fixed_nodes(self):
        self.canvas.itemconfig(self.grid_rects[self.start_node], fill=COLOR_START)
        self.canvas.itemconfig(self.grid_rects[self.goal_node], fill=COLOR_GOAL)

    def add_walls(self, event):
        c, r = event.x // (600 // self.cols), event.y // (600 // self.rows)
        if (0 <= r < self.rows and 0 <= c < self.cols) and (r, c) not in [self.start_node, self.goal_node]:
            if (r, c) in self.walls:
                self.walls.remove((r, c)); self.canvas.itemconfig(self.grid_rects[(r, c)], fill=COLOR_EMPTY)
            else:
                self.walls.add((r, c)); self.canvas.itemconfig(self.grid_rects[(r, c)], fill=COLOR_WALL)

    def get_h(self, node):
        r1, c1 = node; r2, c2 = self.goal_node
        if self.heur_var.get() == "Manhattan": return abs(r1 - r2) + abs(c1 - c2)
        return round(math.sqrt((r1 - r2)**2 + (c1 - c2)**2), 1)

    def start_algo(self):
        self.clear_visual_only()
        start_time = time.time()
        self.algorithm = self.algo_var.get()
        frontier = []; heapq.heappush(frontier, (0, self.start_node))
        path_from = {self.start_node: None}; cost_g = {self.start_node: 0}
        count = 0; found = False

        while frontier:
            priority, current = heapq.heappop(frontier)
            count += 1
            if current == self.goal_node: found = True; break
            if current != self.start_node: self.canvas.itemconfig(self.grid_rects[current], fill=COLOR_VISITED)

            for dr, dc in [(0,1), (1,0), (0,-1), (-1,0)]:
                neighbor = (current[0]+dr, current[1]+dc)
                if (0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols and neighbor not in self.walls):
                    new_g = cost_g[current] + 1
                    if neighbor not in cost_g or new_g < cost_g[neighbor]:
                        cost_g[neighbor] = new_g
                        h_val = self.get_h(neighbor)
                        g_id, h_id = self.text_ids[neighbor]
                        self.canvas.itemconfig(g_id, text=f"{new_g}")
                        self.canvas.itemconfig(h_id, text=f"{h_val}")
                        total_p = (new_g + h_val) if self.algorithm == "A*" else h_val
                        heapq.heappush(frontier, (total_p, neighbor))
                        path_from[neighbor] = current
                        if neighbor != self.goal_node: self.canvas.itemconfig(self.grid_rects[neighbor], fill=COLOR_FRONTIER)
            if count % 5 == 0: self.root.update()
            
        exec_time = int((time.time() - start_time) * 1000)
        if found:
            path = []; temp = self.goal_node
            while temp in path_from: path.append(temp); temp = path_from[temp]
            path.reverse(); self.animate_path(path, count, exec_time)
        else:
            self.stats.config(text=f"Visited: {count} | No Path"); messagebox.showinfo("Result", "No path exists!")

    def animate_path(self, path, count, ms):
        self.stats.config(text=f"Visited: {count} | Cost: {len(path)-1} | Time: {ms}ms")
        for i, step in enumerate(path):
            if step not in [self.start_node, self.goal_node]: self.canvas.itemconfig(self.grid_rects[step], fill=COLOR_PATH)
            if self.dynamic.get() and i < len(path)-1:
                if random.random() < 0.1:
                    obs = (random.randint(0, self.rows-1), random.randint(0, self.cols-1))
                    if obs not in [self.start_node, self.goal_node] and obs not in self.walls:
                        self.walls.add(obs); self.canvas.itemconfig(self.grid_rects[obs], fill=COLOR_WALL)
                        if obs in path[i+1:]: self.start_node = step; self.root.after(100, self.start_algo); return
            self.root.update(); time.sleep(0.05)

    def rand_walls(self):
        self.clear()
        for r in range(self.rows):
            for c in range(self.cols):
                if (r, c) not in [self.start_node, self.goal_node] and random.random() < 0.3:
                    self.walls.add((r, c)); self.canvas.itemconfig(self.grid_rects[(r, c)], fill=COLOR_WALL)

    def clear(self):
        self.walls.clear(); self.clear_visual_only()

    def clear_visual_only(self):
        for (r, c), rect in self.grid_rects.items():
            color = COLOR_EMPTY
            if (r, c) == self.start_node: color = COLOR_START
            elif (r, c) == self.goal_node: color = COLOR_GOAL
            elif (r, c) in self.walls: color = COLOR_WALL
            self.canvas.itemconfig(rect, fill=color)
            g_id, h_id = self.text_ids[(r, c)]; self.canvas.itemconfig(g_id, text=""); self.canvas.itemconfig(h_id, text="")

if __name__ == "__main__":
    root = tk.Tk(); app = PathfindingApp(root); root.mainloop()