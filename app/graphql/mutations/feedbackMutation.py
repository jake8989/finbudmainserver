import strawberry
from app.graphql.schemas.feedbackSchema import FeedBackInputType,FeedBackResponseType
from app.db.config import database
from app.modals.FeedBackModel import FeedBackModel
import uuid
@strawberry.type
class FeedBackMutation():
    @staticmethod
    async def newFeedBack(feedback:FeedBackInputType)->FeedBackResponseType:
        try:
            newFeedback=FeedBackModel(
                feedbackId=str(uuid.uuid4()),
                feedbackUserEmail=feedback.feedbackUserEmail,
                feedbackUserSubject=feedback.feedbackUserSubject,
                feedbackUserMessage=feedback.feedbackUserMessage
            )
            
            await database.db['feedbacks'].insert_one(newFeedback.model_dump(by_alias=True))
            return FeedBackResponseType(success=True,message='Added!')
            
            pass
        except Exception as E:
            return FeedBackResponseType(success=False,message=E)
         
            