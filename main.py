import pygame
import sys
from colors import Colors

pygame.init()

screen_width, screen_height = 500, 620

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Pytris")

clock = pygame.time.Clock()

