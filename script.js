const AREA = "Chester, England";
const VOLUME = 0.5;
const ROOST = true;

const URL = "https://cloud.oscie.net/acdp";


async function getGameList(cloudUrl) {
    try {
        const response = await fetch(`${cloudUrl}/list.json`, { timeout: 10000 });
        games = await response.json();

        return games;
    } catch (error) {
        alert("Failed to fetch game list: " + error);

        return [];
    }
}

async function getWeather()