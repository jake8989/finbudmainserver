import strawberry
from typing import Optional, List
@strawberry.input
class accumulatedDataInput():
    year:str
    username:str
    

@strawberry.type
class cateogoryWiseExpense():
    label:str
    data:List[int]
        
@strawberry.type
class categoryWiseMonthlyExpensesResponse():
    success:bool
    message:str
    categoryWiseExpenses:Optional[List[cateogoryWiseExpense]]=None
    
@strawberry.type
class incomeType():
    amount:int
    incomeDate:str
    
@strawberry.type
class expenseType():
    amount:int
    expenseDate:str 
       
@strawberry.type
class accumulatedDataResponseType():
    success:bool
    message:str
    income:Optional[List[int]]=None
    expense:Optional[List[int]]=None
        