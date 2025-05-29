from math import (
    floor,
)

from build123d import *

length = 200
thickness = 20
width = 140

handle_length = 100
handle_width = 30
handle_spacing = width/3

axis_wedge_height = 15
axis_wedge_thickness = 4.4
axis_wedge_hole_height = axis_wedge_height - 4
axis_wedge_hole_width = 10

blade_wedge_height = 1
blade_wedge_width = 18


with BuildPart() as mainframe:
    with BuildSketch():
        RectangleRounded(length, width, radius=15)
    extrude(amount=thickness)


with BuildPart() as axis_wedge:
    with BuildSketch(mainframe.faces().sort_by(Axis.Z).last):
        Rectangle(axis_wedge_thickness, width)
    extrude(amount=axis_wedge_height)


with BuildPart() as axis_wedge_hole_body:
    with BuildSketch(axis_wedge.faces().sort_by(Axis.Z).last):
        Rectangle(axis_wedge_thickness, axis_wedge_hole_width)
    extrude(amount=-axis_wedge_hole_height+axis_wedge_hole_width/2)


with BuildPart(axis_wedge_hole_body.faces().sort_by(Axis.Z).first) as axis_wedge_hole_head:
    Cylinder(radius=5, height=axis_wedge_thickness, rotation=(0, 90, 0))


with BuildPart() as axis_wedge_hole:
    add(axis_wedge_hole_body.part)
    add(axis_wedge_hole_head.part)


with BuildPart() as blade_wedge:
    with BuildSketch(mainframe.faces().sort_by(Axis.Z).last):
        Rectangle(blade_wedge_width, width)
    extrude(amount=blade_wedge_height)


with BuildPart() as adjuster:
    add(mainframe.part)
    with Locations((length/4, 0)):
        add(axis_wedge.part)
        with GridLocations(0, 55, 1, 3):
            add(axis_wedge_hole.part, mode=Mode.SUBTRACT)
    with Locations((length/4-(blade_wedge_width+axis_wedge_thickness)/2, 0)):
        add(blade_wedge.part)
    fillet(adjuster.edges().group_by(Axis.Z)[0], radius=10)
    fillet(adjuster.edges().group_by(Axis.Z)[-1], radius=1)


exporter3d = Mesher()
exporter3d.add_shape(adjuster.part)
exporter3d.write("planer-blades-adjuster.3mf")
