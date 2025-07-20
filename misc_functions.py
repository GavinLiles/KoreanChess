# misc_functions.py

def add_tuples(x:tuple, y:tuple) -> tuple:
    try:
        return tuple(map(lambda i, j: i + j, x, y))
    except TypeError:
        print('types are incompatible to add.')
        return None

def split_array(list:list, index) -> tuple[list,list]:
    '''
    splits list into two lists at the index specified.
    leaves out the specified index from list.
    '''
    list1 = list[:index]
    list2 = list[index+1:]
    return (list1, list2)

def get_first_item_in(list:list):
    for piece in list:
        if piece:
            return piece
    return None
