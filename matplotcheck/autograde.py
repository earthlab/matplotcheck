# Wrapper functions for matplotcheck functions that run
# and track the passing status of test functions and
# provide formatted results of tests


def run_test(
    func,
    points,
    *args,
    correct_message="default correct",
    error_message="default error",
    **kwargs
):
    """Runs a pre-defined test function and creates a dictionary
    containing the results of the test

    Parameters
    ---------
    func: name of pre-defined test function to run
    points: number of points assigned for passing test
    args: arguments provided to test function
    correct_message: string of custom message returned with passing test
    error_message: string of custom message returned with failing test
    kwargs: keyword arguments provided to test function

    Returns
    -------
    results: dictionary with the following key:value pairs
        points: number of points assigned based on test results
        pass: boolean of passing status of test
        description: string of test function name that was run
        message: string of custom message returned based on passing status
            [correct_message or error_message]
        traceback: error message from test function (when pass is False)
    """
    results = {"points": 0, "pass": False}
    score = 0
    try:
        fname = func.__name__
        results["description"] = fname
        func(*args, **kwargs)
    except Exception as e:
        results["message"] = error_message
        results["traceback"] = e
        pass
    else:
        results["pass"] = True
        results["message"] = correct_message
        results["points"] = points

    return results


def output_results(results):
    """Prints a formatted message containing the total number of points
    summed across a dictionary of results (from one or more tests)

    Parameters
    ---------
    results: dictionary with the following key:value pairs
        points: number of points assigned based on test results
        pass: boolean of passing status of test
        description: string of test function name that was run
        message: string of custom message returned based on passing status
            [correct_message or error_message]
        traceback: error message from test function (when pass is False)

    Returns
    -------
    points: number of points summed across points in results dictionary
    """
    points = 0
    for r in results:
        points += r["points"]
        print("Results for test '{}':".format(r["description"]))
        if r["pass"]:
            print(
                " Pass! {msg} ({p} points)".format(
                    msg=r["message"], p=r["points"]
                )
            )
        else:
            print(
                " Fail! {msg} ({p} points)".format(
                    msg=r["message"], p=r["points"]
                )
            )
            print(" Traceback: {t}".format(t=r["traceback"]))
    return points
