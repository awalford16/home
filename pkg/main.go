package main

import (
        "net/http"
        "time"
        "os"

        "example.com/home_monitor/energy"

        "github.com/prometheus/client_golang/prometheus"
        "github.com/prometheus/client_golang/prometheus/promauto"
        "github.com/prometheus/client_golang/prometheus/promhttp"
)

func recordMetrics(e *energy.EnergyProvider) {
        go func() {
                for {
                        recentUsage := e.GetElectricUsage()
                        electricityUsage.Set(recentUsage)
                        time.Sleep(30 * time.Minute)
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

        provider := energy.NewEnergyProvider(mpan, serialNumber, product, tariff)
        recordMetrics(provider)

        http.Handle("/metrics", promhttp.Handler())
        http.ListenAndServe(":2112", nil)
}
