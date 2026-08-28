# -*- coding: utf-8 -*-
import json, re, unicodedata, collections, os
from pathlib import Path

BASE = Path(__file__).resolve().parent

DATES = {
"U-Cs4R1yM3g":"2023-09-12","OSnR4RVn99c":"2023-09-17","NIYGzltMSdw":"2023-09-20",
"gZIS-GATJFw":"2023-09-28","HIIR1KROS9w":"2023-10-04","r23hvAEALr4":"2023-10-11",
"XT6ITvtd3TA":"2023-10-18","4vNBqHltAXs":"2023-10-25","R7WkWL1zk2g":"2023-10-29",
"HFY3mVm9fPg":"2023-11-01","E5_kcFeb4w8":"2023-11-08","vAY6SsOvceU":"2023-11-15",
"yPhXfmeiqas":"2023-11-22","MfIv_g9PYSw":"2023-11-29","gg4-SvzmMBg":"2023-12-05",
"h-B3Qz1dL3g":"2023-12-14","8GDyZ9EPPMs":"2023-12-20","RO5OaSqjGOc":"2023-12-25",
"BoT8SjHO5_c":"2023-12-28","d7iaRrAImto":"2024-01-02","uzE5rmdBkK0":"2024-01-10",
"Y7GEnWttyoo":"2024-01-17","yi18oU52mgk":"2024-01-24","DNeSpgRTzbU":"2024-01-31",
"WQxK0NEam2E":"2024-02-07","l8Qp7LVPY0Y":"2024-02-14","14p3fI3IiRU":"2024-02-21",
"7yJEHdZ2qJk":"2024-02-28","OJM1IyrwAbk":"2024-03-09","ZDG_F2w1z8w":"2024-03-13",
"YrwsxnW-aow":"2024-03-20","oH9B9bNB7ks":"2024-03-27","ez2eEOWtex4":"2024-04-01",
"Ec8OAZot2-w":"2024-04-03","4G_l6xvI6vo":"2024-04-17","0O36pmT9TBw":"2024-05-05",
"IiVnwOy_CP0":"2024-05-08","nNjpdHfB70Y":"2024-05-29","igOa9fUQxcg":"2024-06-07",
"CTlYjh1Gy6k":"2024-06-12","IuoVrIn4OcM":"2024-07-07","fzojx27z2Go":"2024-08-27",
"FVWcmKURIWQ":"2024-09-08","BILMZyLkaKA":"2024-10-07","6MrRFAKM814":"2024-11-13",
"7yd-jMk7lIs":"2024-11-15","oc2y-TNCA-g":"2025-01-05","sjJUx-I2Rro":"2025-01-16",
"T4tyP1lqd_E":"2025-01-27","9wtCB53TKo4":"2025-02-21","m0gb_Xt8AsE":"2025-04-07",
"iLbRY5jwGoE":"2025-04-13","Qw3m2ysjEkA":"2025-04-17",
# --- 2025-05 이후 (YouTube 댓글 세트리스트에서 수집) ---
"8BsIBeZZEhY":"2024-02-25","_Q3feRXFUbI":"2025-05-30","gT1ARDYPxPs":"2025-06-07",
"eUkFxmnIIOA":"2025-07-21","k0CMRZ5cYO4":"2025-07-25","pfgyOvyp600":"2025-07-30",
"6TQEyFUOX1Y":"2025-08-04","FuXiow-eVF8":"2025-08-04","z1bLSEcoo7E":"2025-08-09",
"Wreee0go3s4":"2025-08-17","BJCv-gDPdzQ":"2025-08-28","CCjz0q-Rbwk":"2025-10-06",
"nHu9HRo-wXM":"2025-11-06","VUtZTWnGiKY":"2025-11-22","qF7kD6MbBdk":"2026-02-11",
"4flP14V9uRI":"2026-06-29","8JNJ8GYgTQk":"2026-08-07",
# --- 3D LIVE ---
"mt8AyISL9Ig":"2025-04-20","zZ2Ce3eDamU":"2026-04-20",
# --- 릴레이 방송 (사용자 제공 세트리스트) ---
"3Utxr_XKd4c":"2024-12-25","vXA6u6L_quw":"2025-07-20","GoNEvx4LU7U":"2025-12-24",
# --- 동영상 탭 (MV / cover) ---
"_xwOiIMM2a4":"2026-04-20","r_RZPiXYIlk":"2026-04-16","JiuTyDdtedo":"2026-04-08",
"eMG7_WLMLtI":"2026-02-18","CJu--agTZ6Q":"2025-08-31","pTwFsTxsf4w":"2025-08-09",
"PHGOpLwYGtE":"2025-08-04","lpa-OXAukNg":"2025-05-23","_ms0s1x5fa8":"2025-05-06",
"kgCmpVtEx54":"2025-05-05","H5ciKLfRfYQ":"2025-05-04","fEqUb8e66R4":"2025-04-25",
"bYZOxUX_iso":"2024-12-26","rrY_9ugEl04":"2024-10-17","OG7UMECO_fI":"2024-10-17",
"VFvdcfTtBR0":"2024-10-01","OHQ-npgd2Ok":"2024-09-24","YA7QcvdHk70":"2024-08-31",
"FnAk_ZGfvdw":"2024-08-24","efF_c9D-R-A":"2024-08-06","vFDysagoQw0":"2024-06-12",
"VT1on_WaMzw":"2024-04-20","oxZeLM9rx7s":"2024-01-10","BWexRFqs3Wg":"2023-11-15",
"45ZfAdZuaok":"2023-09-09",
# --- 스트림 전수조사에서 발견된 누락 방송 ---
"woCEixptAPY":"2024-03-26","KgEDxIOyQ78":"2025-12-04","bTNx6xRYLrQ":"2025-12-29",
"_8u-fp3L7K0":"2026-01-02","KURAzY1Z7eM":"2026-01-22","zi60qBQOoxQ":"2026-01-31",
"fO2ejfMaS4Q":"2026-03-04","cM9H5jKzU1g":"2026-05-02","a8GYotCWqxs":"2026-05-21",
"eOeMvjGGYoc":"2026-08-28",
}

# ---------- artist canonicalisation ----------
ARTIST_ALIAS = {
 "秦 基博":"秦基博", "奥 華子":"奥華子", "tuki．":"tuki.",
 "ryo (supercell)":"ryo(supercell)", "ryo":"ryo(supercell)",
 "レフティーモンスター":"レフティーモンスターP",
 "新しい学校のリーダー":"新しい学校のリーダーズ",
 "ずっと真夜中でいいのに":"ずっと真夜中でいいのに。",
 "ギガP,可不":"Giga", "想太 feat. 歌愛ユキ":"想太",
 "メル feat. 初音ミク":"メル", "阿良々木月火,井口裕香":"阿良々木月火",
 "TOKOTOKO":"TOKOTOKO(西沢さんP)", "藤井 風":"藤井風",
 "DECO*27，ピノキオピー":"DECO*27", "SEVENTHLINKS feat. flower":"SEVENTHLINKS",
 "ピノキオピー feat. 初音ミク":"ピノキオピー", "みきとP feat. 鏡音リン":"みきとP",
 "泉こなた,柊かがみ,柊つかさ,高良みゆき":"泉こなた, 柊かがみ, 柊つかさ, 高良みゆき",
 "いきものがかり":"いきものがかり", "涼宮ハルヒ":"涼宮ハルヒ",
 # --- 신규 수집분 정규화 ---
 "泰基博":"秦基博",                       # 댓글 오타
 "クリス・ハート":"クリスハート", "ヘブンズP":"Heavenz",
 "koyori(電ポルP)":"電ポルP", "iroha(sasaki)":"iroha (sasaki)",
 "ryo (supercell)":"ryo(supercell)",
 "DECO*27 feat. 初音ミク":"DECO*27", "ツミキ feat. 可不":"ツミキ",
 "Junky feat. 鏡音リン":"Junky", "青木月光 feat. 初音ミク":"青木月光",
 "ポリスピカデリー feat. GUMI":"ポリスピカデリー", "水野あつ feat. 可不":"水野あつ",
 "Guiano feat. 裏命":"Guiano", "月村手毬(小鹿なお)":"月村手毬",
 "DAOKO×米津玄師":"DAOKO × 米津玄師", "sasakure UK":"sasakure.UK",
 "八王子P × Giga":"八王子P", "米津玄師,宇多田ヒカル":"米津玄師 × 宇多田ヒカル",
 "宝鐘マリン＆Kobo Kanaeru":"宝鐘マリン", "奥 華子":"奥華子",
 "瀬戸麻沙美、東山奈央、種﨑敦美、内田真礼、久保ユリカ、水瀬いのり":"青ブタ ヒロインズ",
 "桜島麻衣(瀬戸麻沙美),古賀朋絵(東山奈央),双葉理央(種崎敦美),豊浜のどか(内田真礼),梓川かえで(久保ユリカ),牧之原翔子(水瀬いのり)":"青ブタ ヒロインズ",
 "椎名林檎と宇多田ヒカル":"椎名林檎 × 宇多田ヒカル",
}

# ---------- title canonicalisation ----------
TITLE_ALIAS = {
 "だから僕は音楽を辞めた":"だから僕は音楽をやめた",
 "青空のラプソティ":"青空のラプソディ",
 "月陽-ツキアカリ-":"月陽 -ツキアカリ-",
 "四季折の羽":"四季折の羽",
 "Departures~あなたにおくるアイの歌~":"Departures 〜あなたにおくるアイの歌〜",
 "secret base ～君がくれたもの～":"secret base ~ 君がくれたもの ~",
 "真夜中のドア〜stay With Me":"真夜中のドア〜stay with me",
 "奏(かなで)":"奏", "ぐれいてすと":"GREATEST", "You&aIzu":"You & 合図",
 "You＆合図":"You & 合図", "-ERROR":"-ERROR", "ERROR":"-ERROR",
}

HOLO = {"hololive IDOL PROJECT","ReGLOSS","FLOW GLOW","星街すいせい","宝鐘マリン",
 "常闇トワ","七詩ムメイ","IRyS","AZKi","角巻わため","天音かなた","瀬名航 feat. AZKi",
 "音乃瀬奏","轟はじめ","一条莉々華","儒烏風亭らでん"}

VOCALO = {"ピノキオピー","みきとP","164","じん","ジミーサムP","ポリスピカデリー","40mP",
 "かいりきベア","n-buna","DECO*27","niki","ryo(supercell)","supercell","ナノウ",
 "レフティーモンスターP","蝶々P","傘村トータ","柊マグネタイト","バルーン","Chinozo","Giga",
 "ツミキ","TOKOTOKO(西沢さんP)","Ayase","原口沙輔","Neru","すりぃ","くらげP","ハチ","Kanaria",
 "れるりり","cosMo@暴走P","ぬゆり","syudou","いよわ","Junky","カンザキイオリ","emon(Tes.)",
 "Mitchie M","ナナホシ管弦楽団","電ポルP","れをる","メル","青木月光","想太","OSTER project",
 "DATEKEN","wotaku","弌誠","R Sound Design","ひとしずくP×やま△","iroha (sasaki)","Heavenz",
 "理芽","SEVENTHLINKS","MAISONdes","P.I.N.A.","risou","iroha",
 # --- 신규 수집분 ---
 "電ポルP","雄之助","におP","八王子P","ピコン","r-906","きくお","椎乃味醂","水野あつ",
 "石風呂","Kai","Guiano","はるまきごはん×キタニタツヤ","Giga & TeddyLoid",
 "sasakure.UK","biz×ZERA feat.LOLUET","雨衣","春野","HoneyWorks",
 "wowaka","kemu","ナナホシ管弦楽団","Orangestar","Giga",
 "samfree","有機酸","トーマ","黒うさP","Aqu3ra","てにをは"}

ETC = {"Ayumu Imazu_REMOVED","結束バンド","フランシュシュ","B小町","μ's","Petit Rabbit's","桜高軽音部",
 "後ろから這いより隊G","涼宮ハルヒ","泉こなた, 柊かがみ, 柊つかさ, 高良みゆき","阿良々木月火",
 "エミリア (高橋李依)","逢坂大河, 櫛枝実乃梨, 川嶋亜美","釘宮理恵, 堀江由衣, 喜多村英梨",
 "月村手毬","HIMEHINA","ichigo from 岸田教団&THE明星ロケッツ","Tia","花澤香菜","高橋洋子",
 "鈴木このみ","fripSide","ClariS","EGOIST","木村弓","CHiCO with HoneyWorks",
 "P丸様。","夏代孝明","クマムシ"}

# "그 외 곡"에 남는 항목은 가수 옆에 짧은 설명을 붙인다 (게임명 / 우타이테 / VTuber 등)
ETC_NOTE = {          # UI에서 언어별로 번역되는 코드
 "月村手毬":"@gakumas",
 "夏代孝明":"@utaite",
 "P丸様。":"@utaite",
 "HIMEHINA":"@vtuber",
 "クマムシ":"@comedy",
}

# 애니메이션 타이업(OP/ED/삽입곡/캐릭터송/애니 극장판) — 곡 제목 기준
# 값은 출처 작품명. 드라마·CM·게임 타이업은 제외.
ANIME = {
 # --- 캐릭터송 / 애니 유닛 ---
 "サインはB":"【推しの子】","コネクト":"魔法少女まどか☆マギカ",
 "Departures 〜あなたにおくるアイの歌〜":"ギルティクラウン","当事者":"ギルティクラウン",
 "Daydream cafe":"ご注文はうさぎですか？","Deal with the devil":"賭ケグルイ",
 "only my railgun":"とある科学の超電磁砲","STONE OCEAN":"ジョジョの奇妙な冒険 ストーンオーシャン",
 "Snow halation":"ラブライブ！","Stay Alive":"Re:ゼロから始める異世界生活",
 "佐賀事変":"ゾンビランドサガ","恋は渾沌の隷也":"這いよれ！ニャル子さん",
 "太陽曰く燃えよカオス":"這いよれ！ニャル子さん","いのちの名前":"千と千尋の神隠し",
 "ふわふわ時間":"けいおん！","もってけ！セーラーふく":"らき☆すた",
 "God knows...":"涼宮ハルヒの憂鬱","恋愛サーキュレーション":"化物語",
 "オレンジ":"とらドラ！","This game":"ノーゲーム・ノーライフ",
 "白金ディスコ":"偽物語","残酷な天使のテーゼ":"新世紀エヴァンゲリオン",
 "星座になれたら":"ぼっち・ざ・ろっく！","あのバンド":"ぼっち・ざ・ろっく！",
 "青春コンプレックス":"ぼっち・ざ・ろっく！","ギターと孤独と蒼い惑星":"ぼっち・ざ・ろっく！",
 "世界は恋に落ちている":"アオハライド",
 # --- 실제 아티스트의 애니 타이업 ---
 "クラクラ":"SPY×FAMILY Season 2","残響散歌":"鬼滅の刃 遊郭編",
 "打上花火":"打ち上げ花火、下から見るか？横から見るか？",
 "Catch the Moment":"劇場版 ソードアート・オンライン","紅蓮華":"鬼滅の刃",
 "REALiZE":"スパイダーマン：アクロス・ザ・スパイダーバース",
 "四季ノ唄":"サムライチャンプルー","SOULSOUP":"劇場版 SPY×FAMILY CODE: White",
 "なんでもないや":"君の名は。","スパークル":"君の名は。","RAIN":"メアリと魔女の花",
 "オリオンをなぞる":"TIGER & BUNNY","シュガーソングとビターステップ":"血界戦線",
 "UNDEAD":"〈物語〉シリーズ オフ&モンスターシーズン","アイドル":"【推しの子】",
 "勇者":"葬送のフリーレン","ちゅ、多様性。":"チェンソーマン",
 "青空のラプソディ":"小林さんちのメイドラゴン","U":"竜とそばかすの姫",
 "プラチナ":"カードキャプターさくら","メフィスト":"地獄楽",
 "One Last Kiss":"シン・エヴァンゲリオン劇場版","ひまわりの約束":"STAND BY ME ドラえもん",
 "花になって":"薬屋のひとりごと","DADDY ! DADDY ! DO !":"かぐや様は告らせたい",
 "光るなら":"四月は君の嘘","君じゃなきゃダメみたい":"月刊少女野崎くん",
 "青のすみか":"呪術廻戦 懐玉・玉折","SPECIALZ":"呪術廻戦 渋谷事変",
 "悪魔の子":"進撃の巨人","晴る":"葬送のフリーレン","花に亡霊":"泣きたい私は猫をかぶる",
 "怪獣":"チ。―地球の運動について―","変わらないもの":"時をかける少女",
 "恋をしたのは":"聲の形","KICK BACK":"チェンソーマン",
 "地球儀":"君たちはどう生きるか","orion":"3月のライオン",
 "ピースサイン":"僕のヒーローアカデミア","BOW AND ARROW":"メダリスト",
 # --- 2025-05 이후 수집분에서 추가 ---
 "ミックスナッツ":"SPY×FAMILY","POP IN 2":"【推しの子】","怪物":"BEASTARS",
 "Universe":"ドラえもん のび太の宇宙小戦争2021",
 "不可思議のカルテ":"青春ブタ野郎はバニーガール先輩の夢を見ない",
 "鏡面の波":"宝石の国","愛♡スクリ～ム！":"ラブライブ！",
 # --- 3D LIVE 수록곡 ---
 "火炎":"炎炎ノ消防隊","All Alone With You":"ギルティクラウン",
 "BANG!!!":"ギルティクラウン","give it back":"約束のネバーランド",
 "アカシア":"ポケットモンスター",
 # --- 릴레이 / 동영상 탭에서 추가 ---
 "対象a":"ひぐらしのなく頃に解","IRIS OUT":"チェンソーマン レゼ篇",
 "Bling-Bang-Bang-Born":"マッシュル-MASHLE-","My Dearest":"ギルティクラウン",
 "名前のない怪物":"PSYCHO-PASS",
 # --- 누락 방송에서 추가 ---
 "オトノケ":"ダンダダン","ぼなぺてぃーと♡S":"ブレンド・S",
}

# 제목이 같지만 다른 곡 — 병합 시 가수까지 키에 포함
AMBIGUOUS = {"オレンジ"}

def cat(artist, title):
    if artist in HOLO: return "holo", None
    # 동명이곡은 ANIME 제목 매칭보다 가수 판정을 먼저 적용
    if title in AMBIGUOUS and artist in VOCALO:
        return "vocaloid", None
    if title in ANIME: return "anime", ANIME[title]
    if artist in VOCALO: return "vocaloid", None
    if artist in ETC: return "etc", ETC_NOTE.get(artist)
    return "jpop", None

def norm_title(t):
    t = unicodedata.normalize("NFKC", t)
    t = t.replace("～","~").replace("〜","~").replace("／","/")
    t = re.sub(r"\s+","", t).lower()
    return t

def parse(path):
    rows, vid, live = [], None, None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if not line.strip(): continue
        if line.startswith("#"):
            head = line[1:].strip()
            vid, _, lv = head.partition(" !")
            vid, live = vid.strip(), (lv.strip() or None)
            continue
        sec, entry = line.split(":",1)
        # "×100" 같은 반복 표기 → 가창 횟수로 계산
        rep, m = 1, re.search(r"\s*[×x]\s*(\d+)\s*$", entry)
        if m:
            rep = int(m.group(1)); entry = entry[:m.start()]
        acap = bool(re.search(r"アカペラ", entry))
        # 【…】 블록과 알려진 주석만 제거 (가수명 괄호는 보존)
        entry = re.sub(r"\s*【[^】]*】", "", entry)
        entry = re.sub(r"\s*[（(](?:アカペラ|中断|途中まで|SOLO|一般カラオケ人ver\.)[）)]", "", entry)
        entry = entry.strip()
        title, artist = [x.strip() for x in entry.rsplit("/",1)]
        # 게스트 표기(전각 공백 뒤) 제거
        artist = re.sub(r"　.*$", "", artist)
        artist = re.sub(r"\s*ゲスト[：:].*$", "", artist).strip()
        artist = ARTIST_ALIAS.get(artist, artist)
        title = TITLE_ALIAS.get(re.sub(r"\s+","",title), title)
        rows.append(dict(vid=vid, sec=int(sec), title=title, artist=artist,
                         acap=acap, live=live, rep=rep, date=DATES[vid]))
    return rows

rows = (parse(BASE / "setlists.txt") + parse(BASE / "setlists2.txt")
        + parse(BASE / "setlists3.txt") + parse(BASE / "setlists4.txt")
        + parse(BASE / "setlists5.txt") + parse(BASE / "setlists6.txt")
        + parse(BASE / "setlists7.txt"))
print("performances:", len(rows), "streams:", len({r['vid'] for r in rows}))

# ---------- merge by normalised title ----------
groups = collections.defaultdict(list)
for r in rows:
    k = norm_title(r["title"])
    if r["title"] in AMBIGUOUS: k += "|" + r["artist"]
    groups[k].append(r)

songs = []
for key, perfs in groups.items():
    # 날짜 내림차순, 같은 방송 안에서는 부른 시각 늦은 순
    perfs.sort(key=lambda r: (r["date"], r["sec"]), reverse=True)
    tc = collections.Counter(p["title"] for p in perfs)
    ac = collections.Counter(p["artist"] for p in perfs)
    title  = sorted(tc.items(), key=lambda kv:(-kv[1], len(kv[0])))[0][0]
    artist = sorted(ac.items(), key=lambda kv:(-kv[1], len(kv[0])))[0][0]
    c, src = cat(artist, title)
    # 같은 방송에서 여러 번 부른 경우 몇 번째인지 번호를 매긴다
    per_vid = collections.Counter(p["vid"] for p in perfs)
    ordinal = {}
    for vid, cnt in per_vid.items():
        if cnt < 2: continue
        for i, p in enumerate(sorted((x for x in perfs if x["vid"] == vid),
                                     key=lambda x: x["sec"]), 1):
            ordinal[(vid, p["sec"])] = i
    songs.append(dict(
        title=title, artist=artist, cat=c, src=src,
        n=sum(p["rep"] for p in perfs),
        perfs=[dict(v=p["vid"], t=p["sec"], d=p["date"], a=p["acap"], L=p["live"],
                    r=p["rep"], i=ordinal.get((p["vid"], p["sec"])))
               for p in perfs],
    ))

songs.sort(key=lambda s: (s["perfs"][0]["d"], s["perfs"][0]["t"]), reverse=True)
print("unique songs:", len(songs))
print("by category:", collections.Counter(s["cat"] for s in songs))
json.dump(songs, open(BASE / "songs.json","w",encoding="utf-8"),
          ensure_ascii=False, indent=1)

# artists that fell into jpop bucket, for review
print("\n-- jpop bucket artists --")
print(", ".join(sorted({s["artist"] for s in songs if s["cat"]=="jpop"})))
