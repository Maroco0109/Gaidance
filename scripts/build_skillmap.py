#!/usr/bin/env python3
"""경로 A 배치 수집기: 고용24 직업정보(212) → 직군별 정적 스킬맵 JSON.

사용법:
    python3 scripts/build_skillmap.py backend

인증키는 .env의 WORK24_OCCUPATION_KEY(직업정보 API)를 사용한다.
출력은 data/skillmaps/<role_key>.json.
"""
import sys, os, json, re, datetime, urllib.request, urllib.parse
from xml.etree import ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GW = "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo"

# 직군 → 직업(jobCd) 앵커 (README "직군 → 직업 앵커 매핑" 실측)
ROLES = {
    "backend": {
        "role": "Backend Engineer",
        "jobCds": ["K000001176", "K000000853"],
        "occupations": ["응용소프트웨어개발자", "시스템 소프트웨어 개발자(프로그래머)"],
        "portfolio_recommendations": [
            "예약/대기열 시스템 (동시성·트랜잭션 증명)",
            "주문/결제 상태머신 API (도메인 모델링)",
            "Redis 캐시 적용 전후 성능 비교 (측정·개선 기록)",
        ],
    },
    "frontend": {"role": "Frontend Engineer", "jobCds": ["K000001106"],
                 "occupations": ["웹개발자(웹 프로그래머)"], "portfolio_recommendations": []},
    "ai": {"role": "AI/Data Engineer", "jobCds": ["K000001080", "K000001134"],
           "occupations": ["데이터분석가(빅데이터분석가)", "데이터 시스템 전문가"], "portfolio_recommendations": []},
    "security": {"role": "Security Engineer", "jobCds": ["K000000832"],
                 "occupations": ["정보 보안 전문가"], "portfolio_recommendations": []},
}

# 담당업무(execJob) 텍스트에서 뽑을 구체 스택 신호 사전
TECH_KEYWORDS = [
    "자바", "Java", "C++", "C#", "파이썬", "Python", "자바스크립트", "JavaScript",
    "C언어", "FORTRAN", "코볼", "비주얼베이직", "델파이",
    "SQL", "오라클", "Oracle", "MySQL", "데이터베이스", "DBMS",
    "리눅스", "Linux", "유닉스", "Unix", "윈도우", "Windows",
    "네트워크", "웹", "서버", "운영체제", "운영체계", "프레임워크", "알고리즘",
    "클라우드", "AWS", "도커", "Docker", "쿠버네티스",
]


def load_key(name):
    with open(os.path.join(ROOT, ".env"), encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if s.startswith(name + "="):
                return s.split("=", 1)[1].strip().strip('"').strip("'")
    raise SystemExit(f"{name} not found in .env")


def call(code, params):
    url = f"{GW}{code}.do?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    body = urllib.request.urlopen(req, timeout=30).read().decode("utf-8", errors="replace")
    if body.lstrip().startswith("<!DOCTYPE") or body.lstrip().startswith("<html"):
        raise RuntimeError(f"{code} returned HTML error page")
    return ET.fromstring(body)


def detail(key, jobCd, n):
    return call(f"212D0{n}", {"authKey": key, "returnType": "XML", "target": "JOBDTL",
                              "jobGb": "1", "jobCd": jobCd, "dtlGb": str(n)})


def text_of(root, tag):
    for e in root.iter():
        if e.tag == tag and e.text and e.text.strip():
            return e.text.strip()
    return None


def all_text(root, tag):
    return [e.text.strip() for e in root.iter() if e.tag == tag and e.text and e.text.strip()]


def parse_records(root, container, name_tag, status_tag, cont_tag):
    """<container> 반복 요소 → [{name, importance, desc}]"""
    out = []
    for el in root.findall(container):
        nm = el.findtext(name_tag)
        st = el.findtext(status_tag)
        ct = el.findtext(cont_tag)
        if nm:
            try:
                imp = float(st) if st is not None else None
            except ValueError:
                imp = None
            out.append({"name": nm.strip(), "importance": imp,
                        "desc": (ct or "").strip()})
    return out


def merge_top(records_lists, top=12, min_importance=0):
    """여러 직업의 역량 병합 → 이름별 최대 중요도 유지, 임계값 이상만 내림차순 top N.

    KNOW는 고정 능력/지식 목록에 모든 직업을 점수화하므로, 하위 점수 항목은
    직군과 무관한 노이즈다(예: 백엔드 지식에 '식품생산'). min_importance로 절단한다.
    """
    best = {}
    for recs in records_lists:
        for r in recs:
            k = r["name"]
            if k not in best or (r["importance"] or 0) > (best[k]["importance"] or 0):
                best[k] = r
    ranked = sorted(best.values(), key=lambda r: (r["importance"] or 0), reverse=True)
    ranked = [r for r in ranked if (r["importance"] or 0) >= min_importance]
    return ranked[:top]


def extract_tech(texts):
    joined = " ".join(texts)
    found = []
    for kw in TECH_KEYWORDS:
        if kw.lower() in joined.lower() and kw not in found:
            found.append(kw)
    return found


def build(role_key):
    cfg = ROLES[role_key]
    key = load_key("WORK24_OCCUPATION_KEY")

    abil_lists, know_lists, duties, certs = [], [], [], []
    market = {}
    for jobCd in cfg["jobCds"]:
        d02 = detail(key, jobCd, 2)
        d03 = detail(key, jobCd, 3)
        d04 = detail(key, jobCd, 4)
        d05 = detail(key, jobCd, 5)

        duties += all_text(d02, "execJob")
        certs += all_text(d03, "certNm")
        abil_lists.append(parse_records(d05, "jobAbil", "jobAblNm", "jobAblStatus", "jobAblCont"))
        know_lists.append(parse_records(d05, "Knwldg", "knwldgNm", "knwldgStatus", "knwldgCont"))

        if not market:  # 첫 직업 기준(대표 직업)
            market = {
                "salary": text_of(d04, "sal"),
                "job_satisfaction": _num(text_of(d04, "jobSatis")),
                "prospect": text_of(d04, "jobProspectNm"),
                "prospect_detail": text_of(d04, "jobProspect"),
            }

    duties = sorted(set(duties))
    certs = sorted(set(certs))

    return {
        "schema_version": "1.0",
        "role": cfg["role"],
        "role_key": role_key,
        "career_level": "entry_junior",
        "period": _quarter(),
        "generated_at": datetime.date.today().isoformat(),
        "refresh_cadence": "quarterly",
        "sources": {
            "work24_occupation_212": {
                "jobCds": cfg["jobCds"],
                "occupations": cfg["occupations"],
            }
        },
        "market": market,
        "competencies": {
            "abilities": merge_top(abil_lists, top=10, min_importance=85),
            "knowledge": merge_top(know_lists, top=8, min_importance=75),
        },
        "tech_signals": extract_tech(duties),
        "duties": duties,
        "certifications": certs,
        "portfolio_recommendations": cfg["portfolio_recommendations"],
        "notes": ("212 직업정보 기반 정량 역량(0~100 중요도). 능력/지식은 KNOW 기준 추상 역량이며, "
                  "구체 기술 스택(tech_signals)은 담당업무 텍스트에서 추출한 신호 수준. "
                  "실제 공고 요구 스택은 경로 B(사용자 붙여넣기)로 보강한다."),
    }


def _num(s):
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def _quarter():
    d = datetime.date.today()
    return f"{d.year}-Q{(d.month - 1) // 3 + 1}"


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ROLES:
        raise SystemExit(f"usage: build_skillmap.py <{'|'.join(ROLES)}>")
    role_key = sys.argv[1]
    data = build(role_key)
    out_dir = os.path.join(ROOT, "data", "skillmaps")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"{role_key}.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"wrote {out_path}")
    print(f"  abilities={len(data['competencies']['abilities'])} "
          f"knowledge={len(data['competencies']['knowledge'])} "
          f"tech_signals={len(data['tech_signals'])} certs={len(data['certifications'])}")


if __name__ == "__main__":
    main()
