from io import BytesIO
import requests
import random
import pygame


pygame.init()
screen = pygame.display.set_mode((600, 400))
spn = 0.005

def get_map(spn):
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": '-0.124625,51.500706',
        "spn": ",".join([str(spn), str(spn)]),
        "l": "map",
        "size": "600,400"
    }
    response = requests.get(map_api_server, params=map_params)
    if response.status_code == 200:
        return BytesIO(response.content)
    return

running = True
while running:
    map = get_map(spn)
    if map:
        image = pygame.image.load(map)
        screen.blit(image, (0, 0))
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if spn + 0.005 <= 2:
                    spn += 0.005
            elif event.key == pygame.K_DOWN:
                if spn - 0.005 >= 0.005:
                    spn -= 0.005
pygame.quit()