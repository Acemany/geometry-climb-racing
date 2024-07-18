from pygame import (display, key, draw, event, font, mouse, time,
                    init, quit as squit,
                    K_ESCAPE, QUIT,
                    Vector2)


def orient(a: Vector2, b: Vector2, c: Vector2):
    lin = b-a
    return (lin.y*c.x-lin.x*c.y+b.x*a.y-b.y*a.x)/lin.length()


def collide(cpos: Vector2, cd: int, p1: Vector2, p2: Vector2, p3: Vector2):
    collided = False
    # if 0 > orient(p2, p3, cpos) and\
    #    0 > orient(p3, p1, cpos) and\
    #    cd >= orient(p1, p2, cpos):
    if cpos.distance_to(p1)-cd < max(p1.distance_to(p2), p1.distance_to(p3)) and orient(p2, p3, cpos) < cd and\
       cpos.distance_to(p2)-cd < max(p2.distance_to(p1), p2.distance_to(p3)) and orient(p3, p1, cpos) < cd and\
       cpos.distance_to(p3)-cd < max(p3.distance_to(p1), p3.distance_to(p2)) and orient(p1, p2, cpos) < cd:
        collided = True
        collided = True

    WIN.blit(FONT.render(f"{orient(p1, p2, cpos)}", 0, (63, 63, 63)), (20, 40))
    WIN.blit(FONT.render(f"{orient(p2, p3, cpos)}", 0, (63, 63, 63)), (20, 60))
    WIN.blit(FONT.render(f"{orient(p3, p1, cpos)}", 0, (63, 63, 63)), (20, 80))

    draw.circle(WIN, (255, 16, 32) if collided else (16, 255, 32), cpos, 30, poly_thicness)
    draw.circle(WIN, (255, 0, 0), p1, 5, poly_thicness)
    draw.circle(WIN, (0, 255, 0), p2, 5, poly_thicness)
    draw.circle(WIN, (0, 0, 255), p3, 5, poly_thicness)
    draw.polygon(WIN, (255, 16, 32) if collided else (16, 255, 32), (p1, p2, p3), poly_thicness)


init()
WIN = display.set_mode()
WIDTH, HEIGHT = SC_RES = Vector2(WIN.get_size())
CLOCK = time.Clock()
FONT = font.SysFont('Arial', 24, bold=True)

poly_thicness = 1
mouse_pos = Vector2()

while 1:
    WIN.fill((0, 0, 0))

    mouse_pos.update(mouse.get_pos())
    mouse_pressed = mouse.get_pressed()
    keys_pressed = key.get_pressed()

    if keys_pressed[K_ESCAPE] or event.get(QUIT):
        squit()
        quit()

    collide(mouse_pos, 30, Vector2(150, 150), Vector2(250, 200), Vector2(200, 250))
    WIN.blit(FONT.render(f"{mouse_pos}    {int(CLOCK.get_fps())}", 0, (63, 63, 63)), (20, 20))
    display.flip()
    CLOCK.tick(60)
