from math import (
    floor,
)

from build123d import *

length = 200
thickness = 30
width = 140

handle_length = 100
handle_width = 30
handle_spacing = width/3

wedge_height = 15
wedge_thickness = 4
wedge_hole_width = 10


with BuildPart() as mainframe:
    with BuildSketch():
        RectangleRounded(length, width, radius=handle_width/2)
    extrude(amount=thickness)


with BuildPart(mainframe.faces().sort_by(Axis.Z).first) as handle:
    Box(handle_length, handle_width, thickness)
    with GridLocations(handle_length, 0, 2, 1):
        Cylinder(radius=handle_width/2, height=thickness)


with BuildPart() as wedge:
    with BuildSketch(mainframe.faces().sort_by(Axis.Z).last):
        Rectangle(wedge_thickness, width)
    extrude(amount=wedge_height)


with BuildPart() as wedge_hole_body:
    with BuildSketch(wedge.faces().sort_by(Axis.Z).last):
        Rectangle(wedge_thickness, wedge_hole_width)
    extrude(amount=-wedge_height+wedge_hole_width/2)


with BuildPart(wedge_hole_body.faces().sort_by(Axis.Z).first) as wedge_hole_head:
    Cylinder(radius=5, height=wedge_thickness, rotation=(0, 90, 0))


with BuildPart() as wedge_hole:
    add(wedge_hole_body.part)
    add(wedge_hole_head.part)


with BuildPart() as adjuster:
    add(mainframe.part)
    with Locations((length/4, 0)):
        add(wedge.part)
        with GridLocations(0, 55, 1, 3):
            add(wedge_hole.part, mode=Mode.SUBTRACT)
    with GridLocations(0, handle_spacing, 1, 2):
        add(handle.part, mode=Mode.SUBTRACT)
    fillet(adjuster.edges().group_by(Axis.Z)[0], radius=floor((handle_spacing-handle_width)/2))
    fillet(adjuster.edges().group_by(Axis.Z)[-1], radius=1)


exporter3d = Mesher()
exporter3d.add_shape(adjuster.part)
exporter3d.write("planer-blades-adjuster.3mf")
