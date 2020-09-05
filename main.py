import urllib.request
import json
from tkinter import *
from numpy import round
import sqlite3
import config

# Displaying error
def receivedError(city):
    errorWindow = Toplevel()
    errorLabel = Label(errorWindow, text="Received Error, cannot parse results about " + "'" + city + "'", padx=20, pady=10)
    errorLabel.pack()


# Displaying Weather Information
def displayKelvin(data,dataWindow):
    dataWindow.destroy()  # close the Celsius window
    theJSON = json.loads(data)
    print(theJSON)
    dataWindow = Toplevel()
    dataWindow.title("Weather in " + theJSON["name"])
    dataWindow.geometry("400x300")
    dataWindow.configure(background='white')
    #Widgets
    Label(dataWindow, text="Now : " + str(theJSON["main"]["temp"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    Label(dataWindow, text="Min-temp : " + str(theJSON["main"]["temp_min"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    Label(dataWindow, text="Max-temp : " + str(theJSON["main"]["temp_max"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    
    detailsButton = Button(dataWindow, text="More Details...", font=('Arial', 14, 'bold'), pady=5, command=lambda: displayMoreInformation(data, 'K'))
    detailsButton.pack(pady=10)


def displayCelsius(data):
    theJSON = json.loads(data)
    dataWindow = Toplevel()
    dataWindow.geometry("400x300")
    dataWindow.title("Weather in " + theJSON["name"])
    dataWindow.configure(background='white')
    #Widgets
    Label(dataWindow, text="Now : " + str(round(theJSON["main"]["temp"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    Label(dataWindow, text="Min-temp : " + str(round(theJSON["main"]["temp_min"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    Label(dataWindow, text="Max-temp : " + str(round(theJSON["main"]["temp_max"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'), background='white').pack(pady=10)

    convertKelvinButton = Button(dataWindow, text="Press to convert to Kelvin", font=('Arial', 14, 'bold'), padx=10, pady=5, command=lambda: displayKelvin(data, dataWindow))
    convertKelvinButton.pack()
    detailsButton = Button(dataWindow, text="More Details...", font=('Arial', 14, 'bold'), pady=5, command=lambda: displayMoreInformation(data, 'C'))
    detailsButton.pack(pady=10)


def displayMoreInformation(data, temp):
    theJSON = json.loads(data)
    detailsWindow = Toplevel()
    detailsWindow.title("Details "+theJSON["name"]+" "+temp)
    detailsWindow.geometry("400x300")
    detailsWindow.configure(background='white')
    #Widgets
    Label(detailsWindow, text=theJSON["weather"][0]["main"], font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    Label(detailsWindow, text=theJSON["weather"][0]["description"], font=('Arial', 14, 'bold'),  background='white').pack(pady=10)

    if (temp == 'K'):
        Label(detailsWindow, text="Feels like : " + str(theJSON["main"]["feels_like"])+"K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    else:
        Label(detailsWindow, text="Feels like : " + str(round(theJSON["main"]["feels_like"] - 273.15, 1))+"C", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)

    Label(detailsWindow,text="Pressure : "+str(theJSON["main"]["pressure"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)
    Label(detailsWindow,text="Humidity : "+str(theJSON["main"]["humidity"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)
    Label(detailsWindow,text="Visibility : "+str(theJSON["visibility"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)

def saveSearch(city,data):
    theJSON=json.loads(data)
    conn=sqlite3.connect('searched_cities.db')
    c=conn.cursor()

    #Querry to see how many cities are in db
    c.execute("SELECT * FROM cities")
    cities_list=c.fetchall()


    if(len(cities_list)<=2):
        #Check if already in list
        alreadyInList=0
        for record in cities_list:
            if (record[0].upper()==city.upper()):
                alreadyInList=1
        #INSERT
        if(alreadyInList==0):
            c.execute("INSERT INTO cities VALUES(:name,:temp)",
                        {
                            'name':city,
                            'temp':round(theJSON["main"]["temp"]-273.15,1)
                        })
    else:
        #Check if city already in list
        alreadyInList=0
        for record in cities_list:
            if (record[0].upper()==city.upper()):
                alreadyInList=1

        if (alreadyInList==0):
            #DELETE
            c.execute("DELETE from cities WHERE oid in (select oid from cities limit 1)")
            print("s-a sters ceva")
            #INSERT
            c.execute("INSERT INTO cities VALUES(:name,:temp)",
                    {
                        'name':city,
                        'temp':round(theJSON["main"]["temp"]-273.15,1)
                    })
    conn.commit()
    conn.close()


# Getting Information from api and displaying the weather (opening 2nd window)
def getInfoNameAndDisplay(city):
    myapikey = config.myapikey
    try:
        urlData = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + myapikey
        webUrl = urllib.request.urlopen(urlData)
        if (webUrl.getcode() == 200):
            data = webUrl.read() #Reading JSON data
            displayCelsius(data) #Tkinter App
        else:
            receivedError(city)
    except:
        receivedError(city)
    saveSearch(city,data)

#Gives Info about City from api
def getInfoName(city):
    myapikey = config.myapikey
    try:
        urlData = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + myapikey
        webUrl = urllib.request.urlopen(urlData)
        if (webUrl.getcode() == 200):
            return webUrl.read()
    except:
        print("Connection failed")
    

# Tinker app
def main():
    root = Tk()
    root.title("Live Weather")
    root.geometry("400x400")
    root.configure(background='white')

    # Widgets
    enterCityLabel = Label(root, text="Enter a city", font=('Arial', 12, 'bold'), background='white')
    enterCityLabel.pack(pady=10)

    cityEntry = Entry(root, width=35, font=12, justify='center', borderwidth=2)
    cityEntry.pack(padx=10, pady=10)

    
    #connection to Database
    conn=sqlite3.connect('searched_cities.db')
    c=conn.cursor()
    
    try:
        c.execute("""CREATE TABLE cities(
                    name text,
                    temp real
                )""")
    except:
        #Db Already Created
        c.execute("SELECT * FROM cities")
        cities_list=c.fetchall()
        print(cities_list)

        # Read Current Weather In the saved cities
        for i in range (len(cities_list)):
            cities_list[i]=list(cities_list[i])
            cities_list[i][1]=round(json.loads(getInfoName(cities_list[i][0]))["main"]["temp"]-273.15,1)
        print(cities_list)


        if (len(cities_list)>=1):
            recordLabel1=Button(root,text=cities_list[0][0].capitalize()+" - "+str(cities_list[0][1])+"C", font=('Arial', 12, 'bold'), padx=10, pady=5,command=lambda:getInfoNameAndDisplay(cities_list[0][0]),background='white')
            recordLabel1.pack(pady=10)
        if (len(cities_list)>=2):
            recordLabel2=Button(root,text=cities_list[1][0].capitalize()+" - "+str(cities_list[1][1])+"C",font=('Arial', 12, 'bold'), padx=10, pady=5,command=lambda:getInfoNameAndDisplay(cities_list[1][0]),background='white')
            recordLabel2.pack(pady=10)
        if (len(cities_list)>=3):
            recordLabel3=Button(root,text=cities_list[2][0].capitalize()+" - "+str(cities_list[2][1])+"C",font=('Arial', 12, 'bold'), padx=10, pady=5,command=lambda:getInfoNameAndDisplay(cities_list[2][0]),background='white')
            recordLabel3.pack(pady=10)

        print("Already Created")


    conn.commit()
    conn.close()

    showWeatherButton = Button(root, text="Show Weather", font=('Arial', 12, 'bold'), padx=10, pady=5, command=lambda: getInfoNameAndDisplay(cityEntry.get()), background='white')
    showWeatherButton.pack(pady=20)

    # App Loop
    root.mainloop()


if __name__=="__main__":
    main()
