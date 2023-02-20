from django.core.exceptions import ValidationError

def validate_sizes_allowed(values):
    # validates that values contains ints only separated by space
    values = str(values)
    val_list = values.split(" ")
    res = []
    for val in val_list:
        if val.isdigit():
            res.append(int(val))
        else:
            raise ValidationError("Values must be integer numbers separated by space")

    return res

def validate_time_allowed(value):
    # validates that values contains int only in range [300, 30000]
    value = int(value)
    if 300 <= value <= 30000:
        return value
    else:
        raise ValidationError("Value must be an integer in range [300, 30000]")

