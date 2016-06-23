#!/usr/bin/env python2

import pygame
import math

pygame.display.init()

screen = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()
shutdown = False

def rotate(AnchorX,AnchorY,inputx,inputy, WindDirection):
    x = inputx - AnchorX
    y = inputy - AnchorY
    resultx = (x * math.cos(WindDirection)) - (y * math.sin(WindDirection)) + AnchorX
    resulty = (x * math.sin(WindDirection)) + (y * math.cos(WindDirection)) + AnchorY
    return (resultx,resulty)

class Spaceship:
    def __init__(self):
        self.position = (100, 100)
        self.angle = math.pi
        self.vector = (2,2)

    def update(self):
        self.position = (
            (self.position[0] + self.vector[0]) % 800,
            (self.position[1] + self.vector[1]) % 600,
        )

        self.vector = (
            self.vector[0] * 0.99,
            self.vector[1] * 0.99,
        )

    def accelerate(self):
        new_vector = rotate(0, 0, 0, 0.25, self.angle)
        self.vector = (
            self.vector[0] + new_vector[0],
            self.vector[1] + new_vector[1]
        )

    def render(self, screen):
        pygame.draw.polygon(screen, (255, 255, 255),
                            [
                                rotate(self.position[0], self.position[1], self.position[0], self.position[1] + 10, self.angle),
                                rotate(self.position[0], self.position[1], self.position[0]-7, self.position[1] - 10, self.angle),
                                rotate(self.position[0], self.position[1], self.position[0]+7, self.position[1] - 10, self.angle)
                            ],
                            0)

spaceship = Spaceship()
projectiles = []
asteroids = []

if __name__ == "__main__":
    # Game loop
    while not shutdown:
        # Event handling
        pressed_keys = pygame.key.get_pressed()

        # World update
        spaceship.update()
        for p in projectiles:
            p.update()
        for a in asteroids:
            a.update()

        # Rendering
        screen.fill((0,0,0))
        spaceship.render(screen)
        for p in projectiles:
            p.render(screen)
        for a in asteroids:
            a.render(screen)
        pygame.display.update()

        # Time padding
        clock.tick(30)
