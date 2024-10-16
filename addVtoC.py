from pygame import (display, draw, event, font, key, mouse, time,
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT,
                    init, quit as squit,
                    K_ESCAPE,
                    Vector2)
from math import atan2, sin, cos, pi
from sys import exit


def addVtoC(pos: Vector2, rad: float, start: Vector2, end: Vector2, delta: float) -> tuple[float, Vector2]:
    "Move circle with radius rad and position pos from start to end"
    CtoV = start-pos
    VVec = end-start
    move_angle = atan2(*VVec.yx)-atan2(*CtoV.yx)
    return end.distance_to(start)/rad*sin(move_angle)*delta, VVec*abs(cos(move_angle))


init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
FONT = font.SysFont('Monospace', 12, bold=True)
CLOCK = time.Clock()

delta = circle_angle = angular_velocity = 0
velocity = Vector2()
circle_pos = Vector2(200, 400)
circle_radius = 200
offset_rotated = Vector2()
offset = Vector2()
mouse_pos = Vector2()
moving = False

while True:
    WIN.fill(0)

    mouse_pos.update(mouse.get_pos())
    mouse_pressed = mouse.get_pressed()
    keys_pressed = key.get_pressed()
    events = event.get()

    for e in events:
        if e.type == QUIT or keys_pressed[K_ESCAPE]:
            squit()
            exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                offset.update((mouse_pos-circle_pos).rotate(-circle_angle/pi*180))
                if circle_pos.distance_to(mouse_pos) < circle_radius:
                    moving = True
        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                moving = False

    if moving:
        _ = addVtoC(circle_pos, circle_radius, circle_pos+offset_rotated, mouse_pos, delta)
        angular_velocity += _[0]
        velocity += _[1]*delta

    offset_rotated.update(offset.rotate(circle_angle/pi*180))
    circle_angle += angular_velocity
    circle_pos += velocity
    angular_velocity *= 0.9
    velocity *= 0.9

    draw.circle(WIN, (0, 255, 0), circle_pos, circle_radius, 1)
    draw.line(WIN, (0, 255, 0), *(circle_pos+(cos(circle_angle)*circle_radius, sin(circle_angle)*circle_radius),
                                  circle_pos-(cos(circle_angle)*circle_radius, sin(circle_angle)*circle_radius)))
    draw.line(WIN, (0, 255, 0), *(circle_pos+(cos(circle_angle+pi/2)*circle_radius, sin(circle_angle+pi/2)*circle_radius),
                                  circle_pos-(cos(circle_angle+pi/2)*circle_radius, sin(circle_angle+pi/2)*circle_radius)))
    if mouse_pressed[0]:
        draw.line(WIN, (0, 255, 0), circle_pos+offset_rotated, mouse_pos)
        ann = atan2(*(mouse_pos-circle_pos-offset_rotated).yx)
        draw.line(WIN, (0, 255, 0), mouse_pos, mouse_pos+Vector2(cos(ann+pi*1.125), sin(ann+pi*1.125))*10)
        draw.line(WIN, (0, 255, 0), mouse_pos, mouse_pos+Vector2(cos(ann-pi*1.125), sin(ann-pi*1.125))*10)

    display.flip()
    delta = CLOCK.tick(60)/1000
