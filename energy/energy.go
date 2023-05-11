package energy

import (
	"fmt"
	"net/http"
	"os"
	"encoding/base64"
	"encoding/json"
)

func basicAuth(username, password string) string {
	auth := username + ":" + password
	return base64.StdEncoding.EncodeToString([]byte(auth))
}
  
func redirectPolicyFunc(req *http.Request, via []*http.Request) error{
	req.Header.Add("Authorization","Basic " + basicAuth("username1","password123"))
	return nil
}

type EnergyResults struct {
	Results []MeterReading `json:"results"`
}

type MeterReading struct {
	Consumption float64 `json:"consumption"`
}

func GetElectricUsage() float64 {
	client := &http.Client{}

	username := os.Getenv("OCTOPUS_ENERGY_API_KEY")
	mpan := os.Getenv("METER_MPAN")
	serialNumber := os.Getenv("METER_SERIAL_NUMBER")

	url := fmt.Sprintf("https://api.octopus.energy/v1/electricity-meter-points/%s/meters/%s/consumption/", mpan, serialNumber)

	req, err := http.NewRequest("GET", url, nil)
	req.Header.Add("Authorization","Basic " + basicAuth(username,"")) 
	resp, err := client.Do(req)
	if err != nil {
		fmt.Println("Error getting electrical usage:", err)
		return 0
	}
	defer resp.Body.Close()

    var results EnergyResults
    err = json.NewDecoder(resp.Body).Decode(&results)
    if err != nil {
        fmt.Println("Error: ", err)
        return 0
    }

	return results.Results[0].Consumption
}