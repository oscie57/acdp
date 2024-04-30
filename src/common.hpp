#ifndef COMMON_HPP
#define COMMON_HPP

#include <list>
#include <string>

std::string cloudUrl = "https://cloud.oscie.net/acdp";

std::list <std::string> keywords_snow = {
    "snow",
    "blizzard",
    "snowstorm"
};

std::list <std::string> keywords_rain = {
    "rain",
    "mist",
    "shower",
    "drizzle",
    "mist"
};

// CONFIGUATION
// PLEASE FILL THIS INFORMATION OUT IN CONFIG.JSON
std::string apiKey;     // https://openweathermap.org/api
std::string cityName;   // City name for weather
bool roostActive;       // Allows the roost BGM to play randomly
int volume;             // Volume of the audio
std::list selection;    // Game selection

#endif // COMMON_HPP