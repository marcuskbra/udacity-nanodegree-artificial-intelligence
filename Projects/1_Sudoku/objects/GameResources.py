import os, pygame


def load_image(name):
    """A better load of images."""
    fullname = os.path.join("images", name)
    try:
        image = pygame.image.load(fullname)
        image = image.convert() if image.get_alpha() is None else image.convert_alpha()
    except pygame.error:
        print("Oops! Could not load image:", fullname)
    return image, image.get_rect()
