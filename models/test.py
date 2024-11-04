from build123d import *

length, width, thickness = 80.0, 60.0, 10.0
center_hole_dia = 22.0

with BuildPart() as test:
    Box(length, width, thickness)
    Cylinder(radius=center_hole_dia / 2, height=thickness, mode=Mode.SUBTRACT)

exporter = Mesher()
exporter.add_shape(test.part)
exporter.write("test.3mf")
