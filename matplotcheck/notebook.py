# tests to be run on the entire notebook
# formatting of this may change depending on OKGrade


def convert_axes(plt, which_axes="current"):
    """Saves current working plot and axes as variables for testing purposes.
    Axes that is/are saved is denoted by which_axes.

    Parameters
    ---------
    plt: matplotlib plot
        Matplotlib plot to be tested.
    which_axes: string
        String from the following list ['current', 'last', 'first', 'all']
        stating which axes we are saving for testing.

    Returns
    -------
    ax: Matplotlib axes or list
        Matplotlib axes or list of axes as express by which_axes
    """
    fig = plt.gcf()
    if which_axes == "current":
        ax = fig.gca()
    elif which_axes == "last":
        ax = fig.axes[-1]
    elif which_axes == "first":
        ax = fig.axes[0]
    elif which_axes == "all":
        ax = fig.axes
    else:
        raise ValueError(
            "which_axes must be one of the following strings "
            + '["current", "last", "first", "all"]'
        )
    return ax


# JUPYTER NOTEBOOK TEST HELPER FUNCTIONS!


def error_test(n, n_exp):
    """Tests the number of cells that produced an error.

    Parameters
    ----------
    n: int
        Number of cells that that did not produce an error.
    n_exp: int
        Number of cell that are checked if producing an error.

    Returns
    -------
    print statement of test results
    """
    if n == n_exp:
        print("ERRORS TEST: PASSED!")
    else:
        print(
            "ERRORS TEST: FAILED!", n, "of", n_exp, "Cells ran without errors"
        )


def remove_comments(input_string):
    """Helper function for import_test.
    Removes all parts of string that would be commented out by # in python

    Parameters
    ----------
    input_string: string
        String to be modified.

    Returns
    -------
    string
        Sting where all parts commented out by a '#' are removed from
        input_string.
    """
    split_lines = input_string.split("\n")
    return "".join([line.split("#")[0] for line in split_lines])


def import_test(var_dict, n):
    """
    Tests no import statements are found after the first cell in a Jupyter
    Notebook

    Parameters
    ----------
    vars_dict: dictionary
        Dictionary produced by 'locals()' in notebook.
    n: int
        number of cells to be tested for import statement in Jupyter Notebook

    Returns
    -------
    print statement of test results
    """
    flag = True
    for i in range(2, n + 1):
        if "import " in remove_comments(var_dict["_i" + str(i)]):
            flag = False
            break
    if flag:
        print("IMPORT TEST: PASSED!")
    else:
        print("IMPORT TEST: FAILED! Import statement found in cell", i)
