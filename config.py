from dotenv import load_dotenv
import os

load_dotenv()

# 텔레그램 정보
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

# 반복 주기
INTERVAL_SEC = int(os.getenv('INTERVAL_SEC'))

# 검색 파라미터
SEARCH_PARAMS = os.getenv('SEARCH_PARAMS')
