# Introduction

This is the crawler about GWP factors.

# Prerequisites

- Prepare the Python3+ version.
- Install required Python modules

```Bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev
pip3 install -U pdftotext requests beautifulsoup4
```

# Usage

- Clone the repository

```Bash
git clone https://gitlab.com/iii-api-platform/gwp-factors
```

- Running the `` to fetch and collect latest electric CO2e value.

```Bash
python3 ./electric/moeaboe_handler.py
```

- Once running above command, it will update the `./datasets/electric_co2e.csv` file.
- If there's no latest electric CO2e value, it will not update the above CSV file.

# Known Datasets

- 電力排碳係數(經濟部能源局提供)
- 溫室氣體排放係數管理表(環保署提供) (目前有6.0.3與6.0.4版本)
