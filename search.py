from urllib.parse import parse_qs

import requests
from bs4 import BeautifulSoup
from requests.adapters import HTTPAdapter
from urllib3 import Retry

import config

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

SERVERS = {
    'scania': 1,
    'bera': 2,
    'luna': 3,
    'zenith': 4,
    'croa': 5,
    'union': 6,
    'elysium': 7,
    'enosis': 8,
    'red': 9,
    'aurora': 10,
    'arcane': 11,
    'nova': 12,
    'reboot1': 13,
    'reboot2': 14,
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Whale/3.25.232.19 Safari/537.36',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
}


def requests_with_retries(method, url, session=None, retries=10, backoff_factor=1,
                          status_forcelist=(500, 502, 503, 504), **kwargs):
    session = session or requests.Session()

    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        allowed_methods=["HEAD", "GET", "OPTIONS", "POST", "PUT", "DELETE", "PATCH"]
    )

    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    session.mount('https://', adapter)

    headers = kwargs.pop('headers', {})
    headers.update(HEADERS)
    kwargs['headers'] = headers

    response = session.request(method, url, **kwargs)

    return response


def search_items():
    url = 'https://xn--hz2b1j494a9mhnwh.com/skin/board/Maple-Basic-List-PC/getList.php'
    data = {k: v[0] if len(v) == 1 else v for k, v in parse_qs(config.SEARCH_PARAMS).items()}
    data['page'] = 1
    items = []
    while True:
        response = requests_with_retries('POST', url, data=data)
        response.raise_for_status()
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        seqs = [int(item['data-xqad']) for item in soup.find_all('li', class_='auction-item')]
        for seq in seqs:
            item = get_item_info(seq, data['bo_table'], data['search_type'])
            items.append(item)
        if len(seqs) < 15:
            break
        data['page'] += 1

    return items


def get_item_info(item_seq, server, item_type):
    url = 'https://xn--hz2b1j494a9mhnwh.com/maple/item_descrip.php'
    if isinstance(server, str):
        server = SERVERS[server]
    params = {'seq': item_seq, 'server': server, 'type': item_type}
    response = requests_with_retries('POST', url, params=params)
    response.raise_for_status()
    return response.json()[0]


def format_item(item):
    result = f'[{item["name"]}'
    if item['use_tuc']:
        result += f' (+{item["use_tuc"]})'
    if item['star']:
        result += f' ⭐{item["star"]}'
    result += ']\n'

    result += f'가격 : {format_number_korean(item["oncePrice"])}\n'
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
