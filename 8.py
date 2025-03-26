from io import BytesIO
import requests
import pygame

pygame.init()
screen = pygame.display.set_mode((650, 590))
spn = 0.005
center_x = -0.124625
center_y = 51.500706
coords = '-0.124625,51.500706'
now_coords = '-0.124625,51.500706'
first_coords = '-0.124625,51.500706'
t = 'light'
map_api_server = "https://static-maps.yandex.ru/v1?"
server_geocoder = 'http://geocode-maps.yandex.ru/1.x/?'
api_key_static = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
api_key_geocoder = '8013b162-6b42-4997-9691-77b7074026e0'


def get_map(spn, coords, now_coords, theme):
    point = f'{now_coords},pm2rdl'
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
    return None


def get_coords(address):
    geocoder_request = f'{server_geocoder}apikey={api_key_geocoder}&geocode={address}&format=json'
    response = requests.get(geocoder_request)
    if response:
        json_response = response.json()
        try:
            toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            toponym_coords = toponym["Point"]["pos"]
            adres = toponym['metaDataProperty']['GeocoderMetaData']['text']
            return [list(map(float, toponym_coords.split())), adres]
        except (KeyError, IndexError):
            print("Объект не найден")
            return None
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        return None


font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
very_small_font = pygame.font.Font(None, 18)
running = True
flag_text = 0
text = ''
adres = ''
res = None
input_rect = pygame.Rect(5, 460, 640, 30)
reset_button = pygame.Rect(400, 500, 250, 30)
adres_rect = pygame.Rect(5, 540, 640, 30)
clock = pygame.time.Clock()
while running:
    m = get_map(spn, coords, now_coords, t)
    if m:
        image = pygame.image.load(m)
        screen.blit(image, (0, 0))
        pygame.draw.rect(screen, 'white', input_rect)
        text_surface = font.render(text, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect.x + 5, input_rect.y + 5))

        pygame.draw.rect(screen, (255, 204, 0), reset_button)
        text_reset_button = small_font.render('Сброс поискового результата', True, (0, 0, 0))
        screen.blit(text_reset_button, (reset_button.x + 5, reset_button.y + 5))

        pygame.draw.rect(screen, 'white', adres_rect)
        text_adres = very_small_font.render(adres, True, 'black')
        screen.blit(text_adres, (adres_rect.x + 5, adres_rect.y + 5))
        pygame.display.flip()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                flag_text = 1
            elif reset_button.collidepoint(event.pos):
                adres = ''
                center_x, center_y = -0.124625, 51.500706
                coords = first_coords
                now_coords = first_coords
                flag_text = 0
            else:
                flag_text = 0
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and flag_text:
                res = get_coords(text)
                if res:
                    center_x, center_y = res[0]
                    coords = f"{center_x},{center_y}"
                    now_coords = coords
                    text = ''
                    adres = res[1]
                    flag_text = 0
            elif event.key == pygame.K_BACKSPACE and flag_text:
                    text = text[:-1]
            elif event.key == pygame.K_PAGEUP:
                spn = min(spn + 0.005, 2.0)
            elif event.key == pygame.K_PAGEDOWN:
                spn = max(spn - 0.005, 0.005)
            elif event.key == pygame.K_UP:
                center_y = min(center_y + 0.002 * spn / 0.005, 90.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_DOWN:
                center_y = max(center_y - 0.002 * spn / 0.005, -90.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_LEFT:
                center_x = max(center_x - 0.002 * spn / 0.005, -180.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_RIGHT:
                center_x = min(center_x + 0.002 * spn / 0.005, 180.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_t:
                if t == 'light':
                    t = 'dark'
                else:
                    t = 'light'
            elif flag_text:
                text += event.unicode
    clock.tick(60)
pygame.quit()