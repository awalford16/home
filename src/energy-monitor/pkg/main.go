package main

import (
        "net/http"
        "time"
        "os"
        "fmt"

        "github.com/awalford16/home/energy"

        "github.com/prometheus/client_golang/prometheus"
        "github.com/prometheus/client_golang/prometheus/promauto"
        "github.com/prometheus/client_golang/prometheus/promhttp"
)

func recordMetrics(e *energy.EnergyProvider) {
        go func() {
                for {
                        recentUsage, err := e.GetElectricUsage()
                        if err != nil {
                                fmt.Println("Error getting electrical usage")
                                time.Sleep(10 * time.Minute)
                        } else {
                                electricityUsage.Set(recentUsage)
                                time.Sleep(30 * time.Minute)
                        }
                }
        }()

        go func() {
                for {
                        tariff, _ := e.GetElectricCharges()
                        standingChargeExcVAT.Set(tariff.StandingCharges.ValueExcVAT)
                        standingChargeIncVAT.Set(tariff.StandingCharges.ValueIncVAT)
                        standardUnitExcVAT.Set(tariff.StandardUnitRate.ValueExcVAT)
                        standardUnitIncVAT.Set(tariff.StandardUnitRate.ValueIncVAT)
                        time.Sleep(24 * time.Hour)
                }
        }()
}

var (
        electricityUsage = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_usage",
		Help: "kWH of Electricity usage",
	})

        standingChargeExcVAT = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_standing_charge_exc_vat",
		Help: "Standing charge exc. VAT",
	})

        standingChargeIncVAT = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_standing_charge_inc_vat",
		Help: "Standing charge inc. VAT",
	})

        standardUnitExcVAT = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_standard_unit_exc_vat",
		Help: "Standard unit rate exc. VAT",
	})

        standardUnitIncVAT = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_standard_unit_inc_vat",
		Help: "Standard unit rate inc. VAT",
	})
)

func main() {
	mpan := os.Getenv("METER_MPAN")
	serialNumber := os.Getenv("METER_SERIAL_NUMBER")
	product := os.Getenv("OCTOPUS_PRODUCT")
	tariff := os.Getenv("OCTOPUS_TARIFF")

        if mpan == "" || serialNumber == "" {
                fmt.Println("METER_MPAN or METER_SERIAL_NUMBER environment variable is not defined.")
                return
        }

        provider, err := energy.NewEnergyProvider(mpan, serialNumber, product, tariff)
        if err != nil {
                fmt.Println("Failed to initialise energy provider.")
                return
        }

        recordMetrics(provider)

        // Start prometheus metrics server
        http.Handle("/metrics", promhttp.Handler())

        // Health probes
        http.HandleFunc("/healthz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	})

	http.HandleFunc("/readyz", func(w http.ResponseWriter, r *http.Request) {
		w.WriteHeader(http.StatusOK)
		fmt.Fprintln(w, "OK")
	})

        fmt.Println("Starting server on port 2112...")
        http.ListenAndServe(":2112", nil)
}
