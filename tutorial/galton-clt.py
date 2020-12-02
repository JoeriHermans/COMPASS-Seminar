import pygame as pygame
import pymunk as pymunk
import pymunk.pygame_util
import random
import numpy as np

from pygame.color import *
from pygame.key import *
from pygame.locals import *



class Board:

    def __init__(self, intractable=False, num_balls=1000, num_bins=13):
        # Physics
        self._dt = 1 / 120
        self._physics_steps_per_frame = 10
        self._space = self._initialize_space()
        # Render
        ## Initialize the game space
        pygame.init()
        self._resolution = (1000, 1000)
        self._screen = pygame.display.set_mode(self._resolution)
        self._clock = pygame.time.Clock()
        self._draw_options = pymunk.pygame_util.DrawOptions(self._screen)
        # State
        self._complete = False
        self._bins = num_bins
        self._pin = 0
        self._intractable = intractable
        self._balls = [self._allocate_ball() for _ in range(num_balls)]
        # Draw main components of the galton board
        self._allocate_dispenser()
        self._allocate_collector()

    def _allocate_ball(self):
        mass = 10
        radius = 3
        inertia = pymunk.moment_for_circle(mass, 0, radius, (0, 0))
        body = pymunk.Body(mass, inertia)
        x = random.randint(0, 1000)
        y = random.randint(950, 1000)
        body.position = x, y
        shape = pymunk.Circle(body, radius, (0, 0))
        shape.elasticity = 0.0
        shape.friction = 0.0
        self._space.add(body, shape)

        return shape

    def _allocate_pin(self):
        width = 25
        pins_per_row = 1000 / width

        static_body = self._space.static_body
        y = 500
        row = (self._pin // pins_per_row)
        x = (self._pin % pins_per_row) * width
        if row % 2 == 1:
            x += width / 2
        if self._intractable:
            y = 400 + (row * (width * np.sqrt(2))) # Remove to break central limit theorem
        #y = 400 + row * width;
        if y <= 830:
            static_body.position = x, y
            pin = pymunk.Circle(static_body, 6.5)
            pin.elasticity = 0.0
            pin.friction = 0.0
            self._space.add(pin)
            self._pin += 1

    def _allocate_dispenser(self):
        static_body = self._space.static_body
        width = 10
        static_lines = [
            # Top
            pymunk.Segment(static_body, (0.0, 1000.0), (1000.0, 1000.0), 5.0),
            # Sides
            pymunk.Segment(static_body, (0.0, 1000.0), (0.0, 900.0), 5.0),
            pymunk.Segment(static_body, (1000.0, 1000.0), (1000.0, 900.0), 5.0),
            # Funnel
            pymunk.Segment(static_body, (0.0, 950.0), (500 - width, 850.0), 5.0),
            pymunk.Segment(static_body, (1000.0, 950.0), (1000 - 500 + width, 850.0), 5.0)]
        for line in static_lines:
            line.elasticity = 0.95
            line.friction = 0.0
        self._space.add(static_lines)

    def _allocate_collector(self):
        static_body = self._space.static_body
        static_lines = [
            # Bottom
            pymunk.Segment(static_body, (0.0, 0.0), (1000.0, 0), 10.0),
            pymunk.Segment(static_body, (0.0, 0.0), (0.0, 375), 10.0),
            pymunk.Segment(static_body, (1000.0, 0.0), (1000.0, 375), 10.0)]
        # Draw the bin seperators
        pins_to_draw = self._bins - 1
        bin_width = 1000.0 / (self._bins)
        for index in range(pins_to_draw):
            x = index * bin_width + bin_width
            line = pymunk.Segment(static_body, (x, 0.0), (x, 375.0), 2.5)
            static_lines.append(line)
        # Drain energy from the balls
        for line in static_lines:
            line.elasticity = 0.0
            line.friction = 1.0
        self._space.add(static_lines)

    def _clear_screen(self):
        self._screen.fill(THECOLORS["white"])

    def _draw(self):
        self._space.debug_draw(self._draw_options)
        pygame.display.flip()

    def _initialize_space(self):
        space = pymunk.Space()
        space.gravity = (0.0, -900)

        return space

    def _update_balls(self):
        balls_to_remove = [ball for ball in self._balls if ball.body.position.y < 0]
        for ball in balls_to_remove:
            self._space.remove(ball, ball.body)
            self._balls.remove(ball)

    def simulate(self, inputs):
        for _ in range(1000):
            self._allocate_pin()
        while True:
            # Apply physics steps
            for _ in range(self._physics_steps_per_frame):
                self._space.step(self._dt)
            # Update the balls and render
            self._update_balls()
            self._clear_screen()
            self._draw()
            self._clock.tick(100)
            
    
b = Board()
b.simulate()