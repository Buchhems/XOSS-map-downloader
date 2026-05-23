# XOSS NAV+ Map Downloader

Small Python script to download offline map files for the XOSS NAV / NAV+ directly, without using the somewhat fragile XOSS web UI.
You can select a country by name and then either download **all regions** for that country or just a **single region**.

The script uses the same JSON map list that the official XOSS download page loads in the background (`map_list.json` from `geo.imxingzhe.com`).

---

## Features

- Fetches the official XOSS map list (`map_list.json`) used by the XOSS download page.
- Lists all available countries in plain text.
- Select country by **typing its name (or part of it)**
- If a country has multiple regions (e.g., German states), you can:
  - download **all regions**, or  
  - pick **one region** by number.
- Saves each `.map` file in the current working directory.

---

<img width="640" height="640" alt="xoss" src="https://github.com/user-attachments/assets/06b1848a-daec-4aa5-bb13-7ad440b42d58" />


## Requirements

- Python 3 (tested with Python 3.13).
- [`requests`](https://pypi.org/project/requests/) library:

```bash
pip install requests
```

---

## Usage

1. Clone or download this repository.
2. Run the script:

```bash
python xoss-map-downloader.py
```

3. The script will:
   - Fetch the XOSS map list.
   - Print all available countries.
   - Ask you to type a country name (or part of it), e.g. `germany`, `france`, `italy`.
   - If there are multiple matches, it will show them and ask for the full name.
   - If the country has several regions (states/provinces), it will ask:
     - `Download ALL regions? (y/n)`  
       - `y` → downloads every region for that country.  
       - `n` → prints the region list and lets you pick one by number.

4. The downloaded `.map` files are saved in your current directory.

---

## Importing the maps to XOSS NAV / NAV+

The script only **downloads** the `.map` files. To actually use them on your XOSS device, follow the official XOSS steps:

1. Connect your XOSS NAV / NAV+ to your computer via USB.
2. Wait until it appears as a drive.
3. Copy the downloaded `.map` files into the `maps` folder in the root of the device.
4. Safely eject the device and reboot.
5. After GPS fix, the new maps should be available on the device.

Refer to the XOSS support documentation for details on map import procedures if needed.

---

## Notes & Limitations

- The map files are downloaded from the official XOSS/Imxingzhe servers. If those servers are slow or blocked from your network, downloads may time out or fail.
- Large countries or “download all regions” can be several hundred MB combined; make sure you have enough disk space and device storage.
- This script does **not** generate custom maps; it only automates downloading the official `.map` files.
