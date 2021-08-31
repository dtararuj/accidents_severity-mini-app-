"ogolna informacja o pakiecie"

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import ipywidgets as widgets
from IPython.display import clear_output

report=pd.read_csv("data/dane_surowe_do_kalkulatora_task7.csv")

# Data dictionary
## Driver age from range

CarAgeDict = {"0 - 2 years": 0,
             "3 - 5 years" : 1,
             "6 - 10 years": 2,
             "11 - 20 years":3,
             "21 - 30 years":4,
             "31 or more years": 5}

## Choose brand from list below
MakeDict = {"Audi": 32,
            "BMW": 34,
            "Chevrolet": 20,
            "Chrysler": 6,
            "Deawoo": 64,
            "Dodge": 7,
            "Ford": 12,
            "Honda": 37,
            "Hyundai":55,
            "Jeep":2,
            "Kia":63,
            "Land Rover":62,
            "Lexus":59,
            "Mercedes":42,
            "Nissan":52,
            "Porsche":45,
            "Saab":47,
            "Subaru":48,
            "Suzuki" :53,
            "Toyota": 49,
            "Volkswagen":30,
            "Volvo" :51,
            "Others": 99}
            
## Sitting position

SeatposDict = {"Next to the driver" :1,
              "Another place":2 }

## DriverAge 

# 4: 17-21 years
# 5: 22-30 years
# 6: 31-50 years
# 7: 51-65 years
# 8: more than 65 years

## plec kierowcy 

DriverSexDict = {"Woman" :2,
                 "Man" :1}

#slider definition
style = {'description_width': '150px'}
layout = {'width': '500px'}

wiek_slider = widgets.IntSlider(value=20, min=16, max=100,  description = "Driver's age",style = style,layout=layout)
def wiek_kierowcy(x):
    przedzial = 0
    if x <=21:
        przedzial = 4
    elif x<=30:
        przedzial = 5
    elif x<=50:
        przedzial = 6
    elif x <=65:
        przedzial = 7
    else:
        przedzial = 8
    return przedzial



#dropdown definition
CarAge = widgets.Dropdown(options = CarAgeDict, description="Car's age:",style = style,layout=layout)
Make= widgets.Dropdown(options = MakeDict, description="Car's brand:",style = style,layout=layout)
Seatpos= widgets.Dropdown(options = SeatposDict, description='Sitting place',style = style,layout=layout)
DriverSex =widgets.Dropdown(options = DriverSexDict,description="Driver's sex",style = style,layout=layout)

#run button definition
run = widgets.Button(description = "Check!",tooltip='Check the result!',icon='search',button_style='info')

out = widgets.Output()
def przycisk(X):
    with out:
        clear_output()
        wiek = wiek_kierowcy(wiek_slider.value)
        wynik = report[(report["CarAge"]==CarAge.value) & (report["MAKE"]==Make.value)  & 
                       (report["SEATPOS"]==Seatpos.value) & (report["DriverSex"]==DriverSex.value) & 
                       (report["DriverAge"]==wiek)]
        print("In this case probability for:","\n",
        "- death: {:.1%}".format(round(wynik.loc[wynik["INJSEV"]==4,"TotalResult"].values[0],2)),"\n",
        "- serious injuries: {:.1%}".format(round(wynik.loc[wynik["INJSEV"]==3,"TotalResult"].values[0],2)),"\n",
        "- light injuries: {:.1%}".format(round(wynik.loc[wynik["INJSEV"]==1,"TotalResult"].values[0],2)),"\n",  
        "- none injuries: {:.1%}".format(round(wynik.loc[wynik["INJSEV"]==0,"TotalResult"].values[0],2)))  


# all in one app

values = {"slider": wiek_slider.value, "option": CarAge.value,"option2": Make.value, "option3": Seatpos.value,"option4":DriverSex}


def gadzety(x,y,a,b,c):
    values["slider"] = x
    values["option"] = y
    values["option2"] = a
    values["option3"] = b
    values["option4"] = c












