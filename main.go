package main

import (
        "net/http"
        "time"

        "example.com/home_monitor/energy"

        "github.com/prometheus/client_golang/prometheus"
        "github.com/prometheus/client_golang/prometheus/promauto"
        "github.com/prometheus/client_golang/prometheus/promhttp"
)

func recordMetrics() {
        go func() {
                for {
                        opsProcessed.Inc()
                        time.Sleep(2 * time.Second)
                }
        }()

        go func() {
                for {
                        recentUsage := energy.GetElectricUsage()
                        electricityUsage.Set(recentUsage)
                        time.Sleep(30 * time.Minute)
                }
        }()
}

var (
        opsProcessed = promauto.NewCounter(prometheus.CounterOpts{
                Name: "myapp_processed_ops_total",
                Help: "The total number of processed events",
        })

        electricityUsage = promauto.NewGauge(prometheus.GaugeOpts{
		Name: "electricity_usage",
		Help: "kWH of Electricity usage",
	})
)

func main() {
        recordMetrics()

        http.Handle("/metrics", promhttp.Handler())
        http.ListenAndServe(":2112", nil)
}
