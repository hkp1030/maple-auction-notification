import time

import requests

import config

SEARCH_URL = 'https://xn--hz2b1j494a9mhnwh.com/load_auction_items'
STAT_NAMES = [
    ('incstr', 'base_incstr', 'rebirthstr', '', 'STR'),
    ('incdex', 'base_incdex', 'rebirthdex', '', 'DEX'),
    ('incint', 'base_incint', 'rebirthint', '', 'INT'),
    ('incluk', 'base_incluk', 'rebirthluk', '', 'LUK'),
    ('incmhp', 'base_incmhp', 'rebirthmhp', '', '최대 HP'),
    ('incmmp', 'base_incmmp', 'rebirthmmp', '', '최대 MP'),
    ('incpad', 'base_incpad', 'rebirthpad', '', '공격력'),
    ('incmad', 'base_incmad', 'rebirthmad', '', '마력'),
    ('incpdd', 'base_incpdd', 'rebirthpdd', '', '방어력'),
    ('incspeed', 'base_incspeed', 'rebirthspeed', '', '이동속도'),
    ('incjump', 'base_incjump', 'rebirthjump', '', '점프력'),
    ('incbdr', 'base_bdr', 'rebirthbdr', '%', '보스 공격력'),
    ('incimdr', 'base_incimdr', None, '%', '몬스터 방어율 무시'),
    ('incdamr', 'base_damr', 'rebirthdamr', '%', '데미지'),
    ('incstatr', 'base_statr', 'rebirthstatr', '%', '올스탯'),
]


def search_items(max_retries=10, retry_delay=2):
    params = {'s': config.SERVER_NO, 'page': 0, 'c': 0}
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Whale/3.25.232.19 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    }
    items = []
    while True:
        try:
            response = requests.post(SEARCH_URL, params=params, data=config.SEARCH_PARAMS, headers=headers)
            response.raise_for_status()
            response_json = response.json() or []
            items += response_json
            if len(response_json) < 30:
                break
            params['page'] += 1
        except requests.RequestException as e:
            max_retries -= 1
            if max_retries == 0:
                raise e
            time.sleep(retry_delay)
            retry_delay *= 2

    return items


def format_item(item):
    result = f'[{item["name"]}'
    if item['use_tuc']:
        result += f' (+{item["use_tuc"]})'
    if item['star']:
        result += f' ⭐{item["star"]}'
    result += ']\n'

    result += f'가격 : {format_number_korean(item["onceprice"])}\n'
    result += f'남은 시간 : {item["lefttime"]}\n'
    result += f'장비 분류 : {item["gear_type_desc"]}\n'

    for stat, base, additional, suffix, name in STAT_NAMES:
        additional = item.get(additional, 0)
        if item[stat]:
            result += f'{name} : {format_option(item[base], additional, item[stat], suffix)}\n'

    upgrade_count = item["total_tuc"] - item["use_tuc"] - item["recover_tuc"]
    result += f'업그레이드 가능 횟수 : {upgrade_count} (복구 가능 횟수 : {item["recover_tuc"]})\n'

    if item['vicioushammer']:
        result += '황금망치 제련 적용\n'

    result += f'가위 사용 가능 횟수 : {item["karma_count"]}회\n'

    potential = get_potential_level(item['potential1_code'])
    if potential:
        result += f'{potential} 잠재능력 : \n'
        result += f'  {item["potential1_descrip"]}\n'
        result += f'  {item["potential2_descrip"]}\n'
        result += f'  {item["potential3_descrip"]}\n'

    additional_potential = get_potential_level(item['potential4_code'])
    if additional_potential:
        result += f'{additional_potential} 에디셔널 잠재능력 : \n'
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


def format_option(base, additional, final, suffix=''):
    base = int(base)
    additional = int(additional)
    final = int(final)
    reinforce = final - base - additional

    if base == final:
        return f'+{final}{suffix}'

    result = f'+{final}{suffix} ({base}{suffix}'
    if additional:
        result += f' +{additional}{suffix}'
    if reinforce:
        result += f' +{reinforce}{suffix}'
    result += ')'

    return result


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
