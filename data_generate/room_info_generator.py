import pandas as pd
import random

global_stay_seq = 0


def set_room_attributes(row):
    """
    Set room attributes based on stay_seq, stay_type, and room_type
    """
    global global_stay_seq
    stay_seq, stay_type, room_type = row['stay_seq'], row['stay_type'], row['room_type']
    
    if global_stay_seq != stay_seq:
        if stay_type == 1:
            standard_people = 2
            if room_type in [1, 2, 3]:
                standard_people = 2
                max_people = random.randint(3, 4)
                additional_charge = random.randint(2, 3) * 5000
            else:
                max_people = random.randint(4, 6)
                additional_charge = random.randint(4, 6) * 5000
        elif stay_type == 2:
            standard_people = 2
            max_people = random.randint(4, 6)
            if room_type == 5:
                standard_people = random.randint(2, 3)
        elif stay_type == 3:
            if room_type == 1:
                standard_people = 2
        elif stay_type == 4:
            standard_people = 2


    standard_people = 2

    # Logic to set max_people and additional_charge based on stay_type and room_type
    if stay_type == 1 and room_type in [1, 2, 3, 4, 5]:
        max_people = random.randint(2, 4)
        additional_charge = random.randint(10, 15) * 1000
        child_discount_price = random.randint(5, 9) * 1000

    return row

# Apply the function to the DataFrame
# df = df.apply(set_room_attributes, axis=1)
