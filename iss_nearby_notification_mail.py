import requests
import datetime as dt
import smtplib
import time

MY_LAT = 20.1234
MY_LONG = 30.1234

MY_MAIL = "tMY_EMAIL@gmail.com"
MY_PW = "APP_PASSWORD"

response = requests.get(url="http://api.open-notify.org/iss-now.json")
iss_longitude = float(response.json()["iss_position"]["longitude"])
iss_latitude = float(response.json()["iss_position"]["latitude"])
iss_pos = (iss_latitude, iss_longitude)


# if ISS close to my position


def iss_close_to_me():
    response_fun = requests.get(url="http://api.open-notify.org/iss-now.json")
    iss_longitude_fun = float(response_fun.json()["iss_position"]["longitude"])
    iss_latitude_fun = float(response_fun.json()["iss_position"]["latitude"])
    if (iss_latitude_fun - 5) <= MY_LAT <= (iss_latitude_fun + 5) and\
            (iss_longitude_fun - 5) <= MY_LONG <= (iss_longitude_fun + 5):
        print("is close")
        return True


# and currently dark


def is_dark():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }
    response_suntime = requests.get(url="https://api.sunrise-sunset.org/json", params=parameters)
    response_suntime.raise_for_status()
    data = response_suntime.json()["results"]
    sunrise = data["sunrise"]
    sunset = data["sunset"]

    sunrise_hour = int(sunrise.split("T")[1].split(":")[0]) - 2
    sunset_hour = int(sunset.split("T")[1].split(":")[0]) - 2

    now = dt.datetime.now()
    now_hour = now.hour

    if now_hour < sunrise_hour or now_hour > sunset_hour:
        print("is dark")
        return True


# run code every 60 sec
# send me email


while True:
    time.sleep(60)
    if iss_close_to_me() and is_dark():
        print("sending mail")
        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user=MY_MAIL, password=MY_PW)
            connection.sendmail(from_addr=MY_MAIL, to_addrs=MY_MAIL, msg="Subject: ISS nearby notification\n\n"
                                                                         f"with current longitude: "
                                                                         f"{iss_longitude} (your"
                                                                         f"longitude: {MY_LONG}) and latitude: "
                                                                         f"{iss_latitude} (your latitude: "
                                                                         f"{MY_LAT})\nThe"
                                                                         f"ISS could be visible to you right now.")


