import requests
import streamlit as st
import pandas as pd

########## page info ############

st.set_page_config(page_title='U.S. household electricity consumption'
                   , page_icon='🏠')




'''
# U.S. Household Energy Consumption
# 🇺🇸🏠


This application will estimate your yearly energy consumption (in kWh).

'''


############ initiate parameters for API request ############
params={}

############### API ###########################

## test of the API to docker container on the cloud
#test_params = {'state_name': 'TX'}
#url='https://householdpredictions-jaiabuy6eq-ew.a.run.app/predict'

url='https://household-predictions-api-jaiabuy6eq-ew.a.run.app/predict'

#@st.cache_data(ttl=3600) # cache data for 1 hour
def api_call(url, params):
    response=requests.get(url,params).json()
    #output prediction:
    return response.get("KWH")


########### hard-coded constants ###############

label_dict = {'REGIONC': 'Census Region', 'state_name': 'State Name', 'BA_climate': 'Building America Climate Zone', 'TYPEHUQ': 'Type of housing unit', 'STORIES': 'Number of stories in a single-family home', 'YEARMADERANGE': 'Range when housing unit was built', 'NCOMBATH': 'Number of full bathrooms (top-coded)', 'NHAFBATH': 'Number of half bathrooms (top-coded)', 'TOTROOMS': 'Total number of rooms in the housing unit, excluding bathrooms; a derived variable', 'WALLTYPE': 'Major outside wall material', 'ROOFTYPE': "Major roofing material; 'Not applicable' applies to apartment buildings with 5 or more units", 'WINDOWS': 'Number of windows', 'SWIMPOOL': 'Has swimming pool', 'NUMFRIG': 'Number of refrigerators used', 'MICRO': 'Number of microwaves ', 'DISHWASH': 'Has dishwasher', 'CWASHER': 'Has clothes washer in home', 'DRYER': 'Has clothes dryer in home', 'TVCOLOR': 'Number of televisions used', 'DESKTOP': 'Number of desktop computers used', 'NUMLAPTOP': 'Number of laptop computers used', 'TELLWORK': 'Any household member teleworking', 'HEATHOME': 'Space heating equipment used', 'EQUIPM': 'Main space heating equipment type', 'NUMPORTEL': 'Number of portable electric heaters used', 'AIRCOND': 'Air conditioning equipment used', 'LGTIN1TO4': 'Number of inside light bulbs turned on 1 to 4 hours per day', 'LGTIN4TO8': 'Number of inside light bulbs turned on 4 to 8 hours per day', 'LGTINMORE8': 'Number of inside light bulbs turned on more than 8 hours per day', 'SMARTMETER': 'Home has an electricity smart meter', 'SOLAR': "On-site electricity generation from solar; 'Not applicable' applies to apartment buildings with 2 or more units.", 'NHSLDMEM': 'Number of household members (top-coded)', 'SQFTEST': 'Respondent-reported square footage (rounded to the nearest 10)'}
values_dict = {'REGIONC': 'Midwest\nNortheast\nSouth\nWest', 'state_name': 'state_dictionary!A1', 'BA_climate': 'Cold\nHot-Dry\nHot-Humid\nMarine\nMixed-Dry\nMixed-Humid\nSubarctic\nVery-Cold', 'TYPEHUQ': '1 Mobile home\n2 Single-family house detached from any other house \n3 Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)\n4 Apartment in a building with 2 to 4 units\n5 Apartment in a building with 5 or more units', 'STORIES': '1 One story\n2 Two stories\n3 Three stories\n4 Four or more stories\n5 Split-level\n-2 Not applicable', 'YEARMADERANGE': '1 Before 1950\n2 1950 to 1959\n3 1960 to 1969\n4 1970 to 1979\n5 1980 to 1989\n6 1990 to 1999\n7 2000 to 2009\n8 2010 to 2015\n9 2016 to 2020', 'NCOMBATH': '0 - 4', 'NHAFBATH': '0 - 2', 'TOTROOMS': '1-15', 'WALLTYPE': '1 Brick\n2 Wood\n3 Siding (aluminum, fiber cement, vinyl, or steel) \n4 Stucco\n5 Shingle (composition)\n6 Stone \n7 Concrete block \n99 Other', 'ROOFTYPE': '1 Ceramic or clay tiles\n2 Wood shingles/shakes\n3 Metal\n4 Slate or synthetic slate\n5 Shingles (composition or asphalt)\n6 Concrete tiles\n99 Other\n-2 Not applicable', 'WINDOWS': '1 1 or 2 windows\n2 3 to 5 windows\n3 6 to 9 windows\n4 10 to 15 windows\n5 16 to 19 windows\n6 20 to 29 windows\n7 30 or more windows', 'SWIMPOOL': '1 Yes\n0 No\n-2 Not applicable', 'NUMFRIG': '0 - 9', 'MICRO': '0 - 3', 'DISHWASH': '1 Yes\n0 No', 'CWASHER': '1 Yes\n0 No', 'DRYER': '1 Yes\n0 No', 'TVCOLOR': '0 - 14', 'DESKTOP': '0 - 8', 'NUMLAPTOP': '0 - 20', 'TELLWORK': '1 Yes\n0 No', 'HEATHOME': '1 Yes\n0 No', 'EQUIPM': '3 Central furnace \n2 Steam or hot water system with radiators or pipes \n4 Central heat pump\n13 Ductless heat pump, also known as a “mini-split”\n5 Built-in electric units installed in walls, ceilings, baseboards, or floors\n7 Built-in room heater burning gas or oil\n8 Wood or pellet stove \n10 Portable electric heaters\n99 Other \n-2 Not applicable', 'NUMPORTEL': '1 - 9\n-2 Not applicable', 'AIRCOND': '1 Yes\n0 No', 'LGTIN1TO4': '0 - 90', 'LGTIN4TO8': '0 - 84', 'LGTINMORE8': '0 - 99', 'SMARTMETER': "1 Yes\n0 No\n-4 Don't Know", 'SOLAR': '1 Yes\n0 No\n-2 Not applicable', 'NHSLDMEM': '1 - 7', 'SQFTEST': '240-15000'}
# U.S. states selector
states ={'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California', 'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'DC': 'District of Columbia', 'FL': 'Florida', 'GA': 'Georgia', 'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas', 'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts', 'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana', 'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico', 'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma', 'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina', 'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont', 'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming'}
# state to region mapper
state_to_region={'New Mexico': 'WEST', 'Arkansas': 'SOUTH', 'South Carolina': 'SOUTH', 'New Jersey': 'NORTHEAST', 'Texas': 'SOUTH', 'Oklahoma': 'SOUTH', 'Mississippi': 'SOUTH', 'District of Columbia': 'SOUTH', 'Arizona': 'WEST', 'California': 'WEST', 'Louisiana': 'SOUTH', 'Minnesota': 'MIDWEST', 'Vermont': 'NORTHEAST', 'Rhode Island': 'NORTHEAST', 'Illinois': 'MIDWEST', 'Maine': 'NORTHEAST', 'South Dakota': 'MIDWEST', 'Massachusetts': 'NORTHEAST', 'Florida': 'SOUTH', 'Ohio': 'MIDWEST', 'Nebraska': 'MIDWEST', 'Virginia': 'SOUTH', 'Wyoming': 'WEST', 'Pennsylvania': 'NORTHEAST', 'Hawaii': 'WEST', 'New Hampshire': 'NORTHEAST', 'Michigan': 'MIDWEST', 'Maryland': 'SOUTH', 'New York': 'NORTHEAST', 'Colorado': 'WEST', 'North Carolina': 'SOUTH', 'Kentucky': 'SOUTH', 'North Dakota': 'MIDWEST', 'Georgia': 'SOUTH', 'West Virginia': 'SOUTH', 'Oregon': 'WEST', 'Missouri': 'MIDWEST', 'Utah': 'WEST', 'Connecticut': 'NORTHEAST', 'Tennessee': 'SOUTH', 'Wisconsin': 'MIDWEST', 'Idaho': 'WEST', 'Nevada': 'WEST', 'Washington': 'WEST', 'Indiana': 'MIDWEST', 'Delaware': 'SOUTH', 'Iowa': 'MIDWEST', 'Alaska': 'WEST', 'Alabama': 'SOUTH', 'Montana': 'WEST', 'Kansas': 'MIDWEST'}
# state to most frequent climate mapper
climate_dict = {'Alabama': 'Hot-Humid', 'Alaska': 'Subarctic', 'Arizona': 'Cold', 'Arkansas': 'Hot-Humid', 'California': 'Cold', 'Colorado': 'Cold', 'Connecticut': 'Cold', 'Delaware': 'Mixed-Humid', 'District of Columbia': 'Mixed-Humid', 'Florida': 'Hot-Humid', 'Georgia': 'Hot-Humid', 'Hawaii': 'Hot-Humid', 'Idaho': 'Cold', 'Illinois': 'Cold', 'Indiana': 'Cold', 'Iowa': 'Cold', 'Kansas': 'Cold', 'Kentucky': 'Mixed-Humid', 'Louisiana': 'Hot-Humid', 'Maine': 'Cold', 'Maryland': 'Cold', 'Massachusetts': 'Cold', 'Michigan': 'Cold', 'Minnesota': 'Cold', 'Mississippi': 'Hot-Humid', 'Missouri': 'Cold', 'Montana': 'Cold', 'Nebraska': 'Cold', 'Nevada': 'Cold', 'New Hampshire': 'Cold', 'New Jersey': 'Cold', 'New Mexico': 'Cold', 'New York': 'Cold', 'North Carolina': 'Cold', 'North Dakota': 'Cold', 'Ohio': 'Cold', 'Oklahoma': 'Mixed-Humid', 'Oregon': 'Cold', 'Pennsylvania': 'Cold', 'Rhode Island': 'Cold', 'South Carolina': 'Hot-Humid', 'South Dakota': 'Cold', 'Tennessee': 'Mixed-Humid', 'Texas': 'Hot-Dry', 'Utah': 'Cold', 'Vermont': 'Cold', 'Virginia': 'Mixed-Humid', 'Washington': 'Cold', 'West Virginia': 'Cold', 'Wisconsin': 'Cold', 'Wyoming': 'Cold'}
# section to features mapper
section_dict = {'ADMIN': ['DOEID', 'BA_climate', 'IECC_climate_code', 'UATYP10'], 'AIR CONDITIONING': ['AIRCOND', 'COOLAPT', 'ACEQUIPM_PUB', 'ACEQUIPAGE', 'ACEQUIPAUXTYPE_PUB', 'NUMDLHPAC', 'NUMWWAC', 'NUMPORTAC', 'BASECOOL', 'ATTCCOOL', 'GARGCOOL', 'NUMCFAN', 'NUMFLOORFAN', 'USECFAN', 'HOUSEFAN', 'ATTICFAN', 'DEHUMTYPE', 'NUMPORTDEHUM', 'USEDEHUM', 'ELCOOL', 'ZACEQUIPAGE', 'ZAIRCOND', 'ZATTCCOOL', 'ZATTICFAN', 'ZBASECOOL', 'ZCOOLAPT', 'ZCOOLCNTL', 'ZDEHUMTYPE', 'ZGARGCOOL', 'ZHOUSEFAN', 'ZNUMCFAN', 'ZNUMDLHPAC', 'ZNUMFLOORFAN', 'ZNUMPORTAC', 'ZNUMPORTDEHUM', 'ZNUMWWAC', 'ZUSECFAN', 'ZUSEDEHUM', 'ZACEQUIPM_PUB', 'ZACEQUIPAUXTYPE_PUB'], 'APPLIANCES': ['NUMFRIG', 'SIZRFRI1', 'TYPERFR1', 'AGERFRI1', 'ICE', 'SIZRFRI2', 'TYPERFR2', 'AGERFRI2', 'LOCRFRI2', 'WINECHILL', 'NUMFREEZ', 'UPRTFRZR', 'SIZFREEZ', 'FREEZER', 'AGEFRZR', 'RANGE', 'COOKTOP', 'OVEN', 'RANGEFUEL', 'RANGEINDT', 'RCOOKUSE', 'ROVENUSE', 'COOKTOPFUEL', 'COOKTOPINDT', 'COOKTOPUSE', 'OVENFUEL', 'OVENUSE', 'MICRO', 'AMTMICRO', 'OUTGRILLFUEL', 'OUTGRILL', 'NUMMEAL', 'USECOFFEE', 'TOAST', 'TOASTOVN', 'CROCKPOT', 'PRSSCOOK', 'RICECOOK', 'BLENDER', 'APPOTHER', 'ELFOOD', 'LPCOOK', 'UGCOOK', 'DISHWASH', 'DWASHUSE', 'DWCYCLE', 'AGEDW', 'CWASHER', 'TOPFRONT', 'WASHLOAD', 'WASHTEMP', 'AGECWASH', 'DRYER', 'DRYRFUEL', 'DRYRUSE', 'AGECDRYER', 'ZAGECDRYER', 'ZAGECWASH', 'ZAGEDW', 'ZAGEFRZR', 'ZAGERFRI1', 'ZAGERFRI2', 'ZAMTMICRO', 'ZBLENDER', 'ZCOOKTOP', 'ZCOOKTOPFUEL', 'ZCOOKTOPINDT', 'ZCOOKTOPUSE', 'ZCROCKPOT', 'ZCWASHER', 'ZDISHWASH', 'ZDRYER', 'ZDRYRFUEL', 'ZDRYRUSE', 'ZDWASHUSE', 'ZDWCYCLE', 'ZFREEZER', 'ZICE', 'ZLOCRFRI2', 'ZMICRO', 'ZNUMFREEZ', 'ZNUMFRIG', 'ZNUMMEAL', 'ZOUTGRILLFUEL', 'ZOVEN', 'ZOVENFUEL', 'ZOVENUSE', 'ZPRSSCOOK', 'ZRANGE', 'ZRANGEFUEL', 'ZRANGEINDT', 'ZRCOOKUSE', 'ZRICECOOK', 'ZROVENUSE', 'ZSIZFREEZ', 'ZSIZRFRI1', 'ZSIZRFRI2', 'ZTOAST', 'ZTOASTOVN', 'ZTOPFRONT', 'ZTYPERFR1', 'ZTYPERFR2', 'ZUPRTFRZR', 'ZUSECOFFEE', 'ZWASHLOAD', 'ZWASHTEMP', 'ZWINECHILL', 'ZOUTGRILL'], 'ELECTRONICS': ['TVCOLOR', 'TVSIZE1', 'TVTYPE1', 'TVUSE1', 'TVONWD1', 'TVONWE1', 'TVSIZE2', 'TVTYPE2', 'TVUSE2', 'TVONWD2', 'TVONWE2', 'TVSIZE3', 'TVTYPE3', 'TVUSE3', 'TVONWD3', 'TVONWE3', 'CABLESAT', 'COMBODVR', 'SEPDVR', 'INTSTREAM', 'PLAYSTA', 'DVD', 'VCR', 'TVAUDIOSYS', 'DESKTOP', 'NUMLAPTOP', 'NUMTABLET', 'ELPERIPH', 'NUMSMPHONE', 'CELLPHONE', 'TELLWORK', 'TELLDAYS', 'TLDESKTOP', 'TLLAPTOP', 'TLTABLET', 'TLMONITOR', 'TLOTHER', 'ONLNEDUC', 'INTERNET', 'INTYPECELL', 'INTYPEBROAD', 'INTYPEOTH', 'SMARTSPK', 'SSLIGHT', 'SSTEMP', 'SSSECURE', 'SSTV', 'SSOTHER', 'ZCABLESAT', 'ZCELLPHONE', 'ZCOMBODVR', 'ZDESKTOP', 'ZDVD', 'ZELPERIPH', 'ZINTERNET', 'ZINTSTREAM', 'ZINTYPEBROAD', 'ZINTYPECELL', 'ZINTYPEOTH', 'ZNUMLAPTOP', 'ZNUMSMPHONE', 'ZNUMTABLET', 'ZONLNEDUC', 'ZPLAYSTA', 'ZSEPDVR', 'ZSMARTSPK', 'ZSSLIGHT', 'ZSSOTHER', 'ZSSSECURE', 'ZSSTEMP', 'ZSSTV', 'ZTELLDAYS', 'ZTELLWORK', 'ZTLDESKTOP', 'ZTLLAPTOP', 'ZTLMONITOR', 'ZTLOTHER', 'ZTLTABLET', 'ZTVAUDIOSYS', 'ZTVCOLOR', 'ZTVONWD1', 'ZTVONWD2', 'ZTVONWD3', 'ZTVONWE1', 'ZTVONWE2', 'ZTVONWE3', 'ZTVSIZE1', 'ZTVSIZE2', 'ZTVSIZE3', 'ZTVTYPE1', 'ZTVTYPE2', 'ZTVTYPE3', 'ZTVUSE1', 'ZTVUSE2', 'ZTVUSE3', 'ZVCR'], 'ENERGY ASSISTANCE': ['SCALEB', 'SCALEG', 'SCALEE', 'PAYHELP', 'NOHEATBROKE', 'NOHEATEL', 'NOHEATNG', 'NOHEATBULK', 'NOHEATDAYS', 'NOHEATHELP', 'COLDMA', 'NOACBROKE', 'NOACEL', 'NOACDAYS', 'NOACHELP', 'HOTMA', 'ENERGYASST', 'ENERGYASST20', 'ENERGYASST19', 'ENERGYASST18', 'ENERGYASST17', 'ENERGYASST16', 'ENERGYASSTOTH', 'ZCOLDMA', 'ZENERGYASST', 'ZENERGYASST16', 'ZENERGYASST17', 'ZENERGYASST18', 'ZENERGYASST19', 'ZENERGYASST20', 'ZENERGYASSTOTH', 'ZHOTMA', 'ZNOACBROKE', 'ZNOACDAYS', 'ZNOACEL', 'ZNOACHELP', 'ZNOHEATBROKE', 'ZNOHEATBULK', 'ZNOHEATDAYS', 'ZNOHEATEL', 'ZNOHEATHELP', 'ZNOHEATNG', 'ZPAYHELP', 'ZSCALEB', 'ZSCALEE', 'ZSCALEG'], 'ENERGY BILLS': ['ELPAY', 'NGPAY', 'LPGPAY', 'FOPAY', 'SMARTMETER', 'INTDATAACC', 'MEDICALDEV', 'POWEROUT', 'WHYPOWEROUT', 'BACKUP', 'SOLAR', 'OUTLET', 'ELECVEH', 'EVCHRGHOME', 'ELOTHER', 'UGOTH', 'LPOTHER', 'FOOTHER', 'USEEL', 'USENG', 'USELP', 'USEFO', 'USESOLAR', 'USEWOOD', 'ALLELEC', 'ZBACKUP', 'ZELPAY', 'ZFOPAY', 'ZLPGPAY', 'ZNGPAY', 'ZOUTLET', 'ZPOWEROUT', 'ZWHYPOWEROUT'], 'End-use Model': ['KWH', 'BTUEL', 'DOLLAREL', 'ELXBTU', 'PERIODEL', 'ZELAMOUNT', 'KWHSPH', 'KWHCOL', 'KWHWTH', 'KWHRFG', 'KWHRFG1', 'KWHRFG2', 'KWHFRZ', 'KWHCOK', 'KWHMICRO', 'KWHCW', 'KWHCDR', 'KWHDWH', 'KWHLGT', 'KWHTVREL', 'KWHTV1', 'KWHTV2', 'KWHTV3', 'KWHAHUHEAT', 'KWHAHUCOL', 'KWHCFAN', 'KWHDHUM', 'KWHHUM', 'KWHPLPMP', 'KWHHTBPMP', 'KWHHTBHEAT', 'KWHEVCHRG', 'KWHNEC', 'KWHOTH', 'BTUELSPH', 'BTUELCOL', 'BTUELWTH', 'BTUELRFG', 'BTUELRFG1', 'BTUELRFG2', 'BTUELFRZ', 'BTUELCOK', 'BTUELMICRO', 'BTUELCW', 'BTUELCDR', 'BTUELDWH', 'BTUELLGT', 'BTUELTVREL', 'BTUELTV1', 'BTUELTV2', 'BTUELTV3', 'BTUELAHUHEAT', 'BTUELAHUCOL', 'BTUELCFAN', 'BTUELDHUM', 'BTUELHUM', 'BTUELPLPMP', 'BTUELHTBPMP', 'BTUELHTBHEAT', 'BTUELEVCHRG', 'BTUELNEC', 'BTUELOTH', 'DOLELSPH', 'DOLELCOL', 'DOLELWTH', 'DOLELRFG', 'DOLELRFG1', 'DOLELRFG2', 'DOLELFRZ', 'DOLELCOK', 'DOLELMICRO', 'DOLELCW', 'DOLELCDR', 'DOLELDWH', 'DOLELLGT', 'DOLELTVREL', 'DOLELTV1', 'DOLELTV2', 'DOLELTV3', 'DOLELAHUHEAT', 'DOLELAHUCOL', 'DOLELCFAN', 'DOLELDHUM', 'DOLELHUM', 'DOLELPLPMP', 'DOLELHTBPMP', 'DOLELHTBHEAT', 'DOLELEVCHRG', 'DOLELNEC', 'DOLELOTH', 'CUFEETNG', 'BTUNG', 'DOLLARNG', 'NGXBTU', 'PERIODNG', 'ZNGAMOUNT', 'BTUNGSPH', 'BTUNGWTH', 'BTUNGCOK', 'BTUNGCDR', 'BTUNGPLHEAT', 'BTUNGHTBHEAT', 'BTUNGNEC', 'BTUNGOTH', 'CUFEETNGSPH', 'CUFEETNGWTH', 'CUFEETNGCOK', 'CUFEETNGCDR', 'CUFEETNGPLHEAT', 'CUFEETNGHTBHEAT', 'CUFEETNGNEC', 'CUFEETNGOTH', 'DOLNGSPH', 'DOLNGWTH', 'DOLNGCOK', 'DOLNGCDR', 'DOLNGPLHEAT', 'DOLNGHTBHEAT', 'DOLNGNEC', 'DOLNGOTH', 'GALLONLP', 'BTULP', 'DOLLARLP', 'LPXBTU', 'PERIODLP', 'ZLPAMOUNT', 'BTULPSPH', 'BTULPWTH', 'BTULPCOK', 'BTULPCDR', 'BTULPNEC', 'BTULPOTH', 'GALLONLPSPH', 'GALLONLPWTH', 'GALLONLPCOK', 'GALLONLPCDR', 'GALLONLPNEC', 'GALLONLPOTH', 'DOLLPSPH', 'DOLLPWTH', 'DOLLPCOK', 'DOLLPCDR', 'DOLLPNEC', 'DOLLPOTH', 'GALLONFO', 'BTUFO', 'DOLLARFO', 'FOXBTU', 'PERIODFO', 'ZFOAMOUNT', 'BTUFOSPH', 'BTUFOWTH', 'BTUFONEC', 'BTUFOOTH', 'GALLONFOSPH', 'GALLONFOWTH', 'GALLONFONEC', 'GALLONFOOTH', 'DOLFOSPH', 'DOLFOWTH', 'DOLFONEC', 'DOLFOOTH', 'BTUWD', 'ZWDAMOUNT', 'TOTALBTUSPH', 'TOTALDOLSPH', 'TOTALBTUWTH', 'TOTALDOLWTH', 'TOTALBTUOTH', 'TOTALDOLOTH', 'TOTALBTU', 'TOTALDOL'], 'GEOGRAPHY': ['REGIONC', 'DIVISION', 'STATE_FIPS', 'state_postal', 'state_name'], 'HOUSEHOLD CHARACTERISTICS': ['HHSEX', 'HHAGE', 'EMPLOYHH', 'EDUCATION', 'SDESCENT', 'HOUSEHOLDER_RACE', 'NHSLDMEM', 'NUMCHILD', 'NUMADULT1', 'NUMADULT2', 'ATHOME', 'MONEYPY', 'ZATHOME', 'ZEDUCATION', 'ZEMPLOYHH', 'ZHHAGE', 'ZHHSEX', 'ZMONEYPY', 'ZNHSLDMEM', 'ZNUMADULT1', 'ZNUMADULT2', 'ZNUMCHILD', 'ZSDESCENT', 'ZHOUSEHOLDER_RACE'], 'LIGHTING': ['LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'LGTINLED', 'LGTINCFL', 'LGTINCAN', 'LGTOUTANY', 'LGTOUTNITE', 'LGTOUTLED', 'LGTOUTCFL', 'LGTOUTCAN', 'ZLGTIN1TO4', 'ZLGTIN4TO8', 'ZLGTINCAN', 'ZLGTINCFL', 'ZLGTINLED', 'ZLGTINMORE8', 'ZLGTOUTANY', 'ZLGTOUTCAN', 'ZLGTOUTCFL', 'ZLGTOUTLED', 'ZLGTOUTNITE'], 'SPACE HEATING': ['HEATHOME', 'DNTHEAT', 'HEATAPT', 'EQUIPM', 'FUELHEAT', 'EQUIPAGE', 'GEOHP', 'EQUIPAUXTYPE', 'EQUIPAUX', 'FUELAUX', 'USEEQUIPAUX', 'NUMPORTEL', 'NUMFIREPLC', 'NUMDLHP', 'BASEHEAT', 'ATTCHEAT', 'GARGHEAT', 'HUMIDTYPE', 'NUMPORTHUM', 'USEHUMID', 'ELWARM', 'UGWARM', 'LPWARM', 'FOWARM', 'WDWARM', 'ZATTCHEAT', 'ZBASEHEAT', 'ZEQUIPAGE', 'ZEQUIPAUXTYPE', 'ZEQUIPM', 'ZFUELAUX', 'ZFUELHEAT', 'ZGARGHEAT', 'ZHEATAPT', 'ZHEATHOME', 'ZHUMIDTYPE', 'ZNUMDLHP', 'ZNUMFIREPLC', 'ZNUMPORTEL', 'ZNUMPORTHUM', 'ZUSEEQUIPAUX', 'ZUSEHUMID', 'ZDNTHEAT', 'WOODTYPE'], 'THERMOSTAT': ['TYPETHERM', 'HEATCNTL', 'TEMPHOME', 'TEMPGONE', 'TEMPNITE', 'COOLCNTL', 'TEMPHOMEAC', 'TEMPGONEAC', 'TEMPNITEAC', 'ZHEATCNTL', 'ZTEMPGONE', 'ZTEMPGONEAC', 'ZTEMPHOME', 'ZTEMPHOMEAC', 'ZTEMPNITE', 'ZTEMPNITEAC', 'ZTYPETHERM'], 'WATER HEATING': ['H2OAPT', 'H2OMAIN', 'WHEATSIZ', 'WHEATBKT', 'WHEATAGE', 'FUELH2O', 'MORETHAN1H2O', 'FUELH2O2', 'ELWATER', 'FOWATER', 'LPWATER', 'SOLWATER', 'WDWATER', 'UGWATER', 'ZFUELH2O', 'ZFUELH2O2', 'ZH2OAPT', 'ZH2OMAIN', 'ZMORETHAN1H2O', 'ZWHEATAGE', 'ZWHEATBKT', 'ZWHEATSIZ'], 'WEATHER': ['HDD65', 'CDD65', 'HDD30YR_PUB', 'CDD30YR_PUB', 'DBT1', 'DBT99', 'GWT'], 'WEIGHTS': ['NWEIGHT', 'NWEIGHT1', 'NWEIGHT2', 'NWEIGHT3', 'NWEIGHT4', 'NWEIGHT5', 'NWEIGHT6', 'NWEIGHT7', 'NWEIGHT8', 'NWEIGHT9', 'NWEIGHT10', 'NWEIGHT11', 'NWEIGHT12', 'NWEIGHT13', 'NWEIGHT14', 'NWEIGHT15', 'NWEIGHT16', 'NWEIGHT17', 'NWEIGHT18', 'NWEIGHT19', 'NWEIGHT20', 'NWEIGHT21', 'NWEIGHT22', 'NWEIGHT23', 'NWEIGHT24', 'NWEIGHT25', 'NWEIGHT26', 'NWEIGHT27', 'NWEIGHT28', 'NWEIGHT29', 'NWEIGHT30', 'NWEIGHT31', 'NWEIGHT32', 'NWEIGHT33', 'NWEIGHT34', 'NWEIGHT35', 'NWEIGHT36', 'NWEIGHT37', 'NWEIGHT38', 'NWEIGHT39', 'NWEIGHT40', 'NWEIGHT41', 'NWEIGHT42', 'NWEIGHT43', 'NWEIGHT44', 'NWEIGHT45', 'NWEIGHT46', 'NWEIGHT47', 'NWEIGHT48', 'NWEIGHT49', 'NWEIGHT50', 'NWEIGHT51', 'NWEIGHT52', 'NWEIGHT53', 'NWEIGHT54', 'NWEIGHT55', 'NWEIGHT56', 'NWEIGHT57', 'NWEIGHT58', 'NWEIGHT59', 'NWEIGHT60'], 'YOUR HOME': ['TYPEHUQ', 'CELLAR', 'CRAWL', 'CONCRETE', 'BASEOTH', 'BASEFIN', 'ATTIC', 'ATTICFIN', 'STORIES', 'PRKGPLC1', 'SIZEOFGARAGE', 'KOWNRENT', 'YEARMADERANGE', 'BEDROOMS', 'NCOMBATH', 'NHAFBATH', 'OTHROOMS', 'TOTROOMS', 'STUDIO', 'WALLTYPE', 'ROOFTYPE', 'HIGHCEIL', 'DOOR1SUM', 'WINDOWS', 'TYPEGLASS', 'ORIGWIN', 'WINFRAME', 'TREESHAD', 'ADQINSUL', 'DRAFTY', 'UGASHERE', 'SWIMPOOL', 'MONPOOL', 'POOLPUMP', 'FUELPOOL', 'RECBATH', 'MONTUB', 'FUELTUB', 'SQFTEST', 'SQFTRANGE', 'SQFTINCB', 'SQFTINCA', 'SQFTINCG', 'TOTSQFT_EN', 'TOTHSQFT', 'TOTCSQFT', 'ZADQINSUL', 'ZATTIC', 'ZATTICFIN', 'ZBASEFIN', 'ZBASEOTH', 'ZBEDROOMS', 'ZCELLAR', 'ZCONCRETE', 'ZCRAWL', 'ZDOOR1SUM', 'ZDRAFTY', 'ZFUELPOOL', 'ZFUELTUB', 'ZHIGHCEIL', 'ZKOWNRENT', 'ZMONPOOL', 'ZMONTUB', 'ZNCOMBATH', 'ZNHAFBATH', 'ZORIGWIN', 'ZOTHROOMS', 'ZPOOLPUMP', 'ZPRKGPLC1', 'ZRECBATH', 'ZROOFTYPE', 'ZSIZEOFGARAGE', 'ZSQFTEST', 'ZSQFTINCA', 'ZSQFTINCB', 'ZSQFTINCG', 'ZSQFTRANGE', 'ZSTORIES', 'ZSWIMPOOL', 'ZTREESHAD', 'ZTYPEGLASS', 'ZUGASHERE', 'ZWALLTYPE', 'ZWINDOWS', 'ZWINFRAME', 'ZYEARMADERANGE', 'ZTOTROOMS', 'ZTYPEHUQ', 'ZSTUDIO']}


########## separate features by type ##############

geo_features = ['state_name']#, 'REGIONC'] # inferred

selectbox_features=[]
numeric_features=['NCOMBATH', 'NHAFBATH', 'TOTROOMS', 'NUMFRIG', 'MICRO', 'TVCOLOR', 'DESKTOP', 'NUMLAPTOP', 'LGTIN1TO4', 'LGTIN4TO8', 'LGTINMORE8', 'NHSLDMEM', 'SQFTEST']
numeric_features_dropdown = ['NUMPORTEL']
num_checkbox_features = ['TYPEHUQ', 'STORIES', 'YEARMADERANGE', 'WALLTYPE', 'ROOFTYPE', 'WINDOWS', 'SWIMPOOL', 'DISHWASH', 'CWASHER', 'DRYER', 'TELLWORK', 'HEATHOME', 'EQUIPM', 'AIRCOND', 'SMARTMETER', 'SOLAR']

all_features = geo_features+numeric_features+num_checkbox_features+numeric_features_dropdown#+selectbox_features


########### dictionary of mappings ################

mapped_features = {'TYPEHUQ': {'Mobile home': '1', 'Single-family house detached from any other house ': '2', 'Single-family house attached to one or more other houses (for example: duplex, row house, or townhome)': '3', 'Apartment in a building with 2 to 4 units': '4', 'Apartment in a building with 5 or more units': '5'}, 'STORIES': {'One story': '1', 'Two stories': '2', 'Three stories': '3', 'Four or more stories': '4', 'Split-level': '5'}, 'YEARMADERANGE': {'Before 1950': '1', '1950 to 1959': '2', '1960 to 1969': '3', '1970 to 1979': '4', '1980 to 1989': '5', '1990 to 1999': '6', '2000 to 2009': '7', '2010 to 2015': '8', '2016 to 2020': '9'}, 'WALLTYPE': {'Brick': '1', 'Wood': '2', 'Siding (aluminum, fiber cement, vinyl, or steel) ': '3', 'Stucco': '4', 'Shingle (composition)': '5', 'Stone ': '6', 'Concrete block ': '7', 'Other': '99'}, 'ROOFTYPE': {'Ceramic or clay tiles': '1', 'Wood shingles/shakes': '2', 'Metal': '3', 'Slate or synthetic slate': '4', 'Shingles (composition or asphalt)': '5', 'Concrete tiles': '6', 'Other': '99'}, 'WINDOWS': {'1 or 2 windows': '1', '3 to 5 windows': '2', '6 to 9 windows': '3', '10 to 15 windows': '4', '16 to 19 windows': '5', '20 to 29 windows': '6', '30 or more windows': '7'}, 'SWIMPOOL': {'Yes': '1', 'No': '0'}, 'DISHWASH': {'Yes': '1', 'No': '0'}, 'CWASHER': {'Yes': '1', 'No': '0'}, 'DRYER': {'Yes': '1', 'No': '0'}, 'TELLWORK': {'Yes': '1', 'No': '0'}, 'HEATHOME': {'Yes': '1', 'No': '0'}, 'EQUIPM': {'Central furnace ': '3', 'Steam or hot water system with radiators or pipes ': '2', 'Central heat pump': '4', 'Ductless heat pump, also known as a “mini-split”': '13', 'Built-in electric units installed in walls, ceilings, baseboards, or floors': '5', 'Built-in room heater burning gas or oil': '7', 'Wood or pellet stove ': '8', 'Portable electric heaters': '10', 'Other ': '99'}, 'AIRCOND': {'Yes': '1', 'No': '0'}, 'SMARTMETER': {'Yes': '1', 'No': '0'}, 'SOLAR': {'Yes': '1', 'No': '0'}, 'NUMPORTEL': {'0': '0', '1': '1', '2': '2', '3': '3', '4': '4', '5': '5', '6': '6', '7': '7', '8': '8', '9': '9'}}


############# functions ############

@st.cache_data
def make_numeric_input(feature):
    label = label_dict.get(feature)
    min_value, max_value = (int(val) for val in values_dict.get(feature).split('-'))
    return label, min_value, max_value

def record_user_input(feature):
    """
    This function creates an input widget for a feature
    Depending on which type the feature is.
    It will write the user input value into params dictionary.
    """
    ##### geography features ######
    if feature=='state_name':
        state_postal = st.selectbox('Select your state:', states.keys())
        params['state_name'] = states.get(state_postal)
        params['REGIONC'] = state_to_region.get(params['state_name'])
        params['BA_climate'] = climate_dict.get(params['state_name'])

    ##### hard-coded features #####
    elif feature in ['NHAFBATH','NUMLAPTOP','LGTIN4TO8','LGTINMORE8']:
        params[feature]=0

    ##### features that need a dropdown text #####
    elif feature in selectbox_features:
        params[feature] = st.selectbox(label = label_dict.get(feature),
                                    options= values_dict.get(feature).split('\n'))
    ##### features with purely numeric input #####
    elif feature in numeric_features:
        params[feature] = int(st.number_input(*make_numeric_input(feature)))

    ##### features where dropdown input is transferred to numeric #####
    elif feature in num_checkbox_features:
        user_value = st.selectbox(label=label_dict.get(feature),
                                  options=mapped_features.get(feature).keys())
        params[feature] = int(mapped_features.get(feature).get(user_value))

    ##### features which have both numeric range and text #####
    elif feature in numeric_features_dropdown:
        user_value = st.selectbox(label=label_dict.get(feature),
                                  options=mapped_features.get(feature).keys())
        params[feature] = int(mapped_features.get(feature).get(user_value))




############## tabs - organize features by sections ###############

tab_main, tab_household, tab_appliances, tab_admin = st.tabs(['About your home',
                                                   'Household characteristics',
                                                    'Appliances',
                                                    'Admin'])

#############################################
############### user input ##################
#############################################

###### section Main: GEOGRAPHY, ADMIN, basic household (type, no. of persons) ##########

with tab_main:
    st.subheader('About your home')

    main_features = ['TYPEHUQ','NHSLDMEM', 'TELLWORK', 'state_name', 'SQFTEST']
    for feature in main_features:
        record_user_input(feature)


with tab_household:
    st.subheader('Your household')

    ###### section HOUSEHOLD CHARACTERISTICS ######

    household_features = ['STORIES','YEARMADERANGE','NCOMBATH',
                            'NHAFBATH','TOTROOMS', 'WALLTYPE','ROOFTYPE','WINDOWS', 'SWIMPOOL', 'SOLAR',
                            'SMARTMETER']
    for feature in household_features:
        record_user_input(feature)


with tab_appliances:
    st.subheader('Applicances')

    #appliance_features = list(set(all_features).difference(set(main_features+household_features)))

    col1, col2, col3 = st.columns(3)

    with col1:
        st.subheader('Living room :tv: :bulb: :computer:')
        for feature in ['DESKTOP','NUMLAPTOP','TVCOLOR','LGTIN1TO4','LGTIN4TO8','LGTINMORE8']:
            record_user_input(feature)

    with col2:
        st.subheader('Chores :knife_fork_plate:')
        for feature in ['DISHWASH','MICRO','NUMFRIG', 'CWASHER','DRYER']:
            record_user_input(feature)

    with col3:
        st.subheader('Heating and cooling')
        for feature in ['AIRCOND','EQUIPM','HEATHOME' , 'NUMPORTEL']:
            record_user_input(feature)

with tab_admin:
    st.subheader('Parameters sent to the API:')
    st.write(params)



############# callback to calculate kWh ################

st.divider()

if st.button('Estimate my consumption'):
    pred_kwh = api_call(url=url, params=params)
    st.write(f'''
             Your estimated consumption:\n
             {int(pred_kwh)} kWh'''
             )
