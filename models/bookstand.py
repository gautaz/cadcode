import logging
from math import ceil, floor
from build123d import *

logging.basicConfig(level=logging.INFO)

length, height, thickness = 130, 170, 6
externalFilletRatio, internalFilletRatio = 0.6, 0.1

leftBindingCount = 5
rightBindingCount = leftBindingCount+1
bindingCount = leftBindingCount+rightBindingCount
bindingRadius, bindingCoreRadius = thickness/3, 0.8

splineProfile = [
    (0.16, 1),
    (0.24, 0.86),
    (0.15, 0.54),
    (0.32, 0.26),
    (0.64, 0.18),
    (0.84, 0.22),
    (0.87, 0.3),
    (0.82, 0.35),
    (0.87, 0.4),
    (0.98, 0.37),
    (1, 0.29),
    (0.95, 0.2),
    (0.88, 0.1),
    (0.9, 0.05),
    (0.86, 0),
    (0.8, 0.01),
    (0.75, 0.03),
    (0.3, 0.05),
    (0.23, 0.03),
]


with BuildPart() as half_bookstand:
    with BuildSketch() as profile:
        with BuildLine():
            back = Line((0, 0), (0, height))
            Spline(
                [back@1] +
                [(x*length, y*height) for (x, y) in splineProfile] +
                [back@0]
            )
        make_face()

    extrude(amount=thickness)
    fillet(half_bookstand.edges().filter_by(Axis.Z), thickness)
    bindingEdge = half_bookstand.edges().group_by(Axis.X)[0].sort_by(Axis.Z).last
    fillet(half_bookstand.edges().group_by()[0], thickness*externalFilletRatio)
    fillet(half_bookstand.edges().group_by()[-1], thickness*internalFilletRatio)


with BuildPart() as right_binding:
    with Locations(bindingEdge.distribute_locations(
        rightBindingCount,
        start=0.5/bindingCount,
        stop=1-0.5/bindingCount,
    )):
        Cylinder(
            bindingRadius,
            bindingEdge.length/bindingCount,
        )


with BuildPart() as left_binding:
    with Locations(bindingEdge.distribute_locations(
        leftBindingCount,
        start=1.5/bindingCount,
        stop=1-1.5/bindingCount,
    )):
        Cylinder(
            bindingRadius,
            bindingEdge.length/bindingCount,
        )


with BuildPart() as binding_core:
    with Locations(bindingEdge.center()):
        Cylinder(
            bindingCoreRadius,
            height,
            rotation=(90, 0, 0),
        )


with BuildPart() as left_bookstand:
    add(half_bookstand.part)
    add(left_binding.part)
    add(right_binding.part, mode=Mode.SUBTRACT)
    add(binding_core.part, mode=Mode.SUBTRACT)


with BuildPart() as right_bookstand:
    add(half_bookstand.part)
    add(right_binding.part)
    add(left_binding.part, mode=Mode.SUBTRACT)
    add(binding_core.part, mode=Mode.SUBTRACT)


with BuildPart() as bookstand:
    left = mirror(left_bookstand.part, about=Plane.YZ.offset(-bindingRadius-1))
    add(right_bookstand.part)
    frontBB = left.bounding_box()
    frontCover = left.faces().sort_by(Axis.Z).first
    with BuildSketch(frontCover) as front_cover:
        with Locations((frontBB.size.X/6, frontBB.size.Y/4.2)):
            Text(
                "Margaux, Joyeux Noël 2024 !",
                font_size=thickness,
                rotation=180,
                align=(Align.MIN, Align.CENTER),
            )
    extrude(amount=-0.5, mode=Mode.SUBTRACT)


logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(bookstand.part)
exporter3d.write("bookstand.3mf")
logging.info("Export done")
