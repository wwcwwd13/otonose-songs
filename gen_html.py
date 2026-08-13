# -*- coding: utf-8 -*-
import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
songs = json.loads((BASE / "songs.json").read_text(encoding="utf-8"))
data = json.dumps(songs, ensure_ascii=False, separators=(",", ":"))

n_perf = sum(s["n"] for s in songs)
n_stream = len({p["v"] for s in songs for p in s["perfs"]})
dates = sorted(p["d"] for s in songs for p in s["perfs"])

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title id="page-title"></title>
<style>
:root{
  --bg:#12101a; --bg2:#1a1726; --card:#211d2f; --card2:#282338;
  --line:#332c47; --txt:#ece9f5; --dim:#9b93b5; --dim2:#6f6889;
  --accent:#ffd45e; --accent2:#c9a3ff;
  --c-jpop:#5ec8ff; --c-vocaloid:#7de2c3; --c-holo:#ffd45e;
  --c-anime:#ffa878; --c-etc:#b9aee0;
}
*{box-sizing:border-box}
html,body{margin:0;padding:0}
body{
  background:radial-gradient(1200px 600px at 50% -10%,#2a2140 0%,var(--bg) 60%) no-repeat,var(--bg);
  color:var(--txt);
  font-family:"Segoe UI","Malgun Gothic","Hiragino Kaku Gothic ProN","Yu Gothic UI",
    "Noto Sans KR","Noto Sans JP",system-ui,sans-serif;
  font-size:15px; line-height:1.55; -webkit-font-smoothing:antialiased;
}
a{color:inherit}
.wrap{max-width:1000px;margin:0 auto;padding:0 18px 80px}

header{padding:16px 0 16px;text-align:center}
h1{margin:0;font-size:27px;letter-spacing:-.02em;font-weight:700}
h1 .jp{color:var(--accent)}
.range{margin:-1px 0 0;color:var(--dim2);font-size:12px;letter-spacing:.03em}
.langs{justify-content:flex-end;margin-bottom:14px}
.chip.lang{font-size:12px;padding:5px 12px}
.stats{display:flex;justify-content:center;gap:26px;margin:12px 0 0;flex-wrap:wrap}
.stat{line-height:1.2}
.stat b{display:block;font-size:22px;color:var(--accent2);font-variant-numeric:tabular-nums}
.stat span{font-size:11.5px;color:var(--dim2);letter-spacing:.04em}

.controls{
  position:sticky;top:0;z-index:20;padding:12px 0;
  background:linear-gradient(var(--bg) 62%,rgba(18,16,26,.86));
  backdrop-filter:blur(8px);border-bottom:1px solid var(--line);margin-bottom:16px;
}
.row{display:flex;gap:9px;flex-wrap:wrap;align-items:center}
.row+.row{margin-top:9px}
.filterrow{align-items:flex-start}
.chips{display:flex;gap:9px;flex-wrap:wrap;flex:1 1 auto;min-width:0}
.filterrow select{flex:0 0 auto;margin-left:auto;padding:5px 9px;font-size:12.5px;
  border-radius:999px;color:var(--dim)}
.filterrow select:hover{color:var(--txt);border-color:var(--dim2)}
input[type=search]{
  flex:1 1 100%;min-width:180px;background:var(--card);border:1px solid var(--line);
  color:var(--txt);border-radius:9px;padding:9px 12px;font:inherit;font-size:14px;
}
input[type=search]:focus{outline:none;border-color:var(--accent2)}
select{
  background:var(--card);border:1px solid var(--line);color:var(--txt);
  border-radius:9px;padding:9px 11px;font:inherit;font-size:13.5px;cursor:pointer;
}
select:focus{outline:none;border-color:var(--accent2)}
.chip{
  background:var(--card);border:1px solid var(--line);color:var(--dim);
  border-radius:999px;padding:6px 13px;font-size:12.5px;cursor:pointer;
  transition:.14s;white-space:nowrap;
}
.chip:hover{color:var(--txt);border-color:var(--dim2)}
.chip.on{background:var(--accent2);border-color:var(--accent2);color:#1a1226;font-weight:600}
.chip .n{opacity:.65;margin-left:5px;font-size:11px}

.count{color:var(--dim2);font-size:12.5px;margin:0 0 10px}

.song{
  background:var(--card);border:1px solid var(--line);border-radius:10px;
  margin-bottom:5px;
}
.song:hover{border-color:#453c5f}
.song details{margin:0}
.song summary{list-style:none}
.song summary::-webkit-details-marker{display:none}

.top{
  display:grid;grid-template-columns:minmax(0,1fr) 112px 62px 136px;
  gap:10px;align-items:center;padding:7px 12px 7px 14px;
}
summary.top{cursor:pointer;user-select:none}
.meta{min-width:0}
.title{font-size:14.5px;font-weight:600;letter-spacing:-.01em;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.artist{color:var(--dim);font-size:12px;margin-top:1px;
  white-space:nowrap;overflow:hidden;text-overflow:ellipsis}

.col-cat{text-align:center}
.tag{font-size:10.5px;padding:2px 7px;border-radius:999px;border:1px solid;
  font-weight:600;white-space:nowrap}
.tag.jpop{color:var(--c-jpop);border-color:#2b5f7d;background:#12303f}
.tag.vocaloid{color:var(--c-vocaloid);border-color:#2c6b5a;background:#123029}
.tag.holo{color:var(--c-holo);border-color:#7a642a;background:#3a2f13}
.tag.anime{color:var(--c-anime);border-color:#7d4c30;background:#3d2417;cursor:help}
.tag.etc{color:var(--c-etc);border-color:#4d4470;background:#262040}
.src{color:var(--c-anime);opacity:.72;font-size:11.5px}
.src.etc{color:var(--c-etc);opacity:.8}
.src::before{content:"· ";color:var(--dim2);opacity:.8}

.col-n{text-align:right;font-size:12px;color:var(--dim2);
  font-variant-numeric:tabular-nums;white-space:nowrap}
summary.top .col-n{color:var(--dim)}
summary.top:hover .col-n{color:var(--accent2)}
.col-n .car{display:inline-block;width:9px;color:var(--dim2)}
.col-n .car::before{content:"▸"}
details[open] .col-n .car::before{content:"▾"}

.play{
  display:flex;align-items:center;justify-content:center;gap:6px;
  background:linear-gradient(180deg,#ffdd7a,#f2bd35);color:#241a05;
  border-radius:7px;padding:6px 9px;font-size:12px;font-weight:700;
  text-decoration:none;white-space:nowrap;box-shadow:0 1px 0 #00000030;
}
.play:hover{filter:brightness(1.07)}
.play .ic{font-size:9px}

.past{margin:0 12px 9px 14px;padding:5px 8px;background:var(--bg2);
  border-radius:8px;border:1px solid var(--line);
  display:flex;flex-direction:column;gap:1px}
.past a{
  color:var(--dim);font-size:12px;text-decoration:none;padding:3px 6px;
  border-radius:5px;display:flex;justify-content:space-between;gap:10px;
}
.past a:hover{color:var(--txt);background:var(--card2)}
.past a.new{color:var(--accent)}
.past .ago{color:var(--dim2);font-size:11px;font-variant-numeric:tabular-nums}
.past .pin{font-size:10px;color:var(--accent);border:1px solid #7a642a;
  background:#3a2f13;border-radius:999px;padding:0 6px;margin-left:6px}
.live{font-size:10px;color:#8fd9ff;border:1px solid #2b5f7d;background:#12303f;
  border-radius:999px;padding:0 6px;margin-left:6px;font-weight:600}
.live.vid{color:#c9a3ff;border-color:#4d3f75;background:#241b3d}
.rep{font-size:10px;color:#ff9ec4;border:1px solid #7d3a58;background:#3d1a2a;
  border-radius:999px;padding:0 6px;margin-left:6px;font-weight:700}
.acap{font-size:10px;color:var(--c-anime);margin-left:5px}

.empty{text-align:center;color:var(--dim2);padding:60px 0;font-size:14px}
footer{margin-top:40px;padding-top:20px;border-top:1px solid var(--line);
  color:var(--dim2);font-size:12px;text-align:center;line-height:1.9}
footer a{color:var(--dim);text-decoration:none;border-bottom:1px dotted var(--dim2)}
footer a:hover{color:var(--accent2)}
.made{display:inline-block;margin-top:8px;color:#5d5677;font-size:11px;letter-spacing:.02em}
@media(max-width:640px){
  h1{font-size:21px}
  .top{grid-template-columns:minmax(0,1fr) 56px 118px;
       grid-template-areas:"meta n play" "cat cat cat";row-gap:5px}
  .meta{grid-area:meta} .col-n{grid-area:n} .play{grid-area:play}
  .col-cat{grid-area:cat;text-align:left}
}
</style>
</head>
<body>
<div class="wrap">

<header>
  <div class="row langs" id="langs"></div>
  <h1 id="page-heading"><span id="title-prefix"></span><span class="jp" id="title-name"></span><span id="title-rest"></span></h1>
  <p class="range">__RANGE__</p>
  <div class="stats">
    <div class="stat"><b>__NSONG__</b><span></span></div>
    <div class="stat"><b>__NPERF__</b><span></span></div>
    <div class="stat"><b>__NSTREAM__</b><span></span></div>
  </div>
</header>

<div class="controls">
  <div class="row">
    <input type="search" id="q">
  </div>
  <div class="row filterrow">
    <div class="chips" id="chips"></div>
    <select id="sort"></select>
  </div>
</div>

<p class="count" id="count"></p>
<div id="list"></div>

<footer id="foot"></footer>
</div>

<script>
const SONGS = __DATA__;

/* ============================================================
   다국어 — 여기만 고치면 문구가 바뀝니다.
   DEFAULT_LANG 를 "ko" / "ja" / "en" 중 하나로 바꾸면 기본 언어가 변경됩니다.
   ============================================================ */
/* DEFAULT_LANG: "auto" = 브라우저/OS 언어 자동 감지, 또는 "ja"/"ko"/"en"/"id" 로 고정 */
const DEFAULT_LANG  = "auto";
const FALLBACK_LANG = "ja";        // 자동 감지 실패 시
const LANG_ORDER    = ["ja","ko","en","id"];   // 버튼 표시 순서
const MON_EN = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"];
const MON_ID = ["Januari","Februari","Maret","April","Mei","Juni","Juli","Agustus",
                "September","Oktober","November","Desember"];

const I18N = {
  ko: {
    label:"한국어",
    title:"오토노세 카나데 노래 모음",
    titlePrefix:"", titleName:"오토노세 카나데", titleRest:" 노래 모음",
    sub:"Otonose Kanade · 노래방송 세트리스트 아카이브",
    st:["곡","가창 횟수","방송 · 동영상"],
    search:"곡 제목 · 가수 검색",
    sortLabel:"정렬",
    sort:{recent:"최신에 부른 순",title:"제목순",artist:"가수순",count:"많이 부른 순"},
    cat:{all:"전체",jpop:"J-Pop",vocaloid:"보컬로이드",holo:"Hololive Original",
         anime:"애니메이션",etc:"그 외 곡"},
    nSongs:n=>`${n}곡`, times:n=>`${n}회`, rep:n=>`${n}번`, ord:n=>`${n}번째`,
    stream:"방송", video:"동영상", live:n=>`3D LIVE「${n}」`,
    latest:"최신", acap:"아카펠라", fromStart:"처음부터",
    hint:"클릭하면 전체 가창 이력", empty:"결과 없음",
    note:{utaite:"우타이테",gakumas:"학원 아이돌마스터",vtuber:"VTuber",comedy:"개그 콤비"},
    date:(y,m,d)=>`${y}년 ${m}월 ${d}일`,
    f1:"세트리스트 출처", f2:"채널",
    y1:"1년차", y2:"2년차", after:"2025년 5월 이후는 각 방송의 타임스탬프 댓글",
    pl:"歌枠 재생목록", f3:"개인 팬 아카이브 · 날짜는 방송 시작 시각 기준",
    made:"이 페이지는 Claude로 만들었습니다"
  },
  ja: {
    label:"日本語",
    title:"音乃瀬奏 歌枠曲集",
    titlePrefix:"", titleName:"音乃瀬奏", titleRest:" 歌枠曲集",
    sub:"音乃瀬奏 · 歌枠セットリスト アーカイブ",
    st:["曲","歌唱回数","配信 · 動画"],
    search:"曲名 · アーティスト検索",
    sortLabel:"並び替え",
    sort:{recent:"最近歌った順",title:"曲名順",artist:"アーティスト順",count:"歌唱回数順"},
    cat:{all:"すべて",jpop:"J-Pop",vocaloid:"ボーカロイド",holo:"Hololive Original",
         anime:"アニメ",etc:"その他"},
    nSongs:n=>`${n}曲`, times:n=>`${n}回`, rep:n=>`${n}回`, ord:n=>`${n}回目`,
    stream:"配信", video:"動画", live:n=>`3D LIVE「${n}」`,
    latest:"最新", acap:"アカペラ", fromStart:"最初から",
    hint:"クリックで全歌唱履歴", empty:"該当なし",
    note:{utaite:"歌い手",gakumas:"学園アイドルマスター",vtuber:"VTuber",comedy:"お笑いコンビ"},
    date:(y,m,d)=>`${y}年${m}月${d}日`,
    f1:"セットリスト出典", f2:"チャンネル",
    y1:"1年目", y2:"2年目", after:"2025年5月以降は各配信のタイムスタンプコメント",
    pl:"歌枠 再生リスト", f3:"個人ファンアーカイブ · 日付は配信開始時刻基準",
    made:"このページは Claude で作成しました"
  },
  en: {
    label:"EN",
    title:"Otonose Kanade Songs",
    titlePrefix:"", titleName:"Otonose Kanade", titleRest:" Songs",
    sub:"Otonose Kanade · karaoke stream setlist archive",
    st:["songs","performances","streams · videos"],
    search:"Search title or artist",
    sortLabel:"Sort",
    sort:{recent:"Most recently sung",title:"By title",artist:"By artist",count:"Most sung"},
    cat:{all:"All",jpop:"J-Pop",vocaloid:"Vocaloid",holo:"Hololive Original",
         anime:"Anime",etc:"Other"},
    nSongs:n=>`${n} songs`, times:n=>`${n}×`, rep:n=>`${n}×`, ord:n=>`#${n}`,
    stream:"stream", video:"Video", live:n=>`3D LIVE "${n}"`,
    latest:"latest", acap:"a cappella", fromStart:"from start",
    hint:"Click to see every performance", empty:"No results",
    note:{utaite:"utaite",gakumas:"Gakuen Idolmaster",vtuber:"VTuber",comedy:"comedy duo"},
    date:(y,m,d)=>`${MON_EN[m-1]} ${d}, ${y}`,
    f1:"Setlist sources", f2:"Channel",
    y1:"year 1", y2:"year 2", after:"May 2025 onward from timestamp comments",
    pl:"歌枠 playlist", f3:"Personal fan archive · dates are stream start times",
    made:"This page was built with Claude"
  },
  id: {
    label:"ID",
    title:"Koleksi Lagu Otonose Kanade",
    titlePrefix:"Koleksi Lagu ", titleName:"Otonose Kanade", titleRest:"",
    sub:"Otonose Kanade · arsip setlist siaran karaoke",
    st:["lagu","kali dinyanyikan","siaran · video"],
    search:"Cari judul atau artis",
    sortLabel:"Urutkan",
    sort:{recent:"Terbaru dinyanyikan",title:"Judul",artist:"Artis",count:"Paling sering"},
    cat:{all:"Semua",jpop:"J-Pop",vocaloid:"Vocaloid",holo:"Hololive Original",
         anime:"Anime",etc:"Lainnya"},
    nSongs:n=>`${n} lagu`, times:n=>`${n}×`, rep:n=>`${n}×`, ord:n=>`#${n}`,
    stream:"siaran", video:"Video", live:n=>`3D LIVE "${n}"`,
    latest:"terbaru", acap:"a cappella", fromStart:"dari awal",
    hint:"Klik untuk melihat semua penampilan", empty:"Tidak ada hasil",
    note:{utaite:"utaite",gakumas:"Gakuen Idolmaster",vtuber:"VTuber",comedy:"duo komedi"},
    date:(y,m,d)=>`${d} ${MON_ID[m-1]} ${y}`,
    f1:"Sumber setlist", f2:"Kanal",
    y1:"tahun 1", y2:"tahun 2", after:"Mei 2025 ke atas dari komentar timestamp",
    pl:"Playlist 歌枠", f3:"Arsip fan pribadi · tanggal berdasarkan waktu mulai siaran",
    made:"Halaman ini dibuat dengan Claude"
  }
};

const CATS = ["all","jpop","vocaloid","holo","anime","etc"];

/* 언어 결정: 저장된 선택 → 브라우저/OS 언어 → 기본값 */
function detectLang(){
  const nav = navigator.languages && navigator.languages.length
            ? navigator.languages : [navigator.language || ""];
  for (const raw of nav){
    const code = String(raw).toLowerCase().split("-")[0];
    if (I18N[code]) return code;
  }
  return FALLBACK_LANG;
}
function initialLang(){
  try {
    const saved = localStorage.getItem("kanade-lang");
    if (saved && I18N[saved]) return saved;
  } catch(e) {}
  return DEFAULT_LANG === "auto" ? detectLang()
       : (I18N[DEFAULT_LANG] ? DEFAULT_LANG : FALLBACK_LANG);
}

let state = {cat:"all", sort:"recent", q:"", lang:initialLang()};
const T = () => I18N[state.lang];

function fmtDate(d){
  const [y,m,dd] = d.split("-");
  return T().date(+y, +m, +dd);
}
function perfLabel(p){          // "V|cover" / "L|The First Note" → 표시용
  if (!p.L) return {txt:T().stream, cls:""};
  const [k, n] = [p.L.slice(0,1), p.L.slice(2)];
  if (k === "L") return {txt:T().live(n), cls:"live"};
  return {txt:`${T().video} · ${n}`, cls:"live vid"};
}
/* 검색어 정규화 — 가타카나/히라가나, 전각/반각, 대소문자를 같은 것으로 취급 */
function fold(str){
  return str.normalize("NFKC").toLowerCase()
    .replace(/[\u30A1-\u30F6]/g, c => String.fromCharCode(c.charCodeAt(0) - 0x60))
    .replace(/[\u3000\s]+/g, "")
    .replace(/[\u301C\uFF5E]/g, "~");
}
function haystack(s){          // 곡별로 한 번만 계산해 캐시
  if (s._f === undefined) s._f = fold(s.title + " " + s.artist + " " + (s.src || ""));
  return s._f;
}
function srcLabel(s){           // "@utaite" → 번역, 작품명은 그대로
  if (!s) return "";
  return s.startsWith("@") ? (T().note[s.slice(1)] || s.slice(1)) : s;
}
function link(p){
  return `https://www.youtube.com/watch?v=${p.v}&t=${p.t}s`;
}
function esc(s){
  return s.replace(/[&<>"]/g, c => ({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));
}

function buildChips(){
  const counts = {all:SONGS.length};
  SONGS.forEach(s => counts[s.cat] = (counts[s.cat]||0) + 1);
  document.getElementById("chips").innerHTML = CATS.map(k =>
    `<button class="chip${k===state.cat?" on":""}" data-cat="${k}">${T().cat[k]}<span class="n">${counts[k]||0}</span></button>`
  ).join("");
}

function buildShell(){
  const t = T();
  document.documentElement.lang = state.lang;
  document.title = t.title;
  document.getElementById("title-prefix").textContent = t.titlePrefix;
  document.getElementById("title-name").textContent = t.titleName;
  document.getElementById("title-rest").textContent = t.titleRest;
  [...document.querySelectorAll(".stat span")].forEach((e,i) => e.textContent = t.st[i]);
  document.getElementById("q").placeholder = t.search;
  const sel = document.getElementById("sort");
  sel.innerHTML = ["recent","title","artist","count"]
    .map(k => `<option value="${k}"${k===state.sort?" selected":""}>${t.sort[k]}</option>`).join("");
  sel.title = t.sortLabel;
  sel.setAttribute("aria-label", t.sortLabel);
  document.getElementById("langs").innerHTML = LANG_ORDER.filter(k=>I18N[k]).map(k =>
    `<button class="chip lang${k===state.lang?" on":""}" data-lang="${k}">${I18N[k].label}</button>`).join("");
  document.getElementById("foot").innerHTML =
    `${t.f1} · <a href="https://note.com/punikanade_/n/nca6384d2cf08" target="_blank" rel="noopener">こまちゃん 歌枠まとめ ${t.y1}</a>`
    + ` / <a href="https://note.com/punikanade_/n/n4a4aa235f67f" target="_blank" rel="noopener">${t.y2}</a>`
    + ` / ${t.after}<br>`
    + `${t.f2} · <a href="https://www.youtube.com/@OtonoseKanade" target="_blank" rel="noopener">Kanade Ch. 音乃瀬奏 ‐ ReGLOSS</a>`
    + ` / <a href="https://www.youtube.com/playlist?list=PL6qjLH_5VIDXO6ymH_tjQGe_kV8svETJj" target="_blank" rel="noopener">${t.pl}</a><br>`
    + t.f3
    + `<br><span class="made">${t.made}</span>`;
  buildChips();
}

function render(){
  const q = fold(state.q);
  let list = SONGS.filter(s =>
    (state.cat === "all" || s.cat === state.cat) &&
    (!q || haystack(s).includes(q)
        || (s.src && s.src.startsWith("@") && fold(srcLabel(s.src)).includes(q)))
  );

  const coll = new Intl.Collator(["ja","ko","en"]);
  // 최신순: 방송일 내림차순 → 같은 방송이면 방송 안에서 늦게 부른 곡이 먼저
  const recency = s => s.perfs[0].d + "|" + String(s.perfs[0].t).padStart(6,"0");
  if (state.sort === "recent")      list.sort((a,b) => recency(b).localeCompare(recency(a)));
  else if (state.sort === "title")  list.sort((a,b) => coll.compare(a.title, b.title));
  else if (state.sort === "artist") list.sort((a,b) => coll.compare(a.artist, b.artist) || coll.compare(a.title, b.title));
  else if (state.sort === "count")  list.sort((a,b) => b.n - a.n || recency(b).localeCompare(recency(a)));

  const t = T();
  document.getElementById("count").textContent = t.nSongs(list.length);

  if (!list.length){
    document.getElementById("list").innerHTML = `<p class="empty">${t.empty}</p>`;
    return;
  }

  document.getElementById("list").innerHTML = list.map(s => {
    const latest = s.perfs[0];
    const src = srcLabel(s.src);
    const tagTitle = src ? ` title="${t.cat[s.cat]} · ${esc(src)}"` : "";
    return `<div class="song"><details>
      <summary class="top" title="${t.hint}">
        <div class="meta">
          <div class="title">${esc(s.title)}</div>
          <div class="artist">${esc(s.artist)}${src?` <span class="src ${s.cat}">${esc(src)}</span>`:""}</div>
        </div>
        <div class="col-cat"><span class="tag ${s.cat}"${tagTitle}>${t.cat[s.cat]}</span></div>
        <div class="col-n">${t.times(s.n)}<span class="car"></span></div>
        <a class="play" href="${link(latest)}" target="_blank" rel="noopener">
          <span class="ic">▶</span>${fmtDate(latest.d)}${latest.a?`<span class="acap">${t.acap}</span>`:""}
        </a>
      </summary>
      <div class="past">${s.perfs.map((p,i) => { const L = perfLabel(p); return `
        <a class="${i?"":"new"}" href="${link(p)}" target="_blank" rel="noopener">
           <span>${fmtDate(p.d)} ${L.cls?`<span class="${L.cls}">${esc(L.txt)}</span>`:esc(L.txt)}${p.i?`<span class="rep">${t.ord(p.i)}</span>`:""}${p.r>1?`<span class="rep">${t.rep(p.r)}</span>`:""}${p.a?`<span class="acap">${t.acap}</span>`:""}${i?"":`<span class="pin">${t.latest}</span>`}</span>
           <span class="ago">${p.t?`${Math.floor(p.t/3600)}:${String(Math.floor(p.t%3600/60)).padStart(2,"0")}:${String(p.t%60).padStart(2,"0")}`:t.fromStart}</span>
         </a>`;}).join("")}</div>
    </details></div>`;
  }).join("");
}

// 행 안의 재생 버튼 클릭은 fold 토글로 번지지 않게
document.getElementById("list").addEventListener("click", e => {
  if (e.target.closest("a.play")) e.stopPropagation();
});

document.getElementById("chips").addEventListener("click", e => {
  const b = e.target.closest(".chip");
  if (!b) return;
  state.cat = b.dataset.cat;
  buildChips(); render();
});
document.getElementById("langs").addEventListener("click", e => {
  const b = e.target.closest(".chip");
  if (!b) return;
  state.lang = b.dataset.lang;
  try { localStorage.setItem("kanade-lang", state.lang); } catch(e) {}
  buildShell(); render();
});
document.getElementById("sort").addEventListener("change", e => { state.sort = e.target.value; render(); });
document.getElementById("q").addEventListener("input", e => { state.q = e.target.value; render(); });

buildShell(); render();
</script>
</body>
</html>
"""

rng = f"{dates[0][:4]}.{dates[0][5:7]} – {dates[-1][:4]}.{dates[-1][5:7]}"
out = (HTML
       .replace("__DATA__", data)
       .replace("__NSONG__", str(len(songs)))
       .replace("__NPERF__", str(n_perf))
       .replace("__NSTREAM__", str(n_stream))
       .replace("__RANGE__", rng))
open(f"{BASE}/kanade_karaoke_library.html", "w", encoding="utf-8").write(out)
print("written", len(out), "bytes /", len(songs), "songs")
