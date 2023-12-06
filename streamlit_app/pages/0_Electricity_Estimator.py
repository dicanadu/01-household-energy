import requests
import streamlit as st
import pandas as pd
import numpy as np
import time
import matplotlib.pyplot as plt
from concurrent.futures import ThreadPoolExecutor, as_completed

########## page info ############

st.set_page_config(page_title='U.S. household electricity consumption'
                   , page_icon='🏠')

############ initiate parameters for API request ############
params={}

############### API ###########################

url="https://household-predictions-final2-jaiabuy6eq-ew.a.run.app/predict"

# @st.cache_data(ttl=3600) # cache data for 1 hour


def api_call(url, params, toggle_state):
    # Modify the params based on the toggle_state if needed
    if toggle_state:
        params['toggle_state'] = toggle_state
        response = requests.get(url, params).json()
        pred_kwh = response.get("KWH") / 12
        pred_kwh_filter = "monthly"
    else:
        response = requests.get(url, params).json()
        pred_kwh = response.get("KWH")
        pred_kwh_filter = "annual"
    # output prediction:
    return pred_kwh, pred_kwh_filter

def calculate():
    counts = range(300)
    total_counts = len(counts)
    with st.spinner("Running..."):
        with ThreadPoolExecutor() as executor:
            bar = st.progress(0)
            placeholder = st.empty()

            # Initialize variables to track progress
            completed_count = 0

            futures = [executor.submit(api_call, url, params, toggle_state) for count in counts]

            # Wait for all futures to complete
            for future in as_completed(futures):
                result, pred_kwh_filter = future.result()
                completed_count += 1

                # Update progress bar
                progress = completed_count / total_counts
                placeholder.text(f"{int(progress * 100)}%")
                bar.progress(progress)

            # Return the result and pred_kwh_filter from the first completed future
            return result, pred_kwh_filter

def plot_energy_scale(pred_kwh, state_name, pred_kwh_filter):

    # Assuming breakdown_per_state[state_name] is a list
    breakdown_list = breakdown_per_state[state_name]

    if pred_kwh_filter == 'monthly':
        # Convert the list to a NumPy array and perform element-wise division
        temp_kwh_hist = np.array(breakdown_list) / 12
    else:
        # If pred_kwh_filter is not 'monthly', use the data as is
        temp_kwh_hist = np.array(breakdown_list)

    # Define the quartiles
    quartiles = np.percentile(temp_kwh_hist, [0, 25, 50, 75, 100])

    # Your kWh value

    # Scale my_kwh to the same range as quartile_ranges
    scaled_my_kwh = np.interp(pred_kwh, (min(temp_kwh_hist), max(temp_kwh_hist)), (min(quartiles), max(quartiles)))

    # Find the index of the quartile where your scaled kWh falls
    quartile_index = np.searchsorted(quartiles, scaled_my_kwh)

    # Calculate the position within the indexed quartile
    position_within_quartile = (scaled_my_kwh - quartiles[quartile_index - 1]) / (quartiles[quartile_index] - quartiles[quartile_index - 1])

    # Plot the histogram with horizontal bar chart
    fig, ax = plt.subplots(figsize=(10, 1))

    # Evenly space quartile ranges
    quartile_ranges = np.linspace(min(temp_kwh_hist), max(temp_kwh_hist), 5)

    # Set quartile range colors
    colors = ['green', 'yellow', 'darkorange', 'red']

    # Plot quartile ranges with specified colors
    for i in range(4):
        ax.fill_betweenx(y=[0, len(temp_kwh_hist)], x1=quartile_ranges[i], x2=quartile_ranges[i + 1], color=colors[i], alpha=0.3)

    # Calculate the exact location for your scaled kWh
    exact_location = quartile_ranges[quartile_index - 1] + position_within_quartile * (quartile_ranges[quartile_index] - quartile_ranges[quartile_index - 1])

    # Plot a vertical line for your scaled kWh at the exact location
    ax.axvline(x=exact_location, color='black', linestyle=':', label=f'My kWh: {pred_kwh}', linewidth=5)

    # ax.set_title(f"Energy Consumption Quartiles for {state_name}", color='white')
    ax.set_xlabel(f"kWh/{pred_kwh_filter}", color='white')
    ax.get_yaxis().set_visible(False)
    # Remove top and right spines
    ax.spines['top'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    # Set x-axis limits explicitly
    ax.set_xlim(min(temp_kwh_hist), max(temp_kwh_hist))

    ax.set_xticks(quartile_ranges)
    ax.set_xticklabels([f'{int(round(q, -2))}' for q in quartiles])

    # Set the legend text color to white
    legend = ax.legend(loc='upper right', bbox_to_anchor=(0.5, 0.9, 0.508, 0.5))
    for text in legend.get_texts():
        text.set_color('black')

    # Make the x-axis tick labels white
    ax.tick_params(axis='x', colors='white')

    # Make the y-axis tick labels white
    ax.tick_params(axis='y', colors='white')

    # Make the figure background transparent
    fig.patch.set_facecolor('none')
    fig.patch.set_alpha(0.0)

    return fig


########### hard-coded constants ###############

label_dict = {'REGIONC': 'Census Region', 'state_name': 'State Name', 'BA_climate': 'Building America Climate Zone', 'TYPEHUQ': 'Type of housing unit :house_buildings:', 'STORIES': 'Number of stories', 'YEARMADERANGE': 'Age of housing unit', 'NCOMBATH': 'Bathrooms', 'NHAFBATH': 'Half bathrooms', 'TOTROOMS': 'Rooms (excluding bathrooms)', 'WALLTYPE': 'Major outside wall material', 'ROOFTYPE': "Major roofing material; 'Not applicable' applies to apartment buildings with 5 or more units", 'WINDOWS': 'Windows', 'SWIMPOOL': 'Have swimming pool', 'NUMFRIG': 'Refrigerators', 'MICRO': 'Microwaves', 'DISHWASH': 'Have dishwasher', 'CWASHER': 'Have clothes washer', 'DRYER': 'Have clothes dryer', 'TVCOLOR': 'Television', 'DESKTOP': 'Computers', 'NUMLAPTOP': 'Laptop computers', 'TELLWORK': 'Any household member teleworking', 'HEATHOME': 'Space heating equipment', 'EQUIPM': 'Main space heating equipment', 'NUMPORTEL': 'Portable electric heaters', 'AIRCOND': 'Have air conditioner', 'LGTIN1TO4': 'Inside light bulbs', 'LGTIN4TO8': 'Inside light bulbs', 'LGTINMORE8': 'Inside light bulbs', 'SMARTMETER': 'Have electricity smart meter', 'SOLAR': "On-site electricity generation from solar; 'Not applicable' applies to apartment buildings with 2 or more units.", 'NHSLDMEM': 'Household members :man-woman-girl-boy:', 'SQFTEST': 'Square footage :house_with_garden:'}
values_dict = {'REGIONC': 'Midwest\nNortheast\nSouth\nWest', 'state_name': 'state_dictionary!A1', 'BA_climate': 'Cold\nHot-Dry\nHot-Humid\nMarine\nMixed-Dry\nMixed-Humid\nSubarctic\nVery-Cold', 'TYPEHUQ': '1 Mobile home\n2 Single-family house detached from any other house \n3 Single-family house attached to one or more other houses\n4 Apartment in a building with 2 to 4 units\n5 Apartment in a building with 5 or more units', 'STORIES': '1 One story\n2 Two stories\n3 Three stories\n4 Four or more stories\n5 Split-level\n-2 Not applicable', 'YEARMADERANGE': '1 Before 1950\n2 1950 to 1959\n3 1960 to 1969\n4 1970 to 1979\n5 1980 to 1989\n6 1990 to 1999\n7 2000 to 2009\n8 2010 to 2015\n9 2016 to 2020', 'NCOMBATH': '0 - 4', 'NHAFBATH': '0 - 2', 'TOTROOMS': '1-15', 'WALLTYPE': '1 Brick\n2 Wood\n3 Siding (aluminum, fiber cement, vinyl, or steel) \n4 Stucco\n5 Shingle (composition)\n6 Stone \n7 Concrete block \n99 Other', 'ROOFTYPE': '1 Ceramic or clay tiles\n2 Wood shingles/shakes\n3 Metal\n4 Slate or synthetic slate\n5 Shingles (composition or asphalt)\n6 Concrete tiles\n99 Other\n-2 Not applicable', 'WINDOWS': '1 1 or 2 windows\n2 3 to 5 windows\n3 6 to 9 windows\n4 10 to 15 windows\n5 16 to 19 windows\n6 20 to 29 windows\n7 30 or more windows', 'SWIMPOOL': '1 Yes\n0 No\n-2 Not applicable', 'NUMFRIG': '0 - 9', 'MICRO': '0 - 3', 'DISHWASH': '1 Yes\n0 No', 'CWASHER': '1 Yes\n0 No', 'DRYER': '1 Yes\n0 No', 'TVCOLOR': '0 - 14', 'DESKTOP': '0 - 8', 'NUMLAPTOP': '0 - 20', 'TELLWORK': '1 Yes\n0 No', 'HEATHOME': '1 Yes\n0 No', 'EQUIPM': '3 Central furnace \n2 Steam or hot water system\n4 Central heat pump\n13 Ductless heat pump\n5 Built-in electric units\n7 Built-in room heater\n8 Wood or pellet stove \n10 Portable electric heaters\n99 Other \n-2 Not applicable', 'NUMPORTEL': '1 - 9\n-2 Not applicable', 'AIRCOND': '1 Yes\n0 No', 'LGTIN1TO4': '0 - 90', 'LGTIN4TO8': '0 - 84', 'LGTINMORE8': '0 - 99', 'SMARTMETER': "1 Yes\n0 No\n-4 Don't Know", 'SOLAR': '1 Yes\n0 No\n-2 Not applicable', 'NHSLDMEM': '1 - 7', 'SQFTEST': '240-15000'}

# U.S. states selector
states ={'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
# state to region mapper
state_to_region={'New Mexico': 'WEST', 'Arkansas': 'SOUTH', 'South Carolina': 'SOUTH', 'New Jersey': 'NORTHEAST', 'Texas': 'SOUTH', 'Oklahoma': 'SOUTH', 'Mississippi': 'SOUTH', 'District of Columbia': 'SOUTH', 'Arizona': 'WEST', 'California': 'WEST', 'Louisiana': 'SOUTH', 'Minnesota': 'MIDWEST', 'Vermont': 'NORTHEAST', 'Rhode Island': 'NORTHEAST', 'Illinois': 'MIDWEST', 'Maine': 'NORTHEAST', 'South Dakota': 'MIDWEST', 'Massachusetts': 'NORTHEAST', 'Florida': 'SOUTH', 'Ohio': 'MIDWEST', 'Nebraska': 'MIDWEST', 'Virginia': 'SOUTH', 'Wyoming': 'WEST', 'Pennsylvania': 'NORTHEAST', 'Hawaii': 'WEST', 'New Hampshire': 'NORTHEAST', 'Michigan': 'MIDWEST', 'Maryland': 'SOUTH', 'New York': 'NORTHEAST', 'Colorado': 'WEST', 'North Carolina': 'SOUTH', 'Kentucky': 'SOUTH', 'North Dakota': 'MIDWEST', 'Georgia': 'SOUTH', 'West Virginia': 'SOUTH', 'Oregon': 'WEST', 'Missouri': 'MIDWEST', 'Utah': 'WEST', 'Connecticut': 'NORTHEAST', 'Tennessee': 'SOUTH', 'Wisconsin': 'MIDWEST', 'Idaho': 'WEST', 'Nevada': 'WEST', 'Washington': 'WEST', 'Indiana': 'MIDWEST', 'Delaware': 'SOUTH', 'Iowa': 'MIDWEST', 'Alaska': 'WEST', 'Alabama': 'SOUTH', 'Montana': 'WEST', 'Kansas': 'MIDWEST'}
# state to most frequent climate mapper
climate_dict = {'Alabama': 'Hot-Humid', 'Alaska': 'Subarctic', 'Arizona': 'Cold', 'Arkansas': 'Hot-Humid', 'California': 'Cold', 'Colorado': 'Cold', 'Connecticut': 'Cold', 'Delaware': 'Mixed-Humid', 'District of Columbia': 'Mixed-Humid', 'Florida': 'Hot-Humid', 'Georgia': 'Hot-Humid', 'Hawaii': 'Hot-Humid', 'Idaho': 'Cold', 'Illinois': 'Cold', 'Indiana': 'Cold', 'Iowa': 'Cold', 'Kansas': 'Cold', 'Kentucky': 'Mixed-Humid', 'Louisiana': 'Hot-Humid', 'Maine': 'Cold', 'Maryland': 'Cold', 'Massachusetts': 'Cold', 'Michigan': 'Cold', 'Minnesota': 'Cold', 'Mississippi': 'Hot-Humid', 'Missouri': 'Cold', 'Montana': 'Cold', 'Nebraska': 'Cold', 'Nevada': 'Cold', 'New Hampshire': 'Cold', 'New Jersey': 'Cold', 'New Mexico': 'Cold', 'New York': 'Cold', 'North Carolina': 'Cold', 'North Dakota': 'Cold', 'Ohio': 'Cold', 'Oklahoma': 'Mixed-Humid', 'Oregon': 'Cold', 'Pennsylvania': 'Cold', 'Rhode Island': 'Cold', 'South Carolina': 'Hot-Humid', 'South Dakota': 'Cold', 'Tennessee': 'Mixed-Humid', 'Texas': 'Hot-Dry', 'Utah': 'Cold', 'Vermont': 'Cold', 'Virginia': 'Mixed-Humid', 'Washington': 'Cold', 'West Virginia': 'Cold', 'Wisconsin': 'Cold', 'Wyoming': 'Cold'}
# section to features mapper
section_dict = {'ADMIN': ['DOEID', 'BA_climate', 'IECC_climate_code', 'UATYP10'], 'AIR CONDITIONING': ['AIRCOND', 'COOLAPT', 'ACEQUIPM_PUB', 'ACEQUIPAGE', 'ACEQUIPAUXTYPE_PUB', 'NUMDLHPAC', 'NUMWWAC', 'NUMPORTAC', 'BASECOOL', 'ATTCCOOL', 'GARGCOOL', 'NUMCFAN', 'NUMFLOORFAN', 'USECFAN', 'HOUSEFAN', 'ATTICFAN', 'DEHUMTYPE', 'NUMPORTDEHUM', 'USEDEHUM', 'ELCOOL', 'ZACEQUIPAGE', 'ZAIRCOND', 'ZATTCCOOL', 'ZATTICFAN', 'ZBASECOOL', 'ZCOOLAPT', 'ZCOOLCNTL', 'ZDEHUMTYPE', 'ZGARGCOOL', 'ZHOUSEFAN', 'ZNUMCFAN', 'ZNUMDLHPAC', 'ZNUMFLOORFAN', 'ZNUMPORTAC', 'ZNUMPORTDEHUM', 'ZNUMWWAC', 'ZUSECFAN', 'ZUSEDEHUM', 'ZACEQUIPM_PUB', 'ZACEQUIPAUXTYPE_PUB'], 'APPLIANCES': ['NUMFRIG', 'SIZRFRI1', 'TYPERFR1', 'AGERFRI1', 'ICE', 'SIZRFRI2', 'TYPERFR2', 'AGERFRI2', 'LOCRFRI2', 'WINECHILL', 'NUMFREEZ', 'UPRTFRZR', 'SIZFREEZ', 'FREEZER', 'AGEFRZR', 'RANGE', 'COOKTOP', 'OVEN', 'RANGEFUEL', 'RANGEINDT', 'RCOOKUSE', 'ROVENUSE', 'COOKTOPFUEL', 'COOKTOPINDT', 'COOKTOPUSE', 'OVENFUEL', 'OVENUSE', 'MICRO', 'AMTMICRO', 'OUTGRILLFUEL', 'OUTGRILL', 'NUMMEAL', 'USECOFFEE', 'TOAST', 'TOASTOVN', 'CROCKPOT', 'PRSSCOOK', 'RICECOOK', 'BLENDER', 'APPOTHER', 'ELFOOD', 'LPCOOK', 'UGCOOK', 'DISHWASH', 'DWASHUSE', 'DWCYCLE', 'AGEDW', 'CWASHER', 'TOPFRONT', 'WASHLOAD', 'WASHTEMP', 'AGECWASH', 'DRYER', 'DRYRFUEL', 'DRYRUSE', 'AGECDRYER', 'ZAGECDRYER', 'ZAGECWASH', 'ZAGEDW', 'ZAGEFRZR', 'ZAGERFRI1', 'ZAGERFRI2', 'ZAMTMICRO', 'ZBLENDER', 'ZCOOKTOP', 'ZCOOKTOPFUEL', 'ZCOOKTOPINDT', 'ZCOOKTOPUSE', 'ZCROCKPOT', 'ZCWASHER', 'ZDISHWASH', 'ZDRYER', 'ZDRYRFUEL', 'ZDRYRUSE', 'ZDWASHUSE', 'ZDWCYCLE', 'ZFREEZER', 'ZICE', 'ZLOCRFRI2', 'ZMICRO', 'ZNUMFREEZ', 'ZNUMFRIG', 'ZNUMMEAL', 'ZOUTGRILLFUEL', 'ZOVEN', 'ZOVENFUEL', 'ZOVENUSE', 'ZPRSSCOOK', 'ZRANGE', 'ZRANGEFUEL', 'ZRANGEINDT', 'ZRCOOKUSE', 'ZRICECOOK', 'ZROVENUSE', 'ZSIZFREEZ', 'ZSIZRFRI1', 'ZSIZRFRI2', 'ZTOAST', 'ZTOASTOVN', 'ZTOPFRONT', 'ZTYPERFR1', 'ZTYPERFR2', 'ZUPRTFRZR', 'ZUSECOFFEE', 'ZWASHLOAD', 'ZWASHTEMP', 'ZWINECHILL', 'ZOUTGRILL'], 'ELECTRONICS': ['TVCOLOR', 'TVSIZE1', 'TVTYPE1', 'TVUSE1', 'TVONWD1', 'TVONWE1', 'TVSIZE2', 'TVTYPE2', 'TVUSE2', 'TVONWD2', 'TVONWE2', 'TVSIZE3', 'TVTYPE3', 'TVUSE3', 'TVONWD3', 'TVONWE3', 'CABLESAT', 'COMBODVR', 'SEPDVR', 'INTSTREAM', 'PLAYSTA', 'DVD', 'VCR', 'TVAUDIOSYS', 'DESKTOP', 'NUMLAPTOP', 'NUMTABLET', 'ELPERIPH', 'NUMSMPHONE', 'CELLPHONE', 'TELLWORK', 'TELLDAYS', 'TLDESKTOP', 'TLLAPTOP', 'TLTABLET', 'TLMONITOR', 'TLOTHER', 'ONLNEDUC', 'INTERNET', 'INTYPECELL', 'INTYPEBROAD', 'INTYPEOTH', 'SMARTSPK', 'SSLIGHT', 'SSTEMP', 'SSSECURE', 'SSTV', 'SSOTHER', 'ZCABLESAT', 'ZCELLPHONE', 'ZCOMBODVR', 'ZDESKTOP', 'ZDVD', 'ZELPERIPH', 'ZINTERNET', 'ZINTSTREAM', 'ZINTYPEBROAD', 'ZINTYPECELL', 'ZINTYPEOTH', 'ZNUMLAPTOP', 'ZNUMSMPHONE', 'ZNUMTABLET', 'ZONLNEDUC', 'ZPLAYSTA', 'ZSEPDVR', 'ZSMARTSPK', 'ZSSLIGHT', 'ZSSOTHER', 'ZSSSECURE', 'ZSSTEMP', 'ZSSTV', 'ZTELLDAYS', 'ZTELLWORK', 'ZTLDESKTOP', 'ZTLLAPTOP', 'ZTLMONITOR', 'ZTLOTHER', 'ZTLTABLET', 'ZTVAUDIOSYS', 'ZTVCOLOR', 'ZTVONWD1', 'ZTVONWD2', 'ZTVONWD3', 'ZTVONWE1', 'ZTVONWE2', 'ZTVONWE3', 'ZTVSIZE1', 'ZTVSIZE2', 'ZTVSIZE3', 'ZTVTYPE1', 'ZTVTYPE2', 'ZTVTYPE3', 'ZTVUSE1', 'ZTVUSE2', 'ZTVUSE3', 'ZVCR'], 'ENERGY ASSISTANCE': ['SCALEB', 'SCALEG', 'SCALEE', 'PAYHELP', 'NOHEATBROKE', 'NOHEATEL', 'NOHEATNG', 'NOHEATBULK', 'NOHEATDAYS', 'NOHEATHELP', 'COLDMA', 'NOACBROKE', 'NOACEL', 'NOACDAYS', 'NOACHELP', 'HOTMA', 'ENERGYASST', 'ENERGYASST20', 'ENERGYASST19', 'ENERGYASST18', 'ENERGYASST17', 'ENERGYASST16', 'ENERGYASSTOTH', 'ZCOLDMA', 'ZENERGYASST', 'ZENERGYASST16', 'ZENERGYASST17', 'ZENERGYASST18', 'ZENERGYASST19', 'ZENERGYASST20', 'ZENERGYASSTOTH', 'ZHOTMA', 'ZNOACBROKE', 'ZNOACDAYS', 'ZNOACEL', 'ZNOACHELP', 'ZNOHEATBROKE', 'ZNOHEATBULK', 'ZNOHEATDAYS', 'ZNOHEATEL', 'ZNOHEATHELP', 'ZNOHEATNG', 'ZPAYHELP', 'ZSCALEB', 'ZSCALEE', 'ZSCALEG'], 'ENERGY BILLS': ['ELPAY', 'NGPAY', 'LPGPAY', 'FOPAY', 'SMARTMETER', 'INTDATAACC', 'MEDICALDEV', 'POWEROUT', 'WHYPOWEROUT', 'BACKUP', 'SOLAR', 'OUTLET', 'ELECVEH', 'EVCHRGHOME', 'ELOTHER', 'UGOTH', 'LPOTHER', 'FOOTHER', 'USEEL', 'USENG', 'USELP', 'USEFO', 'USESOLAR', 'USEWOOD', 'ALLELEC', 'ZBACKUP', 'ZELPAY', 'ZFOPAY', 'ZLPGPAY', 'ZNGPAY', 'ZOUTLET', 'ZPOWEROUT', 'ZWHYPOWEROUT'], 'End-use Model': ['KWH', 'BTUEL', 'DOLLAREL', 'ELXBTU', 'PERIODEL', 'ZELAMOUNT', 'KWHSPH', 'KWHCOL', 'KWHWTH', 'KWHRFG', 'KWHRFG1', 'KWHRFG2', 'KWHFRZ', 'KWHCOK', 'KWHMICRO', 'KWHCW', 'KWHCDR', 'KWHDWH', 'KWHLGT', 'KWHTVREL', 'KWHTV1', 'KWHTV2', 'KWHTV3', 'KWHAHUHEAT', 'KWHAHUCOL', 'KWHCFAN', 'KWHDHUM', 'KWHHUM', 'KWHPLPMP', 'KWHHTBPMP', 'KWHHTBHEAT', 'KWHEVCHRG', 'KWHNEC', 'KWHOTH', 'BTUELSPH', 'BTUELCOL', 'BTUELWTH', 'BTUELRFG', 'BTUELRFG1', 'BTUELRFG2', 'BTUELFRZ', 'BTUELCOK', 'BTUELMICRO', 'BTUELCW', 'BTUELCDR', 'BTUELDWH', 'BTUELLGT', 'BTUELTVREL', 'BTUELTV1', 'BTUELTV2', 'BTUELTV3', 'BTUELAHUHEAT', 'BTUELAHUCOL', 'BTUELCFAN', 'BTUELDHUM', 'BTUELHUM', 'BTUELPLPMP', 'BTUELHTBPMP', 'BTUELHTBHEAT', 'BTUELEVCHRG', 'BTUELNEC', 'BTUELOTH', 'DOLELSPH', 'DOLELCOL', 'DOLELWTH', 'DOLELRFG', 'DOLELRFG1', 'DOLELRFG2', 'DOLELFRZ', 'DOLELCOK', 'DOLELMICRO', 'DOLELCW', 'DOLELCDR', 'DOLELDWH', 'DOLELLGT', 'DOLELTVREL', 'DOLELTV1', 'DOLELTV2', 'DOLELTV3', 'DOLELAHUHEAT', 'DOLELAHUCOL', 'DOLELCFAN', 'DOLELDHUM', 'DOLELHUM', 'DOLELPLPMP', 'DOLELHTBPMP', 'DOLELHTBHEAT', 'DOLELEVCHRG', 'DOLELNEC', 'DOLELOTH', 'CUFEETNG', 'BTUNG', 'DOLLARNG', 'NGXBTU', 'PERIODNG', 'ZNGAMOUNT', 'BTUNGSPH', 'BTUNGWTH', 'BTUNGCOK', 'BTUNGCDR', 'BTUNGPLHEAT', 'BTUNGHTBHEAT', 'BTUNGNEC', 'BTUNGOTH', 'CUFEETNGSPH', 'CUFEETNGWTH', 'CUFEETNGCOK', 'CUFEETNGCDR', 'CUFEETNGPLHEAT', 'CUFEETNGHTBHEAT', 'CUFEETNGNEC', 'CUFEETNGOTH', 'DOLNGSPH', 'DOLNGWTH', 'DOLNGCOK', 'DOLNGCDR', 'DOLNGPLHEAT', 'DOLNGHTBHEAT', 'DOLNGNEC', 'DOLNGOTH', 'GALLONLP', 'BTULP', 'DOLLARLP', 'LPXBTU', 'PERIODLP', 'ZLPAMOUNT', 'BTULPSPH', 'BTULPWTH', 'BTULPCOK', 'BTULPCDR', 'BTULPNEC', 'BTULPOTH', 'GALLONLPSPH', 'GALLONLPWTH', 'GALLONLPCOK', 'GALLONLPCDR', 'GALLONLPNEC', 'GALLONLPOTH', 'DOLLPSPH', 'DOLLPWTH', 'DOLLPCOK', 'DOLLPCDR', 'DOLLPNEC', 'DOLLPOTH', 'GALLONFO', 'BTUFO', 'DOLLARFO', 'FOXBTU', 'PERIODFO', 'ZFOAMOUNT', 'BTUFOSPH', 'BTUFOWTH', 'BTUFONEC', 'BTUFOOTH', 'GALLONFOSPH', 'GALLONFOWTH', 'GALLONFONEC', 'GALLONFOOTH', 'DOLFOSPH', 'DOLFOWTH', 'DOLFONEC', 'DOLFOOTH', 'BTUWD', 'ZWDAMOUNT', 'TOTALBTUSPH', 'TOTALDOLSPH', 'TOTALBTUWTH', 'TOTALDOLWTH', 'TOTALBTUOTH', 'TOTALDOLOTH', 'TOTALBTU', 'TOTALDOL'], 'GEOGRAPHY': ['REGIONC', 'DIVISION', 'STATE_FIPS', 'state_postal', 'state_name'], 'HOUSEHOLD CHARACTERISTICS': ['HHSEX', 'HHAGE', 'EMPLOYHH', 'EDUCATION', 'SDESCENT', 'HOUSEHOLDER_RACE', 'NHSLDMEM', 'NUMCHILD', 'NUMADULT1', 'NUMADULT2', 'ATHOME', 'MONEYPY', 'ZATHOME', 'ZEDUCATION', 'ZEMPLOYHH', 'ZHHAGE', 'ZHHSEX', 'ZMONEYPY', 'ZNHSLDMEM', 'ZNUMADULT1', 'ZNUMADULT2', 'ZNUMCHILD', 'ZSDESCENT', 'ZHOUSEHOLDER_RACE'], 'LIGHTING': ['LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'LGTINLED', 'LGTINCFL', 'LGTINCAN', 'LGTOUTANY', 'LGTOUTNITE', 'LGTOUTLED', 'LGTOUTCFL', 'LGTOUTCAN', 'ZLGTIN1TO4', 'ZLGTIN4TO8', 'ZLGTINCAN', 'ZLGTINCFL', 'ZLGTINLED', 'ZLGTINMORE8', 'ZLGTOUTANY', 'ZLGTOUTCAN', 'ZLGTOUTCFL', 'ZLGTOUTLED', 'ZLGTOUTNITE'], 'SPACE HEATING': ['HEATHOME', 'DNTHEAT', 'HEATAPT', 'EQUIPM', 'FUELHEAT', 'EQUIPAGE', 'GEOHP', 'EQUIPAUXTYPE', 'EQUIPAUX', 'FUELAUX', 'USEEQUIPAUX', 'NUMPORTEL', 'NUMFIREPLC', 'NUMDLHP', 'BASEHEAT', 'ATTCHEAT', 'GARGHEAT', 'HUMIDTYPE', 'NUMPORTHUM', 'USEHUMID', 'ELWARM', 'UGWARM', 'LPWARM', 'FOWARM', 'WDWARM', 'ZATTCHEAT', 'ZBASEHEAT', 'ZEQUIPAGE', 'ZEQUIPAUXTYPE', 'ZEQUIPM', 'ZFUELAUX', 'ZFUELHEAT', 'ZGARGHEAT', 'ZHEATAPT', 'ZHEATHOME', 'ZHUMIDTYPE', 'ZNUMDLHP', 'ZNUMFIREPLC', 'ZNUMPORTEL', 'ZNUMPORTHUM', 'ZUSEEQUIPAUX', 'ZUSEHUMID', 'ZDNTHEAT', 'WOODTYPE'], 'THERMOSTAT': ['TYPETHERM', 'HEATCNTL', 'TEMPHOME', 'TEMPGONE', 'TEMPNITE', 'COOLCNTL', 'TEMPHOMEAC', 'TEMPGONEAC', 'TEMPNITEAC', 'ZHEATCNTL', 'ZTEMPGONE', 'ZTEMPGONEAC', 'ZTEMPHOME', 'ZTEMPHOMEAC', 'ZTEMPNITE', 'ZTEMPNITEAC', 'ZTYPETHERM'], 'WATER HEATING': ['H2OAPT', 'H2OMAIN', 'WHEATSIZ', 'WHEATBKT', 'WHEATAGE', 'FUELH2O', 'MORETHAN1H2O', 'FUELH2O2', 'ELWATER', 'FOWATER', 'LPWATER', 'SOLWATER', 'WDWATER', 'UGWATER', 'ZFUELH2O', 'ZFUELH2O2', 'ZH2OAPT', 'ZH2OMAIN', 'ZMORETHAN1H2O', 'ZWHEATAGE', 'ZWHEATBKT', 'ZWHEATSIZ'], 'WEATHER': ['HDD65', 'CDD65', 'HDD30YR_PUB', 'CDD30YR_PUB', 'DBT1', 'DBT99', 'GWT'], 'WEIGHTS': ['NWEIGHT', 'NWEIGHT1', 'NWEIGHT2', 'NWEIGHT3', 'NWEIGHT4', 'NWEIGHT5', 'NWEIGHT6', 'NWEIGHT7', 'NWEIGHT8', 'NWEIGHT9', 'NWEIGHT10', 'NWEIGHT11', 'NWEIGHT12', 'NWEIGHT13', 'NWEIGHT14', 'NWEIGHT15', 'NWEIGHT16', 'NWEIGHT17', 'NWEIGHT18', 'NWEIGHT19', 'NWEIGHT20', 'NWEIGHT21', 'NWEIGHT22', 'NWEIGHT23', 'NWEIGHT24', 'NWEIGHT25', 'NWEIGHT26', 'NWEIGHT27', 'NWEIGHT28', 'NWEIGHT29', 'NWEIGHT30', 'NWEIGHT31', 'NWEIGHT32', 'NWEIGHT33', 'NWEIGHT34', 'NWEIGHT35', 'NWEIGHT36', 'NWEIGHT37', 'NWEIGHT38', 'NWEIGHT39', 'NWEIGHT40', 'NWEIGHT41', 'NWEIGHT42', 'NWEIGHT43', 'NWEIGHT44', 'NWEIGHT45', 'NWEIGHT46', 'NWEIGHT47', 'NWEIGHT48', 'NWEIGHT49', 'NWEIGHT50', 'NWEIGHT51', 'NWEIGHT52', 'NWEIGHT53', 'NWEIGHT54', 'NWEIGHT55', 'NWEIGHT56', 'NWEIGHT57', 'NWEIGHT58', 'NWEIGHT59', 'NWEIGHT60'], 'YOUR HOME': ['TYPEHUQ', 'CELLAR', 'CRAWL', 'CONCRETE', 'BASEOTH', 'BASEFIN', 'ATTIC', 'ATTICFIN', 'STORIES', 'PRKGPLC1', 'SIZEOFGARAGE', 'KOWNRENT', 'YEARMADERANGE', 'BEDROOMS', 'NCOMBATH', 'NHAFBATH', 'OTHROOMS', 'TOTROOMS', 'STUDIO', 'WALLTYPE', 'ROOFTYPE', 'HIGHCEIL', 'DOOR1SUM', 'WINDOWS', 'TYPEGLASS', 'ORIGWIN', 'WINFRAME', 'TREESHAD', 'ADQINSUL', 'DRAFTY', 'UGASHERE', 'SWIMPOOL', 'MONPOOL', 'POOLPUMP', 'FUELPOOL', 'RECBATH', 'MONTUB', 'FUELTUB', 'SQFTEST', 'SQFTRANGE', 'SQFTINCB', 'SQFTINCA', 'SQFTINCG', 'TOTSQFT_EN', 'TOTHSQFT', 'TOTCSQFT', 'ZADQINSUL', 'ZATTIC', 'ZATTICFIN', 'ZBASEFIN', 'ZBASEOTH', 'ZBEDROOMS', 'ZCELLAR', 'ZCONCRETE', 'ZCRAWL', 'ZDOOR1SUM', 'ZDRAFTY', 'ZFUELPOOL', 'ZFUELTUB', 'ZHIGHCEIL', 'ZKOWNRENT', 'ZMONPOOL', 'ZMONTUB', 'ZNCOMBATH', 'ZNHAFBATH', 'ZORIGWIN', 'ZOTHROOMS', 'ZPOOLPUMP', 'ZPRKGPLC1', 'ZRECBATH', 'ZROOFTYPE', 'ZSIZEOFGARAGE', 'ZSQFTEST', 'ZSQFTINCA', 'ZSQFTINCB', 'ZSQFTINCG', 'ZSQFTRANGE', 'ZSTORIES', 'ZSWIMPOOL', 'ZTREESHAD', 'ZTYPEGLASS', 'ZUGASHERE', 'ZWALLTYPE', 'ZWINDOWS', 'ZWINFRAME', 'ZYEARMADERANGE', 'ZTOTROOMS', 'ZTYPEHUQ', 'ZSTUDIO']}
# state to price mapper
price_per_state = {'Alabama': 0.1483, 'Alaska': 0.245, 'Arizona': 0.1439, 'Arkansas': 0.1267, 'California': 0.2999, 'Colorado': 0.1503, 'Connecticut': 0.2925, 'Delaware': 0.1583, 'District of Columbia': 0.1628, 'Florida': 0.1551, 'Georgia': 0.1401, 'Hawaii': 0.4152, 'Idaho': 0.116, 'Illinois': 0.1479, 'Indiana': 0.141, 'Iowa': 0.1403, 'Kansas': 0.1346, 'Kentucky': 0.1243, 'Louisiana': 0.1139, 'Maine': 0.2686, 'Maryland': 0.1696, 'Massachusetts': 0.28, 'Michigan': 0.1935, 'Minnesota': 0.1529, 'Mississippi': 0.1305, 'Missouri': 0.1423, 'Montana': 0.1318, 'Nebraska': 0.1239, 'Nevada': 0.1694, 'New Hampshire': 0.2331, 'New Jersey': 0.1802, 'New Mexico': 0.1525, 'New York': 0.2323, 'North Carolina': 0.1409, 'North Dakota': 0.1277, 'Ohio': 0.1568, 'Oklahoma': 0.1325, 'Oregon': 0.1313, 'Pennsylvania': 0.1801, 'Rhode Island': 0.2694, 'South Carolina': 0.1452, 'South Dakota': 0.1305, 'Tennessee': 0.1185, 'Texas': 0.1458, 'Utah': 0.1185, 'Vermont': 0.2121, 'Virginia': 0.1479, 'Washington': 0.1138, 'West Virginia': 0.1438, 'Wisconsin': 0.1732, 'Wyoming': 0.1264}
# breakdown per state in quartiles
breakdown_per_state={'Alabama': [1560.0, 8860.0, 13260.0, 17910.0, 37120.0], 'Alaska': [1450.0, 4330.0, 6810.0, 10090.0, 25870.0], 'Arizona': [1430.0, 8300.0, 12630.0, 17690.0, 34520.0], 'Arkansas': [1300.0, 8560.0, 12150.0, 16970.0, 37100.0], 'California': [1190.0, 3800.0, 5870.0, 8910.0, 31610.0], 'Colorado': [1250.0, 4910.0, 7360.0, 11220.0, 30970.0], 'Connecticut': [1230.0, 4680.0, 7280.0, 10720.0, 30280.0], 'Delaware': [1200.0, 7190.0, 10100.0, 14300.0, 35390.0], 'District of Columbia': [1420.0, 4330.0, 6410.0, 9570.0, 23250.0], 'Florida': [1430.0, 8910.0, 12750.0, 17880.0, 36260.0], 'Georgia': [2000.0, 8280.0, 12400.0, 16950.0, 37150.0], 'Hawaii': [1190.0, 4740.0, 7640.0, 11420.0, 36880.0], 'Idaho': [1550.0, 6600.0, 9690.0, 14470.0, 36800.0], 'Illinois': [1230.0, 5010.0, 7910.0, 11230.0, 32860.0], 'Indiana': [1850.0, 6570.0, 10010.0, 15150.0, 37710.0], 'Iowa': [1920.0, 6260.0, 9260.0, 13250.0, 35060.0], 'Kansas': [1240.0, 6480.0, 10390.0, 13750.0, 34370.0], 'Kentucky': [1520.0, 8220.0, 12150.0, 17660.0, 35230.0], 'Louisiana': [2360.0, 9870.0, 13940.0, 18420.0, 36940.0], 'Maine': [1520.0, 4500.0, 6580.0, 9200.0, 32060.0], 'Maryland': [1910.0, 6900.0, 10130.0, 15380.0, 37410.0], 'Massachusetts': [1210.0, 4610.0, 6660.0, 10450.0, 32370.0], 'Michigan': [1210.0, 5180.0, 7420.0, 10580.0, 37830.0], 'Minnesota': [1210.0, 5500.0, 8470.0, 12020.0, 36280.0], 'Mississippi': [2520.0, 9440.0, 13250.0, 18720.0, 32940.0], 'Missouri': [1740.0, 7400.0, 10990.0, 15630.0, 34030.0], 'Montana': [1360.0, 4910.0, 8320.0, 12800.0, 36230.0], 'Nebraska': [1220.0, 6300.0, 9920.0, 14160.0, 35490.0], 'Nevada': [2610.0, 7040.0, 9930.0, 14190.0, 35450.0], 'New Hampshire': [1220.0, 4560.0, 6630.0, 9980.0, 24320.0], 'New Jersey': [1350.0, 5250.0, 7780.0, 11400.0, 30600.0], 'New Mexico': [1340.0, 4930.0, 7530.0, 10390.0, 24100.0], 'New York': [1190.0, 4080.0, 6380.0, 9770.0, 37860.0], 'North Carolina': [1700.0, 7980.0, 11820.0, 15580.0, 37460.0], 'North Dakota': [1260.0, 6860.0, 10280.0, 15460.0, 37440.0], 'Ohio': [1380.0, 6060.0, 9050.0, 13720.0, 38010.0], 'Oklahoma': [1350.0, 8150.0, 11970.0, 18000.0, 37040.0], 'Oregon': [1230.0, 6580.0, 9700.0, 14480.0, 34600.0], 'Pennsylvania': [1370.0, 5630.0, 9170.0, 13630.0, 36920.0], 'Rhode Island': [1290.0, 4460.0, 7000.0, 9210.0, 27050.0], 'South Carolina': [1720.0, 8320.0, 12130.0, 17070.0, 33860.0], 'South Dakota': [1910.0, 6140.0, 9720.0, 14750.0, 33350.0], 'Tennessee': [1880.0, 9490.0, 12840.0, 17650.0, 37630.0], 'Texas': [1500.0, 8700.0, 12670.0, 17460.0, 37410.0], 'Utah': [1870.0, 6230.0, 8970.0, 11800.0, 29770.0], 'Vermont': [1300.0, 4210.0, 6380.0, 9130.0, 22660.0], 'Virginia': [1200.0, 7880.0, 11920.0, 16610.0, 35610.0], 'Washington': [1230.0, 6460.0, 9740.0, 14140.0, 37560.0], 'West Virginia': [1560.0, 8160.0, 11190.0, 18630.0, 37930.0], 'Wisconsin': [1770.0, 5640.0, 7350.0, 10850.0, 29670.0], 'Wyoming': [1190.0, 5090.0, 7860.0, 11750.0, 32540.0]}

########## separate features by type ##############

geo_features = ['state_name']#, 'REGIONC'] # inferred

selectbox_features=[]
numeric_features=['NCOMBATH', 'NHAFBATH', 'TOTROOMS', 'NUMFRIG', 'MICRO', 'TVCOLOR', 'DESKTOP', 'NUMLAPTOP', 'LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'NHSLDMEM', 'SQFTEST']
numeric_features_dropdown = ['NUMPORTEL'] # numeric
#num_checkbox_features = ['TYPEHUQ', 'STORIES', 'YEARMADERANGE', 'WALLTYPE', 'ROOFTYPE', 'WINDOWS', 'SWIMPOOL', 'DISHWASH', 'CWASHER', 'DRYER', 'TELLWORK', 'HEATHOME', 'EQUIPM', 'AIRCOND', 'SMARTMETER', 'SOLAR']
num_checkbox_features = ['YEARMADERANGE', 'EQUIPM', 'WINDOWS', 'ROOFTYPE', 'WALLTYPE', 'TYPEHUQ', 'STORIES']


# features with yes or no get a toggle
yes_no_features = ['SWIMPOOL', 'DISHWASH', 'CWASHER', 'DRYER', 'TELLWORK', 'HEATHOME', 'AIRCOND', 'SMARTMETER', 'SOLAR']

########### dictionary of mappings ################

#mapped_features = {'TYPEHUQ': {'Mobile home': '1', 'Single-family house detached from any other house ': '2', 'Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)': '3', 'Apartment in a building with 2 to 4 units': '4', 'Apartment in a building with 5 or more units': '5'}, 'STORIES': {'One story': '1', 'Two stories': '2', 'Three stories': '3', 'Four or more stories': '4', 'Split-level': '5'}, 'YEARMADERANGE': {'Before 1950': '1', '1950 to 1959': '2', '1960 to 1969': '3', '1970 to 1979': '4', '1980 to 1989': '5', '1990 to 1999': '6', '2000 to 2009': '7', '2010 to 2015': '8', '2016 to 2020': '9'}, 'WALLTYPE': {'Brick': '1', 'Wood': '2', 'Siding (aluminum, fiber cement, vinyl, or steel) ': '3', 'Stucco': '4', 'Shingle (composition)': '5', 'Stone ': '6', 'Concrete block ': '7', 'Other': '99'}, 'ROOFTYPE': {'Ceramic or clay tiles': '1', 'Wood shingles/shakes': '2', 'Metal': '3', 'Slate or synthetic slate': '4', 'Shingles (composition or asphalt)': '5', 'Concrete tiles': '6', 'Other': '99'}, 'WINDOWS': {'1 or 2 windows': '1', '3 to 5 windows': '2', '6 to 9 windows': '3', '10 to 15 windows': '4', '16 to 19 windows': '5', '20 to 29 windows': '6', '30 or more windows': '7'}, 'SWIMPOOL': {'Yes': '1', 'No': '0'}, 'DISHWASH': {'Yes': '1', 'No': '0'}, 'CWASHER': {'Yes': '1', 'No': '0'}, 'DRYER': {'Yes': '1', 'No': '0'}, 'TELLWORK': {'Yes': '1', 'No': '0'}, 'HEATHOME': {'Yes': '1', 'No': '0'}, 'EQUIPM': {'Central furnace ': '3', 'Steam or hot water system with radiators or pipes ': '2', 'Central heat pump': '4', 'Ductless heat pump, also known as a “mini-split”': '13', 'Built-in electric units installed in walls, ceilings, baseboards, or floors': '5', 'Built-in room heater burning gas or oil': '7', 'Wood or pellet stove ': '8', 'Portable electric heaters': '10', 'Other ': '99'}, 'AIRCOND': {'Yes': '1', 'No': '0'}, 'SMARTMETER': {'Yes': '1', 'No': '0'}, 'SOLAR': {'Yes': '1', 'No': '0'}, 'NUMPORTEL': {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}}
mapped_features = {'TYPEHUQ': {'Mobile home': '1', 'Single-family house detached from any other house ': '2', 'Single-family house attached to one or more other houses': '3', 'Apartment in a building with 2 to 4 units': '4', 'Apartment in a building with 5 or more units': '5'}, 'STORIES': {'One story': '1', 'Two stories': '2', 'Three stories': '3', 'Four or more stories': '4', 'Split-level': '5'}, 'YEARMADERANGE': {'Before 1950': '1', '1950 to 1959': '2', '1960 to 1969': '3', '1970 to 1979': '4', '1980 to 1989': '5', '1990 to 1999': '6', '2000 to 2009': '7', '2010 to 2015': '8', '2016 to 2020': '9'}, 'WINDOWS': {'1 or 2 windows': '1', '3 to 5 windows': '2', '6 to 9 windows': '3', '10 to 15 windows': '4', '16 to 19 windows': '5', '20 to 29 windows': '6', '30 or more windows': '7'}, 'SWIMPOOL': {'Yes': '1', 'No': '0'}, 'DISHWASH': {'Yes': '1', 'No': '0'}, 'CWASHER': {'Yes': '1', 'No': '0'}, 'DRYER': {'Yes': '1', 'No': '0'}, 'TELLWORK': {'Yes': '1', 'No': '0'}, 'HEATHOME': {'Yes': '1', 'No': '0'}, 'EQUIPM': {'Central furnace ': '3', 'Steam or hot water system': '2', 'Central heat pump': '4', 'Ductless heat pump': '13', 'Built-in electric units': '5', 'Built-in room heater': '7', 'Wood or pellet stove ': '8', 'Portable electric heaters': '10', 'Other ': '99'}, 'AIRCOND': {'Yes': '1', 'No': '0'}, 'SMARTMETER': {'Yes': '1', 'No': '0'}, 'SOLAR': {'Yes': '1', 'No': '0'}, 'NUMPORTEL': {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}}

############# default values (and indices) #########

## numeric features defaults
defaults_numeric = {'NCOMBATH': 2, 'TOTROOMS': 6, 'NUMFRIG': 1, 'MICRO': 1, 'TVCOLOR': 2, 'DESKTOP': 0, 'LGTIN1TO4': 4, 'NHSLDMEM': 2, 'SQFTEST': 1530}
# indices of most frequent categorical value
categorical_defaults = {'NUMPORTEL': 0, 'TYPEHUQ': 1, 'STORIES': 0, 'YEARMADERANGE': 3, 'WINDOWS': 3, 'SWIMPOOL': 1, 'DISHWASH': 0, 'CWASHER': 0, 'DRYER': 0, 'TELLWORK': 1, 'HEATHOME': 0, 'EQUIPM': 0, 'AIRCOND': 0, 'SMARTMETER': 1, 'SOLAR': 1}
# boolean defaults for toggle features
binary_defaults={'SWIMPOOL': False, 'DISHWASH': True, 'CWASHER': True, 'DRYER': True, 'TELLWORK': False, 'HEATHOME': True, 'AIRCOND': True, 'SMARTMETER': False, 'SOLAR': False}


############ features by section ########

appliance_features = ['DESKTOP','NUMLAPTOP','TVCOLOR','LGTIN1TO4','LGTIN4TO8','LGTINMORE8'] + ['DISHWASH','MICRO','NUMFRIG', 'CWASHER','DRYER'] + ['AIRCOND','EQUIPM','HEATHOME' , 'NUMPORTEL']


############# functions ############

@st.cache_data
def make_numeric_input(feature):
    """
    Convert a categorical feature to numeric input parameters.

    Parameters:
    - feature (str): The categorical feature for which numeric input parameters are to be generated.

    Returns:
    tuple: A tuple containing the following numeric input parameters:
        - label (str): The label associated with the input feature.
        - min_value (int): The minimum numeric value associated with the feature.
        - max_value (int): The maximum numeric value associated with the feature.
        - default_value (int): The default numeric value for the feature, if available.
    """
    label = label_dict.get(feature)
    min_value, max_value = (int(val) for val in values_dict.get(feature).split('-'))
    return label, min_value, max_value, defaults_numeric.get(feature)


#def record_user_input(feature):
#    """
#    This function creates an input widget for a feature
#    Depending on which type the feature is.
#    It will write the user input value into params dictionary.
#    """
#    ##### geography features ######
#    if feature=='state_name':
#        state_postal = st.selectbox('Select your state :earth_americas:', states.keys(), 4)
#        params['state_name'] = states.get(state_postal)
#        params['PRICEKWH'] = price_per_state.get(params['state_name'])
#        #params['REGIONC'] = state_to_region.get(params['state_name'])
#        params['BA_climate'] = climate_dict.get(params['state_name'])
#
#    ##### hard-coded features #####
#    elif feature in ['NHAFBATH','NUMLAPTOP','LGTIN4TO8','LGTINMORE8', 'SMARTMETER']:
#        params[feature]=0
#
#    ##### yes - no features #####
#    elif feature in yes_no_features:
#        params[feature] = int(st.toggle(label=label_dict.get(feature)
#                                        , value=binary_defaults.get(feature)))
#
#    ##### features that need a dropdown text #####
#    elif feature in selectbox_features:
#        params[feature] = st.selectbox(label = label_dict.get(feature),
#                                    options= values_dict.get(feature).split('\n'))
#    ##### features with purely numeric input #####
#    elif feature in numeric_features:
#        params[feature] = int(st.number_input(*make_numeric_input(feature)))
#
#    ##### features where dropdown input is transferred to numeric #####
#    elif feature in num_checkbox_features:
#        user_value = st.radio(label=label_dict.get(feature),
#                                  options=mapped_features.get(feature).keys()
#                                  , index = categorical_defaults.get(feature))
#        params[feature] = int(mapped_features.get(feature).get(user_value))
#
#    ##### features which have both numeric range and text #####
#    # TODO get rid of them, we impute the text values anyway
#    elif feature in numeric_features_dropdown:
#        user_value = st.selectbox(label=label_dict.get(feature),
#                                  options=mapped_features.get(feature).keys())
#        params[feature] = int(mapped_features.get(feature).get(user_value))
#
def record_user_input_2(feature: str = None, input_type: str = None):
    """
    Records user input based on the specified feature and input type.

    Parameters:
    - feature (str): The feature for which user input is recorded.
    - input_type (str): The type of input method to be used. Possible values include:
        - "selectbox": Handle input with a selectbox (dropdown).
        - "radio": Handle input with radio buttons (single-select).
        - "number_input": Handle input with a numeric input field.
        - "toggle": Handle input with a toggle switch (0/1 switch).

    Returns:
    None
    """
    if feature == 'state_name':
        # Handle state_name input:flag-us:
        state_postal = st.selectbox('Select your state :flag-us:', sorted(states.keys()), 4)
        params['state_name'] = states.get(state_postal)
        params['PRICEKWH'] = price_per_state.get(params['state_name'])
        params['BA_climate'] = climate_dict.get(params['state_name'])
    elif feature in ['NHAFBATH', 'NUMLAPTOP', 'LGTIN4TO8', 'LGTINMORE8', 'SMARTMETER']:
        # Set default to 0 for specific features
        params[feature] = 0
    elif feature == "NUMPORTEL":
        # Handle NUMPORTEL input using a selectbox
        user_value = st.selectbox(label=label_dict.get(feature),
                                  options=mapped_features.get(feature).keys())
        params[feature] = int(mapped_features.get(feature).get(user_value))
    elif input_type == "selectbox" or input_type == "radio":
        # Handle selectbox (dropdown) or radio (single-select) input type
        options = None
        index = None

        if feature in num_checkbox_features:
            options = mapped_features.get(feature).keys()
            index = categorical_defaults.get(feature)

        elif feature in values_dict:
            options = values_dict.get(feature).split('\n')

        elif feature in mapped_features:
            options = mapped_features.get(feature).keys()

        if options is not None:
            user_value = st.selectbox(label=label_dict.get(feature),
                                      options=options,
                                      index=index)
            params[feature] = int(mapped_features.get(feature).get(user_value))
    elif input_type == "number_input":
        # Handle number_input (enter a num) input type
        params[feature] = int(st.number_input(*make_numeric_input(feature)))
    elif input_type == "toggle":
        # Handle toggle (0/1 switch) input type
        params[feature] = int(st.toggle(label=label_dict.get(feature),
                                        value=binary_defaults.get(feature)))

############## tabs - organize features by sections ###############

tab_main, tab_household, tab_appliances, tab_results = st.tabs([

                                                    'About your home'
                                                   ,'Household characteristics'
                                                    ,'Appliances'
                                                    ,'Results'
                                                    ]) #, tab_admin

#############################################
############### user input ##################
#############################################

###### section Main: GEOGRAPHY, ADMIN, basic household (type, no. of persons) ##########

with tab_main:

    st.subheader('About your home')

    c1, c2 = st.columns(2)

    with c1:
        #st.markdown(':red[Your house] :house_buildings:')
        record_user_input_2('TYPEHUQ', 'radio')
        #st.markdown(':red[House area] :european_castle:')
        record_user_input_2('SQFTEST', 'number_input')

    with c2:
        #st.markdown(':red[Your people] 👨‍👩‍👧‍👧')
        record_user_input_2('NHSLDMEM', 'number_input')

        #st.markdown(':red[Your location] :world_map:')
        record_user_input_2('state_name', 'selectbox')


###### section HOUSEHOLD CHARACTERISTICS ######
with tab_household:
    st.subheader('Your household')

    col1, col2 = st.columns(2)

    with col1:

        record_user_input_2('TOTROOMS', 'number_input')
        for feature in ['STORIES','YEARMADERANGE']:
            record_user_input_2(feature, 'selectbox')
        record_user_input_2('HEATHOME', 'toggle')

    with col2:
        record_user_input_2('SMARTMETER', 'toggle')
        for feature in ['NCOMBATH', 'NHAFBATH']:
            record_user_input_2(feature, 'number_input')
        for feature in ['EQUIPM', 'WINDOWS']:
            record_user_input_2(feature, 'selectbox')
        record_user_input_2('SWIMPOOL', 'toggle')

with tab_appliances:
    st.subheader('Appliances')

    col1, col2 = st.columns(2)

    with col1:
        for feature in ['DESKTOP','NUMLAPTOP', 'MICRO']:
            record_user_input_2(feature, 'number_input')
        record_user_input_2('NUMPORTEL', 'selectbox')
        for feature in ['CWASHER','AIRCOND']:
            record_user_input_2(feature, 'toggle')

    with col2:
        for feature in ['TVCOLOR','NUMFRIG']:
            record_user_input_2(feature, 'number_input')
        for feature in ['LGTIN1TO4','LGTIN4TO8','LGTINMORE8']:
            record_user_input_2(feature, 'number_input')
        for feature in ['DRYER','DISHWASH']:
            record_user_input_2(feature, 'toggle')

with st.sidebar:
        toggle_state = st.toggle('Monthly')
        user_price = params['PRICEKWH']
        if st.button('Estimate my consumption'
                     , help = '''Estimate my consumption'''
                     , type = 'primary'):
            pred_kwh, pred_kwh_filter = calculate()
            if params["state_name"] == "Alaska":
                st.snow()
            else:
                st.balloons()
            formatted_pred_kwh_cli = int(pred_kwh)
            formatted_number_cli = int(pred_kwh)*user_price
            formatted_number = "{:.2f}".format(int(pred_kwh)*user_price)

            kwh_est = st.metric(label=f'Your estimated {pred_kwh_filter} consumption:', #\n
                          value = f'{int(pred_kwh)} kWh', #
                         delta = None)

            cost_est = st.metric(label=f'Your estimated {pred_kwh_filter} cost:', #\n
                value = f'${formatted_number}', #
                delta = None)

            with tab_results:
            ############# callback to calculate kWh ################
                ci = 0.08
                lower_bound = 1-ci
                upper_bound = 1+ci

                if toggle_state:
                    col1, col2 = st.columns(2)

                    with col1:

                        st.metric(label=f'Your estimated {pred_kwh_filter} consumption:', #\n
                                value = f'{int(pred_kwh)} kWh', #
                                delta = None)
                        st.markdown(f'''Estimate between: {int(round(formatted_pred_kwh_cli*lower_bound,-1))} - {int(round(formatted_pred_kwh_cli*upper_bound,-1))} kWh.''')
                    with col2:
                        formatted_number = "{:.2f}".format(int(pred_kwh)*user_price)
                        st.metric(label=f'Your estimated {pred_kwh_filter} cost:', #\n
                                value = f'${formatted_number}', #
                                delta = None)
                        st.markdown(f'''Estimated between: \${round(formatted_number_cli*lower_bound)}.00 - \${round(formatted_number_cli*upper_bound)}.00''')

                else:
                    col1, col2 = st.columns(2)

                    with col1:
                        st.metric(label=f'Your estimated {pred_kwh_filter} consumption:', #\n
                                value = f'{int(pred_kwh)} kWh', #
                                delta = None)
                        st.markdown(f'''Estimate between: {int(round(formatted_pred_kwh_cli*lower_bound,-1))} - {int(round(formatted_pred_kwh_cli*upper_bound,-1))} kWh.''')


                    with col2:
                        formatted_number = "{:.2f}".format(int(pred_kwh)*user_price)
                        st.metric(label=f'Your estimated {pred_kwh_filter} cost:', #\n
                                value = f'${formatted_number}', #
                                delta = None)
                        st.markdown(f'''Estimated between: \${round(formatted_number_cli*lower_bound)}.00 - \${round(formatted_number_cli*upper_bound)}.00''')

                # Plotting the energy scale
                st.subheader(f"Energy Consumption Quartiles for {params['state_name']}")
                st.pyplot(plot_energy_scale(int(pred_kwh), params['state_name'], pred_kwh_filter))
