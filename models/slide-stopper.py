import logging
from build123d import *

logging.basicConfig(level=logging.INFO)

thickness, bump_thickness = 2, 1
bump_offset_ratio = 0.73
parts_offset = 1
fixed_y_offset = 3*thickness+2*bump_thickness+parts_offset
width = 12
mobile_length, fixed_length = 16, 22
bump_length = mobile_length/4
screw_diameter, screw_head_diameter = 3, 6

with BuildPart() as mobile:
    with BuildSketch():
        with BuildLine():
            ml1 = Line((0, 0), (mobile_length, 0))
            ml2 = Line(ml1@1, ((ml1@1).X, thickness))
            marc = ThreePointArc(
                ml2@1,
                ((ml2@1).X-bump_length/2, (ml2@1).Y+bump_thickness),
                ((ml2@1).X-bump_length, (ml2@1).Y),
            )
            ml3 = Line(marc@1, (0, (marc@1).Y))
            ml4 = Line(ml3@1, ml1@0)
        make_face()
    extrude(amount=width)
    with Locations(mobile.faces().sort_by(Axis.Y)[-2]):
        # with Locations((0, 0)):
        CounterSinkHole(radius=screw_diameter/2, counter_sink_radius=screw_head_diameter/2)

with BuildPart() as fixed:
    with BuildSketch():
        with BuildLine():
            fl1 = Line((0, fixed_y_offset), (fixed_length, fixed_y_offset))
            fl2 = Line(fl1@1, ((fl1@1).X, fixed_y_offset-2*thickness-bump_thickness))
            fl3 = Line(fl2@1, ((marc@bump_offset_ratio).X, (fl2@1).Y))
            farc = ThreePointArc(
                fl3@1,
                ((fl3@1).X-bump_length/2, (fl3@1).Y-bump_thickness),
                ((fl3@1).X-bump_length, (fl3@1).Y),
            )
            fl4 = Line(farc@1, ((farc@1).X, (farc@1).Y+thickness))
            fl5 = Line(fl4@1, ((fl1@1).X-thickness, (fl4@1).Y))
            fl6 = Line(fl5@1, ((fl5@1).X, (fl5@1).Y+bump_thickness))
            fl7 = Line(fl6@1, (0, (fl6@1).Y))
            fl8 = Line(fl7@1, fl1@0)
        make_face()
    extrude(amount=width)
    with Locations(fixed.faces().sort_by(Axis.Y)[-3]):
        with Locations((4.5, 0)):
            CounterSinkHole(radius=screw_diameter/2, counter_sink_radius=screw_head_diameter/2)

logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(mobile.part)
exporter3d.add_shape(fixed.part)
exporter3d.write("slide-stopper.3mf")
logging.info("Export done")
