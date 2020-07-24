## Post Alerts

새 글 알림이

각 사이트 게시판에 새 글이 올라올 때마다 텔레그램으로 알림을 받을 수 있다.

## 사용법

#### 0. 환경 설정
``` shell
> python -m pip install selenium bs4 python-telegram-bot
```
개발 환경은 `Python 3.8.5 64bit`이고 공통적으로 위와 같은 파이썬 패키지가 필요하다. 위 명령어를 통해 설치한다.

https://sites.google.com/a/chromium.org/chromedriver/downloads

그리고 위 링크에서 자신의 운영체제 및 설치된 크롬 버전에 맞는 크롬 드라이버를 다운받아 루트 경로에 저장한다.

#### 1. 텔레그램 봇 생성

BotFather로부터 텔레그램 봇을 생성하고 해당 봇의 토큰을 받아 온다. 봇을 만드는 법은 아래 링크에 자세히 설명되어 있다.

https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html

#### 2. 파일 생성

각 폴더에 `.env` 파일을 생성한다. 거기에 각 프로젝트 별로 필요한 개인 정보를 저장한다. 자세한 사항은 각 프로젝트 설명을 따른다.

#### 3. 실행

각 프로젝트 설명에 따름

