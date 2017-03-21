import pdir


def interactive_test():
    """
    This function runs pdir2 in bpython, ipython, ptpython.
    Note that giving the right output does not mean pdir2 works correctly,
    because print(string) is not equivalent to repr it in a REPL.
    To ensure everything truely works, manually verification is necessary.
    """
    print("Environment: " + pdir.repl_type)
    import requests
    print("\nShould show result of pdir(requests):")
    print(pdir(requests))
    if pdir.repl_type == 'bpython':
        import sys

        # exit() in bpython interactive mode leads to a ValueError.
        # So I defined an exception hook to silent it.
        # sys.exit(0) is to make tox believe there's no error.
        def deal_with_exception_when_exit(a, b, c):
            sys.exit(0)

        sys.excepthook = deal_with_exception_when_exit
        try:
            exit()
        except:
            pass
    else:
        exit()


if __name__ in ('__main__', '__console__'):
    interactive_test()
