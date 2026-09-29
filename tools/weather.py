import requests
def weather(city: str):

    url = f"https://wttr.in/{city}?format=j1"
    try:
        
        response = requests.get(url, timeout=10)
        print(response.status_code)
        

        data = response.json()

        current = data["current_condition"][0]

        temperature = current["temp_C"]
        feels_like = current["FeelsLikeC"]
        condition = current["weatherDesc"][0]["value"]

        return (
            f"Weather in {city}: "
            f"{condition}, "
            f"{temperature}°C, "
            f"feels like {feels_like}°C"
        )
    except:
        print(response.status_code)
        return (
                f"Can't Found Weather in {city}: "
                f"Can't Found {condition}, "
                f" Can't Found{temperature}°C, "
                f"Can't Found  {feels_like}°C"
                )
