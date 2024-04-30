#include <iostream>
#include <string>
#include <list>

#include <curl/curl.h>

#include "common.hpp"

// Callback function to receive response from curl
size_t curlCallback(void *contents, size_t size, size_t nmemb, std::string *output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

std::string getWeatherCondition(const std::string& cityName, const std::string& apiKey) {
    CURL *curl = curl_easy_init();
    std::string response;

    if ( curl ) {
        std::string url = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName + "&appid=" + apiKey;

        // Set the URL
        curl_easy_setopt(curl, CURLOPT_URL, url.c_str());

        // Set the write callback function
        curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, curlCallback);

        // Set the pointer to the response string
        curl_easy_setopt(curl, CURLOPT_WRITEDATA, &response);

        // Perform the request
        CURLcode res = curl_easy_perform(curl);

        // Check for errors
        if (res != CURLE_OK) {
            std::cerr << "curl_easy_perform() failed: " << curl_easy_strerror(res) << std::endl;
        };

        // Cleanup
        curl_easy_cleanup(curl);
    }

    return response;
}

int main() {
    std::cout << "Hello, World!" << std::endl;
    
    for ( const auto& str : keywords_snow ) {
        std::cout << str << std::endl;
    }

    std::string weatherData = getWeatherCondition(cityName, apiKey);
    std::cout << "Weather data for " << cityName << ":\n" << weatherData << std::endl;

    return 0;
}