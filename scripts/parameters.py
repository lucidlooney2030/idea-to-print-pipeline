"""Single source of truth for all dimensions.
Units: millimeters unless noted.
Every part module imports from here. Never hardcode numbers in geometry.
"""

# --- Printer / material ---
NOZZLE_MM = 0.4
MIN_WALL_MM = 1.2          # 3 perimeters
LAYER_MM = 0.2

# --- Clearances (magnet + plastic) ---
CLEARANCE_PRESS = 0.15     # tight press fit (risk of chip)
CLEARANCE_SLIDE = 0.30     # sliding fit
CLEARANCE_LOOSE = 0.45

# --- Baseline generator magnets ---
OUTER_MAGNET_DIA = 20.0
OUTER_MAGNET_THK = 5.0
INNER_MAGNET_DIA = 5.0
INNER_MAGNET_THK = 5.0
INNER_GROUP_COUNT = 3      # stacked per pole

# --- Derived (do not edit by hand) ---
OUTER_POCKET_DIA = OUTER_MAGNET_DIA + 2 * CLEARANCE_SLIDE   # 20.60
OUTER_POCKET_DEPTH = OUTER_MAGNET_THK + 0.35
INNER_POCKET_DIA = INNER_MAGNET_DIA + 2 * CLEARANCE_SLIDE    # 5.60
INNER_POCKET_DEPTH = INNER_MAGNET_THK + 0.35

# --- Coil former ---
COIL_HOLE_DIA = 2.5       # through-hole for weaving
COIL_COLUMNS = 32         # 16 outer + 16 inner
COIL_ROWS = 5

print("Parameters loaded. Outer pocket:", OUTER_POCKET_DIA, "mm")
