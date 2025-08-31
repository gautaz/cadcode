from build123d import *

support_width, support_height, support_depth = 100, 40, 20
fillet_radius = 10

bike_support_radius = 10/2
bike_support_spacing = 80
bike_support_distance = support_height/4

# bag_support_tight_radius = 11.4/2
bag_support_radius = 12/2
bag_support_spacing = 80
bag_support_distance = support_height/4

bolt_distance = 60
bolt_radius = 4/2
boldhead_radius = 7/2
nut_radius = 7/2


with BuildPart() as whole:
    with BuildSketch():
        RectangleRounded(width=support_width, height=support_height, radius=fillet_radius)
    extrude(amount=support_depth)
    with BuildSketch():
        with Locations((-bike_support_spacing/2, -bike_support_distance), (bike_support_spacing/2, -bike_support_distance)):
            Circle(bike_support_radius)
    with BuildSketch():
        with Locations((-bag_support_spacing/2, bag_support_distance), (bag_support_spacing/2, bag_support_distance)):
            Circle(bag_support_radius)
    extrude(amount=support_depth, mode=Mode.SUBTRACT)
    with BuildSketch(Plane.ZX.offset(-support_height/2)):
        with Locations((support_depth/2, -bolt_distance/2), (support_depth/2, bolt_distance/2)):
            Circle(bolt_radius)
    extrude(amount=support_height, mode=Mode.SUBTRACT)
    with BuildSketch(whole.faces().sort_by(Axis.Y)[0]):
        with Locations((-bolt_distance/2, 0), (bolt_distance/2, 0)):
            RegularPolygon(radius=nut_radius, side_count=6, major_radius=False)
    extrude(amount=-3, mode=Mode.SUBTRACT)
    with BuildSketch(whole.faces().sort_by(Axis.Y)[-1]):
        with Locations((-bolt_distance/2, 0), (bolt_distance/2, 0)):
            Circle(boldhead_radius)
    extrude(amount=-3, mode=Mode.SUBTRACT)
    fillet(whole.edges().group_by(Axis.Z)[0], radius=1)
    fillet(whole.edges().group_by(Axis.Z)[-1], radius=1)


with BuildPart() as top:
    add(Pos(0, bike_support_distance, 0) * whole.part)
    split(bisect_by=Plane.ZX, keep=Keep.TOP)


with BuildPart() as bottom:
    add(Pos(0, bike_support_distance, 0) * whole.part)
    split(bisect_by=Plane.ZX, keep=Keep.BOTTOM)


with BuildPart() as support:
    add(Pos(0, 10, 0) * top.part)
    add(Pos(0, -10, 0) * bottom.part)


exporter3d = Mesher()
exporter3d.add_shape(support.part)
exporter3d.write("bike-bag-support.3mf")
