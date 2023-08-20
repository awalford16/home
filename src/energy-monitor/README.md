# Energy Monitor

## Overview

Energy Monitor is a basic golang application which exports prometheus metrics containing data about energy usage from Octopus Energy.

It requires the following environment variables being set which can be found under your Octopus energy account page:

- OCTOPUS_ENERGY_API_KEY
- METER_MPAN
- METER_SERIAL_NUMBER
- OCTOPUS_PRODUCT
- OCTOPUS_TARIFF
