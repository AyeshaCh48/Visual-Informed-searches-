# Visual-Informed-searches-
# 🤖 Dynamic Pathfinding Visualizer (A* & Greedy BFS)

A highly interactive Python application built with `Tkinter` that visualizes how informed search algorithms navigate through static and dynamic environments. This tool provides real-time insights into the mathematical cost functions of pathfinding by displaying path costs $g(n)$ and heuristics $h(n)$ directly on the grid.

## 🚀 Key Features

* **Dual Algorithm Support:** Compare **A* Search** (Optimal/Complete) and **Greedy Best-First Search** (Fast/Heuristic-focused).
* **Real-Time Mathematical Visualization:**
    * **$g(n)$ (Path Cost):** Top-left orange text showing the actual distance traveled from the start.
    * **$h(n)$ (Heuristic):** Bottom-right purple text showing the estimated distance remaining to the goal.
* **Dynamic Re-planning:** Enable **Dynamic Mode** to simulate real-world scenarios where obstacles appear randomly while the agent is in motion, forcing the algorithm to recalculate the path mid-route.
* **Grid Interaction:**
    * **Manual Mapping:** Left-click or drag to draw custom walls and obstacles.
    * **Auto-Generation:** Instantly generate a map with 30% random obstacle density.
* **Exhaustive Search Feedback:** If the goal is unreachable, the agent visually explores every possible path before notifying the user that no path exists.

---

## 🎨 Visual Legend

| Element | Color | Role |
| :--- | :--- | :--- |
| **Start** | 🟩 Green | Initial position of the agent. |
| **Goal** | 🟥 Red | The target coordinate. |
| **In Queue** | 🟨 Yellow | Nodes in the frontier (Priority Queue) awaiting expansion. |
| **Visited** | 🟦 Blue | Nodes already explored by the algorithm. |
| **Final Path** | 🟩 Bright Green | The calculated route from Start to Goal. |
| **Wall** | ⬛ Dark Grey | Impassable terrain. |



---

## 🛠️ Installation & Usage

### Prerequisites
* Python 3.x
* Tkinter (usually included with standard Python installations)
