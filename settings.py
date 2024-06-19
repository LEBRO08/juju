import re

def extract_prize_value(prize_text):
    try:
        # Regular expression to extract value inside parentheses after $
        match = re.search(r'\(\$([\d.]+)\)', prize_text)
        if match:
            value_str = match.group(1)  # Extract the value part as a string
            return float(value_str)  # Convert to float
        else:
            return None  # Return None if no match found
    except ValueError:
        return None  # Handle the case where conversion fails

def is_prize_value_above_threshold(fields):
    for field in fields:
        if field.name.lower() == "prize":
            prize_text = field.value  # Extract prize text from the prize field
            print(f"Checking prize: {prize_text}")
            value = extract_prize_value(prize_text)
            if value is not None:
                return value > 0.1  # Check if the value is more than $0.1
            else:
                return False  # Return False if extraction failed
    return False  # Return False if no prize field found or extraction failed

def is_pool_value_above_threshold(fields):
    for field in fields:
        if field.name.lower() == "pool":
            pool_text = field.value  # Extract pool text from the pool field
            print(f"Checking pool: {pool_text}")
            value = extract_prize_value(pool_text)
            if value is not None:
                return value > 1  # Check if the value is more than $0.1
            else:
                return False  # Return False if extraction failed
    return False  # Return False if no pool field found or extraction failed

def is_pool_value_above_threshold_1(fields):
    for field in fields:
        if field.name.lower() == "pool":
            pool_text = field.value  # Extract pool text from the pool field
            print(f"Checking pool: {pool_text}")
            value = extract_prize_value(pool_text)
            if value is not None:
                return value > 0.5  # Check if the value is more than $0.5
            else:
                return False  # Return False if extraction failed
    return False  # Return False if no pool field found or extraction failed

def extract_enters_value(enters_text):
    try:
        # Split the text by '/' and take the second part (after the '/')
        value_str = enters_text.split('/')[1].strip()
        return int(value_str)  # Convert to integer
    except (IndexError, ValueError):
        return None  # Return None if extraction fails or value can't be converted to integer

def is_enters_value_at_most_4(fields):
    for field in fields:
        if field.name.lower() == "enters":
            enters_text = field.value  # Extract enters text from the enters field
            print(f"Checking enters: {enters_text}")
            value = extract_enters_value(enters_text)
            if value is not None:
                return value <= 4  # Check if the value is 4 or less
            else:
                return False  # Return False if extraction failed
    return False  # Return False if no enters field found or extraction failed

def is_pool_per_enters_above_threshold(fields):
    pool_value = None
    enters_value = None
    
    for field in fields:
        if field.name.lower() == "pool":
            pool_text = field.value  # Extract pool text from the pool field
            print(f"Checking pool: {pool_text}")
            pool_value = extract_prize_value(pool_text)
            if pool_value is None:
                return False  # Return False if extraction failed
        
        if field.name.lower() == "enters":
            enters_text = field.value  # Extract enters text from the enters field
            print(f"Checking enters: {enters_text}")
            enters_value = extract_enters_value(enters_text)
            if enters_value is None or enters_value == 0:
                return False  # Return False if extraction failed or enters is 0
    
    if pool_value is not None and enters_value is not None and enters_value != 0:
        return pool_value / enters_value >= 0.01
    else:
        return False  # Return False if pool or enters values were not found or valid

def extract_text_between_parentheses(text):
    try:
        match = re.search(r'\((.*?)\)', text)
        if match:
            return match.group(1)  # Extract the text between parentheses
        else:
            return None  # Return None if no match found
    except Exception as e:
        print(f"Error extracting text between parentheses: {e}")
        return None
