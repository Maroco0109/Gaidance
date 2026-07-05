# Gaidance
개발자의 채용 공고를 분석하여 취업 준비생, 이직 준비생들의 목표를 확실하게 해주는 AI 서비스

# 서비스 계획: `개발자 공고 해석기 MCP`

## 0. 핵심 포지셔닝

이 서비스는 **취업 대행 MCP**가 아닙니다.
채용공고를 대신 찾아주고, 이력서와 자소서를 대신 써주는 서비스는 이미 많습니다. 해외에는 JobGPT MCP처럼 채용 검색, 지원서, 이력서, 아웃리치까지 다루는 MCP가 있고, Dice도 기술직 채용 검색용 MCP 서버를 출시했습니다. ([github.com](https://github.com/6figr-com/jobgpt-mcp-server), [dice.com](https://www.dice.com/career-advice/dice-launches-mcp-server-for-ai-powered-job-search))

우리가 잡아야 할 포지션은 이겁니다.

> **최근 개발자 채용공고를 분석해, 직무별 요구역량을 구조화하고, 신입/주니어가 어떤 포트폴리오를 만들어야 하는지 알려주는 MCP**

즉, 핵심 질문은 `어디 지원할까?`가 아니라:

```text
이 직무로 가려면 지금 뭘 증명해야 하지?
```

입니다.

---

## 0.1 운영 모델: 캐시 + 붙여넣기

이 MCP는 실시간으로 채용 플랫폼을 크롤링하지 않습니다. 두 개의 합법적 경로를 병행합니다.

- **경로 A — 배치 캐시:** 개인회원이 접근 가능한 공식 소스(직무정보 API·NCS 표준역량 + 사람인 메타 + 공채속보/공채기업정보)로 4개 직군 스킬맵을 주기적으로(길게는 분기, 짧게는 주간) 갱신해 서버에 정적 데이터로 동봉합니다. 워크넷 채용정보 상세(본문) API는 기업회원 전용이라 사용하지 않습니다. 런타임 툴은 이 캐시 위에서 추론만 하므로 빠르고 안정적입니다.
- **경로 B — 사용자 붙여넣기:** 원티드나 개별 기업 채용페이지처럼 공식 API가 없는 공고는, 사용자가 URL/본문을 직접 붙여넣으면 MCP가 해석만 합니다. 접속·열람 주체가 사용자이므로 크롤링/약관 리스크에서 자유롭습니다.

크롤링 기반 대량 수집은 데이터베이스제작자 권리(저작권법 제93조)와 부정경쟁방지법 위반 소지가 있어(잡코리아–사람인 판례) 설계에서 제외합니다.

---

# 1. 서비스명 후보

| 이름                | 평가              |
| ----------------- | --------------- |
| **DevFit MCP**    | 짧고 범용적          |
| **개발자 공고 해석기**    | 기능이 바로 드러남      |
| **공고번역기**         | 카카오톡 친화적, 기억 쉬움 |
| **신입개발자 로드맵 판독기** | 타깃이 명확함         |
| **포트폴리오 뭐만들지**    | 실사용 질문과 가까움     |

내 추천은 **노출명 `공고번역기`**, 제출명 `개발자 공고 해석기 MCP`입니다.

---

# 2. 목표 유저층

## 1차 타깃: 신입/주니어 개발자

특히 아래 유형입니다.

| 유형          | 실제 고민                                        |
| ----------- | -------------------------------------------- |
| 부트캠프 수료생    | 공고는 많은데 내가 뭘 더 해야 할지 모름                      |
| 비전공 전환자     | CS, 프로젝트, 자격증 중 무엇이 우선인지 모름                  |
| AI/LLM 지망생  | RAG, Agent, MLOps 같은 요구사항을 어느 수준까지 해야 하는지 모름 |
| 보안 지망생      | 정보보안기사, 관제, 웹해킹, 클라우드 보안 중 우선순위 혼란           |
| 백엔드/프론트 지망생 | 공고 요구사항을 포트폴리오로 어떻게 증명할지 모름                  |

## 2차 타깃: 취업 방향을 바꾸려는 개발자

예를 들어:

```text
백엔드 하다가 보안으로 갈 수 있나?
AI Engineer 공고를 보면 뭘 준비해야 하지?
프론트엔드 신입 공고가 요즘 뭘 요구하지?
```

## 3차 타깃: 교육기관/멘토

부트캠프, 스터디 리더, 취업 멘토가 “요즘 공고 기준으로 커리큘럼/포트폴리오 피드백”을 줄 때 쓸 수 있습니다.

---

# 3. 차별화 기능 정의

## 기능 A. 직무별 요구역량 맵

채용공고 여러 개를 수집한 뒤, 직무별로 요구사항을 나눕니다.

```text
Backend Engineer - 신입/주니어 기준

필수로 자주 등장:
- Java / Spring Boot
- REST API
- RDBMS / SQL
- Git
- CS 기본기
- 협업 경험

우대로 자주 등장:
- Redis
- Kafka
- Docker
- AWS
- 대용량 트래픽 경험
- 테스트 코드
```

이 기능은 단순 채용공고 검색과 다릅니다.
워크넷 API는 근무지역, 직종, 임금, 학력, 경력, 우대조건, 고용형태, 자격면허, 등록일, 키워드 등 다양한 파라미터와 결과 필드를 제공합니다. ([data.go.kr](https://www.data.go.kr/data/3038225/openapi.do?recommendDataYn=Y))
사람인 Job Search API도 기업명, 공고명, 업직종 키워드, 직무내용 검색, 지역, 산업, 직무코드, 고용형태, 학력, 등록일, 마감일 등의 조건을 제공합니다. ([oapi.saramin.co.kr](https://oapi.saramin.co.kr/guide/job-search))

따라서 MCP가 할 일은 `검색`이 아니라 **검색 결과를 직무 요구역량으로 재구성**하는 것입니다.

---

## 기능 B. 경력직 공고를 신입용 포트폴리오 언어로 번역

이게 제일 중요한 차별화입니다.

예시:

```text
공고 요구사항:
- MLOps 경험
- RAG 시스템 개발 경험
- 클라우드 환경 배포 경험

신입 포트폴리오로 번역:
1. 단순 챗봇이 아니라 문서 수집 → 임베딩 → 검색 → 답변 → 평가까지 구현
2. Docker로 실행환경 고정
3. FastAPI로 API 제공
4. 벡터DB 교체 실험 기록
5. 검색 실패 케이스와 개선 내역 README 작성
```

신입은 경력직 공고를 보고 “3년 경력 없으니 못함”으로 끝내는 경우가 많습니다.
이 MCP는 경력직 요구사항을 **신입이 증명 가능한 산출물**로 바꿔줘야 합니다.

---

## 기능 C. 자격증 실효성 판정

예시:

```text
Security Engineer 신입 기준

정보보안기사:
- 공공/보안관제/SI/보안솔루션 기업에서 우대 신호로 작동 가능
- 단독으로는 부족
- 로그분석, 취약점 진단, 네트워크 패킷 분석 프로젝트와 결합할 때 설득력 상승

우선순위:
1. 정보보안기사 필기/실기 준비
2. 웹 취약점 진단 리포트 프로젝트
3. Linux 로그 분석 + 탐지 룰 작성
4. 보안관제 시나리오 포트폴리오
```

이 기능은 NCS/ITSQF와도 연결할 수 있습니다. NCS는 산업현장에서 직무 수행에 필요한 지식·기술·태도를 국가 차원에서 체계화한 표준이고, IT분야역량체계인 ITSQF는 IT산업 표준 직무와 직무 수행 능력을 구조화한 체계입니다. ([sw.or.kr](https://www.sw.or.kr/site/sw/02/10203000000002017070309.jsp), [sw.or.kr](https://www.sw.or.kr/site/sw/02/10204020000002017070310.jsp))

---

## 기능 D. 포트폴리오 주제 추천

단순히 “공부하세요”가 아니라, 공고 요구사항과 연결되는 프로젝트를 제안합니다.

예시:

```text
AI/LLM Engineer 신입 포트폴리오 추천

1. 근거 기반 RAG 챗봇
- 보여주는 역량: RAG, Vector DB, 평가, 프롬프트 개선
- 피해야 할 점: 단순 OpenAI API 래핑으로 끝내기

2. 채용공고 분석기
- 보여주는 역량: 크롤링/API, 텍스트 분류, 스킬 추출, 대시보드

3. LLM 보안 테스트 도구
- 보여주는 역량: 프롬프트 인젝션, 입력 검증, 로그 분석, 방어 설계
```

이 기능은 네 상황과도 잘 맞습니다.
너는 AI/LLM 경험도 있고 보안으로 방향 전환을 고민하고 있으니, 실제 유저 페르소나로 테스트하기 좋습니다.

---

# 4. MCP 기능 설계

## Tool 1. `search_dev_jobs`

캐시된 직무별 공고 데이터셋을 조회하거나(경로 A), 사용자가 직접 붙여넣은 공고를 입력으로 받습니다(경로 B). 실시간 플랫폼 크롤링은 하지 않습니다.

### 입력

```json
{
  "role": "AI Engineer",
  "career_level": "junior",
  "period": "recent_90_days",
  "location": "Seoul/Gyeonggi",
  "sources": ["worknet", "saramin"],
  "keywords": ["LLM", "RAG", "Agent", "Python"]
}
```

### 출력

```json
{
  "total_count": 128,
  "jobs": [
    {
      "source": "saramin",
      "company": "Example AI",
      "title": "LLM Engineer",
      "career": "신입/경력",
      "location": "서울",
      "deadline": "2026-07-31",
      "url": "...",
      "raw_description": "..."
    }
  ]
}
```

### MVP 데이터 소스

| 소스  | 사용 이유                                          |
| --- | ---------------------------------------------- |
| 워크넷 | 공공 API, 필드 구조 명확                               |
| 사람인 | 민간 채용공고, 개발직무 데이터 풍부                           |
| 점핏  | 개발자 특화 플랫폼이지만 공식 API 확인 필요. MVP에서는 직접 연동 제외 권장 |

점핏은 개발자 채용, 이력서, 피드, 개발자 인터뷰, 신입 개발자 포지션 모음, AI 추천 포지션을 제공하므로 경쟁/참고 서비스로는 중요하지만, 공식 API 없이 크롤링하면 리스크가 큽니다. ([jumpit.saramin.co.kr](https://jumpit.saramin.co.kr/))

---

## Tool 2. `extract_job_requirements`

공고 본문에서 요구사항을 추출합니다.

### 입력

```json
{
  "job_descriptions": ["..."],
  "role": "Security Engineer",
  "career_level": "entry"
}
```

### 출력

```json
{
  "required_skills": [
    {
      "skill": "Linux",
      "frequency": 42,
      "evidence_examples": ["Linux 서버 운영 경험", "Linux 로그 분석 가능자"]
    },
    {
      "skill": "Network",
      "frequency": 36,
      "evidence_examples": ["TCP/IP 이해", "네트워크 보안 장비 운영"]
    }
  ],
  "preferred_skills": [
    {
      "skill": "정보보안기사",
      "frequency": 18,
      "type": "certification"
    }
  ],
  "soft_requirements": [
    "문제 해결 능력",
    "문서화",
    "협업 경험"
  ]
}
```

스킬 추출은 단순 LLM 프롬프트로만 처리하면 흔들립니다.
논문 쪽에서도 자유형 채용공고/사용자 프로필에서 스킬을 추출하고 표준화하는 작업은 별도 문제로 다뤄지며, SkillGPT는 LLM과 요약·벡터 유사도 검색을 결합해 속도와 정밀도의 균형을 맞추는 접근을 제안합니다. ([arxiv.org](https://arxiv.org/abs/2304.11060))

MVP에서는 다음 구조가 적당합니다.

```text
1. 사전 기반 1차 추출
2. LLM 기반 누락 보정
3. 동의어 정규화
4. 필수/우대/자격증/경험/CS/도구/클라우드 분류
```

---

## Tool 3. `build_role_skill_map`

여러 공고를 묶어 직무별 스킬맵을 만듭니다.

### 입력

```json
{
  "role": "Backend Engineer",
  "career_level": "entry",
  "jobs": ["job_id_1", "job_id_2", "job_id_3"]
}
```

### 출력

```json
{
  "role": "Backend Engineer",
  "career_level": "entry",
  "market_summary": "신입 백엔드 공고는 Java/Spring, RDBMS, REST API, Git, 협업 경험을 반복적으로 요구합니다.",
  "skill_map": {
    "must_have": ["Java", "Spring Boot", "SQL", "REST API", "Git"],
    "strong_signal": ["Docker", "AWS", "Redis", "테스트 코드"],
    "nice_to_have": ["Kafka", "Kubernetes", "대용량 트래픽"]
  },
  "overclaimed_keywords": ["MSA", "대용량 트래픽"],
  "portfolio_implications": [
    "단순 CRUD보다 트랜잭션, 동시성, 테스트를 보여주는 프로젝트가 유리함"
  ]
}
```

여기서 중요한 건 `overclaimed_keywords`입니다.
신입 포트폴리오에서 `MSA`, `대용량 트래픽`, `MLOps`를 말만 크게 쓰면 오히려 약해질 수 있습니다. MCP가 이런 단어를 **신입이 실제로 증명 가능한 수준으로 낮춰 번역**해야 합니다.

---

## Tool 4. `translate_to_junior_portfolio`

경력직 요구사항을 신입용 프로젝트 요구사항으로 바꿉니다.

### 입력

```json
{
  "role": "AI Engineer",
  "requirements": ["RAG", "MLOps", "Vector DB", "LLM Agent", "FastAPI"],
  "user_level": "new_grad",
  "time_budget": "8_weeks"
}
```

### 출력

```json
{
  "portfolio_projects": [
    {
      "title": "근거 기반 RAG 검색 챗봇",
      "why": "RAG, Vector DB, API, 평가 경험을 한 번에 보여줄 수 있음",
      "must_include": [
        "문서 수집/정제",
        "임베딩 모델 선택",
        "검색 품질 평가",
        "답변 근거 표시",
        "실패 케이스 분석"
      ],
      "avoid": [
        "OpenAI API만 호출하는 단순 챗봇",
        "평가 지표 없는 데모"
      ],
      "readme_sections": [
        "문제 정의",
        "아키텍처",
        "검색 성능 비교",
        "실패 케이스",
        "개선 내역"
      ]
    }
  ]
}
```

---

## Tool 5. `compare_user_profile`

사용자 현재 상태와 목표 직무의 간극을 분석합니다.

### 입력

```json
{
  "target_role": "Security Engineer",
  "user_profile": {
    "education": "비전공",
    "projects": ["LLM 챗봇", "FastAPI API 서버"],
    "certifications": ["정보처리기사 필기 준비중"],
    "skills": ["Python", "FastAPI", "Docker", "Linux 기초"],
    "preference": "보안 쪽으로 전환 희망"
  }
}
```

### 출력

```json
{
  "fit_summary": "백엔드/AI 구현 경험은 보안 자동화 포트폴리오로 전환 가능하지만, 네트워크/로그분석/취약점 진단 근거가 부족합니다.",
  "gaps": [
    {
      "gap": "네트워크 보안 기초",
      "priority": "high",
      "reason": "보안관제/보안엔지니어 공고에서 반복 등장"
    },
    {
      "gap": "보안 리포트 작성 경험",
      "priority": "high",
      "reason": "프로젝트를 보안 직무 신호로 바꾸는 데 필요"
    }
  ],
  "next_4_weeks": [
    "Linux 로그 분석 미니 프로젝트",
    "웹 취약점 진단 리포트 1개 작성",
    "정보보안기사 네트워크/시스템 파트 병행"
  ]
}
```

---

# 5. MVP 범위

## 하지 말아야 할 것

초기 MVP에서 아래는 제외하는 게 맞습니다.

| 제외 기능               | 이유                |
| ------------------- | ----------------- |
| 자동 지원               | 윤리/안정성/차별화 모두 불리  |
| 이력서 PDF 생성          | 기존 서비스와 정면충돌      |
| 자소서 생성              | 사람인/잡코리아/트리업류와 겹침 |
| 합격률 예측              | 근거 없는 예측 위험       |
| LinkedIn/원티드/점핏 크롤링 | 약관/안정성 리스크        |
| 모든 직군 지원            | 범위 폭발             |

## MVP에서 할 것

초기 범위는 4개 직군만 추천합니다.

| 직군                | 이유                           |
| ----------------- | ---------------------------- |
| Backend Engineer  | 공고 수 많고 요구역량 추출 쉬움           |
| Frontend Engineer | 신입 대상 명확                     |
| AI/LLM Engineer   | 트렌디하고 차별화 가능                 |
| Security Engineer | 네 관심사와 연결, 자격증/포트폴리오 조언 가치 큼 |

지원 경력 수준은 `신입/주니어`만 잡습니다.

---

# 6. 데이터 파이프라인

## 1단계. 공고 수집 (2개 경로 병행, 합법 소스만)

### 경로 A — 배치 캐시 (백그라운드, 개인회원 접근 가능 소스만)

```text
직무정보 API + NCS 표준역량   →  요구역량 뼈대(백본)
        +
사람인 메타 + 공채속보/공채기업정보  →  시장수요 가중치
↓
직무별 (표준역량 × 수요 가중) 집계
↓
직무별 집계 스킬맵으로 저장 (분기 또는 주간 갱신)
```

- 이 경로의 수집은 전부 허가된 API 호출이라 크롤링/약관 리스크가 없습니다.
- 워크넷 채용정보 상세(본문)는 기업회원 전용이라 제외하고, 개별 공고 본문은 경로 B로 처리합니다.
- 대기업(SKT·삼성SDS·현대모비스) 공고는 공채속보/공채기업정보 API로 수요 신호를 잡습니다.

### 경로 B — 사용자 붙여넣기 (런타임, 비API 소스)

```text
사용자가 원티드/기업 채용페이지 공고 URL·본문 붙여넣기
↓
MCP는 저장 없이 해석만 수행
↓
경로 A 스킬맵과 비교해 갭/포트폴리오 도출
```

- 원티드처럼 공식 API가 없는 소스는 서버가 직접 긁지 않고 사용자가 가져옵니다.
- 접속·열람 주체가 사용자이므로 데이터베이스제작자 권리/약관 문제에서 벗어납니다.

### 수집 소스별 역할 (API 실측 반영, 개인회원 기준)

> 실측 결론: 워크넷(고용24) **채용정보 목록/상세 API는 기업·기관회원 전용**이라, 개인 자격으로는 공고 본문(모집요강)을 API로 확보할 수 없습니다. 따라서 경로 A는 "본문 빈도"가 아니라 **"표준역량 뼈대 × 시장수요 메타"** 모델로 재구성합니다.

| 소스 | 개인회원 이용 | 제공 내용 | 경로 A 역할 |
| --- | --- | --- | --- |
| 직무정보 API(고용24) + NCS(국가직무능력표준, 파일) | ✅ | 직무별 표준 지식·기술·역량 | **요구역량 뼈대(백본)** |
| 공채속보 / 공채기업정보 API(고용24) | ✅ | 대기업 공개채용 공고·기업 메타 | 대기업 수요 신호 |
| 사람인 OAPI | ✅ | 공고 메타(직무·경력·학력·지역·급여, 본문 X, 최대 110건/페이지) | 시장 수요량·회사 분포 |
| 워크넷 채용정보 목록/상세 API | ❌ 기업회원 전용 | 공고 본문(모집요강) | 개인 불가 → 미사용 |
| 사용자 붙여넣기(경로 B) | ✅ | 실제 공고 본문 전문 | **실측 스킬 추출은 여기서** |

- 경로 A 스킬맵 = 직무정보/NCS **표준역량**에 사람인·공채 **시장수요 메타**를 가중치로 얹어 산출. 개별 공고 본문에 의존하지 않으므로 개인 자격으로 구축 가능합니다.
- 실제 공고 본문 기반 스킬 추출·번역은 **경로 B(사용자 붙여넣기)**가 담당합니다(합법).
- **실측 완료(2026-07)**: 신규 고용24 게이트웨이 확정, 직무정보 NCS API 실호출 성공. 상세는 아래 "확정 API 콜" 표.

### 확정 API 콜 (실측 완료, 2026-07)

게이트웨이: `https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo{코드}.do` · 인증: `authKey`(UUID 36자)

| 서비스 | 코드 | 개인 | 핵심 파라미터 | 비고 |
| --- | --- | --- | --- | --- |
| 채용정보 목록/상세 | 210L01 / 210D01 | ❌ | callTp, wantedAuthNo | `개인회원 사용 불가` 응답 실측 |
| 직업정보 능력/지식/환경 | 212D05 | ✅ | target=JOBDTL, jobGb=1, jobCd, dtlGb=5 | jobCd 선확보 필요(212 목록) |
| **직무정보 표준직무기술서** | **215L01** | ✅ | **jobCont**(수행직무 텍스트), limit, returnType=JSON | **NCS 백본. 실호출 성공** |
| 공채속보 목록/상세 | (코드 미확인) | ✅ | — | 대기업 수요 신호 |

**215L01 응답 구조(실측):** `result[능력단위명]` → `ablt_unit`(능력단위코드), `ablt_def`(정의), `knwg_tchn_attd[]`(지식/기술/태도 라벨 배열), `job_lcfn`/`job_mcn`/`job_scfn`(대/중/소분류).

> ⚠️ 215L01은 입력 텍스트를 NCS 능력단위에 **퍼지 매칭**함("백엔드 개발" → 무관 능력단위도 섞임). 배치 시 입력 직무 텍스트를 구체화하고 결과를 분류코드/키워드로 후필터해야 함. XML은 500 반환 → **`returnType=JSON` 사용.**

## 2단계. 공고 정규화

```json
{
  "source": "saramin",
  "company": "회사명",
  "title": "공고 제목",
  "role_raw": "LLM Engineer",
  "role_normalized": "AI Engineer",
  "career_level": "entry_or_junior",
  "employment_type": "full_time",
  "location": "Seoul",
  "posted_at": "2026-07-01",
  "deadline": "2026-07-31",
  "description": "...",
  "url": "..."
}
```

## 3단계. 요구사항 추출

분류 체계는 아래처럼 둡니다.

```text
- Language: Java, Python, JavaScript, TypeScript
- Framework: Spring, React, FastAPI, Next.js
- Infra: Docker, Kubernetes, AWS, Linux
- Data/AI: RAG, Vector DB, PyTorch, MLflow
- Security: Network, WAF, IDS, 취약점 진단, 로그분석
- CS: OS, DB, Network, Algorithm
- Collaboration: Git, Jira, 문서화, 코드리뷰
- Certification: 정보처리기사, 정보보안기사, SQLD, AWS
- Domain: 금융, 커머스, 제조, 보안관제
```

## 4단계. 스킬 정규화

예시:

```text
LLM Application = LLM 앱 개발 = 생성형 AI 서비스 개발
Vector Search = 벡터 검색 = Vector DB = 임베딩 검색
Spring = Spring Boot = Java Spring
AWS = 클라우드 = Public Cloud
```

## 5단계. 역량맵 생성

```text
빈도 기반:
- 여러 공고에서 반복 등장하는가?

필수/우대 기반:
- 필수요건에 등장하는가?
- 우대사항에 등장하는가?

직무 관련성 기반:
- 해당 직무의 핵심 역량인가?
- 범용 협업 도구인가?

신입 증명 가능성 기반:
- 포트폴리오로 증명 가능한가?
- 실무 경력 없이는 증명하기 어려운가?
```

---

# 7. 점수화 모델

합격률 예측은 하지 않습니다.
대신 **포트폴리오 준비 우선순위 점수**를 만듭니다.

```text
Skill Priority Score =
공고 등장 빈도
+ 필수요건 가중치
+ 신입 증명 가능성
+ 직무 핵심성
- 과장 위험도
```

출력 예시:

| 역량         | 빈도 | 필수성 | 신입 증명 가능성 |  우선순위 |
| ---------- | -: | --: | --------: | ----: |
| RAG        | 높음 |  중간 |        높음 | 매우 높음 |
| MLOps      | 중간 |  중간 |        낮음 |    중간 |
| Kubernetes | 낮음 |  낮음 |        낮음 |    낮음 |
| FastAPI    | 중간 |  중간 |        높음 |    높음 |
| 평가/리포트     | 중간 |  높음 |        높음 | 매우 높음 |

이 방식은 “너 합격 가능성 72%” 같은 허풍을 피하면서도 실용적입니다.

---

# 8. 사용자 시나리오

## 시나리오 1. AI Engineer 준비생

```text
사용자:
요즘 AI Engineer 신입 공고 기준으로 뭘 준비해야 돼?

MCP:
최근 공고를 기준으로 보면,
단순 모델 학습보다 LLM 서비스화 경험, RAG, API 연동, Docker, 클라우드 배포, 평가 경험이 반복적으로 등장합니다.

신입 포트폴리오 추천:
1. 근거 기반 RAG 챗봇
2. 채용공고 스킬 추출기
3. LLM 보안 테스트 도구
```

## 시나리오 2. 보안 직무 전환자

```text
사용자:
백엔드/AI 프로젝트 경험 있는데 보안 쪽으로 가려면 뭘 만들어야 해?

MCP:
현재 경험은 보안 자동화/로그분석 쪽으로 전환하기 좋습니다.
다만 네트워크, Linux, 취약점 진단 리포트 근거가 부족합니다.

추천 포트폴리오:
1. Linux auth.log 기반 이상 로그인 탐지
2. DVWA 취약점 진단 리포트
3. LLM 프롬프트 인젝션 방어 테스트 도구
```

## 시나리오 3. 백엔드 신입

```text
사용자:
백엔드 신입 포트폴리오 CRUD 말고 뭐 해야 함?

MCP:
최근 공고 기준으로 단순 CRUD보다 트랜잭션, 테스트, Redis, 배포, 장애 대응 기록이 더 강한 신호입니다.

추천:
1. 예약/대기열 시스템
2. 주문/결제 상태머신 API
3. Redis 캐시 적용 전후 성능 비교
```

---

# 9. 카카오톡 UX 설계

카카오톡 안에서는 긴 리포트보다 짧은 카드형 응답이 낫습니다.
본선 진출작은 카카오톡 내 Kakao Tools 사용자에게 공개되고 사용자 투표도 진행되므로, 일반 사용자가 빠르게 이해할 수 있어야 합니다. ([kakaocorp.com](https://www.kakaocorp.com/page/detail/12059), [b.kakao.com](https://b.kakao.com/views/PlayMCP/AGENTIC_PlAYER_10?t_ch=devtalk&t_src=developers))

## 기본 응답 구조

```text
[직무 요약]
AI Engineer 신입/주니어 공고는 RAG, Python, API 개발, Docker, 클라우드 배포, 평가 경험을 자주 요구합니다.

[지금 만들면 좋은 포트폴리오]
1. 근거 기반 RAG 챗봇
2. LLM 평가 대시보드
3. 문서 검색 API 서버

[버려도 되는 것]
- 논문 구현만 잔뜩 하기
- 모델 학습만 하고 서비스화 안 하기
- README 없이 데모만 올리기

[다음 4주]
1주차: 공고 20개 분석 + 요구역량 정리
2주차: RAG MVP 구현
3주차: 평가/실패 케이스 기록
4주차: 배포 + README 정리
```

## 버튼/후속 질문

```text
- “내 현재 상태와 비교해줘”
- “포트폴리오 주제 더 추천해줘”
- “보안 직무 기준으로 바꿔줘”
- “4주 계획으로 쪼개줘”
- “README 목차 만들어줘”
```

---

# 10. 시스템 아키텍처

```text
사용자 질문
↓
MCP Router
↓
Job Search Tool
- 워크넷 API
- 사람인 API
↓
Job Normalizer
- 직무명 정규화
- 경력 수준 분류
- 중복 제거
↓
Requirement Extractor
- 필수/우대/자격증/경험 분리
- 스킬 정규화
↓
Role Skill Map Builder
- 빈도
- 필수성
- 신입 증명 가능성
↓
Portfolio Translator
- 신입용 프로젝트 변환
- README/증거 산출물 제안
↓
카카오톡용 응답
```

---

# 11. 저장할 데이터

## 공고 캐시

```json
{
  "job_id": "saramin_12345",
  "source": "saramin",
  "title": "AI Engineer",
  "company": "Example",
  "url": "...",
  "posted_at": "2026-07-01",
  "deadline": "2026-07-31",
  "normalized_role": "AI Engineer",
  "career_level": "junior",
  "raw_text_hash": "..."
}
```

## 스킬 추출 결과

```json
{
  "job_id": "saramin_12345",
  "required_skills": ["Python", "RAG", "FastAPI"],
  "preferred_skills": ["Docker", "AWS", "LangChain"],
  "certifications": [],
  "experience_signals": ["LLM 서비스 개발 경험"]
}
```

## 직무별 집계 (경로 A 배치 산출물, 최종 스키마)

이 JSON이 서버에 동봉되는 정적 스킬맵의 단위(직무 × 경력수준)입니다. 런타임 툴은 이 파일들만 읽어 추론합니다.

```json
{
  "schema_version": "1.0",
  "role": "AI Engineer",
  "career_level": "junior",
  "period": "2026-Q3",
  "generated_at": "2026-07-05",
  "refresh_cadence": "weekly",
  "sources": {
    "job_info_ncs": { "type": "backbone", "coverage": "standard_competency" },
    "saramin": { "sample_size": 120, "body_available": false },
    "gongchae": { "sample_size": 30, "body_available": false }
  },
  "skills": [
    {
      "skill": "RAG",
      "category": "Data/AI",
      "frequency": 0.62,
      "evidence_count": 25,
      "requirement_type": "preferred",
      "junior_provable": "high",
      "overclaim_risk": "low",
      "priority_score": 0.81,
      "evidence_examples": ["RAG 시스템 개발 경험", "검색 증강 생성"]
    }
  ],
  "portfolio_recommendations": ["근거 기반 RAG 챗봇"],
  "notes": "역량 뼈대는 직무정보/NCS 표준역량에서, 수요 가중치(frequency)는 사람인·공채 메타에서 산출. 개별 공고 본문 실측은 경로 B(붙여넣기)에서 처리."
}
```

필드 원칙:

```text
- skill / category / junior_provable : 직무정보·NCS 표준역량 뼈대에서 채움
- frequency : 사람인·공채 메타의 직무별 수요 신호로 산출 (개별 공고 본문 아님)
- evidence_examples : 경로 B(붙여넣기) 실측 시 사용자 공고에서 채워짐
- sources.*.body_available : 본문 유무를 명시해 근거 신뢰도 추적
- priority_score : 7장 우선순위 공식(빈도+필수성+신입증명가능성+핵심성-과장위험)의 산출값
- generated_at / period / refresh_cadence : 캐시 신선도 표기 → 응답에 "○○ 기준"으로 노출
```

개인정보는 저장하지 않는 게 낫습니다. 사용자의 이력은 세션 단위로만 처리하고, 저장하더라도 명시적 동의 후 최소화해야 합니다.

---

# 12. 개발 로드맵

## 1주차: 데이터 수집 MVP

목표:

```text
- 워크넷 API 연동
- 사람인 API 연동
- 직무 키워드별 공고 수집
- JSON 정규화
```

직무 키워드:

```text
Backend: 백엔드, 서버개발자, Java, Spring
Frontend: 프론트엔드, React, TypeScript
AI: AI Engineer, LLM, RAG, 머신러닝, 생성형 AI
Security: 보안, 정보보안, 보안관제, 취약점, SOC
```

## 2주차: 요구역량 추출

목표:

```text
- 필수/우대/자격증/경험/기술스택 분리
- 스킬 동의어 사전 구축
- 직무별 Top Skill 출력
```

## 3주차: 신입용 번역 로직

목표:

```text
- 경력직 요구사항 → 신입 포트폴리오 항목 변환
- 직무별 프로젝트 템플릿 작성
- 과장 위험 키워드 경고
```

## 4주차: MCP 서버 및 PlayMCP 등록용 UX

목표:

```text
- MCP Tool 5개 구현
- 카카오톡 카드형 응답 포맷
- 예시 질문 20개
- 실패 케이스 대응
- 개인정보 미저장 정책 명시
```

---

# 13. 예선 제출용 기능 범위

예선에서는 아래 3가지만 보여줘도 충분합니다. 5개 툴 설계 중 예선 스코프는 **3개 툴로 고정**합니다.

| 예선 기능 | 담당 툴 | 데이터 경로 |
| --- | --- | --- |
| 1. 직무 요구역량 분석 | `build_role_skill_map` (캐시 조회) | 경로 A (정적 스킬맵) |
| 2. 포트폴리오 번역 | `translate_to_junior_portfolio` | 입력 기반 추론 (+경로 B 붙여넣기) |
| 3. 내 상태와 비교 | `compare_user_profile` | 입력 기반 추론 (+경로 A 스킬맵 대조) |

`search_dev_jobs`, `extract_job_requirements`는 배치(경로 A) 내부 파이프라인으로 돌리고, **예선 런타임 툴로는 노출하지 않습니다.** 이러면 실시간 API 의존이 없어 데모가 안 죽습니다.

## 1. 직무 요구역량 분석

```text
“AI Engineer 신입 공고 기준으로 요즘 뭐 요구함?”
```

출력:

```text
- 자주 등장하는 기술
- 필수/우대 구분
- 신입에게 중요한 순서
```

## 2. 포트폴리오 번역

```text
“RAG 경험 우대라는데 신입은 뭘 만들어야 함?”
```

출력:

```text
- 만들 프로젝트
- 반드시 포함할 기능
- README에 써야 할 증거
```

## 3. 내 상태와 비교

```text
“나는 Python, FastAPI, Docker 조금 할 줄 아는데 보안 직무 가능?”
```

출력:

```text
- 현재 강점
- 부족한 역량
- 4주 액션 플랜
```

---

# 14. 리스크와 대응

| 리스크        | 설명                           | 대응                            |
| ---------- | ---------------------------- | ----------------------------- |
| 기존 서비스와 중복 | 이력서/자소서 AI는 이미 많음            | 지원서 생성 제외, 공고 해석/포트폴리오 로드맵 집중 |
| 데이터 편향     | 사람인/워크넷 공고만 보면 전체 시장 대표성 부족  | “검색된 공고 기준”이라고 명시             |
| 공고 본문 누락   | API가 상세 본문을 충분히 제공하지 않을 수 있음 | 사용자가 공고 URL/본문 직접 입력 가능하게 설계  |
| 스킬 추출 오류   | LLM이 기술명을 잘못 분류할 수 있음        | 사전 기반 + LLM + 근거 문장 표시        |
| 합격 가능성 환상  | 점수화가 합격률처럼 오해될 수 있음          | “합격 가능성” 대신 “준비 우선순위”로 표현     |
| 개인정보 문제    | 이력서/프로필 저장 리스크               | 기본 미저장, 세션 처리, 사용자 동의 후 저장    |
| 크롤링 법적 리스크 | 사람인/원티드 등 플랫폼 대량 크롤링은 DB제작자 권리·부정경쟁방지법 위반 소지(잡코리아–사람인 판례) | 배치 캐시는 워크넷/사람인 공식 API만 사용, 비API 공고는 사용자 붙여넣기로 처리 |

---

# 15. 경쟁 서비스와의 차별화 정리

| 구분    | 기존 AI 취업 서비스      | 개발자 공고 해석기 MCP         |
| ----- | ----------------- | ---------------------- |
| 목적    | 공고 추천, 이력서/자소서 작성 | 직무 시장 해석, 포트폴리오 방향 설정  |
| 사용 시점 | 지원 직전             | 준비 방향 잡을 때             |
| 핵심 입력 | 이력서, 지원 공고        | 목표 직무, 최근 공고 묶음, 현재 역량 |
| 핵심 출력 | 이력서/자소서           | 요구역량 맵, 부족역량, 프로젝트 주제  |
| 차별화   | 낮음                | 신입/주니어용 번역에 집중         |

사람인도 AI 서류합격 코칭, AI 매치, AI 모의면접 등 취업 준비 기능을 제공하고, 점핏도 개발자 채용/AI 추천 포지션을 제공합니다. ([saramin.co.kr](https://www.saramin.co.kr/?srsltid=AfmBOoq8f4gv4MgVlqbMNUuKkMBUzCQIhSqS-_xLcG_QTtPPfpUryj6y), [jumpit.saramin.co.kr](https://jumpit.saramin.co.kr/))
그래서 우리는 `지원 문서 작성`을 피하고, **채용공고를 학습·포트폴리오 로드맵으로 바꾸는 해석기**로 가야 합니다.

---

# 최종 제안

## 만들 서비스

```text
개발자 공고 해석기 MCP
```

## 한 줄 소개

```text
최근 개발자 채용공고를 분석해 직무별 요구역량을 구조화하고,
신입/주니어가 어떤 포트폴리오와 학습 방향을 잡아야 하는지 알려주는 MCP.
```

## MVP 핵심 기능 3개

```text
1. 직무별 요구역량 맵
2. 경력직 공고의 신입용 포트폴리오 번역
3. 현재 역량 대비 4주 액션 플랜
```

## 가장 강한 차별화 문장

```text
기존 취업 AI는 지원서를 더 잘 쓰게 해준다.
이 MCP는 공고를 읽고, 어떤 사람이 되어야 지원할 수 있는지 알려준다.
```

이 방향이면 “취업 도우미”라는 포화 영역 안에서도 차별화가 가능합니다.
단순 채용 추천이나 자소서 생성이 아니라, **개발자 채용시장을 읽는 도구**로 포지셔닝해야 합니다.
