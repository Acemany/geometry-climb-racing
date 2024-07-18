from pygame import (display, key, draw, event, font, mouse, time,
                    MOUSEBUTTONDOWN, MOUSEBUTTONUP, QUIT,
                    init, quit as squit,
                    K_ESCAPE,
                    Vector2)
from typing import Tuple
from math import atan2, sin, cos, pi


class Circ():
    def __init__(self, pos: Vector2, mass: float = 1000, f: int = 1, radius: int = 20) -> None:
        self.p = pos  # position
        self.pv = Vector2()  # position velocity
        self.m = mass  # mass
        self.a = 0  # angle
        self.r = radius  # angle
        self.av = 0  # angle velocity
        self.w, self.h = self.r, self.r

    def update(self) -> None:
        self.pv += gravity
        # WIN.blit(FONT.render(f"{addVtoC(self.p, self.w/2, self.p+self.lwheel[0].rotate(self.a/pi*180), self.p+self.lwheel[0].rotate((self.a)/pi*180)+self.lwheel[2])}", 0, (63, 63, 63)), (20, 40))
        # WIN.blit(FONT.render(f"{addVtoC(self.p, self.w/2, self.p+self.rwheel[0].rotate(self.a/pi*180), self.p+self.rwheel[0].rotate((self.a)/pi*180)+self.rwheel[2])}", 0, (63, 63, 63)), (20, 60))

        for i, c in enumerate(map_tri):
            draw.circle(WIN, (255, 0, 0), c[0], 5, polythic)
            draw.circle(WIN, (0, 255, 0), c[1], 5, polythic)
            draw.circle(WIN, (0, 0, 255), c[2], 5, polythic)
            # WIN.blit(FONT.render(f"{orient(c[0], c[1], self.p+self.lwheel[0].rotate(self.a))}", 0, (63, 63, 63)), (20 , 100))
            # WIN.blit(FONT.render(f"{orient(c[1], c[2], self.p+self.lwheel[0].rotate(self.a))}", 0, (63, 63, 63)), (20 , 120))
            # WIN.blit(FONT.render(f"{orient(c[2], c[0], self.p+self.lwheel[0].rotate(self.a))}", 0, (63, 63, 63)), (20 , 140))
            if self.p.distance_to(c[0])-self.r < max(c[0].distance_to(c[1]), c[0].distance_to(c[2])) and orient(c[1], c[2], self.p) < self.r and\
               self.p.distance_to(c[1])-self.r < max(c[1].distance_to(c[0]), c[1].distance_to(c[2])) and orient(c[2], c[0], self.p) < self.r and\
               self.p.distance_to(c[2])-self.r < max(c[2].distance_to(c[0]), c[2].distance_to(c[1])) and orient(c[0], c[1], self.p) < self.r:
                cpols.append(c)
                forcto = atan2(*(c[1]-c[0]).yx)-pi/2
                _ = addVtoC(self.p, self.r, self.p, self.p+Vector2(cos(forcto), sin(forcto))*self.r/4+(c[1]-c[0]).normalize(), delta)
                draw.line(WIN, (0, 255, 0), self.p, self.p+Vector2(cos(forcto), sin(forcto))*self.r/4+(c[1]-c[0]).normalize())
                self.av += _[0]
                self.pv += _[1]*delta

        self.p += self.pv
        self.a += self.av
        self.pv /= 1.4
        self.av /= 1.4

    def draw(self) -> None:
        draw.line(WIN, (16, 255, 32), self.p, self.p+Vector2(cos(self.a), sin(self.a))*self.r, polythic)
        draw.circle(WIN, (15, 255, 31), self.p, self.r, polythic)


def orient(a: Vector2, b: Vector2, c: Vector2) -> float:
    lin = b-a
    return (lin.y*c.x-lin.x*c.y+b.x*a.y-b.y*a.x)/lin.length()


def poly_tri(ps: Tuple[Vector2]) -> Tuple[Tuple[Vector2]]:
    "Separate sequence of points to a bunch of triangles"
    out = []
    for a, b in enumerate(ps):
        if a == 0:
            continue
        tdpt = atan2(*(b-ps[a-1]).yx)+pi/2
        out.append((Vector2(ps[a-1]), Vector2(b), (b+ps[a-1])/2+Vector2(cos(tdpt), sin(tdpt))*10))
    return out


def addVtoC(pos: Vector2, rad: float, start: Vector2, end: Vector2, delta: float) -> Tuple[float, Vector2]:
    "Move circle with radius rad and position pos from start to end"
    CtoV = start-pos
    VVec = end-start
    move_angle = atan2(*VVec.yx)-atan2(*CtoV.yx)
    return end.distance_to(start)/rad*sin(move_angle)*delta, VVec*abs(cos(move_angle))


init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
CLOCK = time.Clock()
FONT = font.SysFont('Arial', 24, bold=True)

polyqual = 16
polythic = 1
mapfreq = WIDTH/polyqual
circ = Circ(Vector2(200, HEIGHT/2))
mapr = [Vector2(a*mapfreq, HEIGHT/2+sin(a/1)*100)for a in range(polyqual+1)]
cpols = []
gravity = Vector2(0, 0.1)
offset_rotated = Vector2()
offset = Vector2()
delta = 0
moving = False

while 1:
    WIN.fill((0, 0, 0))

    mouse_pos = Vector2(mouse.get_pos())
    mouse_pressed = mouse.get_pressed()
    keys_pressed = key.get_pressed()

    map_tri = poly_tri(mapr)
    # [mapr.insert(len(mapr)-1, mapr.pop(b))for b, a in enumerate(mapr) if a.x<-5]
    for e in event.get():
        if keys_pressed[K_ESCAPE] or e.type == QUIT:
            squit()
            quit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 1:
                offset.update((mouse_pos-circ.p).rotate(-circ.a/pi*180))
                if circ.p.distance_to(mouse_pos) < circ.r:
                    moving = True
        if e.type == MOUSEBUTTONUP:
            if e.button == 1:
                moving = False

    if moving:
        _ = addVtoC(circ.p, circ.r, circ.p+offset_rotated, mouse_pos, delta)
        circ.av += _[0]
        circ.pv += _[1]*delta

    offset_rotated.update(offset.rotate(circ.a/pi*180))
    circ.update()

    draw .polygon(WIN, (16, 255, 32), (*mapr, SC_RES, (0, HEIGHT)), polythic)
    [draw.polygon(WIN, (16, 255, 32), a, polythic) for a in map_tri]
    [draw.polygon(WIN, (255, 16, 32), a, polythic) for a in cpols]
    circ.draw()
    WIN.blits([(FONT.render(f"{i}", 0, (63, 63, 63)), (20, 20+FONT.get_height()*j))
               for j, i in enumerate((int(CLOCK.get_fps()), mouse_pos, circ.p))])
    display.flip()
    cpols = []
    delta = CLOCK.tick(60)/1000
