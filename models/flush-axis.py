import logging
from build123d import *

logging.basicConfig(level=logging.INFO)

axis_diameter, axis_length = 5, 95
stop_diameter, stop_length = 10, 2

with BuildPart() as axis:
    with BuildSketch():
        Circle(axis_diameter/2)
    extrude(amount=axis_length)
    with BuildSketch():
        Circle(stop_diameter/2)
    extrude(amount=stop_length)

logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(axis.part)
exporter3d.write("flush-axis.3mf")
