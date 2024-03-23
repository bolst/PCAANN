

def to_range(value) -> range:
    if isinstance(value, range):
        return value
    
    if isinstance(value, str):
        value = int(value)

    return range(value, value + 1, 1)