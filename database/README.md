# BuildLog 데이터베이스

BuildLog는 하나의 SQLAlchemy 모델과 Alembic 마이그레이션을 두 데이터베이스 환경에 사용합니다.

- SQLite3: 로컬 개발과 자동 테스트
- Supabase PostgreSQL: 실제 서비스

## SQLite3

기본 `DATABASE_URL`은 `sqlite:///./buildlog.db`입니다. 백엔드 폴더에서 마이그레이션을 실행하면 `backend/buildlog.db`가 만들어집니다.

SQLite3 파일은 생성 결과이므로 Git에서 제외합니다.

## Supabase

Supabase 프로젝트를 만든 뒤 PostgreSQL 연결 주소를 로컬 `.env`의 `DATABASE_URL`에 입력합니다.

```dotenv
DATABASE_URL=postgresql://USER:PASSWORD@HOST:5432/postgres
```

실제 사용자명, 비밀번호와 호스트 주소는 문서나 Git에 저장하지 않습니다.

## 마이그레이션

```powershell
Set-Location backend
..\.venv\Scripts\python.exe -m alembic upgrade head
```

새 데이터 구조 변경은 SQLAlchemy 모델을 수정한 뒤 Alembic 마이그레이션으로 기록합니다. SQLite3 테스트를 먼저 통과하고 Supabase에 적용합니다.

