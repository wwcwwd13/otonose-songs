# otonose-songs handoff

音乃瀬奏의 노래/가라오케 이력을 정적 HTML로 제공하는 작은 데이터 프로젝트다.
새 방송의 세트리스트를 추가하거나 기존 타임스탬프를 고치는 일이 주된 작업이다.

## 파일 역할

- `setlists.txt` ~ `setlists7.txt`: 사람이 편집하는 원본 세트리스트.
- `build.py`: 원본을 읽어 곡을 정규화하고 `songs.json`을 생성한다.
- `songs.json`: 생성 산출물. 직접 수정하지 않는다.
- `gen_html.py`: `songs.json`을 포함한 정적 페이지 `kanade_karaoke_library.html`을 생성한다.
- `index.html`: 실제로 추적되는 배포용 HTML. 생성된 `kanade_karaoke_library.html`의 내용과 같아야 한다.

## 새 방송 추가 절차

1. YouTube ID와 방송일(`YYYY-MM-DD`)을 `build.py`의 `DATES`에 추가한다.
2. 적절한 `setlists*.txt`의 끝에 다음 형식으로 세트리스트를 추가한다. 최근 수집분은 현재 `setlists7.txt`에 이어 붙이고 있다.

   ```text
   #VIDEO_ID
   232:곡명 / 아티스트
   514:곡명 / 아티스트
   ```

   시간은 초 단위 정수다. 예를 들어 `0:03:52`는 `232`, `1:10:41`은 `4241`이다.
   라이브/영상 레이블은 헤더에 `#VIDEO_ID !L|label` 또는 `#VIDEO_ID !V|label`처럼 붙일 수 있다.
3. Windows PowerShell에서는 UTF-8 출력을 지정해 빌드한다.

   ```powershell
   $env:PYTHONIOENCODING='utf-8'
   python build.py
   python gen_html.py
   Copy-Item -LiteralPath kanade_karaoke_library.html -Destination index.html -Force
   Remove-Item -LiteralPath kanade_karaoke_library.html -Force
   ```

4. `songs.json`과 `index.html` 모두에 새 영상 ID가 들어갔는지 확인하고, 원본 및 생성 산출물을 함께 커밋한다.

## 수정 규칙과 주의점

- 타임스탬프 오류는 해당 `setlists*.txt`의 숫자만 고친 뒤 위 절차로 다시 생성한다. `songs.json`이나 `index.html`을 수동으로 고치지 않는다.
- 곡명/아티스트 표기는 원본 세트리스트에 기록한다. `build.py`의 `TITLE_ALIAS`, `ARTIST_ALIAS`, 카테고리 집합(`HOLO`, `VOCALO`, `ETC`)과 `ANIME`가 통합 제목, 표기, 분류를 결정한다.
- 기존 곡은 제목 정규화 후 자동으로 하나의 곡 이력으로 합쳐진다. 동일 제목이지만 서로 다른 곡인 경우는 `AMBIGUOUS` 규칙을 확인한다.
- `gen_html.py`는 기본적으로 `index.html`이 아니라 임시 산출물 `kanade_karaoke_library.html`을 만든다. 위의 복사 단계를 빠뜨리면 실제 사이트 데이터는 갱신되지 않는다.
- 기본 Windows 콘솔 인코딩(CP949)에서는 `build.py`의 일본어 출력이 실패할 수 있다. `PYTHONIOENCODING=utf-8`을 지정하면 정상 완료된다.
- UTF-8로 파일을 읽고 쓴다. PowerShell로 일본어 내용을 확인할 때는 `Get-Content -Encoding utf8`을 사용한다.

## 최근 기준 상태 (2026-09-01)

- 브랜치: `main`
- 최근 방송 추가: `eOeMvjGGYoc` / 2026-08-28 / 10곡 (`setlists7.txt`)
- 최근 타임스탬프 정정: `Wreee0go3s4`의 `Universe`는 `4241`, `鱗`은 `4761`으로 수정됨.

## 빠른 검증 예시

```powershell
git status --short
Select-String -Path songs.json,index.html -Pattern 'VIDEO_ID'
```

새 방송에 대해 두 파일 모두에서 영상 ID가 기대한 곡 수만큼 검출되는지 확인한다.
