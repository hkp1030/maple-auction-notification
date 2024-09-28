# 메이플 옥션 알리미

## 소개

메이플스토리 옥션에서 내가 원하는 아이템을 검색하고, 원하는 조건에 맞는 아이템이 올라왔을 때 텔레그램으로 알림을 받을 수 있는 프로그램입니다. 경매장 아이템 정보는 [메이플마켓](https://메이플마켓.com)에서 크롤링합니다.


## 사용법

1. `.env.template` 파일을 복사하여 `.env` 파일을 만듭니다.
2. `.env` 파일에 텔레그램 봇 토큰과 검색할 아이템의 파라미터를 입력합니다.

### 파이썬으로 직접 실행

가상환경을 만들고, 필요한 패키지를 설치합니다.

```bash
$ python -m venv venv
$ source venv/bin/activate
$ pip install -r requirements.txt
```

프로그램을 실행합니다.

```bash
$ python .
```

### 도커로 실행

도커 이미지를 빌드합니다.

```bash
$ docker build -t maple-auction-notifier .
```

도커 컨테이너를 실행합니다.

```bash
$ docker run -d --name maple-auction-notifier maple-auction-notifier
```
