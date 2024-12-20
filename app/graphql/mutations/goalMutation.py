import uuid
import strawberry
from app.db.config import database
from app.graphql.schemas.GoalSchema import GoalType,GoalInput,GoalReponseType,DeleteGoalInputType,EditGoalInputType,AllUserGoalsResponseType

@strawberry.type
class GoalMutation():
    @staticmethod
    async def addNewGoal(goal:GoalInput)->GoalReponseType:
        try:
           exist_user=await database.db['users'].find_one({"username":goal.username})
           if not exist_user:
              return GoalReponseType(success=False,message="No user Exists!")
           
           allUserGoals=exist_user['goals']
           
           # exception here goals cannot exceed length of 6
           if len(allUserGoals)>=6:
               return GoalReponseType(success=False,message="you cannot create more than 6 goals")
           
           
           existing_goal = next((g for g in allUserGoals if g['goalCategory'] == goal.goalCategory), None)
           if existing_goal:
               return GoalReponseType(success=False,message="A goal with same category exists!")
               
    
           newGoal=GoalType(
               goalId=str(exist_user['settedGoals']+1),
               goalAmount=goal.goalAmount,
               goalCategory=goal.goalCategory,
               goalDescription=goal.goalDescription,
               goalStartDate=goal.goalStartDate,
               goalEndDate=goal.goalEndDate,
               goalType=goal.goalType,
               goalReminderFreq=goal.goalReminderFreq
           )
           newGoal=newGoal.__dict__
           allUserGoals.append(newGoal)
           
           await database.db['users'].find_one_and_update({"username":goal.username},{"$set":{"goals":allUserGoals}})
           await database.db['users'].find_one_and_update({"username":goal.username},{"$set":{"settedGoals":exist_user['settedGoals']+1}})
           #graphql expects the goal to be a object not a dictionary so converting back to object
           newGoal=GoalType(**newGoal)
           return GoalReponseType(success=True,message="goal added successfully!",goal=newGoal)
           
           

        except Exception as e:
            return GoalReponseType(success=False,message=e)
        
    @staticmethod
    async def deleteGoal(goal:DeleteGoalInputType)->GoalReponseType:
        try:
           exist_user=await database.db['users'].find_one({"username":goal.username})
           if not exist_user:
              return GoalReponseType(success=False,message="No user Exists!")
           allUsersGoals=exist_user['goals']
        #    print(allUsersGoals)
           
           goalIdToBeDeleted=goal.goalId
           isExists=False
           for i in range(len(allUsersGoals)):
               if goalIdToBeDeleted == allUsersGoals[i]['goalId']:
                   isExists=True
                   break
           
            
           if isExists==False:
              return GoalReponseType(success=False,message='Goal not found!') 
               
                
                   
               
           
           goalsAfterDeletion=[goal for goal in allUsersGoals if goal['goalId']!=goalIdToBeDeleted]
           
           await database.db['users'].find_one_and_update({"username":goal.username},{"$set":{"goals":goalsAfterDeletion,"settedGoals":exist_user['settedGoals']-1}})
          
           return GoalReponseType(success=True,message='Goal Deleted Succesfully!')     
            
        except Exception as e:
            print(e)
            return GoalReponseType(success=False,message='Server Error!')  
        
        
    @staticmethod
    async def editGoal(goal:EditGoalInputType)->GoalReponseType:
        try:
            exist_user=await database.db['users'].find_one({"username":goal.username})
            if not exist_user:
                return GoalReponseType(success=False,message='User not found!')
            
            updationRequired={}
            if goal.goalAmount is not None and goal.goalAmount!=0:
                updationRequired["goals.$.goalAmount"]=goal.goalAmount
            if goal.goalEndDate is not None:
                updationRequired["goals.$.goalEndDate"]=goal.goalEndDate
            if goal.goalDescription is not None:
                updationRequired["goals.$.goalDescription"]=goal.goalDescription  
            # print(updationRequired)    
            result=await database.db['users'].update_one({"username":goal.username,"goals.goalId":goal.goalId},{"$set":updationRequired})   
            # print(result)  
            user=await database.db['users'].find_one({"username":goal.username})
            updateGoal = next((g for g in user['goals'] if g['goalId'] == goal.goalId), None)
            if result.matched_count==0:
                return  GoalReponseType(success=False,message='GoalId not found!')    
             
            return GoalReponseType(success=True, message=f"Goal with ID {goal.goalId} updated successfully.",goal=GoalType(**updateGoal))
            
            
            
        except Exception as e:
            print(e)
            return GoalReponseType(success=False,message='Server Error!')
    
    
    
            
             
        

        

