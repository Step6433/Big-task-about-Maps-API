from io import BytesIO
import requests
import pygame
import math

pygame.init()
screen_width, screen_height = 650, 450
screen = pygame.display.set_mode((650, 590))
pygame.display.set_caption("Яндекс Карты")
d = screen_width / screen_height
spn = 0.005
spn1 = spn * d
center_x, center_y = -0.124625, 51.500706
coords = f"{center_x},{center_y}"
now_coords = coords
first_coords = coords
map_theme = 'light'
map_api_server = "https://static-maps.yandex.ru/1.x/"
server_geocoder = 'http://geocode-maps.yandex.ru/1.x/'
api_key_static = 'f3a0fe3a-b07e-4840-a1da-06f18b2ddf13'
api_key_geocoder = '8013b162-6b42-4997-9691-77b7074026e0'


def get_map(x, y, coords, now_coords, theme):
    point = f'{now_coords},pm2rdl'
    map_params = {
        "ll": coords,
        "spn": f"{x},{y}",
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


def get_coords(address, flag_postal):
    params = {
        'apikey': api_key_geocoder,
        'geocode': address,
        'format': 'json'
    }
    response = requests.get(server_geocoder, params=params)
    if response:
        try:
            data = response.json()
            toponym = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            coords = toponym["Point"]["pos"].split()
            address = toponym['metaDataProperty']['GeocoderMetaData']['text']
            if flag_post:
                post = toponym["metaDataProperty"]["GeocoderMetaData"]['Address'].get('postal_code', '')
            else:
                post = ''
            return [list(map(float, coords)), address, post]
        except (KeyError, IndexError):
            print("Ошибка: объект не найден")
    return None


def reverse_geocode(lon, lat, flag_postal):
    params = {
        'apikey': api_key_geocoder,
        'geocode': f"{lon},{lat}",
        'format': 'json'
    }
    response = requests.get(server_geocoder, params=params)
    if response:
        try:
            data = response.json()
            toponym = data["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
            address = toponym['metaDataProperty']['GeocoderMetaData']['text']
            if flag_post:
                post = toponym["metaDataProperty"]["GeocoderMetaData"]['Address'].get('postal_code', '')
            else:
                post = ''
            return address, post
        except (KeyError, IndexError):
            print("Ошибка: объект не найден")
    return None, None


font = pygame.font.Font(None, 32)
small_font = pygame.font.Font(None, 24)
input_rect = pygame.Rect(5, 460, 640, 30)
reset_rect = pygame.Rect(400, 500, 250, 30)
postal_rect = pygame.Rect(5, 500, 390, 30)
address_rect = pygame.Rect(5, 540, 640, 30)
running = True
flag_input = False
flag_post = False
search_text = ''
address_text = ''
clock = pygame.time.Clock()
while running:
    m = get_map(spn1, spn, coords, now_coords, map_theme)
    if m:
        screen.blit(pygame.image.load(m), (0, 0))
    pygame.draw.rect(screen, (255, 255, 255), input_rect)
    pygame.draw.rect(screen, (255, 204, 0), reset_rect)
    if flag_post:
        pygame.draw.rect(screen, (248, 96, 74), postal_rect)
    else:
        pygame.draw.rect(screen, (255, 204, 0), postal_rect)
    pygame.draw.rect(screen, (255, 255, 255), address_rect)
    screen.blit(font.render(search_text, True, (0, 0, 0)), (input_rect.x + 5, input_rect.y + 5))
    screen.blit(small_font.render('Сброс поиска', True, (0, 0, 0)), (reset_rect.x + 5, reset_rect.y + 5))
    if flag_post:
        postal_text = 'Выключить дописывание почтового индекса'
    else:
        postal_text = 'Включить дописывание почтового индекса'
    screen.blit(small_font.render(postal_text, True, (0, 0, 0)), (postal_rect.x + 5, postal_rect.y + 5))
    screen.blit(small_font.render(address_text, True, (0, 0, 0)), (address_rect.x + 5, address_rect.y + 5))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                mouse_pos = event.pos
                if 0 <= mouse_pos[0] <= screen_width and 0 <= mouse_pos[1] <= screen_height:
                    dx = (mouse_pos[0] - screen_width / 2) / screen_width
                    dy = (screen_height / 2 - mouse_pos[1]) / screen_height
                    click_lon = center_x + dx * spn1 * 2
                    y = center_y + dy * spn * 2
                    address, postal = reverse_geocode(click_lon, y, flag_post)
                    if address:
                        now_coords = f"{click_lon},{y}"
                        address_text = f"{address}{', ' + postal if postal else ''}"
                elif input_rect.collidepoint(mouse_pos):
                    flag_input = True
                elif reset_rect.collidepoint(mouse_pos):
                    now_coords = first_coords
                    address_text = ''
                    search_text = ''
                elif postal_rect.collidepoint(mouse_pos):
                    flag_post = not flag_post
            elif event.button == 3:
                if 0 <= event.pos[0] <= 650 and 0 <= event.pos[1] <= 450:
                    dx = (event.pos[0] - 650 / 2) / 650
                    dy = (450 / 2 - event.pos[1]) / 450
                    x = center_x + dx * spn1
                    y = center_y + dy * spn
                    search_text = ''
                    params = {
                        'apikey': 'dda3ddba-c9ea-4ead-9010-f43fbc15c6e3',
                        'text': 'o',
                        'lang': 'ru_RU',
                        "ll": f'{x},{y}',
                        "type": "biz"
                    }
                    try:
                        response = requests.get("https://search-maps.yandex.ru/v1/", params=params)

                        if response.status_code == 200:
                            json_response = response.json()
                            organization = json_response["features"][0]
                            org_name = organization["properties"]["CompanyMetaData"]["name"]
                            org_address = organization["properties"]["CompanyMetaData"]["address"]
                            point = organization["geometry"]["coordinates"]
                            org_point = f"{point[0]},{point[1]}"
                            org_lon, org_lat = map(float, point)
                            distance = math.sqrt((org_lon - x) ** 2 + (org_lat - y) ** 2) * 111.319
                            print(distance)
                            if distance <= 50:
                                now_coords = f"{org_lon},{org_lat}"
                                if org_name:
                                    address_text = f"{org_name}, {org_address}"
                                else:
                                    address_text = org_address
                            else:
                                address_text = "Ближайшая организация дальше 50 метров"
                        else:
                                address_text = "Организации не найдены"
                    except Exception as e:
                        address_text = f"Ошибка: {str(e)}"
        elif event.type == pygame.KEYDOWN:
            if flag_input:
                if event.key == pygame.K_RETURN:
                    result = get_coords(search_text, flag_post)
                    if result:
                        center_x, center_y = result[0]
                        coords = now_coords = f"{center_x},{center_y}"
                        address_text = f"{result[1]}{', ' + result[2] if result[2] else ''}"
                    flag_input = False
                elif event.key == pygame.K_BACKSPACE:
                    search_text = search_text[:-1]
                else:
                    search_text += event.unicode
            elif event.key == pygame.K_PAGEUP:
                spn = max(spn / 1.5, 0.0001)
                spn1 = spn * d
            elif event.key == pygame.K_PAGEDOWN:
                spn = min(spn * 1.5, 90.0)
                spn1 = spn * d
            elif event.key == pygame.K_UP:
                center_y = min(center_y + spn / 3, 90.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_DOWN:
                center_y = max(center_y - spn / 3, -90.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_LEFT:
                center_x = max(center_x - spn1 / 3, -180.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_RIGHT:
                center_x = min(center_x + spn1 / 3, 180.0)
                coords = f"{center_x},{center_y}"
            elif event.key == pygame.K_t:
                if map_theme == 'light':
                    map_theme = 'dark'
                else:
                    map_theme = 'light'
    clock.tick(60)
pygame.quit()