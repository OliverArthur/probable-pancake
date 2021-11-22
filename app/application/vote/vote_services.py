from abc import ABC

from fastapi import HTTPException, status

from app.domain.vote.interfaces.vote_repo import IVoteRepo
from app.domain.posts.interfaces.posts_repo import IPostsRepo

class VoteServices(ABC):
    @classmethod
    def vote(
        cls,
        vote_repo: IVoteRepo,
        posts_repo: IPostsRepo,
        user_id: int,
        post_id: int,
        direction: int,
    ) -> str:
        try:
            post = posts_repo.fetch(post_id)
            query_vote = vote_repo.fetch(post_id)

            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found",
                )

            if direction == 1:
                if query_vote:
                    raise HTTPException(
                        status_code=status.HTTP_409_CONFLICT,
                        detail="You have already voted for this post",
                    )

                vote_repo.vote(user_id, post_id)
                return "Voted successfully"
            else:
                if not query_vote:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail="You have not voted for this post",
                    )

                vote_repo.unvote(post_id)
                return "Vote remove successfully"
        except (ValueError, TypeError, AttributeError) as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(e),
            )
