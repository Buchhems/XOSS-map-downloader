#!/usr/bin/env python3
import requests
import os
import sys

MAP_LIST_URL = "https://geo.imxingzhe.com/maps/v1/map_list.json"


def download_map(url, label):
    print("\nDownloading: " + label)
    print("URL: " + url)

    try:
        # much longer timeouts: 10s connect, 600s (10 min) read
        r = requests.get(url, stream=True, timeout=(10, 600))
        r.raise_for_status()
    except requests.exceptions.ReadTimeout:
        print("Download timed out for " + label + ". Try again later or download fewer regions.")
        return
    except Exception as e:
        print("Download failed for " + label + ": " + str(e))
        return

    filename = os.path.basename(url)
    path = os.path.join(os.getcwd(), filename)

    size_bytes = 0
    with open(path, "wb") as f:
        for chunk in r.iter_content(1024 * 256):
            if not chunk:
                continue
            f.write(chunk)
            size_bytes += len(chunk)

    size_mb = size_bytes / (1024 * 1024)
    print("Saved as: " + path + " (" + str(round(size_mb, 1)) + " MB)")


def main():
    print("Getting XOSS map list...")
    try:
        resp = requests.get(MAP_LIST_URL, timeout=20)
        resp.raise_for_status()
    except Exception as e:
        print("Could not get map list:", e)
        sys.exit(1)

    data = resp.json()
    continents = data.get("continent", [])

    # Build a flat list of countries
    countries = []
    for cont in continents:
        for c in cont.get("countries", []):
            countries.append(c)

    if not countries:
        print("No countries found in map list.")
        sys.exit(1)

    # Print all countries
    print("\nAvailable countries:\n")
    for c in countries:
        print("- " + c["name_en"])

    # --- country selection by name only ---
    while True:
        choice = input("\nType country name (or part of it): ").strip().lower()

        matches = []
        for c in countries:
            name = c["name_en"]
            if choice in name.lower():
                matches.append(c)

        if len(matches) == 0:
            print("No country matched, please try again.")
            continue

        if len(matches) == 1:
            country = matches[0]
            break

        print("\nMultiple matches:")
        for i, c in enumerate(matches, start=1):
            print(str(i) + ". " + c["name_en"])

        again = input("Type the FULL name of the one you want: ").strip().lower()
        chosen = None
        for c in matches:
            if again == c["name_en"].lower():
                chosen = c
                break

        if chosen is None:
            print("Still unclear, let’s try again.")
            continue

        country = chosen
        break

    country_name = country["name_en"]
    country_size = country["size_m"]
    print("\nSelected country: " + country_name + " (~ " + str(country_size) + " MB)")

    # >>> YOU WERE MISSING THIS PART <<<
    if "url" in country:
        country_url = country["url"]
    else:
        country_url = None

    if "cities" in country and country["cities"] is not None:
        cities = country["cities"]
    else:
        cities = []

    # Case A: single map for the whole country
    if country_url and not cities:
        download_map(country_url, country_name)
        print("\nDone.")
        return

    # Case B: multiple regions (cities/states)
    if cities:
        print("\n" + country_name + " has several regions.")
        answer = input('Download ALL regions? (y/n): ').strip().lower()

        if answer == "y":
            # Download every region
            for city in cities:
                city_name = city["name_en"]
                url = city["url"]
                if not url:
                    print("Skipping " + city_name + ": no URL.")
                    continue
                label = country_name + "_" + city_name
                download_map(url, label)
            print("\nAll region downloads finished.")
            return
        else:
            # Let user pick a single region
            print("\nRegions for this country:\n")
            for i, city in enumerate(cities, start=1):
                name = city["name_en"]
                size = city["size_m"]
                print(str(i) + ". " + name + " (~ " + str(size) + " MB)")

            choice_city = input("\nChoose region number: ").strip()
            try:
                idx_city = int(choice_city) - 1
            except ValueError:
                print("Not a valid number.")
                sys.exit(1)

            if idx_city < 0 or idx_city >= len(cities):
                print("Region index out of range.")
                sys.exit(1)

            city = cities[idx_city]
            city_name = city["name_en"]
            url = city["url"]
            if not url:
                print("Selected region has no URL.")
                sys.exit(1)

            label = country_name + "_" + city_name
            download_map(url, label)
            print("\nDone.")
            return

    # Fallback if something unexpected happens
    if country_url:
        download_map(country_url, country_name)
    else:
        print("No URL found for this country.")


if __name__ == "__main__":
    main()
