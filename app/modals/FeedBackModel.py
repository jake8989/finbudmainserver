from pydantic import BaseModel
from typing import Optional
class FeedBackModel(BaseModel):
    feedbackId:str
    feedbackUserEmail:str
    feedbackUserSubject:Optional[str]=None
    feedbackUserMessage:str