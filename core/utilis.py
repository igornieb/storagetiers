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
