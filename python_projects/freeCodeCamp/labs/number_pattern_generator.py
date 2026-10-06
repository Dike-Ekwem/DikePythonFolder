#n represents a positive integer
def number_pattern(n):
    if not isinstance(n, int):
        return 'Argument must be an integer value.'
    if n < 1:
        return 'Argument must be an integer greater than 0.'
    
    result_pattern = ''
    for num in range(1, n+1):
        if result_pattern:
            result_pattern += ' '
        result_pattern += str(num)
    return result_pattern


print(number_pattern(200))