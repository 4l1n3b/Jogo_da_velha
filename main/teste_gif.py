import sys

import pygame
from PIL import Image

size=(600,600)
FORMAT = "RGBA"


def pil_to_game(img):
    data = img.tobytes("raw", FORMAT)
    return pygame.image.fromstring(data, img.size, FORMAT)

def get_gif_frame(img, frame):
    img.seek(frame)
    return  img.convert(FORMAT)


def init():
    return pygame.display.set_mode(size)

def exit():
    pygame.quit()


def main(screen, path_to_image):
    gif_img = Image.open(path_to_image)
    if not getattr(gif_img, "is_animated", False):
        print(f"Imagem em {path_to_image} não é um gif animado")
        return
    current_frame = 0
    clock = pygame.time.Clock()
    while True:
        frame = pil_to_game(get_gif_frame(gif_img, current_frame))
        frame = pygame.transform.scale(frame, size)  # aqui você ajusta para ocupar a tela

        screen.blit(frame, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

        current_frame = (current_frame + 1) % gif_img.n_frames

        pygame.display.flip()
        clock.tick(10)


if __name__ == "__main__":
    try:
        screen = init()
        path = 'imagens\VID-20250915-WA0010(1).gif'
        main(screen, path)
    finally:
        exit()