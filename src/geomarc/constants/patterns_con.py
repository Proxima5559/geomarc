LOW_POINTS = 12
LOW_EXTRA_LINES = 4
LOW_POLYGONS = 2

MEDIUM_POINTS = 25
MEDIUM_EXTRA_LINES = 12
MEDIUM_POLYGONS = 5

HIGH_POINTS = 45
HIGH_EXTRA_LINES = 25
HIGH_POLYGONS = 9


COMPLEXITY_SETTINGS = {
    "low": {
        "points": LOW_POINTS,
        "extra_lines": LOW_EXTRA_LINES,
        "polygons": LOW_POLYGONS,
    },
    "medium": {
        "points": MEDIUM_POINTS,
        "extra_lines": MEDIUM_EXTRA_LINES,
        "polygons": MEDIUM_POLYGONS,
    },
    "high": {
        "points": HIGH_POINTS,
        "extra_lines": HIGH_EXTRA_LINES,
        "polygons": HIGH_POLYGONS,
    },
}


STYLE_CHOICES = [
    "line_mesh",
    "polygon_network",
    "angular_sharp",
    "minimal",
    "dense_geometric",
]

STYLE_CONFIGS = {
    "line_mesh": {
        "points_multiplier": 1.0,
        "lines_multiplier": 1.5,
        "polygons_multiplier": 0.5,
    },
    "polygon_network": {
        "points_multiplier": 1.2,
        "lines_multiplier": 0.8,
        "polygons_multiplier": 1.5,
    },
    "angular_sharp": {
        "points_multiplier": 0.9,
        "lines_multiplier": 1.2,
        "polygons_multiplier": 1.0,
    },
    "minimal": {
        "points_multiplier": 0.5,
        "lines_multiplier": 0.5,
        "polygons_multiplier": 0.2,
    },
    "dense_geometric": {
        "points_multiplier": 1.8,
        "lines_multiplier": 2.0,
        "polygons_multiplier": 2.0,
    },
}