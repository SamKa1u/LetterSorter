def get_region(state_name):
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

    return regions.get(state_name)

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

def localize_response(byte_string):
    resp = byte_string.decode('utf-8')
    print(resp)
    resp_list = resp.split()
    state = resp_list[1]
    state = state.lower()
    state = state.capitalize()
    print(state)
    region = get_region(state)
    print(region)
    encoded_reg = encode_region(region)
    print(encoded_reg)
    return encoded_reg