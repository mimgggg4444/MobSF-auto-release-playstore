


### mobsf


```
여러 대의 디바이스를 준비하고, UI 자동화 도구(Appium)로 앱 다운로드 자동화.
ADB를 사용하여 APK를 추출 후 서버로 전송.
서버에서 MobSF를 이용해 자동 분석 후 취약한 앱 탐색.
```



폴더를 선택
안에 있는 apk파일 전부 mobsf에 업로드.
플레이스토어에 등록될 수 있는 확률 퍼센트지로 나오게.
혹은 몇가지 조건이 충족되면 등록, 혹은 등록 안되게.
등록안될 경우 조건이 충족되지 않은 부분과 보완할 부분 작성될 수 있게.

준비물 - mobsf파일을 자동화 검사할 수 있는 방법, 플레이스토어에 등록될 수 있는 조건, 기존의 mobsf의 결과파일을 수정할 수 있는 방법(mobsf파일 라이브러리를 수정할 수 있어야함.)

월
화
수
목
금
토

월

### first.

install docker

enter the command -> docker pull opensecurity/mobile-security-framework-mobsf:latest

### mobsf를 활용한

```
docker run -it --rm -p 8000:8000 opensecurity/mobile-security-framework-mobsf:latest
```


