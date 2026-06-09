"""
puzzle_viewer.py  --  standalone visualizer for the edge-matching puzzle.

Reads an output .txt file (the one written by the solver) and draws the board.
Each piece is a 4-character string whose edges are, in order:
    [top, right, bottom, left]
Every piece is drawn as a square split into 4 triangles (one per edge),
coloured by the edge symbol. Where two touching triangles share the same
colour, that edge matches; mismatched edges are marked in red.

Usage
-----
    python puzzle_viewer.py                       # uses DEFAULT_FILE
    python puzzle_viewer.py path/to/output.txt    # custom file
    python puzzle_viewer.py output.txt result.png # also choose the saved image
"""

import sys
import os
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon, Rectangle


DEFAULT_FILE = "data/output/output.txt"   # used when no path is given
SHOW_EDGE_LABELS = True                    # print the edge symbol on each triangle
SHOW_MISMATCHES = True                     # mark mismatched edges in red
SAVE_PNG = True 

PALETTE = [
    "#E63946", "#457B9D", "#E9C46A", "#9B5DE5", "#43AA8B", "#F4A261",
    "#00B4D8", "#F15BB5", "#90BE6D", "#8E7DBE", "#577590", "#F9844A",
]

def load_grid(path):
    """Read the txt and return a 2D list of piece strings, skipping any header."""
    grid = []
    with open(path, "r") as f:
        for line in f:
            tokens = line.split()
            # a board row is a line whose tokens are all 4-character pieces
            if len(tokens) >= 2 and all(len(t) == 4 for t in tokens):
                grid.append(tokens)
    if not grid:
        raise ValueError(f"No puzzle grid found in {path!r}.")
    width = len(grid[0])
    grid = [row for row in grid if len(row) == width]   # keep it rectangular
    return grid


def build_colormap(grid):
    """Map every distinct edge symbol to a colour from the palette."""
    symbols = sorted({ch for row in grid for piece in row for ch in piece})
    return {s: PALETTE[i % len(PALETTE)] for i, s in enumerate(symbols)}



def _text_color(hex_color):
    """Pick black or white text for good contrast on the given background."""
    r = int(hex_color[1:3], 16) / 255
    g = int(hex_color[3:5], 16) / 255
    b = int(hex_color[5:7], 16) / 255
    luminance = 0.299 * r + 0.587 * g + 0.114 * b
    return "#000000" if luminance > 0.6 else "#FFFFFF"


def count_mismatches(grid):
    """Return mismatched edge segments and the total count.

    Uses the same convention as the solver:
      vertical   : upper[2] == lower[0]
      horizontal : left[1]  == right[3]
    """
    segments = []
    nrows, ncols = len(grid), len(grid[0])
    for r in range(nrows):
        for c in range(ncols):
            piece = grid[r][c]
            if c + 1 < ncols and piece[1] != grid[r][c + 1][3]:      # right edge
                segments.append([(c + 1, r), (c + 1, r + 1)])
            if r + 1 < nrows and piece[2] != grid[r + 1][c][0]:      # bottom edge
                segments.append([(c, r + 1), (c + 1, r + 1)])
    return segments, len(segments)


def draw(grid, save_path=None):
    cmap = build_colormap(grid)
    nrows, ncols = len(grid), len(grid[0])
    mismatch_segments, mismatch_total = count_mismatches(grid)

    fig, ax = plt.subplots(figsize=(ncols * 0.85 + 1.6, nrows * 0.85 + 1.0))
    fig.patch.set_facecolor("#F7F7F5")
    ax.set_facecolor("#F7F7F5")

    for r in range(nrows):
        for c in range(ncols):
            piece = grid[r][c]
            top, right, bottom, left = piece[0], piece[1], piece[2], piece[3]
            TL, TR = (c, r), (c + 1, r)
            BR, BL = (c + 1, r + 1), (c, r + 1)
            C = (c + 0.5, r + 0.5)

            # (triangle vertices, edge symbol, label anchor)
            triangles = [
                ([TL, TR, C], top,    (c + 0.5, r + 0.27)),  # top
                ([TR, BR, C], right,  (c + 0.73, r + 0.5)),  # right
                ([BR, BL, C], bottom, (c + 0.5, r + 0.73)),  # bottom
                ([BL, TL, C], left,   (c + 0.27, r + 0.5)),  # left
            ]
            for verts, sym, anchor in triangles:
                color = cmap[sym]
                ax.add_patch(Polygon(verts, closed=True, facecolor=color,
                                     edgecolor="white", linewidth=0.6, zorder=1))
                if SHOW_EDGE_LABELS:
                    ax.text(anchor[0], anchor[1], sym, ha="center", va="center",
                            fontsize=7, color=_text_color(color), zorder=3)

            # outline of the whole piece
            ax.add_patch(Rectangle((c, r), 1, 1, fill=False,
                                   edgecolor="#2B2B2B", linewidth=1.3, zorder=2))

    # mark mismatched edges
    if SHOW_MISMATCHES and mismatch_segments:
        for (x0, y0), (x1, y1) in mismatch_segments:
            ax.plot([x0, x1], [y0, y1], color="#D7263D", linewidth=4,
                    solid_capstyle="round", alpha=0.9, zorder=4)

    ax.set_xlim(-0.1, ncols + 0.1)
    ax.set_ylim(nrows + 0.1, -0.1)          # invert y so row 0 is on top
    ax.set_aspect("equal")
    ax.axis("off")

    title = f"{nrows}x{ncols} puzzle"
    if SHOW_MISMATCHES:
        title += f"   |   mismatched edges: {mismatch_total}"
    ax.set_title(title, fontsize=12, color="#2B2B2B", pad=12)

    # colour legend for the edge symbols
    handles = [Rectangle((0, 0), 1, 1, facecolor=cmap[s], edgecolor="white")
               for s in sorted(cmap)]
    ax.legend(handles, sorted(cmap), title="edge", loc="center left",
              bbox_to_anchor=(1.01, 0.5), frameon=False, fontsize=9,
              title_fontsize=9)

    fig.tight_layout()
    if save_path:
        fig.savefig(save_path, dpi=150, bbox_inches="tight",
                    facecolor=fig.get_facecolor())
        print(f"Saved image to {save_path}")
    plt.show()

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_FILE
    if not os.path.exists(path):
        sys.exit(f"File not found: {path}")
    grid = load_grid(path)

    save_path = None
    if SAVE_PNG:
        save_path = sys.argv[2] if len(sys.argv) > 2 else os.path.splitext(path)[0] + ".png"
    draw(grid, save_path)


if __name__ == "__main__":
    main()
