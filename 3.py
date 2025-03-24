from io import BytesIO
import requests
import random
import pygame


pygame.init()
screen = pygame.display.set_mode((600, 400))
spn = 0.005
center_x  = -0.124625
center_y = 51.500706

def get_map(spn, center_x, center_y):
    map_api_server = "https://static-maps.yandex.ru/1.x/"
    map_params = {
        "ll": f'{center_x},{center_y}',
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
    map = get_map(spn, center_x, center_y)
    if map:
        image = pygame.image.load(map)
        screen.blit(image, (0, 0))
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if spn + 0.005 <= 2:
                    spn += 0.005
            elif event.key == pygame.K_PAGEDOWN:
                if spn - 0.005 >= 0.005:
                    spn -= 0.005
            elif event.key == pygame.K_UP:
                if center_y + 0.005 <= 60:
                    center_y += 0.005
            elif event.key == pygame.K_DOWN:
                if center_y - 0.005 <= -60:
                    center_y -= 0.005
            elif event.key == pygame.K_LEFT:
                if center_x - 0.005 <= -20:
                    center_x -= 0.005
            elif event.key == pygame.K_RIGHT:
                if center_x + 0.005 <= 20:
                    center_x += 0.005
pygame.quit()