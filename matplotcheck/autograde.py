"""
matplotcheck.autograde
======================

Wrapper functions that run and track the passing status of
matplotcheck functions and provide formatted results of tests.

"""


def run_test(
    func,
    points,
    *args,
    correct_message="default correct",
    error_message="default error",
    **kwargs
):
    """Run a pre-defined test function and creates a dictionary
    containing the results of the test

    Parameters
    ----------
    func : function or method
        Pre-defined test function to run
    points : int or float
        Number of points assigned for passing test
    *args
        Variable arguments passed to test function
    correct_message : str
        Custom message returned with passing test
    error_message : str
        Custom message returned with failing test
    **kwargs
        Keyword arguments passed to test function

    Returns
    -------
    results : dict with the following keys:
        points : int or float : points assigned based on test results
        pass : bool : passing status of test function
        description : str : test function name that was run
        message : str : custom message returned based on passing status
        traceback : AssertionError : returned from test function when pass is
        False
    """
    results = {"points": 0, "pass": False}
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
    """Print a formatted message containing the total number of points
    summed across a list of dictionaries with results from one or more tests

    Parameters
    ----------
    results : list of dictionaries with the following keys:
        points : int or float : points assigned based on test results
        pass : bool : passing status of test function
        description : str : test function name that was run
        message : str : custom message returned based on passing status
        traceback : AssertionError : returned from test function when pass is
        False

    Returns
    -------
    points : int or float
        Number of points summed across points in results list
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
