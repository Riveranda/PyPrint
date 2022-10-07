from sys import argv, stdout, maxsize
from math import log


class InvalidArgException(Exception):
    """The exception thrown when an invalid range is passed.
    """
    
    
def read_lines(filename, bounds, verbose, write):
    """Mass together the lines desired into a single string

    Args:
        filename ([str]): [The file to read from]
        bounds ([list]): [A length 2 list that contains the desired range]
        verbose ([bool]): [Add line numbers]
        write ([bool]): [Are we writing or printing]

    Returns:
        [str]: [Mass string of all lines]
    """
    with open(filename, "r") as f:
        contents = f.readlines()
    bounds = tuple([b + (len(contents) + 1 if b < 0 else 0) for b in bounds]) #Convert negative indicies.
    low = bounds[0]
    mass = ""
    # Python magic that should probably be its own function, but i decided to prove once and for all that i can use ternary operators.                                                 
    C = lambda l, num, up, **kwargs : ((str(num + (low if up != None else 1)) + (3 + (kwargs['offset']-(int(log(num + 1)/log(10)))) if up != None else 3) * " ") if verbose else "") + l
    if(len(bounds) == 2 and bounds[0] > bounds[1]): raise InvalidArgException("Invalid range: " + str(bounds))
    if(len(bounds) == 2):
        up = bounds[1] if len(contents) > bounds[1] else len(contents) + 1 #End of file protection if upperbound is > len of file. Will print to the end of the file
        offset = int(log(up)/log(10))
        if(up - low > 500) and not write:
            while True: # Extremely large selection protection
                try: # raw_input for python 2.7, input for python 3.*
                    s = 'Selection contains: ' + str(up - low) + ' lines, continue? y,n: '
                    sel = raw_input(s).lower()
                except:
                    sel = input(s)
                if sel == 'y': break
                if sel in ('n','q'): quit()
        for num, line in enumerate(contents[low - 1: up]):
            mass += C(line, num, up, offset=offset) 
    return mass if mass != "" else C(contents[bounds[0] - 1], bounds[0] - 1, None)
	

def help():
    print(
"""Welcome to PyPrint!
Print: pp <filename> |lowerbound|:|upperbound|
Write: pp -w <filename> |lowerbound|:|upperbound| <outfile>
Append: pp -a <filename> |lowerbound|:|upperbound| <outfile>

Example:
    pp ServerEnums.java 15:30
    pp ServerEnums.java -w -v :30 serverout.txt

Verbose
    -v If you wish line numbers be included, works for print, write and append. A line number plus 3 spaces will be added to each line. 

Argument Ordering:
    -v, -a, and -w may be included anywhere in the arguments
    Ex: pp -w -v test.txt : test2.txt <- This is valid
    
    The destination folder for writing/appending MUST come after the range if included.

Numbering:
    COUNTING BEGINS AT 1
    THE FIRST LINE OF THE FILE IS REGARDED AS LINE 1
    Any 0's will be converted to 1's. IE 0:5 = 1:5
    This was done to match up with the way vim and all other text editors number their lines.

Negative Indicies:
    Negative indicies are supported.
    -1      Last line of the file
    -2:-1   Last 2 lines of the file. 
    5:-2    Line 5 to the second to last line of the file

Right Inclusivity:
    Right inclusivity is included as a feature. Meaning for the range 1:30, the line 30 will be included.

Acceptable Ranges
You may use Python's list range syntax.

    15:30 Lines 15 to 30. 
    15    Line 15
    :30   Lines 1 to 30
    10:   Line 10 to the end of the file.
    :     The entire file
          Providing No range will use the entire file.
          
Writing:
    Write mode will write the desired contents to the outfile
    WRITE MODE ERASES ANY CURRENT CONTENTS OF THE OUTFILE
    
Appending: 
    Append mode will append the desired contents to the outfile
    Note that append will override write mode. 

Safety:
    For ranges greater than the length of the file, the entire file will be printed with no error.
    Append mode will override write mode. Meaning if you pass both -w and -a, it will append the information.
    
Overflow Protection:
    If you try to print over 500 lines at one time, a confirmation will appear. No such check exists for writing. 
    Please note that stdout.write is extremely fast and can print tens of thousands of lines per second. 
    This was put into place to prevent you from essentially erasing any useful information on your window.
    
Bashrc function: 
    It is recommended to replace the following function in bashrc. Adjust the path if necessary
    
pp(){
        python /scratch/users/tbbender/pyprint.py $*
}
""")
    quit()
    
    
def isnum(s):
    """Determine if a string is an integer or not

    Args:
        s ([str]): [The interger]

    Returns:
        [bool]: [Is an integer]
    """
    try:
        int(s)
    except:
        return False
    return True


def findbounds(arg):
    """Determines the desired bounds from the argument

    Args:
        arg ([str]): [A string representing the desired bounds]

    Returns:
        [list]: [An integer list describing the desired bounds.]
    """
def findbounds(arg):
    """Determines the desired bounds from the argument

    Args:
        arg ([str]): [A string representing the desired bounds]

    Returns:
        [list]: [An integer list describing the desired bounds.]
    """
    bounds = [1, maxsize]
    if arg == ':': return bounds
    try:
        if arg[0] == ':': bounds[0] = 1
        bounds = [int(s) if isnum(s) else bounds[i] for i, s in enumerate(arg.split(':'))] 
    except:
        return [1, maxsize] #If no range, we read the whole file
    bounds = [b if b != 0 else 1 for b in bounds] # Convert 0's to 1's 
    return bounds


def main(args):
    if '-h' in args:
        help()
    #verbose, write, append = False, False, False
    writefile = ""
    options = {
        '-v' : False,
        '-w' : False,
        '-a' : False
    }
    #Iterate over options and setup logic
    for i in options:
        if i in args:
            args.remove(i)
            options[i] = True
            if i in ('-w', '-a'):
                writefile = args[-1]
    bounds = findbounds('' if len(args) < 2 else args[1])
    lines = read_lines(args[0], tuple(bounds), options['-v'], (options['-w'] or options['-a']))
    if options['-w'] or options['-a']:
        with open(writefile, ("a" if options['-a'] else 'w')) as f:
            f.write(lines)
    else:
        stdout.write(lines) #Using stdout to significantly speed up printing in case of large numbers of lines. 
        
        
if __name__ == '__main__':
    main(argv[1:])

