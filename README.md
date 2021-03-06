# Demo
<img src="https://i.imgur.com/vXJWYF8.jpg" alt="alt text" width="850" height="622">

This app tells users the best hours to go out if they're not planning on driving.

Takes into account the temperature, wind, humidity, sun intensity and chance of precipitation.

The former 4 variables are used to calculate the "Feels-like Temperature". And the last variable is used to guarantee no rain.

Weather data provided by AccuWeather.

# Screenshots
<img src="https://i.imgur.com/jQDNWcm.png">
<img src="https://i.imgur.com/aY9VqID.png">
<img src="https://i.imgur.com/XlNILFV.png">

# For Developers:
Due to security reasons, the API key for AccuWeather is not included in the source code. You must create a `config.ini` file at the root level in the following format:

```ini
[accuweather_api_keys]
key=your_key_here
```

You can get a free AccuWeather API Key here: https://developer.accuweather.com/packages
