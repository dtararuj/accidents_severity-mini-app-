import pandas as pd
import math

df=pd.read_csv("data/database.csv")


#Delete useless columns:
df.drop(columns=["Unnamed: 0","HOSPSTAY",'DOF1', 'GAD1','DVEST', 
                 'DVBASIS','BAGDEPLY','BAGFAIL','CASENO','MANAVAIL', 'MANFAIL', 'TREATMNT','DEATH'
                ],inplace = True)

# We need to create 3 small tables to make our calculations easier to apply.

occupants = df[["CASEID", 'PSU','YEAR','AGE', 'BAGAVAIL','CHTYPE', 'HEIGHT', 'INJSEV',
       'MANUSE', 'OCCNO', 'ROLE', 'SEATPOS', 'SEX', 'WEIGHT']]


occupants.drop_duplicates(subset=["CASEID", 'PSU','YEAR','AGE', 'BAGAVAIL','CHTYPE', 'HEIGHT', 'INJSEV',
       'MANUSE', 'OCCNO', 'ROLE', 'SEATPOS', 'SEX', 'WEIGHT'],inplace=True, ignore_index=True)

vehicles= df[['CASEID', 'PSU','YEAR','BODYTYPE', 'MAKE' , 'DVTOTAL','MODELYR']]

vehicles.drop_duplicates(subset=['CASEID', 'PSU','YEAR','BODYTYPE', 'MAKE' , 'DVTOTAL','MODELYR'],inplace=True, ignore_index=True)

accidents = df[['CASEID', 'PSU', 'YEAR','STRATIF']]

accidents.drop_duplicates(subset=['CASEID', 'PSU', 'YEAR','STRATIF'], inplace =True, ignore_index=True)

# Next step is to group data in some columns:

# Column HEIGHT

Height_new=[]
for i in occupants['HEIGHT']:
    if i>=0 and i<=80:
        Height_new.append(1)
    elif i>=81 and i<=120:
        Height_new.append(2)
    elif i>=121 and i<=150:
        Height_new.append(3)
    elif i>=151 and i<=175:
        Height_new.append(4)
    elif i>=176 and i<=190:
        Height_new.append(5)
    elif i>=191:
        Height_new.append(6)
    elif math.isnan(i):
        Height_new.append(None)

occupants['HEIGHT']=Height_new


# Column CHTYPE

Chtype_new=[]

for i in occupants['CHTYPE']:
    if i==0:
        Chtype_new.append(0)
    elif i>=1 and i<=8:
        Chtype_new.append(1) 
    elif math.isnan(i):
        Chtype_new.append(None)


occupants['CHTYPE']=Chtype_new

# Column BAGAVAIL

Bagavail_new=[]

for i in occupants['BAGAVAIL']:
    if i==0 or i==2 or i==3:
        Bagavail_new.append(0) 
    elif i==1:
        Bagavail_new.append(1) 
    elif math.isnan(i):
        Bagavail_new.append(None)


occupants['BAGAVAIL']=Bagavail_new

# Column AGE:

Age_new=[]

for i in occupants['AGE']:
    if i>=0 and i<=3:
        Age_new.append(1)
    elif i>=4 and i<=7:
        Age_new.append(2)
    elif i>=8 and i<=12:
        Age_new.append(3)
    elif i>=13 and i<=16:
        Age_new.append(4)
    elif i>=17 and i<=21:
        Age_new.append(5)
    elif i>=22 and i<=30:
        Age_new.append(6)
    elif i>=31 and i<=50:
        Age_new.append(7)
    elif i>=51 and i<=65:
        Age_new.append(8)
    elif i>=66:
        Age_new.append(9)
    elif math.isnan(i):
        Age_new.append(None)


occupants['AGE']=Age_new

# Grouping function definition:

def classify_value(input_value,mappings): 
    
    for mark,values in  mappings.items():
        if input_value in values: 
            return mark 
         
    return None

x = float('nan')
math.isnan(x)

# Column bodytype

bodytype_mappings = {0:[1,2,3,4,5,6,7,8,9,17],                                       # osobowy
                          1:[61,62,63,64,69,74,78,79],                               # ciezarowka 
                          2:[24,25,28,50,58,59,60],                                  # busy   
                          3:[10,40,41,45,48],                                        # dostawcze 
                          4:[65,68,67,70,80,81,82,89,90],                            # motory&quady
                          5:[12, 14, 15, 16, 19, 20, 21, 22, 29, 30, 31, 32, 33,39], # większe samochody osobowe
                          6:[92, 93, 97, 42, 23, 11]}                                # pozostale 
    

vehicles["BODYTYPE"] = vehicles["BODYTYPE"].apply(classify_value,mappings=bodytype_mappings)

# column STRATIF 

stratif_mappings =       {0:['A','B'], # smiertelne obrażenia
                          1:['J','K'], # poważne obrażenia – hospitalizowany (min. 1noc)
                          2:['C','D'], #  poważne obrażenia – nie hospitalizowany
                          3:['E','F'], # niewielkie obrażenia, ale przewieziony do szpitala
                          4:['G','H']} # niewielkie obrażenia


accidents["STRATIF"] = accidents["STRATIF"].apply(classify_value,mappings=stratif_mappings)

# column SEX
SEX_new=[]

for i in occupants['SEX']:
    if i==1:
        SEX_new.append(1)
    elif i==2:
        SEX_new.append(2)
    elif i>=3:
        SEX_new.append(3)
    elif math.isnan(i):
        SEX_new.append(None)

occupants['SEX'] = SEX_new

# column WEIGHT

WEIGHT_new=[]

for i in occupants['WEIGHT']:
    if i>=0 and i<=20:
        WEIGHT_new.append(1)
    elif i>=21 and i<=40:
        WEIGHT_new.append(2)
    elif i>=41 and i<=60:
        WEIGHT_new.append(3)
    elif i>=61 and i<=80:
        WEIGHT_new.append(4)
    elif i>=81 and i<=100:
        WEIGHT_new.append(5)
    elif i>100:
        WEIGHT_new.append(6)
    elif math.isnan(i):
        WEIGHT_new.append(None)

occupants['WEIGHT'] = WEIGHT_new

#Columns SEATPOS

SEATPOS_new=[]

for i in occupants['SEATPOS']:
    if i>=11 and i<=15:
        SEATPOS_new.append(1)
    elif i>=18:
        SEATPOS_new.append(2)
    elif math.isnan(i):
        SEATPOS_new.append(None)

occupants['SEATPOS'] = SEATPOS_new

#Column ROLE

ROLE_new=[]
for i in occupants['ROLE']:
    if i==1:
        ROLE_new.append(1)
    elif i==2:
        ROLE_new.append(2)
    elif math.isnan(i):
        ROLE_new.append(None)

occupants['ROLE'] = ROLE_new

#Column MANUSE

MANUSE_new=[]

for i in occupants['MANUSE']:
    if i>=0 and i<=1:
        MANUSE_new.append(1)
    elif i>=2 and i<=18:
        MANUSE_new.append(2)
    elif math.isnan(i):
        MANUSE_new.append(None)

occupants['MANUSE'] = MANUSE_new

# Create new tables:
occupants.to_csv("data/occupants.csv", index = False)
accidents.to_csv("data/accidents.csv", index = False)
vehicles.to_csv("data/vehicles.csv", index = False)

