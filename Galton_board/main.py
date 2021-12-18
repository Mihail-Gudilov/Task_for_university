import pygame as pg
from random import randrange
import pymunk.pygame_util

# Combining the coordinate systems pygame and pymunk
pymunk.pygame_util.positive_y_is_up = False
# WIDTH - game window width
# HEIGHT - game window height
WIDTH, HEIGHT = 1200, 1000
# Frames Per Second
FPS = 60
# Initialization of game modules
pg.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
# Rename the game window
pg.display.set_caption("Galton board")
clock = pg.time.Clock()
# Option for drawing objects on a screen
draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()
# Gravity on the y=axis
space.gravity = 0, 7000

ball_mass, ball_radius = 300, 4
# Separating wall width
segment_thickness = 5
# a - offset of the tray from the window
# b - vertical part of the tray
# c - half of neck width
# d - neck length (affects the slope in the tray)
a, b, c, d = 20, 90, 15, 50
# Coordinate points
xlt, xln, xrn, xrt = a, WIDTH // 2 - c, WIDTH // 2 + c, WIDTH - a
y_end_vertp, y_end_inclp, y_end_neck, ypeg = b, HEIGHT // 4 - d, HEIGHT // 4, HEIGHT // 2 - 1.5 * b
# Coordinates of left half of the tray
L1, L2, L3, L4 = (xlt, 0), (xlt, y_end_vertp), (xln, y_end_inclp), (xln, y_end_neck)
# Coordinates of right half of the tray
R1, R2, R3, R4 = (xrt, 0), (xrt, y_end_vertp), (xrn, y_end_inclp), (xrn, y_end_neck)
# Coordinates of horizontal platform
B1, B2 = (0, HEIGHT), (WIDTH, HEIGHT)


def create_ball(space):
    """Return a ball with the given characteristics and in the given coordinates."""
    ball_moment = pymunk.moment_for_circle(ball_mass, 0, ball_radius)
    ball_body = pymunk.Body(ball_mass, ball_moment)
    # Generate X-Axis and Y-Axis Positions
    ball_body.position = randrange(xlt, xrt), randrange(0, y_end_vertp)
    ball_shape = pymunk.Circle(ball_body, ball_radius)
    # elastisitty 0.0 - absolutely inelastic body
    # elastisitty 1.0 - absolutely elastic body
    ball_shape.elasticity = 0.5
    # Coulomb friction model
    # Aluminium = 0.61
    ball_shape.friction = 0.61
    space.add(ball_body, ball_shape)
    return ball_body


def create_segment(from_, to_, thickness, space, color):
    """Create segment (wall) with the given characteristics."""
    segment_shape = pymunk.Segment(space.static_body, from_, to_, thickness)
    segment_shape.color = pg.color.THECOLORS[color]
    space.add(segment_shape)


def create_peg(x, y, space, color):
    """Create pegs with the given characteristics."""
    circle_shape = pymunk.Circle(space.static_body, radius=11, offset=(x, y))
    circle_shape.color = pg.color.THECOLORS[color]
    # elastisitty 0.0 - absolutely inelastic body
    # elastisitty 1.0 - absolutely elastic body
    circle_shape.elasticity = 0.4
    # Coulomb friction model
    # Polyethene = 0.61
    circle_shape.friction = 0.2
    space.add(circle_shape)


peg_y, step = ypeg, 60
for i in range(10):
    peg_x = -1.5 * step if i % 2 else -step
    for j in range(WIDTH // step + 2):
        create_peg(peg_x, peg_y, space, 'bisque4')
        if i == 9:
            create_segment((peg_x, peg_y + 50), (peg_x, HEIGHT), segment_thickness, space, 'bisque4')
        peg_x += step
    peg_y += 0.5 * step
# Create platforms, like segments ((x,y),(x,y))
platforms = (L1, L2), (L2, L3), (L3, L4), (R1, R2), (R2, R3), (R3, R4), (L4, (0, 300)), (R4, (WIDTH, 300))
# Create platforms
for platform in platforms:
    create_segment(*platform, segment_thickness, space, 'bisque4')
# Create horizontal platform
create_segment(B1, B2, 20, space, 'bisque4')
# randrange(256) for i in range(3) - generates three values for RGB
balls = [([randrange(256) for i in range(3)], create_ball(space)) for j in range(2600)]
# Game loop
running = True
while running:
    clock.tick(FPS)
    screen.fill(pg.Color('gray'))
    # pg.event.get() - get events from the queue
    for event in pg.event.get():
        if event.type == pg.QUIT:
            exit()
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                running = False
    space.step(1 / FPS)
    space.debug_draw(draw_options)
    [pg.draw.circle(screen, color, (int(ball.position[0]), int(ball.position[1])),
                    ball_radius) for color, ball in balls]

    pg.display.update()
    #
