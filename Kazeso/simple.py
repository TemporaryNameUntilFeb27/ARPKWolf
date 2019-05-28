#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import random

# this is main script
# simple version

import aiwolfpy
import aiwolfpy.contentbuilder as cb

myname = 'Kazeso'

class SampleAgent(object):
    
    def __init__(self, agent_name):
        # myname
        self.myname = agent_name
        
    def getName(self):
        return self.myname
    
    def initialize(self, base_info, diff_data, game_setting):
        self.base_info = base_info
        # game_setting
        self.game_setting = game_setting

        #生き残っているリスト、死んだリスト
        self.alive_list = []
        self.dead_list = []

        self.myresult = ""
        self.comingout = ""
        self.not_reported = ""
        self.comingout_not_reported = True
        self.divined_list = []

        #全ての占い師から白出しされている
        self.white_list = []
        #一人以上の占い師から白出しされている
        self.white_gray_list = []
        #誰にも占われていない
        self.gray_list = []
        #一人以上の占い師から黒だしされている
        self.dark_list =[]
        #黒出ししている占い師と白だししている占い師がいる
        self.dark_white = []

        #役職持ちのリスト
        self.with_potision_list = []
        self.divined_result_dic = {}

        #エラーが出るため仕方なくselfに含める
        self.vote_ahed=""
        
        #占い師のリスト(騎士に誰を守るか判断させるためのもの)
        self.divined_people_list=[]

        #霊媒師のリスト(騎士に誰を守るか判断させるためのもの)
        self.medium_people_list=[]

        for n in self.base_info['statusMap'].keys():
            if self.base_info['statusMap'][n] == 'ALIVE':
                if int(n) not in self.alive_list:
                    self.gray_list.append(int(n))
                    self.alive_list.append(int(n))
            else:
                if int(n) not in self.dead_list:
                    self.alive.list.remove(int(n))
                    self.dead_list.append(int(n))



        
    def update(self, base_info, diff_data, request):
        self.base_info = base_info
        self.diff_data = diff_data

        if request == 'DAILY_INITIALIZE':
            for i in range(diff_data.shape[0]):
                # IDENTIFY
                if diff_data['type'][i] == 'identify':
                    self.not_reported = True
                    self.myresult = diff_data['text'][i]
                # DIVINE
                elif diff_data['type'][i] == 'divine':
                    self.myresult = diff_data['text'][i]
                    self.not_reported = True
                    print(self.myresult)
                # GUARD
                elif diff_data['type'][i] == 'guard':
                    self.myresult = diff_data['text'][i]
                elif diff_data['type'][i] == 'possessed':
                    self.myresult = "DIVINED Agent[01] WEREWOLF"
                    self.not_reported = True


        elif request == 'TALK':
            for i in range(self.diff_data.shape[0]):
                content = self.diff_data.text[i].split()
                if content[0] == 'COMINGOUT':
                    if content[2] == 'SEER':
                        if int(self.diff_data.agent[i]) not in self.with_potision_list:
                            self.with_potision_list.append(int(self.diff_data.agent[i]))
                        if int(self.diff_data.agent[i]) not in self.divined_people_list:
                            self.divined_result_dic[int(content[1][6:8])] = []
                    if content[2] == 'MEDIUM':
                        if int(self.diff_data.agent[i]) not in self.with_potision_list:
                            self.with_potision.append(int(self.diff_data.agent[i]))
                        if int(self.diff_data.agent[i]) not in self.medium_people_list:
                            self.medium_people_list.append(int(self.diff_data_agent[i]))
                if content[0] == 'DIVINED':
                    print(content)
                    temp_divined_ahed = int(content[1][6:8])
                    #占い結果をリストに格納していく
                    print(self.diff_data)
                    if content[2] == 'HUMAN':
                        #白だしされた人が既に白だしされていたら、ホワイトよりのグレーからホワイトに昇格
                        if temp_divined_ahed in self.white_gray_list and temp_divined_ahed not in self.white_list:
                            self.white_list.append(temp_divined_ahed)
                            self.white_gray_list.remove(temp_divined_ahed)
                        #ホワイトよりのグレーに加える
                        else:
                            self.white_gray_list.append(temp_divined_ahed)
                            if temp_divined_ahed not in self.gray_list:
                                self.gray_list.remove(temp_divined_ahed)
                    if content[2] == 'WEREWOLF':
                        #黒だしされた人が既に白だしされていたら、黒か白かわからないリストに格納
                        if int(temp_divined_ahed) in self.white_gray_list:
                            self.dark_white_list.append(temp_divined_ahed)
                            self.white_list.remove(temp_divined_ahed)
                        #他の人から白だしされてなかったら黒
                        else:
                            self.gray_list.remove(temp_divined_ahed)
                            self.dark_list.append(temp_divined_ahed)


                    self.divined_result_dic[self.diff_data.agent[i]].append(self.diff_data.text[i])
                    print("Agent"+str(self.diff_data.agent[i])+"was divined"+str(self.divined_result_dic[self.diff_data.agent[i]]))

                
        for n in self.base_info['statusMap'].keys():
            if self.base_info['statusMap'][n] == 'ALIVE':
                if int(n) not in self.alive_list:
                    self.alive_list.append(int(n))
            else:
                if int(n) not in self.dead_list:
                    self.alive_list.remove(int(n))
                    self.dead_list.append(int(n))


    def dayStart(self):
        self.talk_turn = 0
        #self.printList()
        return None
    
    def talk(self):
        #カミングアウト
        self.talk_turn+=1
        if self.base_info['myRole'] == 'SEER' and self.comingout_not_reported:
            self.comingout = 'SEER'
            self.comingout_not_reported = False
            return cb.comingout(self.base_info['agentIdx'], self.comingout)
        
        elif self.base_info['myRole'] == 'POSSESSED' and self.comingout_not_reported:
            self.comingout = 'SEER'
            self.comingout_not_reported = False
            return cb.comingout(self.base_info['agentIdx'], self.comingout)


        #占い結果
        if self.base_info['myRole'] == 'SEER' and self.not_reported:
            self.not_reported = False
            print("tell divined result")
            print(self.myresult)
            return self.myresult
        elif self.base_info['myRole'] == 'POSSESSED' and self.not_reported:
            print("tell divined result")
            self.not_reported = False
            self.myresult = "DIVINED Agent[01] WEREWOLF"
            return self.myresult
        elif self.base_info['myRole'] == 'MEDIUM' and self.not_reported:
            self.not_reported = False
            return self.myresult

        if self.talk_turn<=10:
            return cb.skip()
        else:
            return cb.over

    def whisper(self):
        return cb.over()
        
    def vote(self):
        self.printList()
        #人狼は基本潜伏と考える
        if len(self.dark_list)!=0:
            print("vote divined wolf")
            self.vote_ahed = random.choice(self.dark_list)
            print(self.vote_ahed)
        #役職持ち以外、白だしされていない人からグレラン
        elif len((set(self.alive_list)-set(self.with_potision_list))&set(self.gray_list))!=0:
            print("vote graylist and with_potision_list")
            print((set(self.alive_list)-set(self.with_potision_list))&set(self.gray_list))
            self.vote_ahed = random.choice(list((set(self.alive_list)-set(self.with_potision_list))&set(self.gray_list)))
        elif len(set(self.alive_list)-set(self.with_potision_list))!=0:
            print("vote with_potision_list")
            self.vote_ahed = random.choice(list(set(self.alive_list)-set(self.with_potision_list)))
        else:
            print("vote random")
            self.vote_ahed = random.choice(self.alive_list)
        return self.vote_ahed

    def attack(self):
        if len(self.white_list) == 0:
            if len(self.white_gray_list) == 0:
                if len(self.gray_list) == 0:
                    random.choice(self.alive_list)
                else:
                    attack_ahed = random.choice(self.gray_list)
            else:
                attack_ahed = random.choice(self.white_gray_list)
        else:
            attack_ahed = random.choice(self.white_list)

        return attack_ahed
    
    def divine(self):
        idx = random.choice(self.alive_list)
        self.divined_list.append(idx)
        divine_ahed_set = set(self.alive_list) & set(self.divined_list)
        return random.choice(list(divine_ahed_set))
    
    def guard(self):
        return random.choice(self.with_potision_list)

    def printList(self):
        print("self.alive_list")
        print(self.alive_list)

        print("self.dead_list")
        print(self.dead_list)

        print("not divined anyone")
        print(self.gray_list)

        print("all fortune teller divined Human")
        print(self.white_list)

        print("one fortune teller divined Human")
        print(self.white_gray_list)

        print("fortune teller divined Wolf")
        print(self.dark_list)

        print("One fortune teller divined Human but another divined wolf")
        print(self.dark_white)

        print("comingout list")
        print(self.with_potision_list)

        print("fortune teller list and result")
        print(self.divined_result_dic)

    
    def finish(self):
        return None
    


agent = SampleAgent(myname)
    


# run
if __name__ == '__main__':
    aiwolfpy.connect_parse(agent)
    
