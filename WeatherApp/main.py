import urllib.request
import json
from tkinter import *
from numpy import round


# Displaying error
def receivedError(city):
    errorWindow = Toplevel()
    errorLabel = Label(errorWindow, text="Received Error, cannot parse results about " + "'" + city + "'", padx=20, pady=10)
    errorLabel.pack()


# Displaying Weather Information
def displayWeather(data):
    theJSON = json.loads(data)
    print(theJSON)
    dataWindow = Toplevel()
    dataWindow.title("Weather in " + theJSON["name"])
    dataWindow.geometry("400x300")
    dataWindow.configure(background='white')
    #Widgets
    actLabel = Label(dataWindow, text="Now : " + str(theJSON["main"]["temp"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    minLabel = Label(dataWindow, text="Min-temp : " + str(theJSON["main"]["temp_min"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    maxLabel = Label(dataWindow, text="Max-temp : " + str(theJSON["main"]["temp_max"]) + "K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    convertCelsiusButton = Button(dataWindow, text="Press to convert to celsius", font=('Arial', 14, 'bold'), padx=10, pady=5, command=lambda: convertToCelsius(data, dataWindow)).pack(pady=20)
    detailsButton = Button(dataWindow, text="More Details...", font=('Arial', 14, 'bold'), pady=5, command=lambda: displayMoreInformation(data, 'K')).pack()


def convertToCelsius(data, dataWindow):
    dataWindow.destroy()  # close the Kelvin window
    theJSON = json.loads(data)
    dataWindow = Toplevel()
    dataWindow.geometry("400x300")
    dataWindow.title("Weather in " + theJSON["name"])
    dataWindow.configure(background='white')
    #Widgets
    actLabel = Label(dataWindow, text="Now : " + str(round(theJSON["main"]["temp"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    minLabel = Label(dataWindow, text="Min-temp : " + str(round(theJSON["main"]["temp_min"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    maxLabel = Label(dataWindow, text="Max-temp : " + str(round(theJSON["main"]["temp_max"] - 273.15, 1)) + "C", font=('Arial', 14, 'bold'), background='white').pack(pady=10)
    detailsButton = Button(dataWindow, text="More Details...", font=('Arial', 14, 'bold'), pady=5, command=lambda: displayMoreInformation(data, 'C')).pack(pady=10)


def displayMoreInformation(data, temp):
    theJSON = json.loads(data)
    detailsWindow = Toplevel()
    detailsWindow.title("Details")
    detailsWindow.geometry("400x300")
    detailsWindow.configure(background='white')
    weatherLabel = Label(detailsWindow, text=theJSON["weather"][0]["main"], font=('Arial', 14, 'bold'),  background='white').pack(pady=10)
    weatherDescrLabel = Label(detailsWindow, text=theJSON["weather"][0]["description"], font=('Arial', 14, 'bold'),  background='white').pack(pady=10)

    if (temp == 'K'):
        feelsLabel = Label(detailsWindow, text="Feels like : " + str(theJSON["main"]["feels_like"])+"K", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)
    else:
        feelsLabel = Label(detailsWindow, text="Feels like : " + str(round(theJSON["main"]["feels_like"] - 273.15, 1))+"C", font=('Arial', 13, 'bold'),  background='white').pack(pady=10)

    pressureLabel=Label(detailsWindow,text="Pressure : "+str(theJSON["main"]["pressure"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)
    humidityLabel=Label(detailsWindow,text="Humidity : "+str(theJSON["main"]["humidity"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)
    visibilityLabel=Label(detailsWindow,text="Visibility : "+str(theJSON["visibility"]), font=('Arial', 14, 'bold'), background='white').pack(pady=10)




# Getting Information from api
def getInfoName(city):
    myapikey = "7795a887929bc1b5db11fe7b05765513"
    try:
        urlData = "http://api.openweathermap.org/data/2.5/weather?q=" + city + "&appid=" + myapikey
        webUrl = urllib.request.urlopen(urlData)
        if (webUrl.getcode() == 200):
            print("AA")
            data = webUrl.read()
            displayWeather(data)
        else:
            receivedError(city)
    except:
        receivedError(city)


# Tinker app
def main():
    root = Tk()
    root.title("Live Weather")
    root.geometry("400x200")
    root.configure(background='white')

    # Widgets
    enterCityLabel = Label(root, text="Enter a city", font=('Arial', 12, 'bold'), background='white')
    enterCityLabel.pack(pady=10)

    cityEntry = Entry(root, width=35, font=12, justify='center', borderwidth=2)
    cityEntry.pack(padx=10, pady=10)

    showWeatherButton = Button(root, text="Show Weather", font=('Arial', 12, 'bold'), padx=10, pady=5, command=lambda: getInfoName(cityEntry.get()), background='white')
    showWeatherButton.pack(pady=20)

    # App Loop
    root.mainloop()


if __name__=="__main__":
    main()
