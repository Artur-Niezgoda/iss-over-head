import requests
from datetime import datetime
import time as t
import smtplib

MY_LAT = 41.224150  # Your latitude
MY_LONG = 1.725570  # Your longitude
MY_EMAIL = "********@gmail.com"  # Your Email
PASSWORD = "*******************"  # the 16 code generated (for gmail)


def is_iss_overhead() -> bool:
    """
    Check if ISS station is close to the given coordinates.
    :return: return True if ISS station is in 5 degree radius of given coordinates
    """

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return MY_LONG-5 < iss_longitude < MY_LONG+5 and MY_LAT-5 < iss_latitude < MY_LAT+5


def is_it_dark_yet() -> bool:
    """
    Check if it is after sunset but before sunrise
    :return: True if it is at least an hour later or earlier than the hour of sunset or sunrise, respectively
    """

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

    time_now = datetime.utcnow().hour

    return sunset < time_now or time_now < sunrise


can_i_see_it = False

while not can_i_see_it:
    can_i_see_it = (is_iss_overhead() and is_it_dark_yet())
    if can_i_see_it:
        with smtplib.SMTP("smtp.gmail.com", 587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, PASSWORD)
            connection.sendmail(
                from_addr=MY_EMAIL,
                to_addrs=MY_EMAIL,
                msg="Subject: Look Up👆🏼\n\nThe ISS is above you in the sky!".encode("utf8")
            )
        print("An email has been sent")
        break
    t.sleep(60)



