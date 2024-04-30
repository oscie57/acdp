#include <iostream>
#include <fstream>
#include <string>
#include <list>
#include <csignal> // Include for signal handling

#include <curl/curl.h>

#include "nlohmann/json.hpp"
#include "common.hpp"

using json = nlohmann::json;

// Global variable to indicate whether a keyboard interrupt occurred
volatile sig_atomic_t keyboardInterrupt = 0;

// Signal handler function for SIGINT (Ctrl+C)
void signalHandler(int signal) {
    if (signal == SIGINT) {
        keyboardInterrupt = 1; // Set the flag to indicate a keyboard interrupt
    }
}

// Function to read from the configuration file
void readConfigFile() {
    std::ifstream configFile("config.json");
    if (!configFile.is_open()) {
        std::cerr << "Error: Failed to open config file." << std::endl;
        exit(EXIT_FAILURE); // Terminate the program with a failure exit code
    }

    json configJson;

    try {
        configFile >> configJson;

        if (configJson.contains("apiKey")) {
            apiKey = configJson["apiKey"];
        } else {
            std::cerr << "Warning: 'apiKey' not found in config file." << std::endl;
             exit(EXIT_FAILURE); // Terminate the program with a failure exit code
        }

        if (configJson.contains("cityName")) {
            cityName = configJson["cityName"];
        } else {
            std::cerr << "Warning: 'cityName' not found in config file." << std::endl;
            exit(EXIT_FAILURE); // Terminate the program with a failure exit code
        }

        if (configJson.contains("roostActive")) {
            roostActive = configJson["roostActive"];
        } else {
            std::cerr << "Warning: 'roostActive' not found in config file." << std::endl;
            exit(EXIT_FAILURE); // Terminate the program with a failure exit code
        }

        if (configJson.contains("volume")) {
            volume = configJson["volume"];
        } else {
            std::cerr << "Warning: 'volume' not found in config file." << std::endl;
            exit(EXIT_FAILURE); // Terminate the program with a failure exit code
        }

        if (configJson.contains("selection")) {
            selection = configJson["selection"];
        } else {
            std::cerr << "Warning: 'selection' not found in config file." << std::endl;
            exit(EXIT_FAILURE); // Terminate the program with a failure exit code
        }
    } catch (const std::exception& e) {
        std::cerr << "Error: Failed to parse config file. " << e.what() << std::endl;
        exit(EXIT_FAILURE); // Terminate the program with a failure exit code
    }

    configFile.close();
}

// Callback function to receive response from curl
size_t curlCallback(void *contents, size_t size, size_t nmemb, std::string *output) {
    size_t totalSize = size * nmemb;
    output->append((char*)contents, totalSize);
    return totalSize;
}

/*
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
*/

std::string getCurrentHour() {
    time_t now = time(0);
    tm *ltm = localtime(&now);

    std::string hour = std::to_string(ltm->tm_hour);

    if (hour.length() == 1) {
        hour = "0" + hour;
    }

    return hour;
}

void programBoot() {
    std::cout << "Welcome to the Animal Crossing Dynamic Player!\nThe ACDP lets you listen to Animal Crossing games' music based around the weather and time around you.\n" << std::endl;
    std::cout << "This is a BETA version of the Animal Crossing Dynamic Player, created for network streaming in C++.\nThere may be bugs, and playback may occasionally break due to external factors.\nIf this happens, please let me know in my Discord server (https://discord.ggymb84qM54A) in #acdp,\nor create an issue on GitHub (https://github.com/oscie57/acdp/issues).\n" << std::endl;
}

int main() {
    std::signal(SIGINT, signalHandler);
    readConfigFile();

    json games; // requests.get(f"https://cloud.oscie.net/acdp/list.json", timeout=10).json()

    while (!keyboardInterrupt) {
        programBoot();
    }

    int playcount = 0;

    std::cout << "\n\nExiting program...\n" << std::endl;
    std::cout << "While using this app, you listened to the music " << playcount << " times!" << std::endl;
    std::cout << "You also listened for " << "timer.elapsed()" << " seconds! (" << "timer.elapsed() / 60" << " minutes)" << std::endl;

    return EXIT_SUCCESS;


    /*
    for ( const auto& str : keywords_snow ) {
        std::cout << str << std::endl;
    }
    */

    /*
    std::string weatherData = getWeatherCondition(cityName, apiKey);
    std::cout << "Weather data for " << cityName << ":\n" << weatherData << std::endl;
    */

    std::cout << apiKey << std::endl;

    std::string currentHour = getCurrentHour();
    std::string weatherData = "Mist";

    std::cout << "Current hour: " << currentHour << std::endl;

    return 0;
}