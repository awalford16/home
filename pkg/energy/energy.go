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

type EnergyResults struct {
	Results []MeterReading `json:"results"`
}

type TariffResults struct {
	Results []Tariff `json:"results"`
}

type MeterReading struct {
	Consumption float64 `json:"consumption"`
}

type Tariff struct {
	ValueExcVAT float64 `json:"value_exc_vat"`
	ValueIncVAT float64 `json:"value_inc_vat"`
}

type ElectricityCharges struct {
	StandingCharges Tariff
	StandardUnitRate Tariff
	// DayUnitRate Tariff
	// NightUnitRate Tariff
}

type EnergyProvider struct {
	MPAN string
	SerialNumber string
	Product string
	Tariff string
}

func NewEnergyProvider(mpan string, serialNumber string, product string, tariff string) *EnergyProvider {
	return &EnergyProvider{
		MPAN: mpan,
		SerialNumber: serialNumber,
		Product: product,
		Tariff: tariff,
	}
}

func NewElectricityCharges(standingCharge Tariff, standardUnit Tariff) *ElectricityCharges {
	return &ElectricityCharges{
		StandingCharges: standingCharge,
		StandardUnitRate: standardUnit,
	}
}

func (e *EnergyProvider) GetElectricUsage() float64 {
	client := &http.Client{}

	username := os.Getenv("OCTOPUS_ENERGY_API_KEY")
	url := fmt.Sprintf("https://api.octopus.energy/v1/electricity-meter-points/%s/meters/%s/consumption/", e.MPAN, e.SerialNumber)

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

func (e *EnergyProvider) GetElectricCharges() (*ElectricityCharges, error) {
	client := &http.Client{}

	results := make(map[string]Tariff)
	charges := []string { "standing-charges", "standard-unit-rates" }
	username := os.Getenv("OCTOPUS_ENERGY_API_KEY")

	for _, charge := range charges {
		url := fmt.Sprintf("https://api.octopus.energy/v1/products/%s/electricity-tariffs/%s/%s/", e.Product, e.Tariff, charge)

		req, err := http.NewRequest("GET", url, nil)
		req.Header.Add("Authorization","Basic " + basicAuth(username,"")) 
		resp, err := client.Do(req)
		if err != nil {
			fmt.Println("Error getting tariffs:", err)
			return nil, err
		}
		defer resp.Body.Close()

		var result TariffResults
		err = json.NewDecoder(resp.Body).Decode(&result)
		if err != nil {
			fmt.Println("Error: ", err)
			return nil, err
		}

		results[charge] = result.Results[0]
	}

	return NewElectricityCharges(results["standing-charges"], results["standard-unit-rates"]), nil
}
