# python chits_generator.py
import random


def chit():
    num={}
    num['num10'] =[i for i in range(1,16)]
    num['num20'] =[i for i in range(16,31)]
    num['num30'] =[i for i in range(31,46)]
    num['num40'] =[i for i in range(46,61)]
    num['num50'] =[i for i in range(61,76)]
 
    results ={}
    # target => select 15 numbers
    for key,value in zip(num.keys(),num.values()):
        # 1. select each one from 10 steps (9 done,6 left)
        results[key] = [num[key].pop(num[key].index(random.choice(value)))]

    # 2. while loop to run the program till 15 number will selected and not 3 more then 10 gap
    while len([j for i in results.values() for j in i]) < 15:
        # 1. randomly choice from list of the num list
        key = random.choice(list(num.keys()))
        # 2. check if there is less then 3 else continue
        if len(results[key]) < 3 :
            # randomly choice element and add to the results list and pop from num list
            results[key].append(num[key].pop(num[key].index(random.choice(num[key]))))
        else:
            continue
  
       

    ### arranging in the order of requirement  ####
    chit = [[' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' '],
            [' ',' ',' ',' ',' ']]
    row_c1,row_c2 = [],[]

    # 1. first check if any list have 3 element if true append in chit
    for index,value in enumerate(results.values()):
        if len(value) == 3 :
            key = list(results.keys())[index]
            row_c1.append(key)
            row_c2.append(key)
            for i,item in enumerate(value) :
                chit[i][index] = str(item)
    else :
        # clearing all the done list
        for ele in row_c1:
            del results[ele]
        # complete the first row
        row = 0 # current row
        for i in range(5-len(row_c1)):
            # loop lill new key doesnot found
            while True:
                key = random.choice(list(results.keys()))
                if key not in row_c1 : break
            index = int(list(num.keys()).index(key))
            value = results[key].pop(0)
            row_c1.append(key)
            chit[row][index] = str(value)
            if results[key] == []:
                del results[key]

    # 2. check if any list have 2 element if true append in chit
    for key,value in zip(results.keys(),results.values()) :
        if len(value) == 2 :
            row_c2.append(key)
            index = list(num.keys()).index(key)
            for i,item in enumerate(value,1) :
                chit[i][index] = str(item)
   

        # complete the second row  else :
        # no break else to sort the results lists at last
        row = 1 # current row
        for i in range(5-len(row_c2)):
            # loop till new key doesnot found
            while True:
                key = random.choice(list(results.keys()))
                if key not in row_c2 : break
            index = int(list(num.keys()).index(key))
            value = results[key].pop(0)
            row_c1.append(key)
            chit[row][index] = str(value)
            if results[key] == []:
                del results[key]
   
    # complete the third row
    for key,value in zip(results.keys(),results.values()):   
       

        chit[2][list(num.keys()).index(key)] = str(value[0])
        print(chit)
    for key,value in zip(results.keys(),results.values()):   
       

        chit[3][list(num.keys()).index(key)] = str(value[1])
        print(chit)

    return chit


def save_chits_in_file(how_many_chits=1,number_to_start=1):
	with open("Tambola tickets.txt",'w') as file:
		for i,nu in enumerate([x for x in range(how_many_chits)],number_to_start):
			line1,line2,line3 ,line4,line5= chit()
			file.writelines(f'  	    CARTELA - {i}'+'\n')
			file.writelines(str(line1)+'\n')
			file.writelines(str(line2)+'\n')
			file.writelines(str(line3)+'\n')
			file.writelines(str(line4)+'\n')
           
			file.writelines(str(line5)+'\n')
			file.writelines('\n')

# re = 5
re=int(input('Enter the number of chits require :'))
if re != 0 :
	save_chits_in_file(how_many_chits=re)
else :
	print('no chits saved')
