import pandas as pd
import numpy as np

# Load data
occupants=pd.read_csv("data/occupants.csv")
accidents=pd.read_csv("data/accidents.csv")
vehicles=pd.read_csv("data/vehicles.csv")

# 1. We add age of car
vehicles["CarAge"] = np.where((vehicles.YEAR - vehicles.MODELYR) < 0, 0,vehicles.YEAR - vehicles.MODELYR)

# 2. We want to focus only on typical city cars, so we need to skip another types.
vehicles=vehicles[vehicles["BODYTYPE"].isin([0,5])]

# 3. We merge our table to get another necessery information about passagers
tabela=vehicles.merge(occupants, on = ["CASEID","PSU","YEAR"])

# 4.Skip unknown injuries
tabela = tabela[tabela["INJSEV"]!=5]
                
# 5. Let's group injuries
przypisanie = [(tabela.INJSEV == 0),
               (tabela.INJSEV == 1) | (tabela.INJSEV == 2),
               (tabela.INJSEV == 3),
               (tabela.INJSEV == 4) | (tabela.INJSEV == 6)]

co_przypisac = [0,1,3,4]

tabela["INJSEV"] = np.select(przypisanie, co_przypisac)

# 0: none injuries
# 1: (1,2) light injuries
# 3: (3) serious injuries
# 4: (4,6) death

# 6 let's delete NAs
tab0=tabela.dropna(subset=["MODELYR"])

# 7 Let's group car age
warunek = [
    (tab0.CarAge <= 2),
    (tab0.CarAge <= 5) & (tab0.CarAge >2),
    (tab0.CarAge <= 10) & (tab0.CarAge >5),
    (tab0.CarAge <= 20) & (tab0.CarAge >10),
    (tab0.CarAge <= 30) & (tab0.CarAge >20),
    (tab0.CarAge > 30)
]

wartosc = range(6)

tab0["CarAge"] = np.select(warunek, wartosc)

# 0 - 2 years (0)
# 3 - 5 years (1)
# 6 - 10 years (2)
# 11- 20 years (3)
# 21 -30 years (4)
# 31 years or more (5)


# **Main analisis**

#1 Car age impact on severity of the injury
#let's delete NAs
tab=tab0.dropna(subset=["INJSEV"])

# I choose only usefull columns and i will count probability of each injury depend od car age.
pom1=tab.groupby(["CarAge"])["PSU"].count().to_frame().reset_index()
pom2=tab.groupby(["CarAge","INJSEV"])["PSU"].count().to_frame().reset_index()

# Let's change columns name
pom2.rename(columns={'PSU':'NoAccidents'},inplace = True)
pom1.rename(columns={"PSU":'NoAccPerGroup'}, inplace = True )

# Let's join both tables and count ratio
zbiorcza=pom2.merge(pom1, on = "CarAge")
zbiorcza["ratio"] = zbiorcza.NoAccidents/zbiorcza.NoAccPerGroup
CarAgeResult = zbiorcza.groupby(["CarAge","INJSEV"])["ratio"].mean().to_frame().reset_index()

# We have calculated the probability of a given injury in an accident due to the age of the car. 

#2 impact of car brand on the severity of injuries
#remove NA values from the MAKE (brand) column
tab2=tabela.dropna(subset=["MAKE"])

#adds brands that appeared less than 300 times to the other group, i.e. 99

tab2["MAKE"]=np.where(tab2["MAKE"].isin([13,19,22,31,38,84,50,43,60,33,29,1,82,25,36,67,65,10,69,3,14,18,23,24,54,58,9,21]),99, tab2["MAKE"])

#I select only those columns that I need and I do 2 groupings to calculate the damage scales for a given car brand (ratio)
pom11=tab2.groupby(["MAKE"])["PSU"].count().to_frame().reset_index()
pom22=tab2.groupby(["MAKE","INJSEV"])["PSU"].count().to_frame().reset_index()

# Let's change the name of the columns
pom22.rename(columns={'PSU':'NoAccidents'},inplace = True)
pom11.rename(columns={"PSU":'NoAccPerGroup'}, inplace = True )

# let's join both auxiliary tables and calculate the ratio
zbiorcza2=pom22.merge(pom11, on = "MAKE")
zbiorcza2["ratio"] = zbiorcza2.NoAccidents/zbiorcza2.NoAccPerGroup
MakeResult= zbiorcza2.groupby(["MAKE","INJSEV"])["ratio"].mean().to_frame().reset_index()

# In next step we check the impact of sitting place on the severity of injury in case of accident.

#3 the impact of sitting place on the severity of injury
#let's delete NAs
tab3=tabela.dropna(subset=["SEATPOS"])

#I select only those columns that I need and I do 2 groupings to calculate the damage scales for a given sitting place (ratio)
pom111=tab3.groupby(["SEATPOS"])["PSU"].count().to_frame().reset_index()
pom222=tab3.groupby(["SEATPOS","INJSEV"])["PSU"].count().to_frame().reset_index()

# Let's change the name of the columns
pom222.rename(columns={'PSU':'NoAccidents'},inplace = True)
pom111.rename(columns={"PSU":'NoAccPerGroup'}, inplace = True )

# let's join both auxiliary tables and calculate the ratio
zbiorcza3=pom222.merge(pom111, on = "SEATPOS")
zbiorcza3["ratio"] = zbiorcza3.NoAccidents/zbiorcza3.NoAccPerGroup
SeatposResult = zbiorcza3.groupby(["SEATPOS","INJSEV"])["ratio"].mean().to_frame().reset_index()

# In this part we will check the impact of driver's age.

#4 the impact of driver's age on the severity of injuries
# first let's filter only drivers
drivers = occupants.loc[occupants["ROLE"]==1,["CASEID","PSU","YEAR","ROLE", "AGE"]]

# let's delete NAs
AgePerCase= drivers.dropna(subset=["AGE"])

# I will take only first driver from accidents where were more than one car
AgePerCase_1= AgePerCase[AgePerCase.duplicated(keep= "first",subset=["CASEID","PSU","YEAR"])]
AgePerCase_1= AgePerCase[["CASEID","PSU","YEAR","AGE"]]

#for accidents without duplicates i take everything
AgePerCase_2= AgePerCase[AgePerCase.duplicated(keep= False,subset=["CASEID","PSU","YEAR"])]
AgePerCase_2= AgePerCase[["CASEID","PSU","YEAR","AGE"]]

AgePerCase = AgePerCase_1.append(AgePerCase_2)

# I will match age of driver to the particular accident
passagers = tabela.loc[tabela["ROLE"]==2,["CASEID","PSU","YEAR","ROLE","INJSEV"]].drop_duplicates()
tab4 = passagers.merge(AgePerCase, on = ["CASEID","PSU","YEAR"], how ='left').drop_duplicates().dropna()
tab4.rename(columns = {"AGE": "DriverAge"},inplace = True)

# I will delete accidents which was not typical and when driver was younger than 16.
tab4 = tab4[(tab4["DriverAge"]>3) & (tab4["DriverAge"]<9)]

# Let's choose only those columns which i need, and let's make two groupings, to calculate the scale of injuries within the age of the driver of a given accident (ratio)
pom1111=tab4.groupby(["DriverAge"])["PSU"].count().to_frame().reset_index()
pom2222=tab4.groupby(["DriverAge","INJSEV"])["PSU"].count().to_frame().reset_index()

# Let's change the name of the columns
pom2222.rename(columns={'PSU':'NoAccidents'},inplace = True)
pom1111.rename(columns={"PSU":'NoAccPerGroup'}, inplace = True )

# let's join both auxiliary tables and calculate the ratio
zbiorcza4=pom2222.merge(pom1111, on = "DriverAge")
zbiorcza4["ratio"] = zbiorcza4.NoAccidents/zbiorcza4.NoAccPerGroup
DriverAgeResult = zbiorcza4.groupby(["DriverAge","INJSEV"])["ratio"].mean().to_frame().reset_index()


# In this part we will check the impact of driver's sex.

#5 Driver's sex impact on severity of the accident
#  first let's filter only drivers
drivers1 = occupants.loc[occupants["ROLE"]==1,["CASEID","PSU","YEAR","ROLE", "SEX"]]

# let's delete NAs
SexPerCase = drivers1.dropna(subset=["SEX"])

# I will take only first driver from accidents where were more than one car
SexPerCase_1= SexPerCase[SexPerCase.duplicated(keep = "first",subset=["CASEID","PSU","YEAR"])]
SexPerCase_1= SexPerCase[["CASEID","PSU","YEAR","SEX"]]

#for accidents without duplicates i take everything
SexPerCase_2= SexPerCase[SexPerCase.duplicated(keep= False,subset=["CASEID","PSU","YEAR"])]
SexPerCase_2= SexPerCase[["CASEID","PSU","YEAR","SEX"]]

SexPerCase = SexPerCase_1.append(SexPerCase_2)

# I will match  driver's sex to the particular accident
passagers1 = tabela.loc[tabela["ROLE"]==2,["CASEID","PSU","YEAR","ROLE","INJSEV"]].drop_duplicates()
tab5 = passagers.merge(SexPerCase, on = ["CASEID","PSU","YEAR"], how ='left').drop_duplicates().dropna()
tab5.rename(columns = {"SEX": "DriverSex"},inplace = True)

#i will assign pregnant woman as woman
tab5["DriverSex"] = np.where(tab5["DriverSex"]==3,2,tab5["DriverSex"])

#I select only the columns that I need and I do 2 groupings to calculate the injury scales for the driver's sex in a given accident (ratio) 
pom11111=tab5.groupby(["DriverSex"])["PSU"].count().to_frame().reset_index()
pom22222=tab5.groupby(["DriverSex","INJSEV"])["PSU"].count().to_frame().reset_index()

# Let's change the name of the columns
pom22222.rename(columns={'PSU':'NoAccidents'},inplace = True)
pom11111.rename(columns={"PSU":'NoAccPerGroup'}, inplace = True )

# let's join both auxiliary tables and calculate the ratio
zbiorcza5=pom22222.merge(pom11111, on = "DriverSex")
zbiorcza5["ratio"] = zbiorcza5.NoAccidents/zbiorcza5.NoAccPerGroup
DriverSexResult = zbiorcza5.groupby(["DriverSex","INJSEV"])["ratio"].mean().to_frame().reset_index()

# **I will check cumulative probability**

# 1. list of options
## Car age from the range
# for example: 
CarAge = 3

# 0: 0 - 2 years 
# 1: 3 - 5 years 
# 2: 6 - 10 years 
# 3: 11-20 years
# 4: 21 -30 years 
# 5: 31 years or more 

## car brand from below
MAKE = 7

# 2 Jeep
# 6 Chrysler
# 7 Dodge
# 12 Ford
# 13 Lincoln
# 19 Cadillac
# 20 Chevrolet
# 22 Pontiac
# 30 Volkswagen
# 32 Audi
# 34 Bmw
# 35 Nissan/Datsun
# 37 Honda
# 38 Isuzu
# 42 Mercedes Benz
# 45 Porsche
# 47 Saab
# 48 Subaru
# 49 Toyota
# 51 Volvo
# 52 Mitsubishi
# 53 Suzuki
# 55 Hyundai
# 59 Lexus
# 62 Land Rover
# 63 Kia
# 64 Daewoo
# 99 OTHER

## sitting place of passager

SEATPOS = 1

# 1: z przodu obok kierowcy, next to driver
# 2: another place

## driver age from the range

DriverAge = 8

# 4: 17-21 years
# 5: 22-30 years
# 6: 31-50 years
# 7: 51-65 years
# 8: more than 66 years

## friver age

DriverSex = 2

# 1: man
# 2: woman

#2. aggregate probability calculator
## car age
R1 = CarAgeResult.loc[CarAgeResult["CarAge"]== CarAge,["INJSEV","ratio"]].set_index("INJSEV")


## car brand
R2 = MakeResult.loc[MakeResult["MAKE"]==MAKE,["INJSEV","ratio"]].set_index("INJSEV")

## sitting place
R3 = SeatposResult.loc[SeatposResult["SEATPOS"]==SEATPOS,["INJSEV","ratio"]].set_index("INJSEV")

## driver's age
R4 = DriverAgeResult.loc[DriverAgeResult["DriverAge"]==DriverAge,["INJSEV","ratio"]].set_index("INJSEV")

## driver's sex
R5 = DriverSexResult.loc[DriverSexResult["DriverSex"]==DriverSex,["INJSEV","ratio"]].set_index("INJSEV")


#3. results
wynik = (R1 + R2 + R3 + R4 + R5)/5
wynik


#4. Summary

report = CarAgeResult.merge(MakeResult, how = "outer", on = "INJSEV").merge(SeatposResult,how = "outer",on = "INJSEV").merge(DriverAgeResult,how = "outer",on = "INJSEV").merge(DriverSexResult,how = "outer",on = "INJSEV")

report.columns = ['CarAge', 'INJSEV', 'ratio_CarAge', 'MAKE', 'ratio_MAKE', 'SEATPOS', 'ratio_SEATPOS',
       'DriverAge', 'ratio_DriverAge', 'DriverSex', 'ratio_DriverSex']

report["TotalResult"] = (report["ratio_CarAge"] + report["ratio_MAKE"] + report["ratio_SEATPOS"] + report["ratio_DriverAge"] + report["ratio_DriverSex"])/5

report = report[report.columns[[1,0,3,5,7,9,11]]]


report.to_csv("data/dane_surowe_do_kalkulatora_task7.csv",index = False)

