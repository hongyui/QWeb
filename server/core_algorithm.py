import numpy as np
from math import factorial
import itertools
import random
import copy
from math import pi,sqrt,cos,sin,log2,ceil,acos
import time
import matplotlib.pyplot as plt
import csv
import math
import json

NumIter = 1000
experiment = 1
N = 10

def check(gate):
    # print("gate:",gate)
    in_output=[]
    inp=[]
    for i in range(2**n):
        inp.append(i)
    # print(inp)
    for i in range(len(inp)):#這是每個input
        
        arr_1 = [int(b) for b in bin(inp[i])[2:].zfill(n)] #這是input的
        for ta in range(len(gate)):#每一個閘
            notPos = -1
            changeNot = True
            # chec=True#

            for j in range(n): #一個input的二進制 
                val=gate[ta][j]#arr_1[j]:
                if (val == 0 or val == 1) and val != arr_1[j]:
                    changeNot = False
                    break
                elif val == 3:
                    notPos = j
            if notPos != -1 and changeNot:
                arr_1[notPos] = 1 - arr_1[notPos]
            # print(arr_1)
        
        binary_str = ''.join(map(str, arr_1))  # '1010'
        decimal = int(binary_str, 2)
        in_output.append(decimal)
    # print("in_output",in_output)
    tem=0
    if in_output==output:
        return 1
    else:return 0
    
            
    # arr_1 = [int(b) for b in bin(gate_1)[2:].zfill(n)]  # zfill補0
    # arr_2 = [int(b) for b in bin(gate_2)[2:].zfill(n)]
    
def find_cycles(permutation):
    visited = [False] * len(permutation) #記錄每個位置是否已經被走訪（避免重複）
    cycles = []
    cycles_list = []
    
    #q3會用到 要從output對回去input
    inverse_output = [0] * len(permutation)
    for idx, val in enumerate(permutation):
        inverse_output[val] = idx
    for i in range(len(permutation)):
        if not visited[i]:#如果還沒有拜訪過，就準備從這個點開始建立一個新的循環
            current = i
            cycle = []

            while not visited[current]:#只要還沒回到一個已拜訪過的點，就持續往下走：
                visited[current] = True
                cycle.append(current)
                current = permutation[current] #根據 permutation 的定義，跳到下一個點 permutation[current]。
            if len(cycle) > 1:  # ✅ 過濾掉長度為 1 的 cycle
                cycles.append(cycle)
                cycles_list.extend(cycle)

            

    return cycles , cycles_list ,inverse_output

def hamming_distance(a, b):
    return bin(a ^ b).count('1') #看循環的數字 位元差

def measureQ1(qindividuals): #q1
    """Consecutive measures on the qbits in order to generate a classical solution"""
    #a是測量 0~1 
    # print("measureQ1")
    # print("qindividuals",qindividuals)
    # print(len(qindividuals))
    da=[] #暫時性放結果嗎?
    for s in range(len(qindividuals)): #幾個循環 看要測幾個
        #一個循環互有一個十進制
        # print("qindividuals",qindividuals[s])
        trans=[]
        for g in range(len(qindividuals[s])): #第s個循環，要扣多少
            # print("qindividuals",qindividuals[s][g])
            #要開始記錄他的位元 還要轉換成十進制
            a=np.random.rand(1)
            # print("a",a)
            if qindividuals[s][g][0]<a:
                trans.append(1)
            else:trans.append(0)
        # print("trans",trans)
        da.append(trans)
        # da.append(int(''.join(map(str, trans)), 2))
        # print("da",da)
    # print("da:",da)
    # print("da",da) #再來從da排序出solution嗎? da [3, 0, 2]
    
    
    
    return da

def measureQ2(qindividuals): #q2
    """Consecutive measures on the qbits in order to generate a classical solution"""
    #a是測量 0~1 
    # print("q2_bit_table:",q2_bit_table)
    # print("qindividuals:",qindividuals)
    #i是索引值 用於後面找是段哪個邊 並且藥用陣列存
    toto=[]
    # print("measureQ2",qindividuals)
    for bit in range(len(qindividuals)):
        bit_2=[]
        for bb in qindividuals[bit]:
            # print("bb",bb)
            a=np.random.rand(1)
            if bb[0]<a:
                bit_2.append(1)
            else:bit_2.append(0)

        toto.append(bit_2)
    
        
    return toto

def measureQ3(qindividuals): #q3
    #a是測量 0~1 
    toto=[]
    for bit in range(len(qindividuals)):#bit是第幾個cycle
        q3_cycle=[]
        for x in range(len(qindividuals[bit])): #x是每一個swap的
            #每一個點都要記錄2進制
            
            q3_bit10=[]
            nini=len(qindividuals[bit][x])
            for y in qindividuals[bit][x]: #這是每個邊
                # print("每一個城市",y)
                # print("length",len(y))
                q3_bit2=[]
                #因為有一個999
                if nini==1:
                    q3_bit10.append(999)
                else:
                    for z in y:
                        # print("z",z)
                        #一個城市 每一個二進制 要組起來和其他位置比大小
                        
                        a=np.random.rand(1)
                        # print("a",a)
                        if z[0]<a:
                            q3_bit2.append(1)
                        else:q3_bit2.append(0)
                    # print("q3_bit2",q3_bit2)
                    toto_before=int(''.join(map(str, q3_bit2)), 2)
                    # print("toto_before",toto_before)
                    q3_bit10.append(q3_bit2) #裝進去十進制的解
                    
            # print("q3_bit10",q3_bit10)
            #這裡的toto_before 是一個城市的十進制
            q3_cycle.append(q3_bit10)
        toto.append(q3_cycle)


    
        # toto.append(q3_cycle)
    # print("toto",toto)

    return toto

def measureQ4(qindividuals): #q2
    """Consecutive measures on the qbits in order to generate a classical solution"""
    #a是測量 0~1 
    #i是索引值 用於後面找是段哪個邊 並且藥用陣列存
    toto=[]
    # print("measureQ4:",qindividuals) #有cycle 再位置路徑
    # ct=0    
    for bit in range(len(qindividuals)):#bit是第幾個cycle
        q4_cycle=[]
        # print("len(qindividuals)",len(qindividuals))
        for x in range(len(qindividuals[bit])): #x是每一個位置的
            # print("len(qindividuals[bit]):",len(qindividuals[bit])) #5
            
            
            q4_cycle_bit=[]
            for y in range(len(qindividuals[bit][x])): #每一個頭尾機率
                # print("(qindividuals[bit][x]):",qindividuals[bit][x])
                # print("(qindividuals[bit][x]):",len(qindividuals[bit][x]))
                a=np.random.rand(1)
                
                total=qindividuals[bit][x][y][0]
                # print("total",total)
                if(total==999): #因為沒有中繼點的話 我是在q4 table設999
                    q4_cycle_bit.append(0)
                    
                elif(total>a):#如果機率未到 索引直+1
                    q4_cycle_bit.append(0)
                else:#超過 就break就知道第幾個順序了
                    q4_cycle_bit.append(1)
                # print("q4_cycle_bit",q4_cycle_bit)
            #我覺得在這裡修復比較方便
            #toto要看需不需要修復 因為全部加起來頭尾要一樣多，後半要配合數量
            # print("修復前:",q4_cycle_bit)
            q4_cycle_bit=repairQ4(q4_cycle_bit)
            # print("修復後:",q4_cycle_bit)

            q4_cycle.append(q4_cycle_bit)
    
        toto.append(q4_cycle)
    # if ct>0:
    #     print("修復",ct,"次")
        
    # print("toto",toto)
    return toto

def repairQ4(toto):
    # print("toto",toto)
    
    # a=int(len(toto)/2)
    a=0
    # print(a)
    if len(toto)!=1:
        # ct+=1
        count_0 = toto.count(0)
        count_1 = toto.count(1)
        # print("0數量:",count_0)
        # print("1數量:",count_1)
        minu=int((count_0-count_1)/2) #如果出來是正的 代表0多 後半要把0改1 反之 負  (要變幾個)
        if minu>0:
            #0比較多
            true_num=minu
            zero_indices = [i for i in range(a, len(toto)) if toto[i] == 0] #找0的索引
            # print("zero_indices",zero_indices)
            random_indices = random.sample(zero_indices, k=true_num)  # 選minus個
            # print("random_indices",random_indices)
            # print("true_num",true_num)
            for x in range(true_num):
                toto[random_indices[x]]=1
        elif minu<0:
            #1比較多
            true_num=int((count_1-count_0)/2)
            zero_indices = [i for i in range(a, len(toto)) if toto[i] == 1] #找0的索引
            # print("zero_indices",zero_indices)
            random_indices = random.sample(zero_indices, k=true_num)  # 選minus個
            # print("random_indices",random_indices)
            for x in range(true_num):
                toto[random_indices[x]]=0
        # count_0 = toto.count(0)
        # count_1 = toto.count(1)
    
            
    return toto

        

def gen_nbrs(q1,q2,q3,q4,N):
    neighbours1 = [np.array(measureQ1(q1)) for i in range(N)]
    neighbours2 = [(measureQ2(q2)) for i in range(N)]
    neighbours3 = [(measureQ3(q3)) for i in range(N)]
    neighbours4 = [(measureQ4(q4)) for i in range(N)]
    # print("neighbours4",neighbours4)
    return neighbours1,neighbours2,neighbours3,neighbours4

def route_neighbour(n1,n2,n3,n4,q2_bit_table,trans,n):
    #neighbours出來不是解喔 我們要根據1~4排好順序對不對~ 根據q1看順序 根據q2看斷頭 根據q3看路線 q1~q3用成一個list都是差一位元的路線
    
    # 接著q4也要根據q2重新用一下他的排序(但不要改到neighbours4，用copy)最後會留下list和q4來生成電路
    circuit_solution=[]
    for i in range(N):
        #進去算解要十進治
        # da.append(int(''.join(map(str, trans)), 2))
        n1_adj=[]
        # print("n1[i]",n1[i])
        for x_test in n1[i]:
            n1_adj.append(int(''.join(map(str, x_test)), 2))
            
        n2_adj=[]
        qbt=0
        for x_test in n2[i]:
            toto_before=int(''.join(map(str, x_test)), 2)
            if q2_bit_table[qbt]<=toto_before:
                n2_adj.append(toto_before%q2_bit_table[qbt])
            else:n2_adj.append(toto_before)
            qbt+=1

        n3_adj=[]
        for x_test in n3[i]:
            tmp_s=[]
            for y_test in x_test: 
                tmp=[]
                if y_test[0]!=999:
                    for z_test in y_test:
                        toto_before=int(''.join(map(str, z_test)), 2)
                        tmp.append(toto_before)
                else: tmp.append(999)#是999
                tmp_s.append(tmp)
            n3_adj.append(tmp_s)
        
        circuit_solution.append(make_route(n1_adj,n2_adj,n3_adj,n4[i],trans,n)) #地i個族群neighbours進去形成一個我要的路線和閘
        
    return circuit_solution


def route_tenbit(index,solution3,trans,n):
    route=[]
    
    # print("index",index)
    # print("solution3",solution3)
    if solution3[0]!=999:

        #solution3處理
        so33 = sorted(enumerate(solution3), key=lambda x: x[1],reverse=True)
        pp = [idx for idx, val in so33]
        # print("pp",pp)
        # print("trans",trans)
        start=trans[index]
        route.append(start)
        end=trans[index+1]
        arr1=[int(b) for b in bin(start)[2:].zfill(n)]
        arr2=[int(b) for b in bin(end)[2:].zfill(n)]
        # print("start",start)
        # print("end",end)
        # print("arr1",arr1)
        # print("arr2",arr2)
        location=[]
        for ind in range(len(arr1)):
            #來看哪幾個不重複 紀錄索引直
            if arr1[ind]!=arr2[ind]:
                location.append(ind)
        # print("location",location)
        #location 抓pp
        for ie in pp:
            arr1[location[ie]]=abs(1-arr1[location[ie]]) 
            #轉換十進制
            binary_str = ''.join(str(b) for b in arr1)
            decimal = int(binary_str, 2)
            route.append(decimal)


        #轉換十進制
        # binary_str = ''.join(str(b) for b in bits)
        # decimal = int(binary_str, 2)
        # route.append(end)

    else:
        start=trans[index]
        end=trans[index+1]
        route.append(start)
        route.append(end)
        pp=[999]
    # print("route",  route)

    return route


def make_route(solution1,solution2,solution3,solution4,trans,n): #這樣是一組解弄成路線
    route_so=[]
    route_gate=[]
    sorted_with_index = sorted(enumerate(solution1), key=lambda x: x[1],reverse=True)
    original_indices = [idx for idx, val in sorted_with_index]
    # print("trans",trans)
    # print("對應原本的索引：", original_indices) #[1, 2, 0]
    # print("solution3",solution3)
    for so1 in original_indices:

        index=solution2[so1] #因為斷邊 所以從這裡開始
        num=len(solution3[so1])
        
        if num==1:
            #代表只有一個交換 我們在前面只用一個 沒有循環 在這裡偷偷加一
            num=2
        for so2 in range(num-1): #要減一 因為斷邊
            
            if index >=num: #如果超出迴圈 因為是循環 會回到第一個
                index=0
            # print("total_route_single[so1])",total_route_single[so1][index])
            #0805 所以說我在這裡要用的是  
            #差一個函式 是起點和終點 以及solution3的排序狀態 回傳一個roa
            #index是段邊索引直
            #中繼點
            # print("solution3[so1][index] before",ssolution3[so1][index])
            # roa,solution3[so1][index]=route_tenbit(index,solution3[so1][index],trans[so1])
            # print("solution3[so1][index] after",solution3[so1][index])
            roa=route_tenbit(index,solution3[so1][index],trans[so1],n)    
            # print("roa",roa)
            # roa=total_route_single[so1][index][solution3[so1][index]] #第幾個路線不就是看q3嗎
            roa_gate=solution4[so1][index] #閘也要順序
            #roa路線
            #roa_gate是閘的順序
            # print("roa_gate",roa_gate)
            route_so.append(roa)
            route_gate.append(roa_gate)
            index+=1
    # print("route_so",route_so)
    # print("route_gate",route_gate)
    circuit,nope=make_circuit(route_so,route_gate,n) #丟進去生成兩個兩個
    
    return  circuit

def make_route_fin(solution1,solution2,solution3,solution4,trans): #這樣是一組解弄成路線
    route_so=[]
    route_gate=[]
    sorted_with_index = sorted(enumerate(solution1), key=lambda x: x[1],reverse=True)
    original_indices = [idx for idx, val in sorted_with_index]
    # print("trans",trans)
    # print("對應原本的索引：", original_indices) #[1, 2, 0]
    # print("solution3",solution3)
    for so1 in original_indices:

        index=solution2[so1] #因為斷邊 所以從這裡開始
        num=len(solution3[so1])
        
        if num==1:
            #代表只有一個交換 我們在前面只用一個 沒有循環 在這裡偷偷加一
            num=2
        for so2 in range(num-1): #要減一 因為斷邊
            
            if index >=num: #如果超出迴圈 因為是循環 會回到第一個
                index=0
            # print("total_route_single[so1])",total_route_single[so1][index])
            #0805 所以說我在這裡要用的是  
            #差一個函式 是起點和終點 以及solution3的排序狀態 回傳一個roa
            #index是段邊索引直
            #中繼點
            # print("solution3[so1][index] before",ssolution3[so1][index])
            # roa,solution3[so1][index]=route_tenbit(index,solution3[so1][index],trans[so1])
            # print("solution3[so1][index] after",solution3[so1][index])
            roa=route_tenbit(index,solution3[so1][index],trans[so1])    
            # print("roa",roa)
            # roa=total_route_single[so1][index][solution3[so1][index]] #第幾個路線不就是看q3嗎
            roa_gate=solution4[so1][index] #閘也要順序
            #roa路線
            #roa_gate是閘的順序
            # print("roa_gate",roa_gate)
            route_so.append(roa)
            route_gate.append(roa_gate)
            index+=1
    # print("route_gate",route_gate)
    circuit,tota=make_circuit(route_so,route_gate) #丟進去生成兩個兩個
    
    return  circuit,tota


def make_circuit(route,gate,n): #路線 和閘順序 #可執行 但沒100確認
    #所以到這裡就沒有cycle分 照for迴圈生成電路!
    circuit=[]
    # print("完整大小")
    # print("route",route)
    # print("gate",gate)
    #route [[4, 5, 7], [0, 2, 6], [6, 2, 0, 1], [1, 5], [5, 1, 3], [3, 1, 0]]
    #gate [[1, 0], [1, 0], [1, 0, 1, 0], [0], [0, 1], [1, 0]]
    for i in range(len(route)):
        a=0 #a頭b尾
        b=len(route[i])-1
        # x=int(len(gate[i])/2)-1
        # print(x)
        #這裡分三部分 前半 中間 後半
        bit_one=[]
        
        final=len(gate[i])
        
        
        front=int(final/2) #這裡只會有兩種可能 看會不會單數的可以跑 就是差一位元
        # print("front",front)
        # if front==1: #為了一位元 
        #     front=0
        for j in range(front):
            if gate[i][j]==0:
                
                bit=[]
                bit.append(route[i][a])
                bit.append(route[i][a+1])
                a+=1
                circuit.append(bit)
                # print("索引值頭目前在:",a)
                # print("索引值尾目前在:",b)
            elif gate[i][j]==1:
                bit=[]
                bit.append(route[i][b-1])
                bit.append(route[i][b])
                b-=1
                circuit.append(bit)
                # print("索引值頭目前在:",a)
                # print("索引值尾目前在:",b)
            
        # print("circuit:",circuit)   #生成前半
    
        if b-a==1 or front==0: #如果沒問題的話 不用if else
            bit=[]
            bit.append(route[i][a])
            bit.append(route[i][b])
            c=b
            b=a
            a=c
            circuit.append(bit)
            # print("索引值頭目前在:",a)
            # print("索引值尾目前在:",b)
        else:print("有錯!!!!")
        # print("circuit:",circuit)   #生成前半 中間
        if front==0: #為了1bit的
            final=0
        for j in range(front,final): #生成後半 索引直就是front到末
            if gate[i][j]==0:
                bit=[]
                bit.append(route[i][a])
                bit.append(route[i][a+1])
                a+=1
                circuit.append(bit)
                # print("索引值頭目前在:",a)
                # print("索引值尾目前在:",b)
            elif gate[i][j]==1:
                bit=[]
                bit.append(route[i][b-1])
                bit.append(route[i][b])
                b-=1
                circuit.append(bit)
                # print("索引值頭目前在:",a)
                # print("索引值尾目前在:",b)
            
    # print("circuit:",circuit)   #生成前半 中 後半
        
    #再來要換成閘
    real_circuit=[]#生成閘並且也化簡
    for gate in range(len(circuit)): #直接看有個toff
        gate_1=circuit[gate][0]
        gate_2=circuit[gate][1]
        #gpt直接幫忙轉為二進制
        arr_1 = [int(b) for b in bin(gate_1)[2:].zfill(n)]  # zfill補0
        arr_2 = [int(b) for b in bin(gate_2)[2:].zfill(n)]
        # print("gate_1:",gate_1)
        # print("arr_1:",arr_1)
        # print("gate_2:",gate_2)
        # print("arr_2:",arr_2)
        first_za=[] #閘
        start_za=[] #第一個閘
        after_za=[] #第二個閘 因為要拿去修復化簡

        if len(real_circuit)==0: #如果total沒閘就放進來~
            for real in range(n):
                #這裡只會有互相相同 和 不相同 
                #如果相同 就是0或1
                #一樣轉成0白色 1黑色 2wire 3target
                if arr_1[real]==arr_2[real]:
                    first_za.append(arr_1[real])
                else:first_za.append(3)
            real_circuit.append(first_za) #裝進total
            # print("real_circuit",real_circuit)
            # print("first_za",first_za)
        else: #後續
            #要化簡的話 要一直搜尋全電路陣列的最後
            start_za=real_circuit[len(real_circuit)-1]
            for real in range(n):
                #這裡只會有互相相同 和 不相同 
                #如果相同 就是0或1
                #一樣轉成0白色 1黑色 2wire 3target
                if arr_1[real]==arr_2[real]:
                    after_za.append(arr_1[real])
                else:after_za.append(3)
            # print("start_za",start_za)
            # print("after_za",after_za)
            # print("real_circuit",real_circuit)
            #就可以開始化簡 相同化簡 然後 如果3位置一樣 並且其他位置都一樣 只有一個不一樣 可以變成2
            if start_za==after_za: #如果一樣 代表削掉
                # print("一樣")
                
                real_circuit.pop(len(real_circuit)-1)
                # print("pop後",real_circuit)
            else:real_circuit.append(after_za) #裝進total
    
    #前面已經換成閘
    #削掉的第二步 如果前面沒有削掉 才進來這裡 所以用if else
    #這裡先抓 3的位置
    #如果是同位置
    # bool1=True
    # while bool1:
    #     bool1=False
    #     for xc in range(len(real_circuit)-1):
    #         # print("real_circuit",real_circuit)
    #         st_za=real_circuit[xc]
    #         ar_za=real_circuit[xc+1]
    #         index_start_3=st_za.index(3)
    #         index_after_3=ar_za.index(3)
    #         # print("st_za",st_za)
    #         # print("ar_za",ar_za)
    #         # print("index_start_3",index_start_3)
    #         # print("index_after_3",index_after_3)
    #         if index_start_3==index_after_3:
    #             #如果相等 代表有機會化簡
    #             index_c=0 #如果index==1代表 只有差一個 看不同的
    #             index_index=0
    #             for real in range(n):
    #                 if st_za[real]!=ar_za[real] and st_za[real]!=3:
    #                     index_c+=1 #不同的數量
    #                     index_index=real #位置
    #                 if index_c>1:
                        
    #                     break
    #             if index_c==1 and st_za[index_index]!=2 and ar_za[index_index]!=2: #代表可以化簡
    #                 # print("有唷")
    #                 real_circuit.pop(xc) #拔掉 後面會遞前 下面直接原味把indexindex改成2
    #                 real_circuit[xc][index_index]=2
    #                 # print("real_circuit後",real_circuit)
    #                 bool1=True
    #         if bool1==True: #會友上面被pop 但迴圈還是依樣長度
    #             break
        
        
        
            


    return real_circuit,len(circuit)


def factorial_two(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    # numbers = list(range(0, n))
    # permutations = list(itertools.permutations(numbers))
    return result

def walk(start,end,i): #這裡最複雜
    # print("start:",start)
    # print("end:",end)
    # print("i:",i)
    total_route=[] #全部路線陣列

    num_bit=hamming_distance(start,end)
    # print("num_bit",num_bit)
    q4_table_cycle.append(num_bit)
    index=1 #相差位元
    ch=len(i)
    total_route.append([start])
    #索引值紀錄走訪位置
    for su in range(num_bit-1): #走訪次數
        route=[] #路線陣列
        #把頭尾加進去
        empty=0
        for ind in range(ch):
            x=i[ind] #現在走訪到的bit
            if (hamming_distance(start,x)==index and hamming_distance(end,x)==num_bit-index):       #如果和起點相差index 和終點相差num_bit-index 代表加入x路線到陣列
                route.append(x)
                empty+=1    
        if(empty==0):
            #走一個total走訪的
            for ind in range(len(output)):
                if (hamming_distance(start,output[ind])==index and hamming_distance(end,output[ind])==num_bit-index): 
                    route.append(output[ind])
        else: empty=0
        
        total_route.append(route)
        index+=1
    total_route.append([end])
    # print("totalroute",total_route)
    #total_route代表每個位元差內的可選擇內容
    # print("total_route",total_route)
    # 再來要進行組合
    num_ro=[] #路線索引值
    total_combin=[]
    if num_bit==1:
        num_ro.append(len(total_route[1])) #直接跳過生成中間迴圈 讓while直接生效
        combin=[]
        combin.append(total_route[0][0])
        combin.append(total_route[1][0])
        total_combin.append(combin)
    elif num_bit ==2: #應該是只有這個特例
        num_ro.append(len(total_route[1])) #直接跳過生成中間迴圈 讓while直接生效
        for xc in range(len(total_route[1])):
            combin=[]
            combin.append(total_route[0][0])
            combin.append(total_route[1][xc])
            combin.append(total_route[2][0])
            total_combin.append(combin)
    else:    
        for ix in range(num_bit-1):
            num_ro.append(0) #要看空的話要怎麼處理
    
    so=0 #有一個索引直來看是1,2,3,目前第幾個
    pep=1 #代表走訪長度
    # print("num_ro",num_ro)
    # print("total_route",total_route)
    befor=False
    while num_ro[0]!=len(total_route[1]):#當不是第一個索引值超出時
        # print("num_ro out",num_ro)
        if befor ==True:
            #如果對 代表so前一個有被換 要檢查
            if (total_route[so][num_ro[so-1]],total_route[so+1][num_ro[so]])!=1:
                so-=1
                pep=so+1
        befor=False
        combin=[]
        combin.append(total_route[0][0])
        for tim in range(1,pep+1):
            combin.append(total_route[tim][num_ro[tim-1]])
        st=total_route[pep][num_ro[so]]
        empty=0
        sta=num_ro[so+1]
        
        
        for cc in range(sta,len(total_route[pep+1])):#看目前索引直的下一個長度走訪，因為當前這一個只會抓陣列的第一個
            tests=False
            
            found = False  # 設一個旗標
            mid=total_route[pep+1][cc] #下一個 這裡出問題
            # print("配對的是",mid)
            # print("num_ro:",num_ro)
            # print("cc",cc)
            if hamming_distance(st,mid)==1:
                # print("有")
                combin.append(mid) #有的話加入 並且往下一層探索
                num_ro[so+1]=cc #加進去超標 和最後一列才++ 
                # print("num_ro IF ",num_ro)
                # print("combin:",combin)
                found = True  # 設定旗標
                if len(combin)!=num_bit:
                    pep+=1
                    so+=1
                    empty+=1
                    tests=True
                    #在這裡 索引直要跟著變
                else:
                    combin.append(total_route[-1][0])
                    total_combin.append(combin)
                    # pep-=1
                    # so-=1
                    # num_ro[so+1]+=1
                    # print("total_combin:",total_combin)
                    
                    num_ro[so+1]=cc+1
                    # break
                    #我想在這裡break出for迴圈
            else:
                num_ro[so+1]=cc+1
            
            # print("cc進入藥檢檢",cc)
            if tests:
                if cc==len(total_route[pep])-1  : # 設定旗標 and  found == False 0602
                    
                    #如果當前狀態都找完了 +1 找下一個
                    num_ro[so+1]=0
                    #當前一個也是FINAL應該也要再清空
                    num_ro[so]+=1
                    befor=True
                    okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                    while (okay):
                        # print("while")
                        # print("num_ro in",num_ro)
                        if num_ro[so]>=len(total_route[pep]) and so!=0:
                            num_ro[so]=0 #前一個超出 也進位
                            #前前一個再++
                            if so >= 1:
                                so-=1
                            num_ro[so]+=1
                            if so==0: okay=False
                        else:okay=False
                        pep=so+1 
                    break
                if found:
                    break  # 外部有需要也可配合再跳
            else:
                if cc==len(total_route[pep+1])-1  : # 設定旗標 and  found == False 0602
                    
                    #如果當前狀態都找完了 +1 找下一個
                    num_ro[so+1]=0
                    #當前一個也是FINAL應該也要再清空
                    num_ro[so]+=1
                    befor=True
                    okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                    while (okay):
                        # print("while")
                        # print("num_ro in",num_ro)
                        if num_ro[so]>=len(total_route[so+1]) and so!=0:
                            num_ro[so]=0 #前一個超出 也進位
                            #前前一個再++
                            if so >= 1:
                                so-=1
                            num_ro[so]+=1
                            if so==0: okay=False
                        else:okay=False
                        pep=so+1 
                    break
                if found:
                    break  # 外部有需要也可配合再跳
        # print("num_ro dddd",num_ro)
    # print("total_combin:",total_combin)
    # print("len(total_combin)",len(total_combin))
    
    # print("total_route原本的",total_route)


    if len(total_combin)==0: #全部路線走訪一次生成
        # print("來!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        total_route=[]
        index=1
            
        total_route.append([start])
        for su in range(num_bit-1): #走訪次數
            route=[] #路線陣列
            
            
            #走一個total走訪的
            # print("output",output)
            for ind in range(len(output)):
                # print("start:",start)
                if (hamming_distance(start,output[ind])==index and hamming_distance(end,output[ind])==num_bit-index): 
                    route.append(output[ind])
            else: empty=0
            
            total_route.append(route)
            index+=1
        total_route.append([end])

        # print("len(total_combin)==0")
        # print("len(total_combin)==0")
        # print("len(total_combin)==0")
        # print("total_route total",total_route)
        num_ro=[] #路線索引值
        # input_num=[]
        # for xc in range (num_bit+1): #為適應pep 所以加入一樣的長度
        #     input_num.append(input_list)
        # print("input_num",input_num)
        for ix in range(num_bit-1):
            num_ro.append(0) #要看空的話要怎麼處理
        # print("input",input_list)
        # for xcb in range(2**n):
        so=0 #有一個索引直來看是1,2,3,目前第幾個
    pep=1 #代表走訪長度
    # print("num_ro",num_ro)
    # print("total_route",total_route)
    befor=False
    while num_ro[0]!=len(total_route[1]):#當不是第一個索引值超出時
        # print("num_ro out",num_ro)
        if befor ==True:
            #如果對 代表so前一個有被換 要檢查
            if (total_route[so][num_ro[so-1]],total_route[so+1][num_ro[so]])!=1:
                so-=1
                pep=so+1
        befor=False
        combin=[]
        combin.append(total_route[0][0])
        for tim in range(1,pep+1):
            combin.append(total_route[tim][num_ro[tim-1]])
        st=total_route[pep][num_ro[so]]
        empty=0
        sta=num_ro[so+1]
        
        
        for cc in range(sta,len(total_route[pep+1])):#看目前索引直的下一個長度走訪，因為當前這一個只會抓陣列的第一個
            tests=False
            
            found = False  # 設一個旗標
            mid=total_route[pep+1][cc] #下一個 這裡出問題
            # print("配對的是",mid)
            # print("num_ro:",num_ro)
            # print("cc",cc)
            if hamming_distance(st,mid)==1:
                # print("有")
                combin.append(mid) #有的話加入 並且往下一層探索
                num_ro[so+1]=cc #加進去超標 和最後一列才++ 
                # print("num_ro IF ",num_ro)
                # print("combin:",combin)
                found = True  # 設定旗標
                if len(combin)!=num_bit:
                    pep+=1
                    so+=1
                    empty+=1
                    tests=True
                    #在這裡 索引直要跟著變
                else:
                    combin.append(total_route[-1][0])
                    total_combin.append(combin)
                    # pep-=1
                    # so-=1
                    # num_ro[so+1]+=1
                    # print("total_combin:",total_combin)
                    
                    num_ro[so+1]=cc+1
                    # break
                    #我想在這裡break出for迴圈
            else:
                num_ro[so+1]=cc+1
            
            # print("cc進入藥檢檢",cc)
            if tests:
                if cc==len(total_route[pep])-1  : # 設定旗標 and  found == False 0602
                    
                    #如果當前狀態都找完了 +1 找下一個
                    num_ro[so+1]=0
                    #當前一個也是FINAL應該也要再清空
                    num_ro[so]+=1
                    befor=True
                    okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                    while (okay):
                        # print("while")
                        # print("num_ro in",num_ro)
                        if num_ro[so]>=len(total_route[pep]) and so!=0:
                            num_ro[so]=0 #前一個超出 也進位
                            #前前一個再++
                            if so >= 1:
                                so-=1
                            num_ro[so]+=1
                            if so==0: okay=False
                        else:okay=False
                        pep=so+1 
                    break
                if found:
                    break  # 外部有需要也可配合再跳
            else:
                if cc==len(total_route[pep+1])-1  : # 設定旗標 and  found == False 0602
                    
                    #如果當前狀態都找完了 +1 找下一個
                    num_ro[so+1]=0
                    #當前一個也是FINAL應該也要再清空
                    num_ro[so]+=1
                    befor=True
                    okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                    while (okay):
                        # print("while")
                        # print("num_ro in",num_ro)
                        if num_ro[so]>=len(total_route[so+1]) and so!=0:
                            num_ro[so]=0 #前一個超出 也進位
                            #前前一個再++
                            if so >= 1:
                                so-=1
                            num_ro[so]+=1
                            if so==0: okay=False
                        else:okay=False
                        pep=so+1 
                    break
                if found:
                    break  # 外部有需要也可配合再跳
        # print("total_combin:",total_combin)
        # print("len(total_combin)",len(total_combin))

    return total_combin

def test(): #路線 和閘順序 #可執行 但沒100確認
    #在分配路線的地方 根據word一一驗證選取過程 0601
    print("start:",start)
    print("end:",end)
    print("i:",i)
    total_route=[] #全部路線陣列

    num_bit=hamming_distance(start,end)
    # print("num_bit",num_bit)
    q4_table_cycle.append(num_bit)
    index=1 #相差位元
    ch=len(i)
    total_route.append([start])
    #索引值紀錄走訪位置
    for su in range(num_bit-1): #走訪次數
        route=[] #路線陣列
        #把頭尾加進去
        empty=0
        for ind in range(ch):
            x=i[ind] #現在走訪到的bit
            if (hamming_distance(start,x)==index and hamming_distance(end,x)==num_bit-index):       #如果和起點相差index 和終點相差num_bit-index 代表加入x路線到陣列
                route.append(x)
                empty+=1    
        if(empty==0):
            #走一個total走訪的
            for ind in range(len(output)):
                if (hamming_distance(start,output[ind])==index and hamming_distance(end,output[ind])==num_bit-index): 
                    route.append(output[ind])
        else: empty=0
        
        total_route.append(route)
        index+=1
    total_route.append([end])
    #total_route代表每個位元差內的可選擇內容
    print("total_route",total_route)
    # 再來要進行組合
    num_ro=[] #路線索引值
    total_combin=[]
    if num_bit==1:
        num_ro.append(len(total_route[1])) #直接跳過生成中間迴圈 讓while直接生效
        combin=[]
        combin.append(total_route[0][0])
        combin.append(total_route[1][0])
        total_combin.append(combin)
    elif num_bit ==2: #應該是只有這個特例
        num_ro.append(len(total_route[1])) #直接跳過生成中間迴圈 讓while直接生效
        for xc in range(len(total_route[1])):
            combin=[]
            combin.append(total_route[0][0])
            combin.append(total_route[1][xc])
            combin.append(total_route[2][0])
            total_combin.append(combin)
    else:    
        for ix in range(num_bit-1):
            num_ro.append(0) #要看空的話要怎麼處理
    
    so=0 #有一個索引直來看是1,2,3,目前第幾個
    pep=1 #代表走訪長度
    # print("num_ro",num_ro)
    # print("total_route",total_route)
    
    while num_ro[0]!=len(total_route[1]):#當不是第一個索引值超出時
        # print("num_ro out",num_ro)
        
        combin=[]
        combin.append(total_route[0][0])
        for tim in range(1,pep+1):
            combin.append(total_route[tim][num_ro[tim-1]])
        st=total_route[pep][num_ro[so]]
        empty=0
        sta=num_ro[so+1]
        # print("sta:",sta)
        # print("so",so)
        # print("pep",pep)
        
        for cc in range(sta,len(total_route[pep+1])):#看目前索引直的下一個長度走訪，因為當前這一個只會抓陣列的第一個
            # print("num_ro for ",num_ro)
            # print("sta:",sta)
            # print("cc",cc)
            
            found = False  # 設一個旗標
            mid=total_route[pep+1][cc] #下一個 這裡出問題
            # print("mid",mid)
            # print("num_ro:",num_ro)
            # print("cc",cc)
            if hamming_distance(st,mid)==1:
                # print("有")
                combin.append(mid) #有的話加入 並且往下一層探索
                num_ro[so+1]=cc #加進去超標 和最後一列才++
                # print("combin:",combin)
                found = True  # 設定旗標
                if len(combin)!=num_bit:
                    pep+=1
                    so+=1
                    empty+=1
                    #在這裡 索引直要跟著變
                else:
                    combin.append(total_route[-1][0])
                    total_combin.append(combin)
                    # num_ro[so+1]+=1
                    # print("total_combin:",total_combin)
                    
                    num_ro[so+1]=cc+1
                    # break
                    #我想在這裡break出for迴圈
            else:num_ro[so+1]=cc+1
            
            if cc==len(total_route[pep+1])-1  : # 設定旗標 and  found == False
                #如果當前狀態都找完了 +1 找下一個
                num_ro[so+1]=0
                #當前一個也是FINAL應該也要再清空
                num_ro[so]+=1
                okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                while (okay):
                    # print("while")
                    # print("num_ro in",num_ro)
                    if num_ro[so]>=len(total_route[so+1]) and so!=0:
                        num_ro[so]=0 #前一個超出 也進位
                        #前前一個再++
                        if so >= 1:
                            so-=1
                        num_ro[so]+=1
                        if so==0: okay=False
                    else:okay=False
                    pep=so+1 
                break
            if found:
                break  # 外部有需要也可配合再跳
    # print("total_combin:",total_combin)
    # print("len(total_combin)",len(total_combin))
    
    # print("total_route原本的",total_route)


    if len(total_combin)==0: #全部路線走訪一次生成
        print("來!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        total_route=[]
        index=1
            
        total_route.append([start])
        for su in range(num_bit-1): #走訪次數
            route=[] #路線陣列
            
            
            #走一個total走訪的
            # print("output",output)
            for ind in range(len(output)):
                # print("start:",start)
                if (hamming_distance(start,output[ind])==index and hamming_distance(end,output[ind])==num_bit-index): 
                    route.append(output[ind])
            else: empty=0
            
            total_route.append(route)
            index+=1
        total_route.append([end])

        # print("len(total_combin)==0")
        # print("len(total_combin)==0")
        # print("len(total_combin)==0")
        print("total_route total",total_route)
        num_ro=[] #路線索引值
        # input_num=[]
        # for xc in range (num_bit+1): #為適應pep 所以加入一樣的長度
        #     input_num.append(input_list)
        # print("input_num",input_num)
        for ix in range(num_bit-1):
            num_ro.append(0) #要看空的話要怎麼處理
        # print("input",input_list)
        # for xcb in range(2**n):
        so=0 #有一個索引直來看是1,2,3,目前第幾個
        pep=1 #代表走訪長度


        while num_ro[0]!=len(total_route[1]):#當不是第一個索引值超出時
            print("num_ro out",num_ro)
            
            combin=[]
            combin.append(total_route[0][0])
            for tim in range(1,pep+1):
                combin.append(total_route[tim][num_ro[tim-1]])
            st=total_route[pep][num_ro[so]]
            empty=0
            sta=num_ro[so+1]
            # print("sta:",sta)
            # print("so",so)
            # print("pep",pep)
            
            for cc in range(sta,len(total_route[pep+1])):#看目前索引直的下一個長度走訪，因為當前這一個只會抓陣列的第一個
                print("num_ro for ",num_ro)
                # print("sta:",sta)
                # print("cc",cc)
                
                found = False  # 設一個旗標
                mid=total_route[pep+1][cc] #下一個 這裡出問題
                # print("mid",mid)
                # print("num_ro:",num_ro)
                # print("cc",cc)
                if hamming_distance(st,mid)==1:
                    # print("有")
                    combin.append(mid) #有的話加入 並且往下一層探索
                    num_ro[so+1]=cc #加進去超標 和最後一列才++
                    # print("combin:",combin)
                    found = True  # 設定旗標
                    if len(combin)!=num_bit:
                        pep+=1
                        so+=1
                        empty+=1
                        #在這裡 索引直要跟著變
                    else:
                        combin.append(total_route[-1][0])
                        total_combin.append(combin)
                        # print("combin",combin)
                        # num_ro[so+1]+=1
                        # print("total_combin:",total_combin)
                        
                        num_ro[so+1]=cc+1
                        # break
                        #我想在這裡break出for迴圈
                else:num_ro[so+1]=cc+1
                
                if cc==len(total_route[pep+1])-1  : # 設定旗標 and  found == False
                    #如果當前狀態都找完了 +1 找下一個
                    num_ro[so+1]=0
                    #當前一個也是FINAL應該也要再清空
                    num_ro[so]+=1
                    okay=True #來裝前一個+1如果報表的話 前前一個要進位 這樣會無止盡 所以用布林來限制 就是如果沒大於 就ok 以及 如果加到num_ro[0]的話 也結束
                    while (okay):
                        # print("while")
                        # print("num_ro in",num_ro)
                        if num_ro[so]>=len(total_route[so+1]) and so!=0:
                            num_ro[so]=0 #前一個超出 也進位
                            #前前一個再++
                            if so >= 1:
                                so-=1
                            num_ro[so]+=1
                            if so==0: okay=False
                        else:okay=False
                        pep=so+1 
                    break
                if found:
                    break  # 外部有需要也可配合再跳
        # print("total_combin:",total_combin)
        # print("len(total_combin)",len(total_combin))

    return total_combin

def updateQ(qindividuals1,qindividuals2,qindividuals3,qindividuals4,neighbours1,neighbours2,neighbours3,neighbours4,original_indices,cycles_bit):
    t = 0   
    while t < N/2: #直接用q1~q4
        #q1
        
        bit_len = len(qindividuals1[0])
        # print("bit_len",bit_len)
        # bit_len = max(1, int(log2(max(best_sol1) + 1)))  # 確保能表示最大值
        best_so = neighbours1[original_indices[t]]
        best_so_list = best_so.tolist()
        best_sol1 = [list(map(int, num)) for num in best_so_list]
        
        worst_so = neighbours1[original_indices[N-1-t]]
        worst_so_list = worst_so.tolist()
        worst_sol1 = [list(map(int, num)) for num in worst_so_list]

        theta = 0.01 / (t+1)   #旋轉角度
        thetaq4 = 0.01 / (t+1)   #旋轉角度
        # theta = 0.005 / (t+1)   #旋轉角度
        # thetaq4 = 0.001 / (t+1)   #旋轉角度
        # print('best_sol1',best_sol1[0][0])
        # print("qq",qindividuals1[0][0])
        for i in range(len(qindividuals1)):
            for j in range(len(qindividuals1[i])):
                if best_sol1[i][j]!=worst_sol1[i][j]:
                    qindividuals1[i][j][best_sol1[i][j]]+=theta
                    qindividuals1[i][j][worst_sol1[i][j]]-=theta
                    #預防變負的
                    if qindividuals1[i][j][worst_sol1[i][j]]<=0:
                        #最好的方法 把他加回去 然後再設0
                        qindividuals1[i][j][best_sol1[i][j]]=1
                        qindividuals1[i][j][worst_sol1[i][j]]=0
        # print("q",qindividuals1)
        
        
        best_sol2 = neighbours2[original_indices[t]]
        
        worst_sol2 = neighbours2[original_indices[N-1-t]]
        # print('best_sol2[i][j]',best_sol2[0][0])
        # print("qin2",qindividuals2[0][0])

        for i in range(len(qindividuals2)):
            for j in range(len(qindividuals2[i])):
                if best_sol2[i][j]!=worst_sol2[i][j]:
                    qindividuals2[i][j][best_sol2[i][j]]+=theta
                    qindividuals2[i][j][worst_sol2[i][j]]-=theta
                    #預防變負的
                    if qindividuals2[i][j][worst_sol2[i][j]]<=0:
                        #最好的方法 把他加回去 然後再設0
                        qindividuals2[i][j][best_sol2[i][j]]=1
                        qindividuals2[i][j][worst_sol2[i][j]]=0

        
        
        best_so3 = neighbours3[original_indices[t]]
    
        worst_so3 = neighbours3[original_indices[N-1-t]]
        # print('best_so3[i][j][k][l]',best_so3[0])
        # print('best_so3[i][j][k][l]',best_so3[0][0])
        
        # print("ddd")
        # print("best sol3",best_so3)
        # print("qin3",qindividuals3)
        # print("best sol3",best_so3)
        # print('best_sol3 3',best_so3[0][0][0])
        # print("qin3",qindividuals3[0][0][0])
        # print('best_sol3 4',best_so3[0][0][0][0])
        # print("qin3",qindividuals3[0][0][0][0])

        for i in range(len(qindividuals3)):
            for j in range(len(best_so3[i])):
                for k in range(len(best_so3[i][j])):
                    q3_b2=len(qindividuals3[i][j][k]) 
                    if best_so3[i][j][k]!=999 and worst_so3[i][j][k]!=999:
                        for l in range(q3_b2):
                            # print('best_so3[i][j][k][l]',best_so3[i][j][k][l])
                            # print("qindividuals3[i][j][k][l]",qindividuals3[i][j][k][l])
                            # print("theta/q3_b2",theta/q3_b2)
                            if best_so3[i][j][k][l]!=worst_so3[i][j][k][l] :
                                # qindividuals3[i][j][k][l][best_so3[i][j][k][l]]+=theta/q3_b2
                                # qindividuals3[i][j][k][l][worst_so3[l]]+=theta/q3_b2
                                qindividuals3[i][j][k][l][best_so3[i][j][k][l]]+=theta
                                qindividuals3[i][j][k][l][worst_so3[i][j][k][l]]-=theta
                                #預防變負的
                                if qindividuals3[i][j][k][l][worst_so3[i][j][k][l]]<=0:
                                    #最好的方法 把他加回去 然後再設0
                                    qindividuals3[i][j][k][l][best_so3[i][j][k][l]]=1
                                    qindividuals3[i][j][k][l][worst_so3[i][j][k][l]]=0
        # print("qindividuals3",qindividuals3)

        #q4
        # print("qindividuals3",qindividuals3)
        
        best_sol4 = neighbours4[original_indices[t]]
        worst_sol4 = neighbours4[original_indices[N-1-t]]
        # print('best sol4',best_sol4[0])
        # print('best sol4',best_sol4[0][0])
        for i in range(cycles_bit): #循環
            for j in range(len(best_sol4[i])): #一個循環裡面幾個
                if len(best_sol4[i][j])!=1:
                    for k in range(len(best_sol4[i][j])): #一個路徑的閘
                        # print('best_so4[i][j][k][l]',best_sol4[i][j][k])
                        if best_sol4[i][j][k]!=worst_sol4[i][j][k]:
                            qindividuals4[i][j][k][best_sol4[i][j][k]]+=thetaq4
                            qindividuals4[i][j][k][worst_sol4[i][j][k]]-=thetaq4
                            #預防變負的
                            if qindividuals4[i][j][k][worst_sol4[i][j][k]]<=0:
                                #最好的方法 把他加回去 然後再設0
                                qindividuals4[i][j][k][best_sol4[i][j][k]]=1
                                qindividuals4[i][j][k][worst_sol4[i][j][k]]=0
                        

                




        t += 1

    # print("qindividuals4",qindividuals4)


            

async def core_algorithm_v1(output,n):
    # 把input output處理好循環 並加入cycles 量子態
    cycles ,cycles_list ,inverse_output= find_cycles(output)
    # print("inverse_output:",inverse_output)
    #建立量子態
    # bits=len(output)
    cycles_bit=len(cycles)

    # print("fac:",fac)
    check_zero=True
    if cycles_bit==1:
        bits=1
    elif cycles_bit==0:
        bits=0
        check_zero=False
        # print(">>>>>>>>>>>>>>>>>>>>")
        yield f"data: {json.dumps({'total_epochs':NumIter,'epoch':NumIter,'circuit':[]})}\n\n"
    else:
        bits = ceil(log2(cycles_bit))
    if check_zero:
        qindividuals1=[]
        # cycles_bit=2
        #1個量子表示cycles順序選擇
        for cy in range(cycles_bit):

            qindividuals1_on=np.zeros((bits,2)) #上面per選擇的機率
            qindividuals1_on.fill(1 / 2)
            qindividuals1.append(qindividuals1_on)
        # print("qindividuals1:",qindividuals1)

        #n個量子表示一個cycles內的選擇斷邊
        qindividuals2=[]
        qindividuals3=[]
        qindividuals4=[]#q4
        q2_bit_table=[] #轉為qubit的編碼 紀錄長度
        q4_table=[] #因為後面q4需要用到位元差 先存下來
        trans=[]
        for i in cycles:
            q4_table_cycle=[] #還是需要分cycle出來
            # print("q4_table_cycle:",q4_table_cycle)
            #一個cycle代表一個循環的q_bit要選擇哪一個邊
            #這裡也要考慮只有一組交換
            # print("q2一個量子:",i)
            
            su=len(i)
            if su==2:
                q2_bit_table.append(1)
            else:q2_bit_table.append(su)
            
            # print("長度:",su)
            q2_bits=ceil(log2(su))
            # print("bit需要的數量:",q2_bits)

        
            q2=np.zeros((q2_bits,2))
            q2.fill(1 / 2)
            qindividuals2.append(q2)
            
            #for回圈走訪cycles 用索引直 算hamming 
            #在這裡生成q3
            # i=[0, 3, 5, 1, 6]
            # 我要計算0到3、3到5、5到1、1到6、6到0，之間的hamming距離
            #因為最後要和第一個生閘 用一個新陣列 再加入第一個
            two_q3=[] #0805 裝一個cycle內的 這是第二維
            two_q4=[] #0805 q4也是要一起看 這是第二維

            route_single=[] #不用
            
            i.reverse() #最重要 翻轉生成電路
            #如果cycle只有2個交換，只需一次就好
            length=len(i)
            # print("length",length)
            ic=copy.copy(i)
            i.append(i[0])
            trans.append(i)
            # print("i",i)
            #這裡有個超級大重點 因為斷邊後會少一截 但每個族群斷的邊是不一樣的 所以會少斷邊的前一個
            #0805 註解:length以2為基準 如果長度2代表不會循環 本身一次即循環

            if length!=2:
                for x in range(length):#-1是因為長度和間格會差一 這是一次循環內每一個
                    start=i[x]
                    end=i[x+1]  
                    #0805 我會抓到兩個值 起點和終點
                    n_bit=hamming_distance(start,end)
                    # print("n_bit",n_bit)  
                    n_a_q3=ceil(log2(n_bit))
                    # print(n_a_q3)
                    three_q3=[]
                    if n_a_q3==0:
                        three_q3.append([999,999])
                        two_q3.append(three_q3)
                    else:
                        qindividuals3_on=np.zeros((n_a_q3,2)) #上面per選擇的機率
                        qindividuals3_on.fill(1 / 2)
                        for q33 in range(n_bit):
                            three_q3.append(qindividuals3_on)
                        two_q3.append(three_q3)

                    #q4解決好
                    bit_gate_q4=2*n_bit-1 -1 #q4數量計算公式 自己推的 差3bit 5個閘 4bit 7個閘 再減一代表 因為q4是考慮前先動還是後動 中間的不考慮

                    if bit_gate_q4==0: #代表差一個閘
                        q4=[]
                        q4.append([999,999]) #數字999時 就是差一位元
                        two_q4.append(q4)
                        # print("q4",q4)
                    else:
                        q4=np.zeros((bit_gate_q4,2))
                        q4.fill(1 / 2)
                        two_q4.append(q4)

            else:
                start=i[0]
                end=i[1]
                #0805 這是複製上面的 應該這裡也是一樣的
                #0805 我會抓到兩個值 起點和終點
                n_bit=hamming_distance(start,end)
                # print("n_bit",n_bit)  
                n_a_q3=ceil(log2(n_bit))
                # print("n_bit",n_bit)
                # print(n_a_q3)
                three_q3=[]
                if n_a_q3==0:
                    three_q3.append([999,999])
                    two_q3.append(three_q3)
                else:
                    qindividuals3_on=np.zeros((n_a_q3,2)) #上面per選擇的機率
                    qindividuals3_on.fill(1 / 2)
                    for q33 in range(n_bit):
                        three_q3.append(qindividuals3_on)
                    two_q3.append(three_q3)

                #q4解決好
                bit_gate_q4=2*n_bit-1 -1 #q4數量計算公式 自己推的 差3bit 5個閘 4bit 7個閘 再減一代表 因為q4是考慮前先動還是後動 中間的不考慮

                if bit_gate_q4==0: #代表差一個閘
                    q4=[]
                    q4.append([999,999]) #數字999時 就是差一位元
                    two_q4.append(q4)
                    # print("q4",q4)
                else:
                    q4=np.zeros((bit_gate_q4,2))
                    q4.fill(1 / 2)
                    two_q4.append(q4)
                
            qindividuals3.append(two_q3) #0805
            qindividuals4.append(two_q4) #0805

        #update Q2要用到
        bit_lengths_q2=[]
        for i in qindividuals2:
            bit_lengths_q2.append(len(i))

        # experiment=0
        qq1=copy.deepcopy(qindividuals1)
        qq2=copy.deepcopy(qindividuals2)
        qq3=copy.deepcopy(qindividuals3)
        qq4=copy.deepcopy(qindividuals4)
        total_best=[]

        for e in range(experiment):
            if e!=0:
                qindividuals1=copy.deepcopy(qq1)
                qindividuals2=copy.deepcopy(qq2)
                qindividuals3=copy.deepcopy(qq3)
                qindividuals4=copy.deepcopy(qq4)
            
            best_gate = float('inf')
            i=0 
            while i < NumIter:
                i = i + 1
                neighbours1,neighbours2,neighbours3,neighbours4 = gen_nbrs(qindividuals1,qindividuals2,qindividuals3,qindividuals4,N)
                circuit_solution=route_neighbour(neighbours1,neighbours2,neighbours3,neighbours4,q2_bit_table,trans,n) 
                length_with_index = [(len(row), i) for i, row in enumerate(circuit_solution)]
                # 按長度排序（由小到大），保持原始索引
                sorted_length_with_index = sorted(length_with_index, key=lambda x: x[0])
                # print("sorted_length_with_index",sorted_length_with_index)
                # 提取排序後的長度與索引
                sorted_lengths = [item[0] for item in sorted_length_with_index]
                original_indices = [item[1] for item in sorted_length_with_index]
                local_gate=sorted_lengths[0]
                
                updateQ(qindividuals1,qindividuals2,qindividuals3,qindividuals4,neighbours1,neighbours2,neighbours3,neighbours4,original_indices,cycles_bit)
                
                
                if best_gate>local_gate:
                    best_gate=local_gate
                    best_solution=circuit_solution[original_indices[0]]
                yield f"data: {json.dumps({'total_epochs':NumIter,'epoch':i,'circuit':best_solution})}\n\n"
            
