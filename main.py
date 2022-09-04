import requests
from datetime import datetime


MY_LAT = 41.224150 # Your latitude
MY_LONG = 1.725570 # Your longitude


def is_iss_overhead() -> bool:
    """
    Check if ISS station is close to the given coordinates.
    :return: boolean, return True if ISS station is in 5 degree radius of given coordinates
    """

    response = requests.get(url="http://api.open-notify.org/iss-now.json")
    response.raise_for_status()
    data = response.json()

    iss_latitude = float(data["iss_position"]["latitude"])
    iss_longitude = float(data["iss_position"]["longitude"])

    return MY_LONG-5 < iss_longitude< MY_LONG+5 and MY_LAT-5 < iss_latitude < MY_LAT+5


parameters = {
    "lat": MY_LAT,
    "lng": MY_LONG,
    "formatted": 0,
}


def is_it_dark_yet():
    """
    Check if it is after sunset but before sunrise
    :return: boolean, True if it is at least an hour later or earlier than the hour of sunset or sunrise, respectively
    """

    response = requests.get("https://api.sunrise-sunset.org/json", params=parameters)
    response.raise_for_status()
    data = response.json()
    sunrise = int(data["results"]["sunrise"].split("T")[1].split(":")[0])
    sunset = int(data["results"]["sunset"].split("T")[1].split(":")[0])

    time_now = datetime.utcnow()

    return sunset < time_now or time_now < sunrise


#If the ISS is close to my current position
# and it is currently dark
# Then send me an email to tell me to look up.
# BONUS: run the code every 60 seconds.



