import smtplib
import requests
import time
from datetime import datetime

MY_LAT = 0.00
MY_LONG = 00.00
#add your co-ordinates

my_email = ""
password = ""
#add your email and password

def position_checker():

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    if MY_LAT + 5 <= iss_latitude <= MY_LAT - 5 and MY_LONG + 5 <= iss_longitude <= MY_LONG - 5:
        return True

def check_if_night():
    parameters = {
        "lat": MY_LAT,
        "lng": MY_LONG,
        "formatted": 0,
    }

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.now().hour
    
    if time_now <= sunrise or time_now >= sunset:
        return True

def send_mail():
    if position_checker() and check_if_night():

        with smtplib.SMTP("smtp.gmail.com") as connection:
            connection.starttls()
            connection.login(user = my_email, password = password)
            connection.sendmail(
                    from_addr = my_email,
                    to_addrs = my_email,
                    msg = "Subject:Look Up\n\nLook up the ISS is here, and the sky is clear"
                    )

while True:
    time.sleep(60)
    send_mail()
