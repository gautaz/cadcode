import logging
from math import ceil, floor
from build123d import *

logging.basicConfig(level=logging.INFO)

width, thickness = 80, 4
eyes = [(-17, 5.5), (-25.5, 2.5)]

def translate_position(position, vector):
    return tuple(sum(x) for x in zip(position, vector))

def translate_positions(positions, vector):
    return [translate_position(position, vector) for position in positions]


with BuildPart() as cat:

    with BuildSketch(Plane.XY.rotated((0, 0, -4.6))):
        with BuildLine():
            Bezier((99.62, 483.0),(103.7, 475.55),(97.7, 462.47),(96.28, 454.0))
            Bezier((96.28, 454.0),(93.36, 436.52),(94.2, 438.75),(94.0, 422.0))
            Bezier((94.0, 422.0),(93.8, 406.03),(80.07, 397.01),(81.04, 380.0))
            Bezier((81.04, 380.0),(81.98, 363.62),(106.39466, 370.23644),(113.0, 365.59))
            Bezier((113.0, 365.59),(160.41358, 325.85073),(196.40241, 340.63727),(211.0, 336.55999999999995))
            Bezier((211.0, 336.55999999999995),(221.48644, 333.01643999999993),(232.62, 316.8299999999999),(244.99, 323.16999999999996))
            Bezier((244.99, 323.16999999999996),(255.15, 328.39),(254.87, 345.18999999999994),(258.03000000000003, 354.99999999999994))
            Bezier((258.03000000000003, 354.99999999999994),(260.49, 362.6499999999999),(263.18, 364.47999999999996),(266.68, 370.99999999999994))
            Bezier((266.68, 370.99999999999994),(269.11, 375.5299999999999),(273.06, 393.18999999999994),(294.0, 394.81999999999994))
            Bezier((294.0, 394.81999999999994),(354.60047, 399.42443999999995),(400.04966, 350.77693999999997),(507.0, 366.7099999999999))
            Bezier((507.0, 366.7099999999999),(533.49496, 368.12846999999994),(534.17535, 342.7241199999999),(582.0, 343.99999999999994))
            Bezier((582.0, 343.99999999999994),(625.89, 343.67999999999995),(666.21, 358.47999999999996),(706.0, 357.99999999999994))
            Bezier((706.0, 357.99999999999994),(724.49585, 357.73875999999996),(738.35758, 335.30055999999996),(752.15, 351.18999999999994))
            Bezier((752.15, 351.18999999999994),(760.697, 361.03527999999994),(755.57774, 374.26172999999994),(753.5699999999999, 378.99999999999994))
            Bezier((753.5699999999999, 378.99999999999994),(742.8597599999999, 401.51132999999993),(710.1281099999999, 406.5148899999999),(687.0, 405.9599999999999))
            Bezier((687.0, 405.9599999999999),(675.68381, 405.4276999999999),(658.38095, 396.81076999999993),(653.25, 411.99999999999994))
            Bezier((653.25, 411.99999999999994),(651.62303, 426.66524999999996),(668.45823, 432.59707999999995),(679.0, 439.05999999999995))
            Bezier((679.0, 439.05999999999995),(733.13489, 472.68875999999995),(743.39365, 518.91545),(693.0, 519.0))
            Bezier((693.0, 519.0),(660.64109, 518.60725),(628.32132, 513.47212),(596.0, 517.29))
            Bezier((596.0, 517.29),(518.11547, 527.78021),(474.18646, 600.65979),(369.0, 600.0))
            Bezier((369.0, 600.0),(264.41304, 590.48259),(226.71723, 556.40199),(145.0, 561.0))
            Bezier((145.0, 561.0),(113.26242, 560.50478),(34.658453, 589.82408),(37.04, 540.0))
            Bezier((37.04, 540.0),(39.652887, 506.6985),(86.892464, 506.29687),(99.62, 483.0))
        make_face()
        mirror(about=Plane.XZ, mode=Mode.REPLACE)
    extrude(amount=thickness)

    width_scale = width / cat.part.bounding_box().size.X
    scale(by=(width_scale, width_scale, 1))
    (x_offset, y_offset, _) = cat.part.center()
    cat.part.move(Location((-x_offset, 3-y_offset, 0)))

    with BuildSketch():
        Ellipse(12, 8)
    extrude(amount=thickness, mode=Mode.SUBTRACT)

    fillet(cat.edges().group_by(Axis.Z)[0], 1)
    fillet(cat.edges().group_by(Axis.Z)[-1], 1)

    with BuildSketch(cat.faces().sort_by(Axis.Z).last):
        with Locations(eyes):
            Circle(3)
    extrude(amount=-thickness/3, mode=Mode.SUBTRACT)

    with BuildSketch(cat.faces().sort_by(Axis.Z).last):
        with Locations(translate_positions(eyes, (-0.3, 1))):
            Circle(1.5)
    extrude(amount=-thickness)


logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(cat.part)
exporter3d.write("reading-ring.3mf")
logging.info("Export done")
