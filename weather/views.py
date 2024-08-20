from django.shortcuts import render
import requests

# Utility function to convert Kelvin to Celsius and truncate to an integer
def kelvin_to_celsius(temp_k):
    return int(temp_k - 273.15)

def weather(request):
    data = {}
    if request.method == 'POST':
        city = request.POST.get('city')
        if city:
            # Directly use the provided API key
            api_key = "e2afbf395718c9ddfad22429e3b24536"

            # Fetch city weather data from OpenWeatherMap API (current weather API)
            weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
            
            try:
                # Get city weather data
                response = requests.get(weather_url)
                response.raise_for_status()
                weather_data = response.json()

                # Process and format the data
                data = {
                    "city": city,
                    "country_code": weather_data['sys']['country'],
                    "coordinate": f"{weather_data['coord']['lat']}, {weather_data['coord']['lon']}",
                    "temp": kelvin_to_celsius(weather_data['main']['temp']),
                    "humidity": weather_data['main']['humidity'],
                    "weather_description": weather_data['weather'][0]['description'],
                    "daily_temp": []  # Since we're not using the One Call API, we can't fetch daily temperatures
                }
            except requests.HTTPError as e:
                data['error'] = f"Error fetching data: {str(e)}"
            except KeyError as e:
                data['error'] = f"Unexpected response structure: {str(e)}"
            except requests.RequestException as e:
                data['error'] = f"Request failed: {str(e)}"
        else:
            data['error'] = 'City name is required.'
    else:
        # Initialize data for GET request or after a POST request without a city
        data = {
            "city": None,
            "country_code": None,
            "coordinate": None,
            "temp": None,
            "humidity": None,
            "weather_description": None,
            "daily_temp": [],
            "error": None
        }

    return render(request, "weather.html", data)
