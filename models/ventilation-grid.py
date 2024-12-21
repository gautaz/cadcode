from math import floor
import logging
from build123d import *

logging.basicConfig(level=logging.INFO)

length, height, thickness = 400, 53, 18
groove_depth, groove_thickness = 5, 14
hole_radius = 3
holes_xcount = floor((length-2*groove_depth)/(3*hole_radius))
holes_ycount = floor((height-groove_depth)/(3*hole_radius))


with BuildPart() as grid:
    Box(length, height, thickness)

    with BuildSketch(grid.faces().sort_by(Axis.X).first):
        Rectangle(groove_thickness, height)
    extrude(amount=-groove_depth, mode=Mode.SUBTRACT)

    with BuildSketch(grid.faces().sort_by(Axis.X).last):
        Rectangle(groove_thickness, height)
    extrude(amount=-groove_depth, mode=Mode.SUBTRACT)

    with BuildSketch(grid.faces().sort_by(Axis.Y).first):
        with Locations((0.5, 0)):
            Rectangle(groove_thickness-1, length)
    extrude(amount=-groove_depth, mode=Mode.SUBTRACT)

    with BuildSketch(grid.faces().sort_by(Axis.Z).last):
        with Locations((0, groove_depth/2)):
            with GridLocations(
                hole_radius*3, hole_radius*3,
                holes_xcount, holes_ycount,
            ):
                Circle(hole_radius)
            with GridLocations(
                hole_radius*3, hole_radius*3,
                holes_xcount-1, holes_ycount-1,
            ):
                Circle(hole_radius)
    extrude(amount=-thickness, mode=Mode.SUBTRACT)


logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(grid.part)
exporter3d.write("ventilation-grid.3mf")
logging.info("Export done")
