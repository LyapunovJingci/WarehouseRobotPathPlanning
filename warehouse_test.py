#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 31 21:14:11 2020

@author: jingci
"""

from new_small_maze import Maze
from RL_brain_Robo1 import QLearningTable1
from RL_brain_Robo2 import QLearningTable2
from RL_brain_Robo3 import QLearningTable3
from returnBrain1 import ReturnQLearningTable1
from returnBrain2 import ReturnQLearningTable2
from returnBrain3 import ReturnQLearningTable3
import matplotlib.pyplot as plt
import pickle
#HUMANWALK1 = [2,2,2,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
HUMANWALK1 = [4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4,4]
UNIT = 20
STATE0 = "RAW"
STATE1 = "MAP"
STATE2 = "PATH"
CHOSENSTATE = STATE2
RECORDDATA = False

def update():
    totalReward1 = 0
    totalReward2 = 0
    totalReward3 = 0
    rewardList1 = []
    rewardList2 = []
    rewardList3 = []
    totalRewardList = []

    freeze1 = False
    freeze2 = False
    freeze3 = False
    for episode in range(300):
        # initial observation
        observation1, observation2, observation3 = env.resetRobot()
        #nearbyEnvironment(observation1)
        human1, human2 = env.resetHuman()
        humanWalkHelper = 0
        wait_time = 0
        while True:
            # fresh env
            env.render()
            
            if humanWalkHelper % 2 == 0:
                if humanWalkHelper/2 < len(HUMANWALK1):
                    human1 = env.humanStep1(HUMANWALK1[int(humanWalkHelper/2)])
                else:
                    human1 = env.humanStep1(4)
            else:
                human1 = env.humanStep1(4)
            humanWalkHelper +=1

            # RL choose action based on observation
            if freeze1:
                action1 = 4
            else:
                # Choose action
                action1 = chooseAction(episode, RL1, observation1)   
                # RL take action and get next observation and reward
                #directEnvironment = directNearbyEnvironment(observation1)
                
                observation1_, reward1, done1 = env.step1(action1)
                totalReward1+=reward1
                # RL learn from this transition
                learn (episode, RL1, action1, reward1, observation1, observation1_)

                # swap observation
                observation1 = observation1_
            
            if freeze2:
                action2 = 4
            else:                
                # Choose action
                action2 = chooseAction(episode, RL2, observation2)        
                # RL take action and get next observation and reward
                #------------------------------------
                
                directEnvironment2 = directNearbyEnvironment(observation2)
                if human1 in directEnvironment2:
                    print('进这儿')
                    if human1 == directEnvironment2[0] and action2 == 0:
                        observation2_, reward2, done1 = env.step2(1)
                    elif human1 == directEnvironment2[1] and action2 == 1:
                        if wait_time > 5:
                            observation2_, reward2, done2 = env.step2(4)
                        else:
                            observation2_, reward2, done2 = env.step2(4)
                            wait_time +=1
                    elif human1 == directEnvironment2[2] and action2 == 3:
                        observation2_, reward2, done2 = env.step2(2)
                    elif human1 == directEnvironment2[3] and action2 == 2:
                        observation2_, reward2, done2 = env.step2(3)
                else:
                    observation2_, reward2, done2 = env.step2(action2)
                

                #------------------------------------   
                
                #observation2_, reward2, done2 = env.step2(action2)
                totalReward2+=reward2
                # RL learn from this transition
                learn (episode, RL2, action2, reward2, observation2, observation2_)

                # swap observation
                observation2 = observation2_
                
            if freeze3:
                action3 = 4
            else:
                # Choose action
                action3 = chooseAction(episode, RL3, observation3) 
                # RL take action and get next observation and reward         
                #---------------------------------------------
                '''
                directEnvironment = directNearbyEnvironment(observation3)
                if observation1 in directEnvironment or observation2 in directEnvironment:
                    print("进来了")
                    if observation2 == directEnvironment[0] or observation1 == directEnvironment[0]:
                        if action3 == 0:
                            observation3_, reward3, done3 = env.step3(1)
                        else:
                            observation3_, reward3, done3 = env.step3(action3)
                    elif observation2 == directEnvironment[1] or observation1 == directEnvironment[1]:
                        if action3 == 1:
                            observation3_, reward3, done3 = env.step3(0)
                        else:
                            observation3_, reward3, done3 = env.step3(action3)
                    elif observation2 == directEnvironment[2] or observation1 == directEnvironment[2]:
                        print("又进来了")
                        print(action3)
                        if action3 == 3:
                            observation3_, reward3, done3 = env.step3(4)
                        else:
                            observation3_, reward3, done3 = env.step3(action3)
                    elif observation2 == directEnvironment[3] or observation1 == directEnvironment[3]:
                        print("又进来了")
                        print(action1)
                        if action3 == 2:
                            observation3_, reward3, done3 = env.step3(4)
                        else:
                            observation3_, reward3, done3 = env.step3(action3)
                else:
                    observation3_, reward3, done3 = env.step3(action3)
                
                
                
                '''
                #---------------------------------------------
                observation3_, reward3, done3 = env.step3(action3)
                totalReward3+=reward3
                # RL learn from this transition
                learn (episode, RL3, action3, reward3, observation3, observation3_)

                # swap observation
                observation3 = observation3_
            
            # break while loop when end of this episode
                
            if (done1 == 'hit' or done1 == 'arrive') and (done2 == 'hit' or done2 == 'arrive') and (done3 == 'hit' or done3 == 'arrive'):
                print (episode, 'trial: ','Robot1: ', totalReward1, '; Robot2: ', totalReward2, '; Robot3: ', totalReward3)
                #print (freeze1, freeze2, freeze3)
                rewardList1.append(totalReward1)
                rewardList2.append(totalReward2)
                rewardList3.append(totalReward3)
                totalRewardList.append(totalReward1+totalReward2+totalReward3)
                totalReward1 = 0
                totalReward2 = 0
                totalReward3 = 0
                if done1 == 'arrive' and done2 == 'arrive' and done3 == 'arrive':
                    for i in range(50):
                        if startReturnTable (episode, observation1, ReturnRL1,1) == 'arrive':
                            break
                    for i in range(50): 
                        if startReturnTable (episode, observation2, ReturnRL2,2) == 'arrive':
                            break
                    for i in range(50): 
                        if startReturnTable (episode, observation3, ReturnRL3,3) == 'arrive': 
                            break

                freeze1 = False
                freeze2 = False
                freeze3 = False
                break
            if done1 == 'hit' or done1 == 'arrive':
                freeze1 = True
            if done2 == 'hit' or done2 == 'arrive':
                freeze2 = True
            if done3 == 'hit' or done3 == 'arrive':
                freeze3 = True
       
        # Train the map and dump into pickle
        '''
        if episode == 2500:     
            f1 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_q_table1.txt', 'wb')
            pickle.dump(RL1.q_table,f1)
            f1.close()
            f2 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_table2.txt', 'wb')
            pickle.dump(RL2.q_table,f2)
            f2.close()
            f3 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_table3.txt', 'wb')
            pickle.dump(RL3.q_table,f3)
            f3.close()
        '''
    if RECORDDATA:
        f1 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable1.txt', 'wb')
        pickle.dump(ReturnRL1.q_table,f1)
        f1.close()
        f2 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable2.txt', 'wb')
        pickle.dump(ReturnRL2.q_table,f2)
        f2.close()
        f3 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/Return_qtable3.txt', 'wb')
        pickle.dump(ReturnRL3.q_table,f3)
        f3.close()
        f4 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable1.txt', 'wb')
        pickle.dump(RL1.q_table,f4)
        f4.close()
        f5 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable2.txt', 'wb')
        pickle.dump(RL2.q_table,f5)
        f5.close()
        f6 = open('/Users/jingci/Desktop/RL/warehouseTest/WarehouseRobotPathPlanning-master/path_qtable3.txt', 'wb')
        pickle.dump(RL3.q_table,f6)
        f6.close()

    plot(rewardList1)
    plot(rewardList2)
    plot(rewardList3)   
    plot(totalRewardList)                    
    # end of game         
    print('game over')
    env.destroy()
    #print(rewardList)
    
def startReturnTable (episode, observation, RL, robotNumber):
    #observation1, observation2, observation3 = env.resetRobot()
    while True:
        env.render()
        action = chooseNoRandomAction(RL, observation)
        if robotNumber == 1:
            observation_, reward, done = env.returnStep1(action)
        elif robotNumber == 2:
            observation_, reward, done = env.returnStep2(action)
        elif robotNumber == 3:
            observation_, reward, done = env.returnStep3(action)
        learn (episode, RL, action, reward, observation, observation_)
        observation = observation_
        #print (done)
        if done == 'arrive' or done == 'hit':
            break
    return done

def chooseNoRandomAction(RL, observation):
    return RL.choose_action(str(observation),1)
      
def chooseAction (episode, RL, observation):
    if episode < -1:
        return RL.choose_action(str(observation), 0.9 + episode * 0.001)
    else:
        return RL.choose_action(str(observation),1)

def learn (episode, RL, action, reward, observation, observation_):
     if episode < 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.03, 0.9)
     elif episode < 1500 and episode >= 500:
         RL.learn(str(observation), action, reward, str(observation_), 0.3-0.0002*(episode-500), 0.9)
     else:
         RL.learn(str(observation), action, reward, str(observation_), 0.001, 0.9)
 
def plot(reward):
    plt.style.use('seaborn-deep')
    plt.plot(reward,linewidth= 0.3)
    plt.title('Q Learning Total Reward')
    plt.xlabel('Trial')
    plt.ylabel('Reward')
    plt.show() 

def nearbyEnvironment(coordinate):
    left = [coordinate[0]-UNIT, coordinate[1], coordinate[2]-UNIT, coordinate[3]]
    right = [coordinate[0]+UNIT, coordinate[1], coordinate[2]+UNIT, coordinate[3]]
    up = [coordinate[0], coordinate[1]-UNIT, coordinate[2], coordinate[3]-UNIT]
    down = [coordinate[0], coordinate[1]+UNIT, coordinate[2], coordinate[3]+UNIT]
    upleft = [coordinate[0]-UNIT, coordinate[1]-UNIT, coordinate[2]-UNIT, coordinate[3]-UNIT]
    upright = [coordinate[0]+UNIT, coordinate[1]-UNIT, coordinate[2]+UNIT, coordinate[3]-UNIT]
    downleft = [coordinate[0]-UNIT, coordinate[1]+UNIT, coordinate[2]-UNIT, coordinate[3]+UNIT]
    downright = [coordinate[0]+UNIT, coordinate[1]+UNIT, coordinate[2]+UNIT, coordinate[3]+UNIT]
    nearby = [upleft, up, upright, left, right, downleft, down, downright]
    return nearby

def directNearbyEnvironment(coordinate):
    left = [coordinate[0]-UNIT, coordinate[1], coordinate[2]-UNIT, coordinate[3]]
    right = [coordinate[0]+UNIT, coordinate[1], coordinate[2]+UNIT, coordinate[3]]
    up = [coordinate[0], coordinate[1]-UNIT, coordinate[2], coordinate[3]-UNIT]
    down = [coordinate[0], coordinate[1]+UNIT, coordinate[2], coordinate[3]+UNIT]
    nearby = [up, down, left, right]
    return nearby
    
if __name__ == "__main__":
    env = Maze()
    RL1 = QLearningTable1(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    RL2 = QLearningTable2(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    RL3 = QLearningTable3(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    backupRL1 = QLearningTable1(actions=list(range(env.n_actions)),state=STATE1)
    backupRL2 = QLearningTable2(actions=list(range(env.n_actions)),state=STATE1)
    backupRL3 = QLearningTable3(actions=list(range(env.n_actions)),state=STATE1)
    ReturnRL1 = ReturnQLearningTable1(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    ReturnRL2 = ReturnQLearningTable2(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    ReturnRL3 = ReturnQLearningTable3(actions=list(range(env.n_actions)),state=CHOSENSTATE)
    env.after(300, update)
    env.mainloop()
