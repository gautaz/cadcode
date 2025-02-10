import logging
from build123d import *

logging.basicConfig(level=logging.INFO)

ext_base_length, ext_base_width = 17.86, 17.86
ext_top_length, ext_top_width = 13.12, 13.12
ext_base_fillet_radius, ext_top_fillet_radius = 0.75, 1.5

int_base_length, int_base_width = 14.4, 14.4
int_top_length, int_top_width = 11, 11
int_base_fillet_radius, int_top_fillet_radius = 0.4, 0.9

ext_cap_height, int_cap_height = 8.5, 5

junction_diameter = 5.4
ext_cross, int_cross = 4.12, 1.12
cross_chamfer_length = 0.2

f_small, f_medium = 4, 5.5

lab_length_ratio, lab_width_ratio = 0.5, 0.6
labels = [
    ("5", f_medium),
    ("%", f_medium),
    ("F5", f_small),
    ("F17", f_small),
]

with BuildPart() as keycap:
    with BuildSketch():
        RectangleRounded(ext_base_length, ext_base_width, ext_base_fillet_radius)
    with BuildSketch(Plane.XY.offset(ext_cap_height)):
        RectangleRounded(ext_top_length, ext_top_width, ext_top_fillet_radius)
    loft()
    with BuildSketch():
        RectangleRounded(int_base_length, int_base_width, int_base_fillet_radius)
    with BuildSketch(Plane.XY.offset(int_cap_height)):
        RectangleRounded(int_top_length, int_top_width, int_top_fillet_radius)
    loft(mode=Mode.SUBTRACT)
    with BuildSketch():
        Circle(junction_diameter/2)
    extrude(amount=int_cap_height)
    with BuildSketch():
        with BuildLine():
            Polyline([
                (0, ext_cross/2),
                (int_cross/2, ext_cross/2),
                (int_cross/2, int_cross/2),
                (ext_cross/2, int_cross/2),
                (ext_cross/2, 0),
            ])
            mirror(about=Plane.XZ)
            mirror(about=Plane.YZ)
        make_face()
    extrude(amount=int_cap_height, mode=Mode.SUBTRACT)
    chamfer(keycap.edges(Select.LAST).group_by(Axis.Z)[0], cross_chamfer_length)
    with BuildSketch(keycap.faces().group_by(Axis.Z)[-1]) as keycap_labels:
        for index, location in enumerate(GridLocations(
            ext_top_length*lab_length_ratio,
            ext_top_width*lab_width_ratio,
            2,
            2,
        )):
            with Locations(location):
                Text(labels[index][0], font_size=labels[index][1], font="Beon")
    for keycap_label in keycap_labels.sketch.faces():
        add(keycap_label)
        extrude(amount=-ext_cap_height, mode=Mode.SUBTRACT)


logging.info("Exporting...")
exporter3d = Mesher()
exporter3d.add_shape(keycap.part)
exporter3d.write("keycap.3mf")
logging.info("Export done")
