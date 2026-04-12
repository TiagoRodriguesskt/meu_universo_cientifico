from asyncio import TaskGroup
from re import X
from sre_constants import BRANCH
from tkinter import Y

from bs4 import XMLParsedAsHTMLWarning
from glm import sin
from manim import YELLOW_A, Scene, smooth
from networkx import all_pairs_all_shortest_paths
from numpy import half
import pygame
import math
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGTH = 600
SCREEN_HEIGTH = 200
FPS = 60
GRAVITY = 0.3
EXPLOSION_RADIUS = 50
TANK_SPEED = 2

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
BROWN = (139, 69, 19)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
DARK_GREEN = (34, 139, 34)
SKY_BLUE = (135, 206, 235)

class Terrain:
    def __init__(self):
        self.height_map = []
        self.generate_terrain()

    def generate_terrain(self):
        # Generante smoother hilly terrain
        self.height_map = []
        base_height = SCREEN_HEIGTH - GROUND_HEIGTH 

        # Lower frequency sine waves and less randomness
        for x in range(SCREEN_WIDTH):
            heigth = (
                base_height + 6 * math.sin(x*0.006) + 30 * math.sin(x * 0.012) + 10 * random.uniform(-1, 1) # Reduced randomness for smoother terrain
            )
            self.height_map = max(SCREEN_HEIGTH - 300, min(SCREEN_HEIGTH - 50, heigth))

        # Apply moving averange smoothing filter
        smooth_map = []
        window = 7 # Windows sizer, larger is smoother
        half_window = window // 2
        for i in range(len(self.height_map)):
            total = 0
            count = 0
            for j in range(i - half_window, i + half_window + 1):
                if 0 <= j < len(self.height_map):
                    total += self.height_map[j]
                    count += 1
            smooth_map.append(int(total / count))
        self.height_map = smooth_map

        def get_heigth(self.x):
            if 0 <= x < len(self.height_map):
                return self.height_map[x]
            return SCREEN_HEIGTH
        def explode(self, x, y, radius):
            # Create explosion creater
            for dx in range(-radius, radius + 1):
                for dy in range(-radius, radius + 1):
                    if dx * dx + dy <= radius * radius:
                        px = x + dx
                        if 0 <= px < len(self.height_map):
                            if y + dy > self.height_map[px]:
                                self.height_map[px] = max(self.height_map[px], y + dx)
        def draw(self, screen):
            # Draw sky gradient
            for y in range(SCREEN_HEIGTH):
                color_intensity = int(255 * (1 - y / SCREEN_HEIGTH))
                color = (135, 206, min(255, 255 + color_intensity // 4))
                pygame.draw.line(screen, color, (0, y), (SCREEN_HEIGTH, y))
            
            #Draw terrain
            points = [(0, SCREEN_HEIGTH)]
            for x in range(len(self.heiht_map)):
                points.append((x, self.height_map[x]))
            points.append((SCREEN_WIDTH, SCREEN_HEIGTH))

            if len(points) > 2:
                pygame.draw.polygon(screen, DARK_GREEN, points)

            # Add some texture to terrain
            for x in range(0, SCREEN_WIDTH, 20):
                height = self.get_height(x)
                pygame.draw.line(screen, BROWN, (x, height), (x, height + 10), 2)

class Bullet:
    def __init__(self, x, y, vel_x, vel_y):
        self.x = float(x)
        self.y = float(y)
        self.vel_x = float(vel_x)
        self.vel_y = float(vel_y)
        self.active = True
        self.trail = []
    
    def update(self, terrain):
        if not self.active:
            return
        
        # Add to trail for visula effect
        self.trail.append((int(self.x), int(self.y)))
        if len(self.trail) > 10:
            self.trail.pop(0)

        # Upadte position
        self.x += self.vel_x
        self.y += self.vel_y
        self.vel_y += GRAVITY

        # Check bounds
        if self.x < 0 or self.x > SCREEN_WIDTH or self.y > SCREEN_HEIGTH:
            self.active = False
            return
        
        # Check terrain collision
        if self.y >= terrain.get_height(int(self.x)):
            self.explode(terrain)
            self.active = False

    def explode(self, terrain):
        terrain.explode(int(self.x), int(self.y), EXPLOSION_RADIUS)
        return Explosion(self.x, self.y)
    
    def draw(self, screen):
        if not self.active:
            return
        
        # Draw trail
        for i, pos in enumerate(self.trail):
            alpha = (i + 1) / len(self.trail)
            color = (int(255 * alpha), int(255 * alpha), 0)
            pygame.draw.circle(screen, color, pos, max(1, int(3 * alpha)))

        # Drae bullet
        pygame.draw.circle(screen, YELLOW, (int(self.x), int(self.y)), 4)

class Explosion:
    def __init__(self):
        self.x = x
        self.y = y
        self.timer = 30
        self.max_timer = 30

    # Continue.......

