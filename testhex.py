def pygame_colours():
    while True:
        yield 255, 0, 0 # red
        yield 255, 255, 0 # yellow
        yield 0, 0, 255 # blue
        yield 0, 255, 0 # green
def pygame_hex():
    '''Requires PyGame 1.8 or better to save as PNG'''
    import pygame
    pygame.init()
    screen = pygame.display.set_mode((IMAGE_WIDTH, IMAGE_HEIGHT))
    colours = pygame_colours()
    for x,y in hex_centres():
        pygame.draw.polygon(screen, colours.next(), list(hex_points(x,y)))
