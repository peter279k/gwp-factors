# Introduction

This is the crawler about GWP factors.

# Prerequisites

- Prepare the Python3.6.9+ version.
- Install required Python modules.

```Bash
sudo apt-get update
sudo apt-get install build-essential libpoppler-cpp-dev pkg-config python3-dev python3-pil tesseract-ocr
pip3 install -U pdftotext requests beautifulsoup4 pyexcel-ods3 pytesseract
```

# Usage

- Clone the repository

```Bash
git clone https://gitlab.com/iii-api-platform/gwp-factors
```

# 電力碳排係數(能源署)

- Running the following command to fetch and collect latest electric CO2e value.

```Bash
python3 ./electric/moeaea_handler.py
```

- Once running above command, it will update the `./datasets/electric_co2e.csv` file.
- If there's no latest electric CO2e value, it will not update the above CSV file.

# GWP Factor Fetcher (環保署)

- Running the `python3 ./gwp_factor/download_epa_file.py` to download EPA files.
- Running the `python3 ./gwp_factor/parse_epa_file.py` to parse EPA GWP factor files.
- Running the `python3 ./gwp_factor/fill_zero_cfc_gwp.py` to fill the zero in specific factor files.
- All parsed CSV files will be saved in `./datasets` directory.

# CFP Calculator (產品碳足跡網)

- Creating the `cfp_auth.txt` in this repository root folder to store the CFP website user name and password.
- Running the `python3 ./cfp_calculate/fetch_pdf_file.py` to download factor PDF file.
- Once it's failed for three times, the Python program will be terminated.
- The factor PDF file will be saved in `./datasets` directory. (Parsing PDF file is WIP.)

- The `pdftotext` is not worked under the Cronjob in the host operating system.
    - To resolve above issue, using the `./cfp_calculate/Dockerfile` to build the Docker image.
    - Then run the Docker image as the container to run the `parse_pdf_file.py` Python program.
    - The building steps are as follows:

```bash
# Building the Docker image
cd ./cfp_calculate
docker build -t cfp_calculate . --no-cache

# Run the Docker image as the container (Ensuring current working directory is the gwp-factors project root)
cd /path/to/gwp-factors
docker stop cfp_calculate
docker rm cfp_calculate
docker run -itd --volume $PWD:/root/gwp-factors --name cfp_calculate cfp_calculate sh


# Setup the Cronjob
*/10 * * * * cd /home/localadmin/gwp-factors; docker exec cfp_calculate sh -c "cd /root/gwp-factors/ && python3 ./cfp_calculate/parse_pdf_file.py"
```

# GWP Values Fetching (IPCC AR4, AR5, AR6) 溫室氣體潛勢值


- Running the `python3 ./gwp_value/gwp_value.py` to download the CSV file.

# Known Datasets

- 電力排碳係數(經濟部能源局提供)
- 溫室氣體排放係數管理表(環保署提供) (目前有6.0.3與6.0.4版本)
- 產品碳足跡資訊網 (WIP for parsing factor PDF file)
  - https://cfp-calculate.tw/cfpc/WebPage/LoginPage.aspx
