import strawberry
from typing import Optional

@strawberry.input
class FeedBackInputType():
    feedbackUserEmail:str
    feedbackUserSubject:Optional[str]=None
    feedbackUserMessage:str
    
    
@strawberry.type
class FeedBackResponseType():
    success:bool
    message:str
        