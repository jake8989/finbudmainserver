import strawberry
from app.graphql.schemas.UserSchema import UserType 
from app.graphql.mutations.userMutation import UserMutations
from app.graphql.mutations.userMutation import UserMutationResponse
from app.graphql.mutations.expenseMutation import ExpenseMutation,ExpenseCategoryResponse
from app.graphql.mutations.goalMutation import GoalMutation
from app.graphql.queries.goalQuery import GoalQuery
from app.graphql.schemas.GoalSchema import GoalReponseType,AllUserGoalsResponseType
from app.graphql.schemas.ExpenseSchema import ExpenseResponseType,ExpenseGetCategoriesResponseType
from app.graphql.queries.testQuery import TestQuery
from app.graphql.queries.expenseQuery import ExpenseQuery
from app.graphql.mutations.incomeMutation import IncomeMutation
from app.graphql.schemas.IncomeSchema import AddIncomeResponseType
from app.graphql.queries.chartQuery import ChartQuery
from app.graphql.schemas.chartSchema import accumulatedDataResponseType,categoryWiseMonthlyExpensesResponse
from app.graphql.schemas.feedbackSchema import FeedBackResponseType
from app.graphql.mutations.feedbackMutation import FeedBackMutation
from app.graphql.mutations.OTPMutation import OTPMutation
from app.graphql.schemas.OTP import OTPSendResponseType
# from app.graphql.queries.testQuery import 
@strawberry.type
class Mutation:
    registerUser: UserMutationResponse = strawberry.mutation(resolver=UserMutations.registerUser)
    loginUser:UserMutationResponse = strawberry.mutation(resolver=UserMutations.loginUser)
    createExpense:ExpenseResponseType=strawberry.mutation(resolver=ExpenseMutation.createExpense)
    createExpenseCategory:ExpenseCategoryResponse=strawberry.mutation(resolver=ExpenseMutation.createNewExpenseCategory)
    addNewGoal:GoalReponseType=strawberry.mutation(resolver=GoalMutation.addNewGoal)
    deleteGoal:GoalReponseType=strawberry.mutation(resolver=GoalMutation.deleteGoal)
    editGoal:GoalReponseType=strawberry.mutation(resolver=GoalMutation.editGoal)
    addIncome:AddIncomeResponseType=strawberry.mutation(resolver=IncomeMutation.createIncome)
    newFeedBack:FeedBackResponseType=strawberry.mutation(resolver=FeedBackMutation.newFeedBack)
    generateAndSendOTP:OTPSendResponseType=strawberry.mutation(resolver=OTPMutation.generateAndSendOTP)
    verifyOTP:OTPSendResponseType=strawberry.mutation(resolver=OTPMutation.verifyOTP)

@strawberry.type
class Query:
    testQuery:str=strawberry.mutation(resolver=TestQuery.testQuery)
    getAllExpenseCategories:ExpenseGetCategoriesResponseType=strawberry.mutation(resolver=ExpenseQuery.getAllExpenseCategories)
    getAllUserGoals:AllUserGoalsResponseType=strawberry.mutation(resolver=GoalQuery.getAllUserGoals)
    getAccumulatedData:accumulatedDataResponseType=strawberry.mutation(resolver=ChartQuery.getAccumulatedData)
    getCategoryWiseExpenseData:categoryWiseMonthlyExpensesResponse=strawberry.mutation(resolver=ChartQuery.getCategoryWiseExpenseData)
