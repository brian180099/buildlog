# BuildLog

BuildLog는 공부한 내용, 프로젝트 할 일, 오류와 해결 방법을 기록하고 공개한 개발 경험을 다른 사용자와 나누는 서비스입니다.

현재 **Phase 3 — 공통 화면과 반응형 틀**까지 로컬 구현이 완료됐습니다. 인증과 화면 기반은 SQLite3로 동작하며, 실제 기록 기능은 다음 Phase부터 차례로 연결합니다. Supabase는 운영 환경 검증 때 연결합니다.

## 기술 구성

- 프론트엔드: React, TypeScript, Vite
- 백엔드: FastAPI, SQLAlchemy 2, Alembic
- 운영 데이터베이스: Supabase PostgreSQL
- 로컬·테스트 데이터베이스: SQLite3
- 테스트: Vitest, Testing Library, pytest

## 준비 사항

- Node.js 24 이상
- Python 3.13 이상
- npm

Supabase 프로젝트는 로컬 개발을 시작할 때 없어도 됩니다. 기본 설정은 SQLite3를 사용합니다.

## 처음 실행하기

### 1. 환경 설정

프로젝트 루트의 `.env.example`을 복사해 `.env`를 만듭니다.

```powershell
Copy-Item .env.example .env
```

`.env`는 Git에서 제외됩니다. 실제 비밀번호, Supabase 연결 주소와 보안 키를 `.env.example`이나 소스 코드에 적지 마세요.

로컬에서는 기본값을 그대로 사용할 수 있습니다. 실제 Supabase를 연결할 때만 `DATABASE_URL`을 Supabase PostgreSQL 연결 주소로 바꿉니다.

### 2. 백엔드 설치

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -e ".\backend[dev]"
```

### 3. 데이터베이스 준비

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m alembic upgrade head
Set-Location ..
```

기본 설정에서는 `backend/buildlog.db` SQLite3 파일이 만들어집니다. 이 파일은 Git에 저장되지 않습니다.

### 4. 백엔드 실행

```powershell
.\.venv\Scripts\python.exe -m uvicorn app.main:app --app-dir backend --reload
```

- API: http://localhost:8000
- 상태 확인: http://localhost:8000/api/health
- API 문서: http://localhost:8000/docs

### 5. 프론트엔드 설치와 실행

새 PowerShell 창에서 실행합니다.

```powershell
Set-Location frontend
npm.cmd install
npm.cmd run dev
```

- 웹 화면: http://localhost:5173

## 검사 명령

### 백엔드

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m ruff check app tests
..\.venv\Scripts\python.exe -m pytest
```

### 프론트엔드

```powershell
Set-Location frontend
npm.cmd run lint
npm.cmd run test
npm.cmd run build
```

## 데이터베이스 사용 원칙

- 자동 테스트는 SQLite3를 사용합니다.
- 실제 서비스는 Supabase PostgreSQL을 사용합니다.
- 두 환경은 같은 SQLAlchemy 모델과 Alembic 마이그레이션을 사용합니다.
- SQLite3 테스트를 통과한 뒤 Supabase 환경에서 주요 저장·조회와 권한을 다시 확인합니다.
- Supabase 연결 정보는 `.env`에만 저장합니다.

## 프로젝트 구조

```text
buildlog/
├─ backend/              FastAPI, SQLAlchemy, Alembic, pytest
│  ├─ alembic/           데이터베이스 변경 이력
│  ├─ app/               API와 데이터 모델
│  └─ tests/             백엔드 테스트
├─ database/             데이터베이스 사용 안내
├─ docs/                 MVP, PRD, 기능 명세와 개발 계획
├─ frontend/             React, TypeScript, Vite
├─ .env.example          비밀값이 없는 환경 설정 예시
└─ README.md
```

## 현재 데이터 구조

- 사용자
- 공부 기록
- 할 일
- 오류 기록
- 댓글
- 좋아요
- 신고

신고에는 신고 당시 대상 정보가 남습니다. 공부 기록이나 오류 기록이 삭제되면 연결된 댓글과 좋아요는 함께 삭제되지만, 기존 신고는 운영자 확인을 위해 유지할 수 있는 구조입니다.

## 기획 문서

- [MVP](docs/mvp.md)
- [제품 요구사항](docs/PRD.md)
- [기능 동작 설명서](docs/spec.md)
- [개발 계획](docs/plan.md)

## GitHub

- 저장소: https://github.com/brian180099/buildlog

