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

def check(gate,n):
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
    # neighbours1 =[np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]]),np.array([[1, 1, 1],
    #    [1, 1, 1],
    #    [1, 1, 1],
    #    [0, 1, 0],
    #    [1, 1, 0]])]
    #     # n1_adj [7, 7, 7, 2, 6]
    #     # n2_adj [4, 5, 0, 9, 0]
    
    # neighbours2 =[[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]],[[0, 0, 0, 1, 0, 0], [1, 0, 1], [0, 0, 0], [1, 0, 0, 1], [0, 0]]]
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
        
        # print("n1",n1_adj)
        # print("n2",n2_adj)
        # n1_adj= [0, 1]
        # n2_adj= [0, 0]
        # print("n1",n1_adj)
        # print("n2",n2_adj)
        # n1_adj= [1, 1]
        # n2_adj= [1, 0]
        circuit_solution.append(make_route(n1_adj,n2_adj,n3_adj,n4[i],trans,n)) #地i個族群neighbours進去形成一個我要的路線和閘
        
    return circuit_solution


def route_tenbit(index,solution3,trans,n):
    route=[]
    
    # print("index",index)
    # print("solution3",solution3)
    if solution3[0]!=999:

        #solution3處理
        # print("solution3",solution3)
        so33 = sorted(enumerate(solution3), key=lambda x: x[1],reverse=True)
        # print("so33",so33)  
        pp = [idx for idx, val in so33]
        # print("pp",pp)
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
            # print("decimal",decimal)

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


def build_q3(index,solution3,trans,fg,n):
    #算個位元差回傳 build多一個參數 陣列 跟收到的要看看
    route=[]
    lc_one=0
    lc_two=0
    # print("index",index)
    # print("tra",trans)
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
        bin_minus=hamming_distance(start,end)
        arr1=[int(b) for b in bin(start)[2:].zfill(n)]
        arr2=[int(b) for b in bin(end)[2:].zfill(n)]
        if fg:
            lc_one=start
            lc_two=end
        # print("start",start)
        # print("end",end)
        # print("arr1",arr1)
        # print("arr2",arr2)
        location=[]
        for ind in range(len(arr1)):
            #來看哪幾個不重複 紀錄索引直
            if arr1[ind]!=arr2[ind]:
                location.append(ind)

    else:
        start=trans[index]
        end=trans[index+1]
        route.append(start)
        route.append(end)
        bin_minus=hamming_distance(start,end)
        arr1=[int(b) for b in bin(start)[2:].zfill(n)]
        arr2=[int(b) for b in bin(end)[2:].zfill(n)]
        pp=[999]
        if fg:
            lc_one=start
            lc_two=end
        location=[]
        for ind in range(len(arr1)):
            #來看哪幾個不重複 紀錄索引直
            if arr1[ind]!=arr2[ind]:
                location.append(ind)
        
    # print("route",  route)

    return location,bin_minus,lc_one,lc_two

def build_nt_q3(nt_o,nt_t,n): #計算循環下一個的第一組
    #算個位元差回傳 build多一個參數 陣列 跟收到的要看看
    route=[]
    lc_one=0
    lc_two=0
    # print("index",index)
    # print("tra",trans)
    # print("solution3",solution3)
    
    start=nt_o
    route.append(start)
    end=nt_t
    arr1=[int(b) for b in bin(start)[2:].zfill(n)]
    arr2=[int(b) for b in bin(end)[2:].zfill(n)]

    location=[]
    for ind in range(len(arr1)):
        #來看哪幾個不重複 紀錄索引直
        if arr1[ind]!=arr2[ind]:
            location.append(ind)


    return location

def analyze_sequences_ka(data,hamm,common_value,inp_cycle_total): #目前這個才對
    # 初始化：counts 用來存數量 (int)，elements 用來存找到的元素 (list)
    counts = [0] * (len(data))
    elements = [[] for _ in range(len(data))]

    # print("counts",counts)
    # print("elements",elements)
    #0223 取自最後一個陣列出來
    get_fi=data[-1]
    matched_elements=[]
    
    #v3
    tw_b=data[0] #未配對位置索引直

    # print("data",data)
    # print("最後一個確認",get_fi)

    # if hamm[]==1: 代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下

    if len(data)==1:
        counts.append(0)
        elements.append([])
    # 走訪到倒數第二個，因為最後一個沒有「下一個」可以比對
    for i in range(len(data) - 1):
        # print("i",i)
        # print("elements",elements)
        current_arr = data[i]
        # print("current_arr",current_arr)
        matched_elements = []
        kc_ham=hamm[i]
        if len(elements[i])!=0: #代表空的 可以給全滿hamm[i] 
            kc_ham=hamm[i]-1-len(elements[i])
        # 建立探索指標，從下一個開始
        next_idx = i + 1
        ton=False #看是不是可以決定 要不要app insert
        # ka_count=-1
        ka_count=len(elements[i])
        while next_idx < len(data) and kc_ham>0: #判斷有沒有超出陣列
            # print("elements",elements)
            next_arr = data[next_idx] #比對的是下一個
            # print("next_arr",next_arr)
            # 找出 current_arr 中有出現在 next_arr 裡的元素
            # 且該元素還沒被這一次探索記錄過
            found = [x for x in current_arr if x in next_arr and x not in matched_elements]
            # print("found",found)
            if found:
                matched_elements.extend(found)
            
            #如果現在是
            #bug修復 當已有尾消的陣列 再加上頭 會導致錯位
            tmp_fd=[] #新陣列站存
            for fd in found: #pop出來 放進
                data[i].remove(fd) #刪頭
                data[next_idx].remove(fd) #刪接
                #回傳接頭.
                
                tmp_fd.insert(0,fd)
                
                elements[next_idx].append(fd)
                kc_ham-=1#美有一個就-1長度
            # ka_count+=1
            # print("ka_count",ka_count)
            # print("elements",elements)
            for td in tmp_fd:
                if ton:
                    elements[i].insert(ka_count,td)
                else:
                    elements[i].append(td)
            #特例自己一 前一個可以幫忙消 單獨在算一次
            if hamm[i]==1 and i!=0 and len(found)==1 and (counts[i-2]+1 < hamm[i-1]): #代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下  #且不是第一個 因為要往前看 #且此輪可以和下個配對到
                # print("特例單")
                found = [x for x in data[i-1] if x in next_arr and x not in matched_elements]
                if found:
                    matched_elements.extend(found)
                    tmp_fd=[] #新陣列站存
                    # print("tmp_fd",tmp_fd)
                    for fd in found: #pop出來 放進
                        data[i-1].remove(fd) #刪頭
                        data[next_idx].remove(fd) #刪接
                        #回傳接頭.
                        tmp_fd.insert(0,fd)
                        elements[next_idx].append(fd)
                        kc_ham-=1#美有一個就-1長度
                    for fd in tmp_fd:
                        elements[i-1].append(fd)
                
            # 條件判斷：如果 next_arr 長度為 1，代表可以繼續往後看
            if len(found) == 1 and (next_idx + 1) < len(data) and hamm[next_idx]==1:
                # print("如果 next_arr 長度為 1")
                next_idx += 1
                ton=True
            else:
                # 否則停止這次向後的探索
                break
        
        # 紀錄結果：數量給 0 (不再是空列表)，元素保持列表
        counts[i]=len(matched_elements)
        
            
        # print("ele",elements)
        # print("此輪counts",counts)
        # print("此輪elements",elements)
        # elements.append(matched_elements)
    # print("counts",counts)
    # print("elements",elements)
    return counts, elements, get_fi,  elements[-1], elements[0], tw_b

def analyze_sequences_kb(data,hamm,common_value): #目前這個才對
    # 初始化：counts 用來存數量 (int)，elements 用來存找到的元素 (list)
    counts = [0] * (len(data))
    elements = [[] for _ in range(len(data))]
    # print("counts",counts)
    # print("elements",elements)
    #0223 取自最後一個陣列出來
    get_fi=data[-1]
    matched_elements=[]
    # print("common_value",common_value)
    #v3
    tw_b=data[0] #未配對位置索引直

    # print("data",data)
    # print("最後一個確認",get_fi)

    # if hamm[]==1: 代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下

    if len(data)==1:
        counts.append(0)
        elements.append([])
    # 走訪到倒數第二個，因為最後一個沒有「下一個」可以比對
    for i in range(len(data) - 1):
        # print("i",i)
        current_arr = data[i]
        matched_elements = []
        kc_ham=hamm[i]
        if len(elements[i])!=0: #代表空的 可以給全滿hamm[i] 
            kc_ham=hamm[i]-1-len(elements[i])
        # 建立探索指標，從下一個開始
        next_idx = i + 1
        ton=False #看是不是可以決定 要不要app insert
        # ka_count=-1
        ka_count=len(elements[i])
        while next_idx < len(data) and kc_ham>0: #判斷有沒有超出陣列
            # print("elements",elements)
            next_arr = data[next_idx] #比對的是下一個
            # 找出 current_arr 中有出現在 next_arr 裡的元素
            # 且該元素還沒被這一次探索記錄過
            if i==0: #第一個
                kb_found=[] #在這裡以特例 要配合˙
                # print("matched_elements",matched_elements)
                # print('common_value not in matched_elements',common_value not in matched_elements)
                if common_value in next_arr and common_value not in matched_elements:
                    kb_found =[common_value]
                
                    if len(kb_found)==1:
                        matched_elements.extend(kb_found)
            
            found = [x for x in current_arr if x in next_arr and x not in matched_elements]
            if found:
                matched_elements.extend(found)
            if i==0:
                found=kb_found+found
            
            #如果現在是
            #bug修復 當已有尾消的陣列 再加上頭 會導致錯位
            tmp_fd=[] #新陣列站存
            for fd in found: #pop出來 放進
                data[i].remove(fd) #刪頭
                data[next_idx].remove(fd) #刪接
                #回傳接頭.
                
                tmp_fd.insert(0,fd)
                
                elements[next_idx].append(fd)
                kc_ham-=1#美有一個就-1長度
            
            # ka_count+=1
            # # print("ka_count",ka_count)
            # print("elements",elements)
            for td in tmp_fd:
                if ton:
                    elements[i].insert(ka_count,td)
                else:
                    elements[i].append(td)
            #特例自己一 前一個可以幫忙消 單獨在算一次
            if hamm[i]==1 and i!=0 and len(found)==1 and (counts[i-2]+1 < hamm[i-1]): #代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下  #且不是第一個 因為要往前看 #且此輪可以和下個配對到
                # print("特例單")
                found = [x for x in data[i-1] if x in next_arr and x not in matched_elements]
                if found:
                    matched_elements.extend(found)
                    tmp_fd=[] #新陣列站存
                    # print("tmp_fd",tmp_fd)
                    for fd in found: #pop出來 放進
                        data[i-1].remove(fd) #刪頭
                        data[next_idx].remove(fd) #刪接
                        #回傳接頭.
                        tmp_fd.insert(0,fd)
                        elements[next_idx].append(fd)
                        kc_ham-=1#美有一個就-1長度
                    for fd in tmp_fd:
                        elements[i-1].append(fd)
                
            # 條件判斷：如果 next_arr 長度為 1，代表可以繼續往後看
            if len(found) == 1 and (next_idx + 1) < len(data) and hamm[next_idx]==1:
                # print("如果 next_arr 長度為 1")
                next_idx += 1
                ton=True
            else:
                # 否則停止這次向後的探索
                break
        
        # 紀錄結果：數量給 0 (不再是空列表)，元素保持列表
        counts[i]=len(matched_elements)
        
            
        # print("ele",elements)
        # print("此輪counts",counts)
        # print("此輪elements",elements)
        # elements.append(matched_elements)
    # print("counts",counts)
    # print("elements",elements)
    return counts, elements, get_fi,  elements[-1], elements[0], tw_b


def analyze_sequences(data,hamm):
    # print("data",data)
    # print("hamm",hamm)
    counts = []   # 紀錄出現的數量
    elements = [] # 紀錄出現的元素
    
    # print("data",data)
    if len(data)==1:
        counts.append(0)
        elements.append([])
    # 走訪到倒數第二個，因為最後一個沒有「下一個」可以比對
    for i in range(len(data) - 1):
        current_arr = data[i]
        # print("current_arr",current_arr)
        matched_elements = []
        kc_ham=hamm[i]
        if len(elements[i])!=0: #代表空的 可以給全滿hamm[i] 
            kc_ham=hamm[i]-1-len(elements[i])
        # 建立探索指標，從下一個開始
        next_idx = i + 1
        
        while next_idx < len(data) and kc_ham>0: #判斷有沒有超出陣列
            next_arr = data[next_idx] #比對的是下一個
            # print("next_arr",next_arr)
            # 找出 current_arr 中有出現在 next_arr 裡的元素
            # 且該元素還沒被這一次探索記錄過
            found = [x for x in current_arr if x in next_arr and x not in matched_elements]
            # print("found",found)
            if found:
                matched_elements.extend(found)
                
            # 條件判斷：如果 next_arr 長度為 1，代表可以繼續往後看
            if len(next_arr) == 1 and len(found) == 1 and (next_idx + 1) < len(data):
                next_idx += 1
            else:
                # 否則停止這次向後的探索
                break
        
        # 紀錄結果：數量給 0 (不再是空列表)，元素保持列表
        # print("matched_elements",matched_elements)
        counts.append(len(matched_elements))
        elements.append(matched_elements)
        
    return counts, elements
def analyze_sequences_test(data,hamm): #目前這個才對
    # 初始化：counts 用來存數量 (int)，elements 用來存找到的元素 (list)
    counts = [0] * (len(data))
    elements = [[] for _ in range(len(data))]

    # print("counts",counts)
    # print("elements",elements)
    #0223 取自最後一個陣列出來
    get_fi=data[-1]
    matched_elements=[]
    
    #v3
    tw_b=data[0] #未配對位置索引直

    # print("data",data)
    # print("hamm",hamm)
    # print("最後一個確認",get_fi)

    # if hamm[]==1: 代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下

    if len(data)==1:
        counts.append(0)
        elements.append([])
    # 走訪到倒數第二個，因為最後一個沒有「下一個」可以比對
    for i in range(len(data) - 1):
        current_arr = data[i]
        # print("current_arr",current_arr)
        matched_elements = []
        kc_ham=hamm[i]
        if len(elements[i])!=0: #代表空的 可以給全滿hamm[i] 
            kc_ham=hamm[i]-1-len(elements[i])

        # 建立探索指標，從下一個開始
        next_idx = i + 1
        ton=False #看是不是可以決定 要不要app insert
        while next_idx < len(data) and kc_ham>0: #判斷有沒有超出陣列
            next_arr = data[next_idx] #比對的是下一個
            # print("next_arr",next_arr)
            # 找出 current_arr 中有出現在 next_arr 裡的元素
            # 且該元素還沒被這一次探索記錄過
            found = [x for x in current_arr if x in next_arr and x not in matched_elements]
            if found:
                matched_elements.extend(found)
            
            #如果現在是
            #bug修復 當已有尾消的陣列 再加上頭 會導致錯位
            tmp_fd=[] #新陣列站存
            for fd in found: #pop出來 放進
                data[i].remove(fd) #刪頭
                data[next_idx].remove(fd) #刪接
                #回傳接頭.
                
                tmp_fd.insert(0,fd)
                
                elements[next_idx].append(fd)
                
                kc_ham-=1#美有一個就-1長度
            
            if ton:
                elements[i]=tmp_fd+elements[i]
            else:
                for fd in tmp_fd:
                    elements[i].append(fd)
            #特例自己一 前一個可以幫忙消 單獨在算一次
            if hamm[i]==1 and i!=0 and len(found)==1 and (counts[i-2]+1 < hamm[i-1]): #代表他是1並且沒有被蕭 如果後面可以消 前面的要看一下  #且不是第一個 因為要往前看 #且此輪可以和下個配對到
                # print("特例單")
                found = [x for x in data[i-1] if x in next_arr and x not in matched_elements]
                if found:
                    matched_elements.extend(found)
                    tmp_fd=[] #新陣列站存
                    for fd in found: #pop出來 放進
                        data[i-1].remove(fd) #刪頭
                        data[next_idx].remove(fd) #刪接
                        #回傳接頭.
                        tmp_fd.insert(0,fd)
                        elements[next_idx].append(fd)
                    for fd in tmp_fd:
                        elements[i-1].append(fd)
                
            # 條件判斷：如果 next_arr 長度為 1，代表可以繼續往後看
            if len(found) == 1 and (next_idx + 1) < len(data) and hamm[next_idx]==1:
                # print("如果 next_arr 長度為 1")
                next_idx += 1
                ton=True
            else:
                # 否則停止這次向後的探索
                break
        
        # 紀錄結果：數量給 0 (不再是空列表)，元素保持列表
        counts[i]=len(matched_elements)
        
            
        # print("ele",elements)
        # print("此輪counts",counts)
        # print("此輪elements",elements)
        # elements.append(matched_elements)
    # print("counts",counts)
    # print("elements",elements)
    return counts, elements, get_fi,  elements[-1], elements[0], tw_b



def custom_set_zero(data):
    for i in range(len(data)):
        item = data[i]
        
        if isinstance(item, list):
            # 檢查這是否為最深層的數值列表 (即列表內不再有列表)
            is_deepest = all(not isinstance(x, list) for x in item)
            
            if is_deepest:
                if len(item) == 1:
                    data[i] = [999]
                else:
                    # 長度大於 1 的深層列表，內容全部歸零
                    data[i] = [0] * len(item)
            else:
                # 如果不是最深層，繼續往裡面走
                custom_set_zero(item)
                
                # 特殊處理：如果子層處理完後，發現目前這層原本應該是容器但變成了某種狀態
                # 這裡會持續遞迴直到最底層
        else:
            # 如果直接遇到數值
            if item != 999:
                data[i] = 0

def pre_dici(nt_one, nt_two, lc_one, lc_two, next_index, q3_index):

    #先預測有沒有機會配對到
    it_index=0
    nt_one_lc_two=hamming_distance(nt_one,lc_two)
    nt_one_lc_one=hamming_distance(nt_one,lc_one)
    nt_two_lc_two=hamming_distance(nt_two,lc_two)
    nt_two_lc_one=hamming_distance(nt_two,lc_one)
    #1是 這個循環最後要尾 新的要頭
    #2是 這個循環最後要頭 新的要頭
    #好像不用
    #3是 這個循環最後要尾 新的要尾
    #4是 這個循環最後要頭 新的要尾

    common_value=-1
    #直接搜尋有沒有機會
    for val_a in q3_index:
        for val_b in next_index:
            if val_a ==val_b: #2 和配對到的 下一個頭
                common_value = val_a
                break  # 找到第一個就跳出迴圈
    
    if common_value != -1:
        if nt_one_lc_two==1 or nt_one_lc_one==1 : # 尾頭
            it_index=1 #這樣就ok

    return it_index


def dici(nt_one,nt_two,lc_one,lc_two,get_fi,he_fi,nt_index):

    #obe來判斷是否可以用1.3 因為會有限制 前後加起來不能超過
    #2.4是因為它們吃的是頭 不用尾
    obe=False
    ka_four=0
    inp_cycle_total=0
    # get_fi
    if len(he_fi)!=0: #他不是空的 
        if len(get_fi)>1: #要大於1
            obe=True
    else:obe=True #==0 直接過

    #這是有的
    # print("common_value",common_value)
    
    nt_one_lc_two=hamming_distance(nt_one,lc_two)
    nt_one_lc_one=hamming_distance(nt_one,lc_one)
    nt_two_lc_two=hamming_distance(nt_two,lc_two)
    nt_two_lc_one=hamming_distance(nt_two,lc_one)
    #才去看hamm 然後配對1.2.3.4
    #要先3後2 後1  因為3.2都不太會需要用到新的 可以用舊的
    #正常條so3
    common_value = []  # 先預設一個空值

    #找循環間共同索引直
    if len(get_fi)>0:
        for val in get_fi:
            if val in nt_index:
                common_value.append(val) 
    #3
    if nt_two_lc_two==1 and len(common_value)!=0 and obe : #因為有順序 所以1.3先拉到前面判斷
            inp_cycle_total=3 

    #2
    if inp_cycle_total==0 and len(he_fi)>0: #代表前面是沒配對到
        common_value=[] #調回來
        if he_fi[0] in nt_index : #如果第一個有在裡面的話 就可以繼續配對2.4
            common_value.append(he_fi[0])
            if nt_one_lc_one==1 and len(common_value)!=0 :#and obe_after:
                inp_cycle_total=2

    #1
    
    if inp_cycle_total==0: #如果==0 代表前面沒達成
        #找循環間共同索引直 #2被重製了
        if len(get_fi)>0:
            for val in get_fi:
                if val in nt_index:
                    common_value.append(val) 
        if nt_one_lc_two==1 and len(common_value)!=0 and obe :#and obe_after #代表兩個都符合了
            inp_cycle_total=1 #這樣就ok

    
    #4 好像是獨立出來的 如果前 後 都一定要配到的 如果沒有 可以幫忙媒合
        
    if nt_two_lc_one==1 and len(common_value)!=0 and len(he_fi)>0:
        ka_four=1
                

        #226 
        
        #1是 這個循環最後要尾 新的要頭 正常看還有多少get_fi
        #有get_fi 就直接配對(原本的)尾就好 不要頭? 因為你都有測index了
        #2是 這個循環最後要頭 新的要頭 
        #這個好像只能是和本的頭 第一個 對 所以直接看he_fi的第一個索引直有沒有配對
        #抓1,2,3,4 和 位置  #這個原本的就不用動 新的頭要弄

        #3是 這個循環最後要尾 新的要尾 正常看還有多少get_fi
        #有get_fi 就直接配對(原本的)尾就好 因為你都有測index了
        #注意這裡要好好的條後面的尾

        #4是 這個循環最後要頭 新的要尾 
        #這個好像只能是和本的頭 第一個 對 所以直接看he_fi的第一個索引直有沒有配對
        #注意這裡要好好的條後面的尾

        #先直接看索引值

        #把one two 去和 目前最後的 位置去搭配 ##抓對喔lc_one和lc_two (if final)
        #hamming nt_one,lc_two ==1 , hamming nt_one,lc_one == hamm值的-1 1
        #hamming nt_one,lc_two ==hamm值的-1 , hamming nt_one,lc_one == 1 2  和1相反
        #hamming nt_two,lc_two ==1 , hamming nt_two,lc_one == hamm值的-1 3  和1,2不同的是把nt_one改成nt_two
        #hamming nt_two,lc_two ==hamm值的-1 , hamming nt_two,lc_one == 1 3

        #分別對應1~4 放進一個值
        #設一個if  >0 #接著才丟到 看索引值的地方 把目前剩餘的local 和new的build_q3 特別針對ntone two 的local媒合
        #如果有成功媒到 額外紀錄這個值放進前面說是cycle_total  如果沒有媒合到 就是丟0進去 不管

    # if inp_cycle_total==0: #代表在上面沒有進去或得到 還是有可能是2.4
    #     common_value=-1

    #接著判斷是否為2.4例外 是否就是可化簡
    #原本的he_fi 和 nt_index 有沒有關係
    # common_indices = None # 記錄這些值在 he_fi 中的索引位置

    ###### 好像只能是第一個才能
    # if len(common_value)!=0: #有的話再看一次nt_one 和 lc_two  (2,4)
    #     inp_cycle_total=4
    #     for idx, val in enumerate(he_fi):
    #         if val in nt_index:
    #             # for 迴圈 enumerate來看 
    #             # 然後抓到的common_indices
    #             common_value = val
    #             common_indices = idx +1 #索引值加一 就是位元差
                #如果 common_indices==nt_one_lc_two (2) 或 ==nt_two_lc_two (4) 這樣代表
                # q3_hamming_mid[-1]-common_indices和 ==nt_one_lc_one (2) 或 ==nt_two_lc_one (4)
                #這邊有的話就直接break
                #有的話紀錄 common_value 就是要接的位置索引值




    return common_value,inp_cycle_total,ka_four


def make_route(solution1,solution2,solution3,solution4,trans,n): #這樣是一組解弄成路線
    
    # print("start!!!!!!!!!!!!!!!11")
    # print("solution1",solution1)
    # print("solution2",solution2)
    # print("輸出樣式solution3",solution3)
    # set_zero(solution3)
    custom_set_zero(solution3)
    # print("輸出樣式solution3",solution3)    
    route_so=[]
    route_gate=[]
    sorted_with_index = sorted(enumerate(solution1), key=lambda x: x[1], reverse=True)
    original_indices = [idx for idx, val in sorted_with_index]
    # print("trans",trans)
    # print("sorted_with_index",sorted_with_index)
    # print("對應原本的索引：", original_indices) #[1, 2, 0]
    # print("solution3",solution3)
    
    #0201每一個解 用斷邊和循環順序，先建立位置
    q3_index=[]
    q3_hamming=[]
    #v4
    kb_counts = []   # 紀錄出現的數量
    kb_elements = [] # 紀錄出現的元素
    route_so=[] #刷新裝
    length_cycle=len(solution1) #紀錄總長度
    cy_cy_zerone=[] #紀錄循環間有沒有機會消除
    #紀錄循環間當前剩餘和頭 和 下一個的頭的剩餘和尾
    #如果最後一次的話就紀錄剩餘和頭就好
    #這裡會有兩次判斷 
    #v3
    ky_lc_one=[]
    ky_lc_two=[]
    ky_nt_index=[]
    ky_nt_index_leap=[]
    ky_q3_index_mid=[]

    for ind,so1 in enumerate(original_indices):
        q3_index_mid=[]
        q3_hamming_mid=[]
        index=solution2[so1] #因為斷邊 所以從這裡開始
        
        
        num=len(solution3[so1])
        
        if num==1:
            #代表只有一個交換 我們在前面只用一個 沒有循環 在這裡偷偷加一
            num=2
        fg=False
        for so2 in range(num-1): #要減一 因為斷邊
            
            if index >=num: #如果超出迴圈 因為是循環 會回到第一個
                index=0
            # print("trans[so1]",trans[so1])
            # print("index",index)
            if so2 == num-2:
                fg=True
            t1,ham,lc_one,lc_two=build_q3(index,solution3[so1][index],trans[so1],fg,n)
            # print("solution3[so1][index]",solution3[so1][index])
            if fg:
                ky_lc_one.append(lc_one)
                ky_lc_two.append(lc_two)
            #roa路線
            #roa_gate是閘的順序
            # print("roa_gate",roa_gate)
            q3_index_mid.append(t1)
            q3_hamming_mid.append(ham) #中間節點數量=hamming -1 
            
            index+=1
        q3_index.append(q3_index_mid)
        q3_hamming.append(q3_hamming_mid)
        # print("q3_index",q3_index)
        if ind<len(original_indices)-1:  #最後一組 不用配對
            # print("下一個循環",trans[original_indices[ind+1]])
            #抓下一個的頭尾
            nt_one=trans[original_indices[ind+1]][solution2[original_indices[ind+1]]]
            nt_two=trans[original_indices[ind+1]][solution2[original_indices[ind+1]]+1]
            
            next_index=build_nt_q3(nt_one,nt_two,n) #v3應該不需要
        
            #這東西在這裡目的是 未了要先判斷 有沒有機會配對而已 所以應該是傳入
            it_index=pre_dici(nt_one, nt_two, lc_one, lc_two, next_index, q3_index_mid[-1])
            cy_cy_zerone.append(it_index) #好像沒用了
        #=--------------------------------------------------------------
        # v4 參數準備
        
        #這是整體的要準備 不知用不用的到
        # print("q3_index",q3_index) 
        # print("q3_hamming",q3_hamming) #和hamming
        # cy_cy_zerone 整體循環間化簡

        # lc_one 當前的 0
        # lc_two 當前的-1

        #q3_index_mid 還沒分析的索引值
        #q3_hamming_mid #和hamming

        
        # nt_one 下個的 0
        # nt_two 下個的 -1
        # next_index 下個 可配對的索引值
        # print("q3_index_mid",q3_index_mid)
        # print("q3_hamming_mid",q3_hamming_mid)
        # print("next_index",next_index)
        # #it_index 循環間有沒有機會化簡
        # print("it_index",it_index)

    #在這裡判斷多少量-------------------------------------------------------------------
    kb_cy=[]
    kb_index=[]
    ka_nt_index=[]
    ka_bool=True
    # print("一組")
    for ind,so1 in enumerate(original_indices):

        q3_index_mid_copy = copy.deepcopy(q3_index[ind])
        q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
        # print("開始了")
        # print("q3_index_mid",q3_index[ind])
        # print("q3_hamming",q3_hamming[ind])
        #延續觀察q3 共同索引值 
        # print()
        
        #v4 拉到都生成好後
        # if ind==0: #先做這個
        if ka_bool: #一開始一定true 正常輸入出
            # print("q3_index_mid_copy",q3_index_mid_copy)
            counts_tmp,elements_tmp,get_fi,he_fi,tw_aa,tw_bb=analyze_sequences_test(q3_index_mid_copy,q3_hamming_mid_copy)
            # print("yes",counts_tmp)
            # if ind==0: #第一個不用
            kb_cy.append(0)
            kb_index.append(-1) #索引值一定0以上 

        else:
            #還沒改好 如果
            #insert q3_index_mid_copy,q3_hamming_mid_copy 然後就可以開始配對
            #0302
            # print("進入for搜尋common_value")
            # print("common_value",common_value)
            #直接給一版 
            if inp_cycle_total==3: #3不用加進analyze_sequences_ka配對 先獨立的那種 另外處理 後續如果 沒成功 就再看4
                #直接做 看的是[0] 一個是正常版 一個是[0]套進去 比對出來
                q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                # print("q3_index_mid_copy",q3_index_mid_copy)
                counts_tmp,elements_tmp,get_fi,he_fi,tw_aa,tw_bb=analyze_sequences_test(q3_index_mid_copy,q3_hamming_mid_copy)
                kb_count=sum(counts_tmp)
                kb_val=-1
                
                if len(elements_tmp[0])!=0 and elements_tmp[0][-1] in common_value :
                    pass
                else:#代表需手動
                    for idx,val in enumerate(common_value): #再迴圈中套用kb
                        q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                        q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                        kb_counts_tmp,kb_elements_tmp,kb_get_fi,kb_he_fi,kb_tw_aa,kb_tw_bb=analyze_sequences_kb(q3_index_mid_copy,q3_hamming_mid_copy,val)
                        
                        # print("counts_tmp",counts_tmp)
                        # if idx==0: #第一組直接加
                        #     counts_tmp=kb_counts_tmp
                        #     kb_count=sum(counts_tmp) #計算次數
                        #     elements_tmp=kb_elements_tmp
                        #     get_fi=kb_get_fi
                        #     he_fi=kb_he_fi
                        #     tw_aa=kb_tw_aa
                        #     tw_bb=kb_tw_bb
                        #     kb_val=val

                        #大於等於 因為沒有+1代表加了有效
                        if sum(kb_counts_tmp)>=kb_count: 
                            # print("大於代表加了有效")
                            counts_tmp=kb_counts_tmp
                            kb_count=sum(counts_tmp) #計算次數
                            elements_tmp=kb_elements_tmp
                            get_fi=kb_get_fi
                            he_fi=kb_he_fi
                            tw_aa=kb_tw_aa
                            tw_bb=kb_tw_bb
                            kb_val=val

                #for搜尋完
                if kb_val!=-1: #有東西
                    kb_cy.append(inp_cycle_total) #有
                    kb_index.append(kb_val)
                else:
                    kb_cy.append(0)
                    kb_index.append(-1)
                
            
            elif inp_cycle_total==1 or inp_cycle_total==2: #1.2在這裡處理 不同的是 因為3不用加進analyze_sequences_ka配對 先獨立的那種 另外處理 後續如果 沒成功 就再看4  三也要另外看==
                for idx,val in enumerate(common_value):
                    
                    q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                    q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                    q3_hamming_mid_copy.insert(0, 1)
                    q3_index_mid_copy.insert(0,[val])
                    kb_counts_tmp,kb_elements_tmp,kb_get_fi,kb_he_fi,kb_tw_aa,kb_tw_bb=analyze_sequences_ka(q3_index_mid_copy,q3_hamming_mid_copy,val,inp_cycle_total)
                    # 拿掉[0] 並同時仙裝進去
                    #直接拿掉 是為了 要配對而已 已有另外紀錄
                    kb_counts_tmp.pop(0)
                    kb_elements_tmp.pop(0)
                    q3_hamming_mid_copy.pop(0)
                    q3_index_mid_copy.pop(0)

                    if idx==0: #第一組直接加
                        counts_tmp=kb_counts_tmp
                        kb_count=sum(counts_tmp) #計算次數
                        elements_tmp=kb_elements_tmp
                        get_fi=kb_get_fi
                        he_fi=kb_he_fi
                        tw_aa=kb_tw_aa
                        tw_bb=kb_tw_bb
                        kb_val=val

                    elif sum(kb_counts_tmp)>kb_count:
                        counts_tmp=kb_counts_tmp
                        kb_count=sum(counts_tmp) #計算次數
                        elements_tmp=kb_elements_tmp
                        get_fi=kb_get_fi
                        he_fi=kb_he_fi
                        tw_aa=kb_tw_aa
                        tw_bb=kb_tw_bb
                        kb_val=val

                #for搜尋完
                if counts_tmp[0]!=0: #有東西
                    kb_cy.append(inp_cycle_total) #有
                    kb_index.append(kb_val)
                else:
                    kb_cy.append(0)
                    kb_index.append(-1)
                    
                # print("counts_tmp",counts_tmp)
                # print("elements_tmp",elements_tmp)
                # print("kb_cy",kb_cy)
                # print("kb_index",kb_index)

            # kb_four_index_head #他的索引值
            #一樣
            #直接做 看的是[0] 一個是正常版 一個是[0]套進去 比對出來
            elif ka_four==1:
                q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                kc_one_index=q3_index_mid_copy[0]
                q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                counts_tmp,elements_tmp,get_fi,he_fi,tw_aa,tw_bb=analyze_sequences_test(q3_index_mid_copy,q3_hamming_mid_copy)
                kb_count=sum(counts_tmp)
                if kb_four_index_head in kc_one_index:
                    kc_go=True
                else: kc_go=False
            
                if len(elements_tmp[0])==0 and kc_go:#不等於才看'
                    q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                    q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                    
                    kb_counts_tmp,kb_elements_tmp,kb_get_fi,kb_he_fi,kb_tw_aa,kb_tw_bb=analyze_sequences_kb(q3_index_mid_copy,q3_hamming_mid_copy,kb_four_index_head) #丟對了
                    
                    #大於代表加了有效
                    if sum(kb_counts_tmp)>=kb_count: 
                        # print("大於代表加了有效")
                        counts_tmp=kb_counts_tmp
                        kb_count=sum(counts_tmp) #計算次數
                        elements_tmp=kb_elements_tmp
                        get_fi=kb_get_fi
                        he_fi=kb_he_fi
                        tw_aa=kb_tw_aa
                        tw_bb=kb_tw_bb
                elif len(elements_tmp[0])!=0 and kc_go:
                    if elements_tmp[0][-1]!=kb_four_index_head:
                        q3_index_mid_copy = copy.deepcopy(q3_index[ind])
                        q3_hamming_mid_copy = copy.deepcopy(q3_hamming[ind])
                        kb_counts_tmp,kb_elements_tmp,kb_get_fi,kb_he_fi,kb_tw_aa,kb_tw_bb=analyze_sequences_kb(q3_index_mid_copy,q3_hamming_mid_copy,kb_four_index_head) #丟對了
                        
                        #大於代表加了有效
                        if sum(kb_counts_tmp)>=kb_count: 
                            # print("大於代表加了有效")
                            counts_tmp=kb_counts_tmp
                            kb_count=sum(counts_tmp) #計算次數
                            elements_tmp=kb_elements_tmp
                            get_fi=kb_get_fi
                            he_fi=kb_he_fi
                            tw_aa=kb_tw_aa
                            tw_bb=kb_tw_bb
                
                kb_cy.append(0)
                kb_index.append(-1)
                   
            

    
        if ind<len(original_indices)-1:  #最後一組 不用配對
            # print("下一個循環",trans[original_indices[ind+1]])
            #抓下一個的頭尾
            nt_one=trans[original_indices[ind+1]][solution2[original_indices[ind+1]]]
            nt_two=trans[original_indices[ind+1]][solution2[original_indices[ind+1]]+1]
            
            nt_index=build_nt_q3(nt_one,nt_two,n) #v3應該不需要
            ka_nt_index.append(nt_index)
            common_value,inp_cycle_total,ka_four=dici(nt_one,nt_two,ky_lc_one[ind],ky_lc_two[ind],get_fi,he_fi,nt_index) 
            # print("common_value",common_value)
            # print("inp_cycle_total",inp_cycle_total)
            # print("ka_four",ka_four)
            # print("get_fi",get_fi)
            # print("he_fi",he_fi)
            if len(he_fi)!=0:
                kb_four_index_head=he_fi[0]
            if inp_cycle_total!=0 or ka_four==1: #代表有
                ka_bool=False
            else:ka_bool=True
        # print("lc_one",lc_one) #當前最後頭
        # print("lc_two",lc_two) #當前最後尾
        # print("tw_aa",tw_aa) #頭的排序 如果=0 代表沒有後 有的話 抓0
        # print("tw_bb",tw_bb) #未配對位置索引直
        ky_q3_index_mid.append(q3_index_mid[-1])
        #要跳過第一個
        if ind>0:
            ky_nt_index.append(tw_bb) #剩下的
            ky_nt_index_leap.append(tw_aa) #配對的
        
        index=solution2[so1] #因為斷邊 所以從這裡開始
        
        # print("counts_tmp",counts_tmp)
        # print("elements_tmp",elements_tmp)
        # print("q3_index",q3_index)
        for j,tmpi in enumerate(counts_tmp): #生成中間節點順序 solution3的解
            # print("j",j)
            if tmpi !=0: #代表有要處理
                #這裡有三個特例
                #1.基本的 往後看
                #2.下一個是 q3_hamming[ind][j+1]==1
                #3. 當前是q3_hamming[ind][j]==1
                if q3_hamming[ind][j]==1: #3先 (須測試)  (3-2可以)
                    # print("現在是一格")
                    # print("tmpi",tmpi)
                    #自己會跟前一個往下扣 在那個陣列才會最後排序
                    #自己不用調
                    dn=1-tmpi #這樣就會是負的 應證上
                    if q3_hamming[ind][j-1]!=1:
                        for tmpj in range(tmpi-1):
                            et=elements_tmp[j-1][-1-tmpj] #位置索引值
                            #看全索引直(q3_index[ind])裡面是第幾個
                            ad_et=0
                            for inde in q3_index[ind][j-1]: #這是裡面的值
                                if inde==et:
                                    # 真正條q3的地方 索引值
                                    break
                                else:ad_et+=1
                            # print("index",index)
                            # print("sol3",solution3)
                            # print("要調的so3位置",ad_et)
                            solution3[so1][index-1][ad_et]+=dn
                            dn+=1 #如果有下一個 高一點  這樣才能排後面的前面一點
                    # print("tmpi前夕",tmpi)
                    index=(index+1)%len(solution3[so1])
                    up=tmpi #要升的值 up
                    
                    for tmpj in range(tmpi):
                        # print("elements_tmp[j][tmpj]",elements_tmp[j][tmpj])
                        et=elements_tmp[j+1][tmpj] #位置索引值
                        # print("up_et",et)
                        ad_et=0
                        # print("q3_index[ind][j+1]",q3_index[ind][j+1])
                        for inde in q3_index[ind][j+1]: #這是裡面的值
                            if inde==et:
                                # 真正條q3的地方 索引值
                                break
                            else:ad_et+=1
                        # print("adet",ad_et)
                        # print("index",index)
                        # print("sol3",solution3)
                        solution3[so1][index][ad_et]+=up
                        up-=1 #如果有下一個 高一點  這樣才能排後面的前面一點
                    # print("結果3--------",solution3)
                
                elif q3_hamming[ind][j+1]==1: #2先 (須測試) (3-2可以)
                    # print("下一個是一格")
                    #下一個是 q3_hamming[ind][j+1]==1
                    #自己會跟前一個往下扣 在那個陣列才會最後排序
                    dn=-tmpi #這樣就會是負的 應證上
                    for tmpj in range(tmpi):
                        et=elements_tmp[j][-1-tmpj] #位置索引值
                        #看全索引直(q3_index[ind])裡面是第幾個
                        ad_et=0
                        for inde in q3_index[ind][j]: #這是裡面的值
                            if inde==et:
                                # 真正條q3的地方 索引值
                                break
                            else:ad_et+=1
                        # print("index",index)
                        # print("sol3",solution3)
                        # print("要調的so3位置",ad_et)
                        solution3[so1][index][ad_et]+=dn
                        dn+=1 #如果有下一個 高一點  這樣才能排後面的前面一點

                    index=(index+1)%len(solution3[so1])
                    nt=(index+1)%len(solution3[so1])
                    up=tmpi-1 #要升的值 up
                    if tmpi!=1 and q3_hamming[ind][j+2]!=1: #大於二 代表一定會有後後 不能是len(1)
                        for tmpj in range(tmpi-1):
                            # print("elements_tmp[j][tmpj]",elements_tmp[j][tmpj])
                            et=elements_tmp[j+2][tmpj] #位置索引值
                            ad_et=0
                            for inde in q3_index[ind][j+2]: #這是裡面的值
                                if inde==et:
                                    # 真正條q3的地方 索引值
                                    break
                                else:ad_et+=1
                            # print("index",index)
                            # print("sol3",solution3)
                            solution3[so1][nt][ad_et]+=up
                            up-=1 #如果有下一個 高一點  這樣才能排後面的前面一點
                    # print("結果2--------",solution3)
                else : #1.基本的 往後看
                    # print("基本")
                    #下一個是 q3_hamming[ind][j+1]==1
                    #自己會跟前一個往下扣 在那個陣列才會最後排序
                    dn=-tmpi #這樣就會是負的 應證上
                    for tmpj in range(tmpi):
                        et=elements_tmp[j][-1-tmpj] #位置索引值
                        #看全索引直(q3_index[ind])裡面是第幾個
                        ad_et=0
                        for inde in q3_index[ind][j]: #這是裡面的值
                            if inde==et:
                                # 真正條q3的地方 索引值
                                break
                            else:ad_et+=1
                        # print("index",index)
                        # print("sol3",solution3)
                        # print("要調的so3位置",ad_et)
                        solution3[so1][index][ad_et]+=dn
                        dn+=1 #如果有下一個 高一點  這樣才能排後面的前面一點

                    index=(index+1)%len(solution3[so1])
                    up=tmpi #要升的值 up
                    for tmpj in range(tmpi):
                        # print("elements_tmp[j][tmpj]",elements_tmp[j][tmpj])
                        et=elements_tmp[j+1][tmpj] #位置索引值
                        ad_et=0
                        for inde in q3_index[ind][j+1]: #這是裡面的值
                            if inde==et:
                                # 真正條q3的地方 索引值
                                break
                            else:ad_et+=1
                        # print("index",index)
                        # print("sol3",solution3)
                        solution3[so1][index][ad_et]+=up
                        up-=1 #如果有下一個 高一點  這樣才能排後面的前面一點
                    # print("結果1--------",solution3)
                            
            else:index=(index+1)%len(solution3[so1])
            # print("so3後",solution3)
            # print("----------------------------")
        # print("kb_cy",kb_cy)
        # print("kb_index",kb_index)
        # print("ind",ind)
        #0302繼續 
        #如果kb_cy.append(0) 
        #        kb_index.append(-1) #有的話 抓這裡 然後條機率 這個 左右都要喔
        # print("看抓的值對不對",kb_cy[ind])
        #這裡的改成 目前的 是後  -1是前喔
        # print("original_indices",original_indices)
        # print("kb_cy[ind]",kb_cy[ind])
        if ind<=len(original_indices)-1 and kb_cy[ind]>0 : #有沒有大於0阿
            # print("近來了")
            # print("ind",ind)
            ka_mi=original_indices[ind-1]
            if len(solution3[ka_mi])==1:
                tmp_index=0
            else:
                tmp_index=solution2[ka_mi]-2 
            if kb_cy[ind]==1 or kb_cy[ind]==3 : #1.3做的是差不多
                if len(solution3[ka_mi][tmp_index])!=1: #先處理前面 如果不是==1 就是999
                    ad_et=0
                    # print("q3_index[ind]",q3_index[ind])
                    # print("q3_index[ind]",q3_index[ind][0])
                    
                    # print("q3_index_mid",q3_index[ind])
                    # print("kb_index[ind]",kb_index[ind])
                    for inde in q3_index[ind-1][-1]: #這是裡面的值
                        if inde==kb_index[ind]:
                            # 真正條q3的地方 索引值
                            break
                        else:ad_et+=1
                    # print("ad_et",ad_et)
                    # print("ad_et",ad_et)
                    # print("s3",solution3[ka_mi][tmp_index])
                    # print("len",len(solution3[ka_mi][tmp_index]))
                    # print("min",min(solution3[ka_mi][tmp_index]))
                    solution3[ka_mi][tmp_index][ad_et]+=min(solution3[ka_mi][tmp_index])-1
                    # print("s3 after",solution3[ka_mi][tmp_index])
                #前面好了
                tmp_index=solution2[original_indices[ind]] #重新賦予值
                if len(solution3[original_indices[ind]][tmp_index])!=1: #再處理後面 如果不是==1 就是999
                    ad_et=0
                    
                    for inde in ka_nt_index[ind-1]: #這是裡面的值
                        if inde==kb_index[ind]:
                            # 真正條q3的地方 索引值
                            break
                        else:ad_et+=1
                    # print("ad_et",ad_et)
                    # print("s3",solution3[original_indices[ind]][tmp_index])
                    # print("len",len(solution3[original_indices[ind]][tmp_index]))
                    # print("min",min(solution3[original_indices[ind]][tmp_index]))
                    if kb_cy[ind]==1:
                        solution3[original_indices[ind]][tmp_index][ad_et]+=(len(solution3[original_indices[ind]][tmp_index])+1)
                    # elif kb_cy[ind]==3: #不用加
                    #     solution3[original_indices[ind]][tmp_index][ad_et]-=(len(solution3[original_indices[ind]][tmp_index])+1)
                    # print("s3 after",solution3[original_indices[ind]][tmp_index])
            #接著是2.4        
            if kb_cy[ind]==2 or kb_cy[ind]==4: #2.4做的是差不多
                # if len(solution3[ka_mi][tmp_index])!=1: #先處理前面 如果不是==1 就是999
                #     ad_et=0
                #     for inde in q3_index[ind][-1]: #這是裡面的值
                #         if inde==kb_index[ind]:
                #             # 真正條q3的地方 索引值
                #             break
                #         else:ad_et+=1
                #     print("近來2.4")
                #     print("ad_et",ad_et)
                #     print("s3",solution3[ka_mi][tmp_index])
                #     print("len",len(solution3[ka_mi][tmp_index]))
                #     print("min",min(solution3[ka_mi][tmp_index]))
                #     solution3[ka_mi][tmp_index][ad_et]+=0.5
                #     print("s3 after",solution3[ka_mi][tmp_index])
                # #前面好了
                #不需要前面 因為吃的是第一個
                tmp_index=solution2[original_indices[ind]] #重新賦予值
                if len(solution3[original_indices[ind]][tmp_index])!=1: #再處理後面 如果不是==1 就是999
                    ad_et=0
                    for inde in ka_nt_index[ind-1]: #這是裡面的值
                        if inde==kb_index[ind]:
                            # 真正條q3的地方 索引值
                            break
                        else:ad_et+=1
                    # print("近來了")
                    # print("ad_et",ad_et)
                    # print("s3",solution3[original_indices[ind]][tmp_index])
                    # print("len",len(solution3[original_indices[ind]][tmp_index]))
                    # print("min",min(solution3[original_indices[ind]][tmp_index]))
                    if kb_cy[ind]==2:
                        solution3[original_indices[ind]][tmp_index][ad_et]+=(len(solution3[original_indices[ind]][tmp_index])+1)
                    # elif kb_cy[ind]==4:
                    #     solution3[original_indices[ind]][tmp_index][ad_et]-=(len(solution3[original_indices[ind]][tmp_index])+1)
                    # print("s3 after",solution3[original_indices[ind]][tmp_index])


                    
                    

            
        #在寫出一下1,2,3,4 要怎麼嘉進so3
        #1.要 舊的+ min-1 新的+len()
        #2.   舊的不用動  新的+len()

        #3.    舊的+ min-1 新的不用動
        #4.    舊的不用動    新的不用動

        #1是 這個循環最後要尾 新的要頭 正常看還有多少get_fi
        #2是 這個循環最後要頭 新的要頭 
        #3是 這個循環最後要尾 新的要尾 正常看還有多少get_fi
        #4是 這個循環最後要頭 新的要尾 

        # print(f"出現數量結果 (counts): {counts}")
        # print(f"出現元素結果 (elements): {elements}")
    # print("q3_index",q3_index)
    # print("q3_hamming",q3_hamming)
    #這一段是在建立q3
    for ind,so1 in enumerate(original_indices):

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

    # print("so3後",solution3)
    # print("route_so",route_so)

    # print("route_gate",route_gate)
    circuit,nope=make_circuit(route_so,route_gate,n) #丟進去生成兩個兩個
    
    return  circuit


def cnt(best_solution):
    a=[]
    # print("best",best_solution)
    # for idx in range(len(best_solution)):
    idx=0
    while idx < len(best_solution)-1:
        # print("best_solution[]",best_solution[idx])
        ind = best_solution[idx].index(3) #抓3的index
        # print("ind",ind)
        tmp=True
        next_i=idx+1 #下一個是索引值
        a_tmp=[]
        a_tmp.append(best_solution[idx]) #先放頭
        while tmp and idx < len(best_solution)-1: #在這裡看 cn n
            # print("dasdad")
            next_3=best_solution[next_i].index(3)
            # print("next3",next_3)
            if ind ==next_3: #
                a_tmp.append(best_solution[next_i])
                next_i += 1 #下一個索引+1
                idx += 1  #前一圈索引值+1 不知道會不會有問題
                
            else:tmp=False
        idx+=1
        # print("idx",idx)
        # print("a_tmp",a_tmp)
        # a_tmp=[[0,0,3],[1,0,3],[0,1,3],[1,1,3]] #4
        # a_tmp=[[0,0,3],[1,0,3],[0,1,3],[1,1,3],[0,0,3],[0,0,3],[1,1,3]] #3個
        # a_tmp=[[0,0,3],[1,0,3],[0,1,3],[1,1,3],[1,0,3],[1,1,3]] #2個
        a_index=[]
        index_three=a_tmp[0].index(3)
        simplified = []

        for item in a_tmp:
            if item in simplified:
                simplified.remove(item)  # 發現重複，立即成對抵消
            else:
                simplified.append(item)  # 沒出現過，先加入

        a_tmp=simplified

        if len(a_tmp)>2:
            
            b_tmp=[[1,0,3],[0,0,3],[1,1,3],[0,1,3]]
            
            for inds,ja in enumerate(a_tmp):
                if ja in b_tmp :
                    # idx = b_tmp.index(ja)
                    b_tmp.remove(ja)
                    a_index.append(inds)

            for i in sorted(a_index, reverse=True):
                a_tmp.pop(i)

            iee=[]
            for ie in range(3):
                if ie!=index_three:
                    iee.append(2)
                else:
                    iee.append(3)
            if len(b_tmp)==0:#代表not
                a.append(iee)
            elif len(b_tmp)==1: #代表not +ccnot
                a.append(iee)
                a.append(b_tmp[0])
                
        elif len(a_tmp)==2:
            ka=a_tmp[0]
            kb=a_tmp[1]
            k_tmp=[]
            k_ct=0 #看會不會有 0,1 1,0的 不能和
            for inx in range(3):
                if ka[inx] == kb[inx]:
                     k_tmp.append(ka[inx])
                else: 
                    k_tmp.append(2)
                    k_ct+=1
            if k_ct==1:
                a.append(k_tmp)
            else:
                a.append(ka)
                a.append(kb)

               
        else:a.append(a_tmp[0])
        
    # print("a",a)

    a_cnt=[]
    for idx in a:
        if idx==[0,2,3]:
            a_cnt.extend([[3,2,2], [1,2,3], [3,2,2]])
        elif idx==[2,0,3]:
            a_cnt.extend([[2,3,2],[2,1,3],[2,3,2]])
        elif idx==[0,3,2]:
            a_cnt.extend([[3,2,2],[1,3,2],[3,2,2]])
        elif idx==[2,3,0]:
            a_cnt.extend([[2,2,3],[2,3,1],[2,2,3]])
        elif idx==[3,0,2]:
            a_cnt.extend([[2,3,2],[3,1,2],[2,3,2]])
        elif idx==[3,2,0]:
            a_cnt.extend([[2,2,3],[3,2,1],[2,2,3]])
        elif idx==[0,0,3]:
            a_cnt.extend([[3,2,2],[2,3,2],[1,1,3],[2,3,2],[3,2,2]])
        elif idx==[0,1,3]:
            a_cnt.extend([[3,2,2],[1,1,3],[3,2,2]])
        elif idx==[1,0,3]:
            a_cnt.extend([[2,3,2],[1,1,2],[2,3,2]])
        elif idx==[0,3,0]:
            a_cnt.extend([[3,2,2],[2,2,3],[1,3,1],[2,2,3],[3,2,2]])
        elif idx==[0,3,1]:
            a_cnt.extend([[3,2,2],[1,3,1],[3,2,2]])
        elif idx==[1,3,0]:
            a_cnt.extend([[2,2,3],[1,3,1],[2,2,3]])
        elif idx==[3,0,0]:
            a_cnt.extend([[2,3,2],[2,2,3],[3,1,1],[2,2,3],[2,3,2]])
        elif idx==[3,0,1]:
            a_cnt.extend([[2,3,2],[3,1,1],[2,3,2]])
        elif idx==[3,1,0]:
            a_cnt.extend([[2,2,3],[3,1,1],[2,2,3]])
        else:
            a_cnt.append(idx)
    # print("a_cnt",a_cnt)
    #相同抵銷
    b_cnn=[]
    while len(a_cnt)>1:
        ka_a=a_cnt[0]
        ka_b=a_cnt[1]
        if ka_a==ka_b:
            a_cnt.pop(1)
            a_cnt.pop(0)
        else:
            b_cnn.append(ka_a)
            a_cnt.pop(0)
    # print("a_cnt",a_cnt)
    b_cnn.append(a_cnt[0])
    # print("bcnn",b_cnn)

    return b_cnn

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
        
        
        
            


    return real_circuit,len(real_circuit)


def factorial_two(n):
    result = 1
    for i in range(1, n + 1):
        result *= i
    
    # numbers = list(range(0, n))
    # permutations = list(itertools.permutations(numbers))
    return result



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
                if i == NumIter and n==3:
                    best_solution=cnt(best_solution)
                    # print(check(aaa,n))
                    # print("aaa",aaa)
                yield f"data: {json.dumps({'total_epochs':NumIter,'epoch':i,'circuit':best_solution})}\n\n"
                
                # print("total_epochs",NumIter)
                # print("epoch",i)
                # print("circuit",best_solution)
                
                
            

# output=[1,2,3,4,5,6,7,0]
# core_algorithm_v1(output,3)