# millionaireuncle.github.io

앱들의 개인정보 처리방침, 계정 삭제 안내, `app-ads.txt`를 두는 GitHub Pages 사이트. 주소는 `https://millionaireuncle.github.io/`.

## 구조

```
index.html                     앱 목록 (스토어의 개발자 웹사이트)
app-ads.txt                    AdMob 판매자 확인. 모든 앱 공용 (AdMob 계정 하나)
assets/site.css                공용 스타일 (라이트·다크)
<앱>/privacy/index.html        ko/로 넘기는 페이지 (예전 주소가 스토어와 앱에 들어가 있다)
<앱>/privacy/ko/index.html     개인정보 처리방침 (한국어)
<앱>/privacy/en/index.html     Privacy Policy (English)
<앱>/privacy/ja/index.html     プライバシーポリシー (日本語)
<앱>/delete-account/...        계정 삭제 안내 (Google Play가 요구, 계정이 있는 앱만). 언어별 폴더는 privacy와 같다
<앱>/licenses/...              오픈소스 라이선스. 언어별 폴더는 privacy와 같다. 언어마다 같은 목록은 _includes/에 두고 include로 넣는다
_includes/<앱>-licenses.html    라이선스 목록 (앱 저장소의 스크립트가 만든다. Flip Voca는 pnpm licenses:page)
```

앱 폴더 이름은 짧은 영문 소문자로 한다(`flipvoca`). 주소가 스토어 등록 정보와 앱 설정 화면에 들어가므로 정한 뒤에는 바꾸지 않는다.

## 새 앱 추가

1. `flipvoca/`를 복사해 새 앱 폴더를 만들고 내용(수집 항목, 처리 위탁, 시행일)을 고친다.
2. `index.html` 앱 목록에 추가한다.
3. 다른 광고 네트워크나 AdMob 계정을 쓰면 `app-ads.txt`에 줄을 더한다.

`main`에 push하면 1분쯤 뒤 반영된다. Jekyll로 빌드하지만, 맨 위에 front matter(`---`)가 없는 파일은 그대로 내보낸다. include를 쓰는 페이지만 front matter에 `layout: null`을 둔다.
