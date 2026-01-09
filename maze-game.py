import collections
import time
import matplotlib.pyplot as plt
import numpy as np

# 1. Define the Maze
# 0 = Empty Space, 1 = Wall
maze = [
    [0, 1, 0, 0, 0],-
    [0, 1, 0, 1, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 1, 1, 0],
    [0, 0, 0, 0, 0]
]

# --- BFS Implementation ---
def solve_bfs(maze, start, end):
    queue = collections.deque([[start]])
    visited = set([start])
    rows, cols = len(maze), len(maze[0])

    while queue:
        path = queue.popleft()
        r, c = path[-1]
        if (r, c) == end: return path

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                queue.append(path + [(nr, nc)])
                visited.add((nr, nc))
    return None

# --- DFS Implementation ---
def solve_dfs(maze, start, end):
    stack = [[start]]
    visited = set([start])
    rows, cols = len(maze), len(maze[0])

    while stack:
        path = stack.pop()
        r, c = path[-1]
        if (r, c) == end: return path

        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and maze[nr][nc] == 0 and (nr, nc) not in visited:
                stack.append(path + [(nr, nc)])
                visited.add((nr, nc))
    return None

# --- Visualization Function (Matplotlib) ---
def plot_maze_comparison(maze, bfs_path, dfs_path, start, end):
    """
    Plots the maze and overlays the BFS and DFS paths side-by-side.
    """
    grid = np.array(maze)
    rows, cols = grid.shape

    fig, axes = plt.subplots(1, 2, figsize=(12, 6))

    # Helper to plot a single path on a specific axis
    def plot_on_axis(ax, path, title):
        # 1. Show the Maze Grid (White=Empty, Black=Wall)
        # We invert the colors (1-grid) so 0(empty) is white and 1(wall) is black
        ax.imshow(1 - grid, cmap='gray', vmin=0, vmax=1)

        # 2. Plot the grid lines for clarity
        ax.set_xticks(np.arange(-0.5, cols, 1), minor=True)
        ax.set_yticks(np.arange(-0.5, rows, 1), minor=True)
        ax.grid(which='minor', color='black', linestyle='-', linewidth=1)
        ax.tick_params(which='minor', size=0)

        # 3. Plot the Path
        if path:
            # Unzip path into r (y-axis) and c (x-axis) coordinates
            path_r, path_c = zip(*path)
            # Plot path as a red line with dots
            ax.plot(path_c, path_r, color='red', linewidth=3, marker='o', markersize=8, label='Path')

            # 4. Mark Start (Green) and End (Blue)
            # Note: scatter takes (x, y), so we pass (c, r)
            ax.scatter(start[1], start[0], color='green', s=200, zorder=5, label='Start', edgecolors='white')
            ax.scatter(end[1], end[0], color='blue', s=200, zorder=5, label='End', edgecolors='white')

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.legend(loc='upper right')

        # Invert Y axis so (0,0) is top-left
        # (imshow does this by default, but good to ensure)

    # Plot BFS
    bfs_title = f"BFS (Shortest Path)\nLength: {len(bfs_path) if bfs_path else 0}"
    plot_on_axis(axes[0], bfs_path, bfs_title)

    # Plot DFS
    dfs_title = f"DFS (Any Path)\nLength: {len(dfs_path) if dfs_path else 0}"
    plot_on_axis(axes[1], dfs_path, dfs_title)

    plt.tight_layout()
    plt.show()

# --- Main Execution ---
start_pos = (0, 0)
end_pos = (4, 4)

# Run Algorithms
start_time = time.perf_counter()
bfs_path = solve_bfs(maze, start_pos, end_pos)
bfs_time = (time.perf_counter() - start_time) * 1000

start_time = time.perf_counter()
dfs_path = solve_dfs(maze, start_pos, end_pos)
dfs_time = (time.perf_counter() - start_time) * 1000

# Print Text Metrics
print(f"{'Algorithm':<10} | {'Time (ms)':<15} | {'Path Length':<15}")
print("-" * 45)
print(f"{'BFS':<10} | {bfs_time:.5f} ms      | {len(bfs_path) if bfs_path else 'No Path'}")
print(f"{'DFS':<10} | {dfs_time:.5f} ms      | {len(dfs_path) if dfs_path else 'No Path'}")

# Trigger Visualization
plot_maze_comparison(maze, bfs_path, dfs_path, start_pos, end_pos)