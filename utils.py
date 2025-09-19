import json
import re

def get_r_count(data):
    r_count = {}
    for p in data["projects"]:
        if p["huvudsaklig_9r_strategi"] not in r_count.keys():
            r_count[p["huvudsaklig_9r_strategi"]] = 1
        else:
            r_count[p["huvudsaklig_9r_strategi"]] = r_count[p["huvudsaklig_9r_strategi"]] + 1
    
    return r_count

def get_additional_rs_count(data):
    rs_count = {}
    for p in data["projects"]:
        for r in p["ovriga_r_strategier"]:
            if r not in rs_count.keys():
                rs_count[r] = 1
            else:
                rs_count[r] = rs_count[r] + 1

    R_STRATEGIES = {
        "R0 - Refuse": 0,
        "R1 - Rethink": 0,
        "R2 - Reduce": 0,
        "R3 - Reuse": 0,
        "R4 - Repair": 0,
        "R5 - Refurbish": 0,
        "R6 - Remanufacture": 0,
        "R7 - Repurpose": 0,
        "R8 - Recycle": 0,
        "R9 - Recover": 0,
    }

    for rs in rs_count.keys():
        for r in R_STRATEGIES.keys():
            if rs in r:
                R_STRATEGIES[r] = rs_count[rs]
    
    return R_STRATEGIES


def get_r_over_time(data):

    YEARS = {
        "2016": 0,
        "2017": 0,
        "2018": 0,
        "2019": 0,
        "2020": 0,
        "2021": 0,
        "2022": 0,
        "2023": 0,
        "2024": 0,
        "2025": 0,
    }

    r_over_years = {
        "R0 - Refuse": YEARS.copy(),
        "R1 - Rethink": YEARS.copy(),
        "R2 - Reduce": YEARS.copy(),
        "R3 - Reuse": YEARS.copy(),
        "R4 - Repair": YEARS.copy(),
        "R5 - Refurbish": YEARS.copy(),
        "R6 - Remanufacture": YEARS.copy(),
        "R7 - Repurpose": YEARS.copy(),
        "R8 - Recycle": YEARS.copy(),
        "R9 - Recover": YEARS.copy(),
    }

    hits = 0
    for p in data["projects"]:
        end_date = p["metadata"]["Projekttid"]


        # find all 4-digit years
        years = re.findall(r"\b\d{4}\b", end_date)

        if len(years) >= 2:
            year = years[1]
        else:
            year = years[0]
        year = years[1]

        main_r = p["huvudsaklig_9r_strategi"]

        # Match strategy, or create
        for r in r_over_years.keys():
            #print(f"if {main_r.lower()} in {r.lower()}")
            if main_r.lower() in r.lower():
                #print(f"Hit! {main_r.lower()} is in {r.lower()}")
                r_over_years[r][year] = r_over_years[r][year] +1
                hits += 1
    
    return r_over_years
            

def get_flow_counts(data):

    flow_counts = {}
    flows = ["narrow", "slow", "regenerate", "close"]
    flow_data = []

    for p in data["projects"]:
        flow_data.append(p["flodes_definitioner"])
        for flow in p["flodes_definitioner"]:
            if flow.lower() in flow_counts:
                flow_counts[flow.lower()] = flow_counts[flow.lower()] + 1
            else:
                if flow.lower() in flows:
                    flow_counts[flow.lower()] = 1
                else:
                    print(f"Flödet '{flow}' finns inte sedan tidigare definierat. Kontrollera analysen ")

    print(flow_data)
    return flow_counts


def get_main_flow(data):
    main_flow_count = {}
    flows = ["narrow", "slow", "regenerate", "close"]


    for p in data["projects"]:
        if p["flodes_definitioner"]:
            main_flow = p["flodes_definitioner"][0]
            if main_flow.lower() in main_flow_count.keys():
                main_flow_count[main_flow.lower()] = main_flow_count[main_flow.lower()] + 1
            else:
                if main_flow.lower() in flows:
                    main_flow_count[main_flow.lower()] = 1
                else:
                    print(f"Flödet '{main_flow}' finns inte sedan tidigare definierat. Kontrollera analysen ")

    #print(main_flow_count)
    return main_flow_count

def get_categories(data):
    categories = set()

    for p in data["projects"]:
        for cat in p["metadata"]["Kategorier"]:
            categories.add(cat)

    return categories

