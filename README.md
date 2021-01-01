## Post Alerts

새 글 알림이

각 사이트 게시판에 새 글이 올라올 때마다 텔레그램으로 알림을 받을 수 있다.

## 사용법

#### 환경 설정

https://sites.google.com/a/chromium.org/chromedriver/downloads

위 링크에서 자신의 운영체제 및 설치된 크롬 버전에 맞는 크롬 드라이버를 다운받아 프로젝트 루트 경로(`post-alerts` 폴더 안)에 저장한다.

```shell
> python3 -m pip install --upgrade pip
> python3 -m pip install -r requirements.txt
```

개발 환경은 `macOS Big Sur 11.1` `Python 3.9.1 64bit`이고 공통적으로 위와 같은 파이썬 패키지가 필요하다. 위 명령어를 통해 설치한다.

- `selenium` : 파이썬에서 크롬 드라이버를 실행할 수 있다.

- `bs4` : `BeautifulSoup`를 래핑한 패키지로서 html을 파싱하고 특정 태그를 찾아준다.

- `python-telegram-bot` : 텔레그램으로 메시지를 보내는 API를 제공한다.

- `python-dotenv` : 개인 정보를 `.env` 파일에 따로 관리할 수 있다.

#### 텔레그램 봇 생성

BotFather로부터 텔레그램 봇을 생성하고 해당 봇의 토큰을 받아 온다. 봇을 만드는 법은 아래 링크에 자세히 설명되어 있다.

https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html

#### 파일 생성

각 폴더에 `.env` 파일을 생성한다. 거기에 각 프로젝트 별로 필요한 개인 정보를 저장한다. 자세한 사항은 각 프로젝트 설명을 따른다.

#### 실행

각 프로젝트 설명에 따른다.

## 각 폴더 설명

#### 1. `common`

`functions.py` 안에 각 프로젝트에서 공통적으로 쓰이는 함수와 클래스가 있다. 이를 각 프로젝트에서 `import`해서 사용한다.

#### 2. 그 외

각 사이트의 새로운 게시글을 텔레그램으로 보내준다.

## 공식 문서

#### 1. Selenium (Python)

https://selenium-python.readthedocs.io/index.html

#### 2. Beautiful Soup

https://www.crummy.com/software/BeautifulSoup/bs4/doc/

#### 3. Python Telegram Bot

https://python-telegram-bot.readthedocs.io/en/stable/index.html

#### 4. Python dotenv

https://saurabh-kumar.com/python-dotenv/

## 개발 노트

### 셀레늄 예외

#### `StaleElementReferenceException`

특정 웹 엘리먼트가 변경됐는데 바뀌기 전의 웹 엘리먼트를 참조했을 때 발생한다.

#### `NoSuchElementException`

현재 페이지에서 특정 웹 엘리먼트를 `Timedout` 시간 내에 찾지 못하면 발생한다.

### Element search perfomance

```bash
ID > name > css selector > xpath
```

ID로 검색하는 것이 제일 빠르고 xpath로 검색하는 것이 가장 느리다. 주로 CSS SELECTOR를 이용해 검색한다.

특정 웹 엘리먼트 검색은 `BeautifulSoup`가 `Selenium`보다 빠르다.

하지만 엘리먼트 클릭이나 키 전송, 페이지 이동이 필요할 땐 어쩔 수 없이 `Selenium`을 사용한다.

### 셀레늄 alert 창 처리

```py
# alert = driver.switch_to_alert().accept() - deprecated
alert = driver.switch_to.alert.accept()
```
