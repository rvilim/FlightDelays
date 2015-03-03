from datetime import date
import workalendar.usa
import datetime

def statelookup(abbrev):    
    states = {
            'PA': 'Pennsylvania',
            'FL': 'Florida',
            'NY': 'NewYork',
            'UT': 'Utah',
            'MA': 'Massachusetts',
            'KY': 'Kentucky',
            'GA': 'Georgia',
            'VA': 'Virginia',
            'MN': 'Minnesota',
            'CA': 'California',
            'MI': 'Michigan',
            'IL': 'Illinois',
            'NC': 'NorthCarolina',
            'OH': 'Ohio',
            'MD': 'Maryland',
            'NV': 'Nevada',
            'IN': 'Indiana',
            'OK': 'Oklahoma',
            'AZ': 'Arizona',
            'TX': 'Texas',
            'MO': 'Missouri',
            'OR': 'Oregon',
            'TN': 'Tennessee',
            'MS': 'Mississippi',
            'WA': 'Washington',
            'AR': 'Arkansas',
            'CO': 'Colorado',
            'SC': 'SouthCarolina',
            'CT': 'Connecticut',
            'SD': 'SouthDakota',
            'HI': 'Hawaii',
            'LA': 'Louisiana',
            'WI': 'Wisconsin',
            'AL': 'Alabama',
            'NJ': 'NewJersey',
            'IA': 'Iowa',
            'ME': 'Maine',
            'RI': 'RhodeIsland',
            'NE': 'Nebraska',
            'ID': 'Idaho',
            'NM': 'NewMexico',
            'WY': 'Wyoming',
            'MT': 'Montana',
            'ND': 'NorthDakota',
            'AK': 'Alaska',
            'VT': 'Vermont',
            'NH': 'NewHampshire',
            'WV': 'WestVirginia',
            'KS': 'Kansas'}
    
    try:
        return states[abbrev]
    except:
        return states['NY']
        
        
def getholidays(year, stateabbrev):
    holidaylist=["Independence Day", "Thanksgiving Day", "Labor Day", "New year", "Christmas Day", "Memorial Day" ]
    
    state=statelookup(stateabbrev)

    cal = getattr(workalendar.usa, state)()
    holidays=cal.holidays(year)
    
    daysoff=[]
    
    for holiday in holidaylist:
        a= [i for i, v in enumerate(holidays) if v[1] == holiday+' (Observed)']
        if(not a):
            a= [i for i, v in enumerate(holidays) if v[1] == holiday]
            
        daysoff.append(holidays[a[0]][0])

    return daysoff