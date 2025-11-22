# autocorrection
from autocorrect import corrected_state

def get_region(state):
    """
    Returns the region associated with a given state name.

    Parameters:
        state_name (str): The name of the state

    Returns:
        str: The region of the state ('North', 'South', 'Midwest', or 'West'),
             or None if state not found
    """
    regions = {
        "Alaska": "West",
        "Alabama": "South",
        "Arkansas": "South",
        "Arizona": "West",
        "California": "West",
        "Colorado": "West",
        "Connecticut": "North",
        "District of Columbia": "South",
        "Delaware": "South",
        "Florida": "South",
        "Georgia": "South",
        "Hawaii": "West",
        "Iowa": "Midwest",
        "Idaho": "West",
        "Illinois": "Midwest",
        "Indiana": "Midwest",
        "Kansas": "Midwest",
        "Kentucky": "South",
        "Louisiana": "South",
        "Massachusetts": "North",
        "Maryland": 'South',
        "Maine": "North",
        "Michigan": "Midwest",
        "Minnesota": "Midwest",
        "Missouri": "Midwest",
        "Mississippi": "South",
        "Montana": "West",
        "North Carolina": "South",
        "North Dakota": "Midwest",
        "Nebraska": "Midwest",
        "New Hampshire": "North",
        "New Jersey": "North",
        "New Mexico": "West",
        "Nevada": "West",
        "New York": "North",
        "Ohio": "Midwest",
        "Oklahoma": "South",
        "Oregon": "West",
        "Pennsylvania": "North",
        "Rhode Island": "North",
        "South Carolina": "South",
        "South Dakota": "Midwest",
        "Tennessee": "South",
        "Texas": "South",
        "Utah": "West",
        "Virginia": "South",
        "Vermont": "North",
        "Washington": "West",
        "Wisconsin": "Midwest",
        "West Virginia": "South",
        "Wyoming": "West"
    }
    return regions.get(state)

def encode_region(region):
    """
    Returns the value associated with a given region for UART comms.

    Parameters:
        region (str): The name of the region

    Returns:
        str: The comm value of the region ('0', '1', '2', or '3'),
             or None if state not found
    """
    encoded_regions = {
        "South": "0",
        "North": "1",
        "West": "2",
        "Midwest": "3",
    }
    return encoded_regions.get(region)
def detect_abbrev(state):
    """
    Detects abbreviated state names and replaces with full name 

    Parameters:
        state (str): The name of the potentially abbreviated state 

    Returns:
        full_state (str): full name of state
    """
    state_abbrev = {
        "AK": "Alaska",
        "AL":"Alabama",
        "AR":"Arkansas",
        "AZ":"Arizona",
        "CA":"California",
        "CO":"Colorado",
        "CT":"Connecticut",
        "DC":"District of Columbia",
        "DE":"Delaware",
        "FL":"Florida",
        "GA":"Georgia",
        "HI":"Hawaii",
        "IA":"Iowa",
        "ID":"Idaho",
        "IL":"Illinois",
        "IN":"Indiana",
        "KS":"Kansas",
        "KY":"Kentucky",
        "LA":"Louisiana",
        "MA":"Massachusetts",
        "MD":"Maryland",
        "ME":"Maine",
        "MI":"Michigan",
        "MN":"Minnesota",
        "MO":"Missouri",
        "MS":"Mississippi",
        "MT":"Montana",
        "NC":"North Carolina",
        "ND":"North Dakota",
        "NE":"Nebraska",
        "NH":"New Hampshire",
        "NJ":"New Jersey",
        "NM":"New Mexico",
        "NV":"Nevada",
        "NY":"New York",
        "OH":"Ohio",
        "OK":"Oklahoma",
        "OR":"Oregon",
        "PA":"Pennsylvania",
        "RI":"Rhode Island",
        "SC":"South Carolina",
        "SD":"South Dakota",
        "TN":"Tennessee",
        "TX":"Texas",
        "UT":"Utah",
        "VA":"Virginia",
        "VT":"Vermont",
        "WA":"Washington",
        "WI":"Wisconsin",
        "WV":"West Virginia",
        "WY":"Wyoming"    
    }
    # determine if state name is an abbreviation
    name_length = len(state)
    print("[localization] name length:",name_length)
    if name_length < 3:
        state_name = state_abbrev.get(state) # get full state name
        print("[localization] abbreviation detected")
    else:
        state_name = state
        
    return state_name

def localize_response(resp):
    """
    Calls helper functions encode_region and get_region to deduce region from raw state string.
    State is validated by autocorrect in process.

    Parameters:
        byte_string (str): The byte string response from the backend

    Returns:
        encoded_reg (str): The comm value of the region ('0', '1', '2', or '3'),
             or None if state not found
        
    """
    # extract unvalidated state text from backend response
    flag = resp['Just State Flag']
    message = resp['message']
    print("[localization] Just State:", flag)
    
    if message:
        print("[localization] message:", message)
        # extract state based on its location in message response\
        try:
            raw_state = False
            if flag:
                _ = message.split()
                print("[localization] split list:",_)
                raw_state = _[0] + " " + _[1]
            else:     
                _ = message.split()
                print("[localization] split list:",_)
                raw_state = _[1]
        except Exception as e:
            print(f"[localization] Message parsing error: {e}")
            return None
        
        # detect abbreviated state replace with full name
        print("[localization] raw state", raw_state)
        state = detect_abbrev(raw_state)
        
        # autocorrect state text 
        valid_state = corrected_state(state)        
        print("[localization] autocorrected state:",valid_state)
        
        # determine region and encode
        region = get_region(valid_state)
        print("[localization] region:",region)
        encoded_reg = encode_region(region)
        print("[localization] encoded region:",encoded_reg)
        return encoded_reg
        
    else:
        return None
