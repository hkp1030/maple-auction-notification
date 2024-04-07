import requests

import config

SEARCH_URL = 'https://xn--hz2b1j494a9mhnwh.com/load_auction_items'


def search_items():
    params = {'s': config.SERVER_NO, 'page': 0, 'c': 0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Whale/3.25.232.19 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    response = requests.post(SEARCH_URL, params=params, data=config.SEARCH_PARAMS, headers=headers)
    return response.json()


def format_item(item):
    result = f'[{item["name"]} (+{item["use_tuc"]}) ⭐{item["star"]}] \n'
    result += f'가격: {format_number_korean(item["onceprice"])}\n'
    result += f'남은 시간: {item["lefttime"]}\n'
    result += f'가위 사용 가능 횟수: {item["karma_count"]}회\n'

    potential = get_potential_level(item['potential1_code'])
    if potential:
        result += f'{potential} 잠재능력: \n'
        result += f'  {item["potential1_descrip"]}\n'
        result += f'  {item["potential2_descrip"]}\n'
        result += f'  {item["potential3_descrip"]}\n'

    additional = get_potential_level(item['potential4_code'])
    if additional:
        result += f'{additional} 에디셔널 잠재능력: \n'
        result += f'  {item["potential4_descrip"]}\n'
        result += f'  {item["potential5_descrip"]}\n'
        result += f'  {item["potential6_descrip"]}\n'

    return result


def format_number_korean(number):
    units = ['', '만', '억', '조', '경']
    result = []
    unit_index = 0

    while number > 0:
        part = number % 10000
        if part > 0:
            result.insert(0, f'{part}{units[unit_index]}')
        number //= 10000
        unit_index += 1

    return ' '.join(result) if result else '0'


def get_potential_level(code):
    code //= 10000
    if code == 1:
        return '레어'
    elif code == 2:
        return '에픽'
    elif code == 3:
        return '유니크'
    elif code == 4:
        return '레전더리'
    else:
        return None
