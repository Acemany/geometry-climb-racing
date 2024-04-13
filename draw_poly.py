from pygame import (MOUSEBUTTONDOWN, MOUSEMOTION, MOUSEBUTTONUP, QUIT,
                    display, key, draw, event, font, mouse, time,
                    init, quit as squit,
                    K_ESCAPE,
                    Vector2)


init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
CLOCK = time.Clock()
FONT = font.SysFont('Monospace', 24, bold=True)

points = [Vector2(i) for i in ((0.0, 60.0), (80.0, 60.0), (100.0, 0.0), (180.0, 0.0), (200.0, 60.0), (300.0, 80.0), (300.0, 120.0), (260.0, 120.0), (240.0, 100.0), (220.0, 100.0), (200.0, 120.0), (100.0, 120.0), (80.0, 100.0), (60.0, 100.0), (40.0, 120.0), (0.0, 120.0))]
picked = 0

while 1:
    WIN.fill(0)

    mouse_pos = Vector2(mouse.get_pos())
    keys_pressed = key.get_pressed()

    for e in event.get():
        if e.type == QUIT or keys_pressed[K_ESCAPE]:
            print([list(i) for i in points])
            squit()
            exit()
        elif e.type == MOUSEBUTTONDOWN:
            d = max(*SC_RES)
            for i in points:
                dist = i.distance_to(e.pos)
                if d > dist:
                    d = dist
                    picked = i
        elif e.type == MOUSEMOTION:
            if picked:
                picked.update((mouse_pos+(5, 5))//10*10)
        elif e.type == MOUSEBUTTONUP:
            picked = 0

    for i in points:
        draw.circle(WIN, (0, 216, 0), i, 3)
    draw.polygon(WIN, (0, 255, 0), points, 1)
    WIN.blits([(FONT.render(f"{int(j.x):>5},{int(j.y):<5}", 1, (63, 63, 63)), (25, i*25+25)) for i, j in enumerate(points)])
    display.flip()
    CLOCK.tick(60)
print([i.xy for i in points])
