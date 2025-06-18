from build123d import *

stay_depth = 30

frame_junction_inner_radius = 16
frame_junction_outter_radius = 20

mudguard_junction_outter_width = 52
mudguard_junction_inner_width = 46
mudguard_junction_inner_depth = 18
mudguard_clamp_width = 3

mudguard_inner_radius = 345
mudguard_axial_offset = 45
mudguard_min_frame_distance = 40
mudguard_max_frame_distance = 60
mudguard_link_depth = mudguard_max_frame_distance - mudguard_min_frame_distance

frame_arc = CenterArc(center=(0, 0), radius=frame_junction_outter_radius, start_angle=0, arc_size=180)
left_point = (-mudguard_min_frame_distance, mudguard_junction_outter_width/2)
right_point = (-mudguard_min_frame_distance, -mudguard_junction_outter_width/2)
left_tangent = PointArcTangentLine(point=left_point, arc=frame_arc, side=Side.LEFT)
right_tangent = PointArcTangentLine(point=right_point, arc=frame_arc, side=Side.RIGHT)


with BuildPart() as junction:
    with BuildSketch():
        with BuildLine():
            Line(left_tangent @ 0, left_tangent @ 1)
            Line(left_tangent @ 1, right_tangent @ 1)
            Line(right_tangent @ 1, right_tangent @ 0)
            Line(right_tangent @ 0, left_tangent @ 0)
        make_face()
    extrude(amount=stay_depth)


with BuildPart() as outter_frame_link:
    with BuildSketch():
        Circle(radius=frame_junction_outter_radius)
    extrude(amount=stay_depth)


with BuildPart() as inner_frame_link:
    with BuildSketch():
        Circle(radius=frame_junction_inner_radius)
    extrude(amount=stay_depth)


with BuildPart() as mudguard_link:
    extrude(junction.faces().sort_by(Axis.X)[0], amount=mudguard_link_depth)


with BuildPart() as canevas:
    add(junction.part)
    add(outter_frame_link.part)
    add(inner_frame_link.part, mode=Mode.SUBTRACT)
    add(mudguard_link.part)


with BuildPart() as mudguard_hole:
    with BuildLine(Plane.XZ):
        CenterArc(center=(-mudguard_inner_radius, stay_depth + mudguard_axial_offset), radius=mudguard_inner_radius, start_angle=0, arc_size=-20)
    with BuildSketch(Plane.XY.offset(stay_depth + mudguard_axial_offset)):
        with BuildLine():
            l1 = Line((0, mudguard_clamp_width - mudguard_junction_inner_width / 2), (0, - mudguard_junction_outter_width / 2))
            l2 = Line(l1 @ 1, l1 @ 1 + (-mudguard_link_depth, 0))
            l3 = Line(l2 @ 1, l2 @ 1 + (0, mudguard_junction_outter_width))
            l4 = Line(l3 @ 1, l3 @ 1 + (mudguard_link_depth, 0))
            l5 = Line(l4 @ 1, l4 @ 1 + (0, (mudguard_junction_inner_width - mudguard_junction_outter_width) / 2 - mudguard_clamp_width))
            l6 = Line(l5 @ 1, l5 @ 1 + (mudguard_clamp_width, 0))
            l7 = Line(l6 @ 1, l6 @ 1 + (0, mudguard_clamp_width))
            arc = SagittaArc(l7 @ 1, (mudguard_clamp_width, -mudguard_junction_inner_width/2), sagitta=mudguard_junction_inner_depth)
            l8 = Line(arc @ 1, arc @ 1 + (0, mudguard_clamp_width))
            l9 = Line(l8 @ 1, l1 @ 0)
        make_face()
    sweep()


with BuildPart(Plane.ZX) as bolt_thread:
    Cylinder(radius=3, height=mudguard_junction_outter_width)


with BuildPart() as bolt_head:
    with BuildSketch(Plane.ZX.offset(19)):
        Circle(5)
    extrude(amount=10)


with BuildPart() as nut:
    with BuildSketch(Plane.ZX.offset(-19)):
        RegularPolygon(radius=5, side_count=6, major_radius=False)
    extrude(amount=-10)


with BuildPart() as bolt:
    add(bolt_thread.part)
    add(bolt_head.part)
    add(nut.part)


with BuildPart() as whole:
    add(Pos(mudguard_min_frame_distance, 0, 0) * canevas.part)
    add(Pos(-5, 0, 0) * mudguard_hole.part, mode=Mode.SUBTRACT)
    add(Pos(17, 0, stay_depth/2) * bolt.part, mode=Mode.SUBTRACT)


with BuildPart() as left:
    add(whole.part)
    split(bisect_by=Plane.ZX, keep=Keep.TOP)


with BuildPart() as right:
    add(whole.part)
    split(bisect_by=Plane.ZX, keep=Keep.BOTTOM)


with BuildPart() as stay:
    add(Pos(0, 5, 0) * left.part)
    add(Pos(0, -5, 0) * right.part)


exporter3d = Mesher()
exporter3d.add_shape(stay.part)
exporter3d.write("bike-mudguard-stay.3mf")
