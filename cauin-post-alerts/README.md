## cauin-post-alerts

중앙인 새 글 알림이

중앙인에 새 글이 올라올 때마다 해당 글을 텔레그램을 통해 알림을 받을 수 있다.

## 사용법

#### 0. 환경 설정
``` shell
> python -m pip install selenium bs4 python-telegram-bot
```
위 명령어로 필요한 패키지를 설치한다.

https://sites.google.com/a/chromium.org/chromedriver/downloads

그리고 위 링크에서 자신의 운영체제 및 설치된 크롬 버전에 맞는 크롬 드라이버를 다운받아 저장하고, `cauin-post-alerts.py`에서 크롬 드라이버를 불러오는 부분을 해당 경로로 수정한다.

#### 1. 텔레그램 봇 생성

BotFather로부터 텔레그램 봇을 생성하고 해당 봇의 토큰을 받아 온다. 봇을 만드는 법은 아래 링크에 자세히 설명되어 있다.

https://blog.psangwoo.com/coding/2016/12/08/python-telegram-bot-1.html

#### 2. 파일 생성

`cauin-post-alerts.py` 파일과 동일한 경로에 `info.txt` 파일을 생성한다.
그리고 텍스트 파일 각 줄마다 자신의 중앙인 아이디와 패스워드, 텔레그램 봇 토큰을 입력한다. 예시는 아래와 같다.

```
아이디
패스워드
텔레그램 봇 토큰
```

#### 3. 실행

```shell
> python cauin-post-alerts.py
```
