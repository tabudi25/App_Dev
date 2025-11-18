# Constants and configuration for the memory game

# Colors
COLOR_BG_PANEL = "#000000"
COLOR_PANEL_ACCENT = "#34495e"
COLOR_BTN_TEXT = "white"

# Font
FONT_NAMES = "Tahoma"

# Theme-specific music files mapping
THEME_MUSIC = {
    "naruto": "narutomusic.mp3",
    "op": "onepiecemusic.mp3",
    "slam": "slamdunkmusic.mp3",
    "db": "dragonballmusic.mp3",
    "bleach": "bleachmusic.mp3",
}

# Theme image paths
NARUTO_PATHS_4X4 = [f"naruto{i}.png" for i in range(1, 9)]
NARUTO_PATHS_6X6 = [f"naruto{i}.png" for i in range(1, 19)]
NARUTO_PATHS_8X8 = [f"naruto{i}.png" for i in range(1, 33)]
OP_PATHS_4X4 = [f"op{i}.png" for i in range(1, 9)]
OP_PATHS_6X6 = [f"op{i}.png" for i in range(1, 19)]
OP_PATHS_8X8 = [f"op{i}.png" for i in range(1, 33)]
SLAM_PATHS_4X4 = [f"slam{i}.png" for i in range(1, 9)]
SLAM_PATHS_6X6 = [f"slam{i}.png" for i in range(1, 19)]
SLAM_PATHS_8X8 = [f"slam{i}.png" for i in range(1, 33)]
DB_PATHS_4X4 = [f"db{i}.png" for i in range(1, 9)]
DB_PATHS_6X6 = [f"db{i}.png" for i in range(1, 19)]
DB_PATHS_8X8 = [f"db{i}.png" for i in range(1, 33)]
BLEACH_PATHS_4X4 = [f"bleach{i}.png" for i in range(1, 9)]
BLEACH_PATHS_6X6 = [f"bleach{i}.png" for i in range(1, 19)]
BLEACH_PATHS_8X8 = [f"bleach{i}.png" for i in range(1, 33)]

THEME_IMAGES = {
    "naruto": {4: NARUTO_PATHS_4X4, 6: NARUTO_PATHS_6X6, 8: NARUTO_PATHS_8X8},
    "op": {4: OP_PATHS_4X4, 6: OP_PATHS_6X6, 8: OP_PATHS_8X8},
    "slam": {4: SLAM_PATHS_4X4, 6: SLAM_PATHS_6X6, 8: SLAM_PATHS_8X8},
    "db": {4: DB_PATHS_4X4, 6: DB_PATHS_6X6, 8: DB_PATHS_8X8},
    "bleach": {4: BLEACH_PATHS_4X4, 6: BLEACH_PATHS_6X6, 8: BLEACH_PATHS_8X8},
}

