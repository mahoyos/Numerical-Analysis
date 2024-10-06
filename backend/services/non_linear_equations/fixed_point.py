def evaluate_function_at_point(function_expression, x):
    function_expression = function_expression.replace('^', '**')
    return eval(function_expression)


def fixed_point_service(initial_guess, tolerance, max_iterations, function_expression, g_expression):
    iteration_data = []
    x = initial_guess
    f_value = evaluate_function_at_point(function_expression, x)
    error = 100
    iteration_count = 0
    iteration_data.append((iteration_count, x, f_value, error))

    while error > tolerance and f_value != 0 and iteration_count < max_iterations:
        x_new = evaluate_function_at_point(g_expression, x)
        f_value = evaluate_function_at_point(function_expression, x_new)
        iteration_count += 1
        error = abs(x_new - x)
        x = x_new
        iteration_data.append((iteration_count, x, f_value, error))

    result = {
        "root": x,
        "iterations": iteration_data
    }
    return result
