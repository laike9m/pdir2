import pdir


def interactive_test():
    """
    This function runs pdir2 on bpython, ipython, ptpython.
    Note that giving the right output does not mean pdir2 works correctly,
    because print(string) is not equivalent to repr it in a REPL.
    To ensure everything truely works, manually verification is necessary.
    """
    print("\nShould show result of pdir(pdir):")
    print(pdir(pdir))
    exit()


if __name__ in ('__main__', '__console__'):
    interactive_test()
