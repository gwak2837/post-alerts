## Post Alerts

새 글 알림이

각 사이트 게시판에 새 글이 올라올 때마다 텔레그램으로 알림을 받을 수 있다.



## 사용법

#### 0. 환경 설정

https://sites.google.com/a/chromium.org/chromedriver/downloads

그리고 위 링크에서 자신의 운영체제 및 설치된 크롬 버전에 맞는 크롬 드라이버를 다운받아 루트 경로에 저장한다.

``` shell
> python -m pip install selenium bs4 python-telegram-bot python-dotenv
```

그리고 개발 환경은 `macOS Catalina 10.15.6` `Python 3.8.5 64bit`이고 공통적으로 위와 같은 파이썬 패키지가 필요하다. 위 명령어를 통해 설치한다.

- `selenium` : 파이썬에서 크롬 드라이버를 실행할 수 있다.

- `bs4` : `BeautifulSoup`를 래핑한 패키지로서 html을 파싱하고 특정 태그를 찾아준다.

- `python-telegram-bot` : 텔레그램으로 메시지를 보내는 API를 제공한다.

- `python-dotenv` : 개인 정보를 `.env` 파일에 따로 관리할 수 있다.

#### 1. 텔레그램 봇 생성

BotFather로부터 텔레그램 봇을 생성하고 해당 봇의 토큰을 받아 온다. 봇을 만드는 법은 아래 링크에 자세히 설명되어 있다.

https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html

#### 2. 파일 생성

각 폴더에 `.env` 파일을 생성한다. 거기에 각 프로젝트 별로 필요한 개인 정보를 저장한다. 자세한 사항은 각 프로젝트 설명을 따른다.

#### 3. 실행

각 프로젝트 설명에 따른다.



## 각 폴더 설명

#### 1. `common`

`functions.py` 안에 각 프로젝트에서 공통적으로 쓰이는 함수와 클래스가 있다. 이를 각 프로젝트에서 `import`해서 사용한다.

#### 2. 그 외

각 사이트의 새로운 게시글을 텔레그램으로 보내준다.
