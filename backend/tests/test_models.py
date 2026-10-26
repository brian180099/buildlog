from sqlalchemy import inspect
from sqlalchemy.orm import Session

from app.db.session import create_db_engine
from app.models import Base, Comment, RecordLike, Report, StudyRecord, User


def test_all_phase_one_tables_are_created_in_sqlite() -> None:
    engine = create_db_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    table_names = set(inspect(engine).get_table_names())

    assert table_names == {
        "comments",
        "error_records",
        "record_likes",
        "reports",
        "study_records",
        "todo_items",
        "users",
    }


def test_record_deletion_cascades_reactions_but_preserves_report_snapshot() -> None:
    engine = create_db_engine("sqlite:///:memory:")
    Base.metadata.create_all(engine)

    with Session(engine) as session:
        user = User(
            email="learner@example.com",
            password_hash="not-a-real-password",
            nickname="learner",
        )
        study = StudyRecord(
            author=user,
            title="FastAPI 기초",
            content="라우터와 의존성 주입을 공부했다.",
            is_public=True,
        )
        session.add_all([user, study])
        session.flush()

        session.add_all(
            [
                Comment(author=user, study_record=study, content="유용한 기록"),
                RecordLike(user=user, study_record=study),
                Report(
                    reporter=user,
                    target_type="study_record",
                    target_id=study.id,
                    target_snapshot={"title": study.title},
                    reason="테스트 신고",
                ),
            ]
        )
        session.commit()

        session.delete(study)
        session.commit()

        assert session.query(Comment).count() == 0
        assert session.query(RecordLike).count() == 0
        report = session.query(Report).one()
        assert report.target_snapshot == {"title": "FastAPI 기초"}

