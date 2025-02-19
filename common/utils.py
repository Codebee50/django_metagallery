def get_first_error(errors):
    """
    Gets the first message in a serializer.errors
    
    Parameters:
    errors: The error messages of a serializer i.e serializer.errors
    """
    field, error_list = next(iter(errors.items()))
    return str(error_list[0]) 

def format_first_error(errors, with_key=True):
    field, error_list = next(iter(errors.items()))
    if isinstance(error_list, list):
        return f"({field}) {error_list[0]}" if with_key else error_list[0]
    else:
        return format_first_error(error_list)