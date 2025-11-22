from difflib import SequenceMatcher
valid_names = {
    "Alaska",
    "Alabama",
    "Arkansas",
    "Arizona",
    "California",
    "Colorado",
    "Connecticut",
    "District of Columbia",
    "Delaware",
    "Florida",
    "Georgia",
    "Hawaii",
    "Iowa",
    "Idaho",
    "Illinois",
    "Indiana",
    "Kansas",
    "Kentucky",
    "Louisiana",
    "Massachusetts",
    "Maryland",
    "Maine",
    "Michigan",
    "Minnesota",
    "Missouri",
    "Mississippi",
    "Montana",
    "North Carolina",
    "North Dakota",
    "Nebraska",
    "New Hampshire",
    "New Jersey",
    "New Mexico",
    "Nevada",
    "New York",
    "Ohio",
    "Oklahoma",
    "Oregon",
    "Pennsylvania",
    "Rhode Island",
    "South Carolina",
    "South Dakota",
    "Tennessee",
    "Texas",
    "Utah",
    "Virginia",
    "Vermont",
    "Washington",
    "Wisconsin",
    "West Virginia",
    "Wyoming"
}

def corrected_state(input_name):
    """
    Autocorrects inputed state name by finding closest match in list valid_names.
    
    Parameters:
    input_name (str): Potentionally mispelled state

    Returns:
    str: Closest matching valid state name.
    """
    highest_ratio = 0.0
    closest_match = input_name
    
    for correct_name in valid_names:
        ratio = SequenceMatcher(None, input_name.lower(), correct_name.lower()).ratio() # get ratio of similarity between input and states in valid_names 
        if ratio > highest_ratio:                                                       # update/store state with highest similarity 
            highest_ratio = ratio
            closest_match = correct_name
            
    return closest_match
