from build123d import *

fillet_radius = 1

inner_stand_junction_radius = 11.7
inner_stand_junction_length = 23
outer_stand_junction_radius = 12.5
outer_stand_junction_length = 26

wheel_junction_radius = 6
outer_wheel_junction_length = 1.5
inner_wheel_junction_length = 15

pin_radius = 3.5

wheel_junction_hole_radius = 3.15
wheel_junction_hole_length = 24
wheel_junction_hole_bump_width = 0.25
wheel_junction_hole_bump_length = 0.5


with BuildPart() as lower_stand_junction:
    with BuildSketch():
        Circle(inner_stand_junction_radius)
    extrude(amount=inner_stand_junction_length)
    fillet(lower_stand_junction.edges().group_by(Axis.Z)[0], radius=fillet_radius)


with BuildPart() as upper_stand_junction:
    with BuildSketch(lower_stand_junction.faces().sort_by(Axis.Z).last):
        Circle(outer_stand_junction_radius)
    extrude(amount=outer_stand_junction_length-inner_stand_junction_length)
    fillet(upper_stand_junction.edges().group_by(Axis.Z)[-1], radius=fillet_radius)


with BuildPart() as wheel_junction:
    stand_plane = Plane(upper_stand_junction.faces().sort_by(Axis.Z).last)
    wheel_plane = stand_plane.move(Location((outer_stand_junction_radius, 0, 0))).rotated((0, 45, 0)).offset(outer_wheel_junction_length)
    with BuildSketch(wheel_plane):
        with Locations((-wheel_junction_radius, 0)):
            Circle(wheel_junction_radius)
    extrude(amount=-(inner_wheel_junction_length+outer_wheel_junction_length))
    fillet(wheel_junction.edges().group_by(Axis.Z)[-1], radius=fillet_radius)


with BuildPart() as pin:
    with BuildSketch(Plane.YZ.offset(outer_stand_junction_radius)):
        with Locations((0, inner_stand_junction_length)):
            Circle(pin_radius)
    extrude(amount=-3)
    fillet(pin.edges().group_by(Axis.X)[-1], radius=fillet_radius)


with BuildPart() as wheel_junction_hole:
    with BuildSketch(wheel_plane):
        with Locations((-wheel_junction_radius, 0)):
            Circle(wheel_junction_hole_radius)
    extrude(amount=-wheel_junction_hole_length)
    with BuildSketch(wheel_plane.offset(-wheel_junction_hole_length)):
        with Locations((-wheel_junction_radius, 0)):
            Circle(wheel_junction_hole_radius-wheel_junction_hole_bump_width)
    extrude(amount=-wheel_junction_hole_bump_length)
    with BuildSketch(wheel_plane.offset(-wheel_junction_hole_length-wheel_junction_hole_bump_length)):
        with Locations((-wheel_junction_radius, 0)):
            Circle(wheel_junction_hole_radius)
    extrude(amount=-20)


with BuildPart() as junction:
    add(lower_stand_junction.part)
    add(upper_stand_junction.part)
    add(wheel_junction.part)
    add(pin.part)
    add(wheel_junction_hole, mode=Mode.SUBTRACT)



exporter3d = Mesher()
exporter3d.add_shape(junction.part)
exporter3d.write("stand-wheel-junction.3mf")
