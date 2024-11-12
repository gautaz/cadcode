from build123d import *


length, centerToBeak, width, thickness = 70, 42, 7, 9
springThickness, springRadius, springLever = 1.5, 3, 17

polylinePoints = [
    (0.53*centerToBeak, 0),
    (0, 0), # spring center
    (centerToBeak-length, 0.9*width),
    (centerToBeak-length, width),
    (centerToBeak, width),
    (centerToBeak, 0.9*width),
]


with BuildPart() as clothespin:

    with BuildSketch() as profile:
        with BuildLine():
            pl = Polyline(polylinePoints)
            sp = Spline([
                pl@0,
                (0.75*centerToBeak, 0.3*width),
                (0.77*centerToBeak, 0),
            ])
            TangentArc([sp@1, pl@1], tangent=(1, 0))
        make_face()
    extrude(amount=thickness)

    with BuildSketch():
        Circle(springRadius)
    extrude(amount=thickness, mode=Mode.SUBTRACT)

    with BuildSketch(mode=Mode.PRIVATE) as springStroke:
        Circle(springLever)
    springNotchCenter = (
        profile.edges().sort_by(Axis.Y).last
        .find_intersection_points(springStroke.edges().first)
        .sort_by(Axis.X).last
    )

    with Locations(springNotchCenter):
        Box(springThickness+0.5, springThickness, 2*thickness, mode=Mode.SUBTRACT)

    with Locations((centerToBeak/2, 0)):
        Cylinder(springThickness/2, 2*thickness, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(1)):
        with Locations((springRadius*2+1, 0)):
            Rectangle(6, 12)
    extrude(amount=thickness/2-1, mode=Mode.SUBTRACT)

    with BuildSketch(Plane.XY.offset(thickness/2)):
        with Locations((springRadius*2, 0)):
            Rectangle(4, 10)
    extrude(amount=thickness/2-1)


exporter3d = Mesher()
exporter3d.add_shape(clothespin.part)
exporter3d.write("clothespin.3mf")
