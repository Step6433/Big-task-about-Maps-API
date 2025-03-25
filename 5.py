from io import BytesIO
import requests
import pygame

pygame.init()
screen = pygame.display.set_mode((650, 450))
spn = 0.005
center_x = -0.124625
center_y = 51.500706
coords = '-0.124625,51.500706'
t = 'light'
map_api_server = "https://static-maps.yandex.ru/v1?"
server_geocoder = 'http://geocode-maps.yandex.ru/1.x/?'
api_key_static = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
api_key_geocoder = '8013b162-6b42-4997-9691-77b7074026e0'

def get_map(spn, coords, theme):
    point = f'{coords},pm2rdl'
    map_params = {
        "ll": coords,
        "spn": ",".join([str(spn), str(spn)]),
        "l": "map",
        "size": "650,450",
        'pt': point,
        "theme": theme,
        "apikey": api_key_static
    }
    response = requests.get(map_api_server, params=map_params)
    if response.status_code == 200:
        return BytesIO(response.content)
    return

def get_coords(adres):
    geocoder_request = f'{server_geocoder}apikey={api_key_geocoder}&geocode={adres}&format=json'
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        toponym_coords = toponym["Point"]["pos"]
        return list(map(float, toponym_coords.split()))
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")

font = pygame.font.Font(None, 32)
running = True
flag_text = 0
text = ''
while running:
    m = get_map(spn, coords, t)
    input_rect = pygame.Rect(0, 420, 650, 30)
    if m:
        image = pygame.image.load(m)
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, '#FFFFFF', input_rect)
        text_surf = font.render(text, True, (0, 0, 0))
        screen.blit(text_surf, input_rect)
        pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                flag_text = 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_PAGEUP:
                if spn + 0.005 <= 2:
                    spn += 0.005
            elif event.key == pygame.K_PAGEDOWN:
                if spn - 0.005 >= 0.005:
                    spn -= 0.005
            elif event.key == pygame.K_UP:
                if center_y + 0.002 <= 90:
                    center_y += 0.002
            elif event.key == pygame.K_DOWN:
                if center_y - 0.002 >= -90:
                    center_y -= 0.002
            elif event.key == pygame.K_LEFT:
                if center_x - 0.002 >= -180:
                    center_x -= 0.002
            elif event.key == pygame.K_RIGHT:
                if center_x + 0.002 <= 180:
                    center_x += 0.002
            elif event.key == pygame.K_t:
                if t == 'light':
                    t = 'dark'
                else:
                    t = 'light'
            if flag_text:
                if event.key == pygame.K_RETURN:
                    coords = get_coords(text)
                    coords = f'{coords[0]},{coords[1]}'
                    flag_text = 0
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    text += event.unicode
pygame.quit()