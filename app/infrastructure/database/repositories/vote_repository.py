from app.domain.vote.entities.vote import Vote, VoteCreate
from app.infrastructure.database.models.vote import Vote as VoteModel
from app.infrastructure.database.sqlalchemy import db


def fetch(post_id: int, user_id: int) -> Vote:
    return (
        db.query(VoteModel)
        .filter(VoteModel.post_id == post_id, VoteModel.user_id == user_id)
        .first()
    )


def vote(user_id: int, post_id: int) -> None:
    vote_model = VoteModel(user_id=user_id, post_id=post_id)

    db.add(vote_model)
    db.commit()
    db.refresh(vote_model)


def unvote(post_id: int) -> None:
    vote_model = db.query(VoteModel).filter(VoteModel.post_id == post_id).first()

    db.delete(vote_model)
    db.commit()
