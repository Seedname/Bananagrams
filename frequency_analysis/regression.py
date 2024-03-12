import math
def inverse_regression(x_values: list[float], y_values: list[float], power: float) -> dict:
    n = len(x_values)
    y_t = sum(y_values)
    x_inv = sum([1/x**power for x in x_values])
    x_inv_sq = sum([1/x**(2*power) for x in x_values])
    y_x = sum([y/x**power for x, y in zip(x_values, y_values)])

    a = y_x / x_inv_sq
    b = 0
    # a = (y_x - y_t * x_inv / n) / (x_inv_sq - x_inv**2 / n)
    # b = (y_t - a * x_inv) / n

    func = lambda x: a/x**power + b
    error = sum([(y - func(x)) ** 2 for x, y in zip(x_values, y_values)])
    mean = y_t / n
    total_sum_of_squares = sum([(y - mean) ** 2 for y in y_values])
    r2 = 0
    r = 0
    if total_sum_of_squares > 0:
        r2 = 1 - error/total_sum_of_squares
    if r2 >= 0:
        r = math.sqrt(r2)

    return {"a": a, "b": b, "r": r, "r2": r2}