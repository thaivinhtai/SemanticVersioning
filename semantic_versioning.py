"""Software versioning is the process of assigning unique version numbers to
unique states of computer software. These numbers are generally assigned in
ncreasing order and correspond to new developments in the software.

Modern computer software is often tracked using two different software
versioning schemes—internal version number that may be incremented many times
in a single day, such as a revision control number, and a released version that
typically changes far less often, such as semantic versioning or a project
codename.

Semantic versioning is a simple set of rules and requirements that dictate
how version numbers are assigned and incremented. These rules are based on
but not necessarily limited to pre-existing widespread common practices in
use in both closed and open-source software.

Version numbers are denoted using a standard tuple of integers:
                                major.minor.patch

        A 'major' version identifies the product stage of the project. The
        basic intent is that 'major' versions are incompatible, large-scale
        upgrades of the software component. This enables a check of a client
        application against the latest version of the software component to
        ensure compatibility. If there is a discrepancy between the two,
        the client application MUST be updated accordingly.

        A 'minor' version is incremented when substantial new functionality or
        improvement are introduced; the 'major' version number doesn't change.
        A 'minor' version retains backward compatibility with older 'minor'
        versions. It is NOT forward compatible as a previous minor version
        doesn't include new functionality or improvement that has been
        introduced in this newer 'minor' version.

        A 'patch' version is incremented when bugs were fixed or implementation
        details were refactored. The major and 'minor' version don't change.
        A 'patch' version is backward and forward compatible with older and
        newer patches of the same 'major' and 'minor' version.
"""

def convert_string_to_version_component_numbers(s):
    """Convert a Semantic Versioning Component Number String to a Tuple.

    This function takes an argument 's', a string representation of a semantic
    versioning 3-component number (at least 1), and that returns a tuple
    composed of 3 integers (major, minor, patch).

    If only 1-component number is given, the function returns 'minor' and
    'patch' equal to 0.

    Parameters
    ----------
    s : str
        a string representation of a semantic versioning 3-component number
        (at least 1)

    Returns
    -------
    tuple
        composed of 3 integers (major, minor, patch)
    """
    # If 's' is not string, print message, return None.
    if not isinstance(s, str):
        return print("The parameters must be string.")

    s = s.split(".")

    # If there is any empty string in s,
    # that means there are more than 2 point side by side (..)
    if "" in s:
        return print("Cannot convert.")

    # append 0 till length = 3
    while len(s) < 3:
        s.append(0)

    # if there is any component that is not number, print message, return None.
    try:
        for index in range(len(s)):
            s[index] = int(s[index])
    except ValueError:
        return print("All components must be number.")

    return tuple(s)


def compare_versions(this, other):
    """Compare Versions.

    This function that takes two argument this and other, both tuples composed
    of 3 integers (major, minor, patch) and compares them.

    Parameters
    ----------
    this : tuple
        composed of 3 integers (major, minor, patch)
    other : tuple
        composed of 3 integers (major, minor, patch)

    Returns
    -------
    int
        1 if 'this' is 'above other';
        0 if 'this' equals 'other';
        -1 if 'this' is below 'other'.
    """
    # if 'this' or 'other'  is not tuple type, print message, return None.
    if not isinstance(this, tuple) or not isinstance(other, tuple):
        return print("Both parameters must be tuple type.")

    # if 'this' and 'other' is empty, print message, return None.
    if not this and not other:
        return print("Nothing to compare.")

    # if there is any non-int in 'this' or 'other', print message, return None.
    for element in (this + other):
        if not isinstance(element, int) or len(this) > 3 or len(other) > 3:
            return print("Wrong input format.")

    # handle un-full component numbers.
    while len(this) < 3:
        this = this + tuple([0])
    while len(other) < 3:
        other = other + tuple([0])

    # let compare.
    if len(this) == 0:
        return -1
    if len(other) == 0:
        return 1
    if this[0] > other[0]:
        return 1
    if this[0] < other[0]:
        return -1
    if this[1] > other[1]:
        return 1
    if this[1] < other[1]:
        return -1
    if this[2] > other[2]:
        return 1
    if this[2] < other[2]:
        return -1
    return 0


class Version:
    """Waypoint 3.
    This class just care firs 3 arguments.

    This class accept:
        a string representation of a semantic versioning 3-component number
        (at least 1);
        from 1 to 3 integers representing, in that particular 'order', 'major',
        'minor', and 'patch';
        a tuple of 3 integers (major, minor, patch)
    """
    def __init__(self, *param):
        self.major = None
        self.minor = None
        self.patch = None
        if len(param) == 1 and isinstance(param[0], str):
            temp = convert_string_to_version_component_numbers(param[0])
            self.major = temp[0]
            self.minor = temp[1]
            self.patch = temp[2]
        elif isinstance(param[0], tuple):
            while len(param[0]) < 3:
                param[0] = param[0] + tuple([0])
            temp = param[0]
            if isinstance(temp[0], int) and isinstance(temp[1], int) and\
                    isinstance(temp[2], int):
                self.major = temp[0]
                self.minor = temp[1]
                self.patch = temp[2]
        elif isinstance(param[0], int) and len(param) == 1:
            self.major = param[0]
            self.minor = 0
            self.patch = 0
        elif isinstance(param[0], int) and isinstance(param[1], int) and\
                len(param) == 2:
            self.major = param[0]
            self.minor = param[1]
            self.patch = 0
        elif isinstance(param[0], int) and isinstance(param[1], int) and\
                isinstance(param[2], int) and len(param) == 3:
            self.major = param[0]
            self.minor = param[1]
            self.patch = param[2]

    def __repr__(self):
        """Compute "Official" String Representations."""
        return f"Version({self.major}, {self.minor}, {self.patch})"

    def __str__(self):
        """Compute "Informal" String Representation."""
        return f"{self.major}.{self.minor}.{self.patch}"

    def __lt__(self, other):
        """self < other"""
        try:
            if self.major < other.major:
                return True
            if self.major > other.major:
                return False
            if self.minor < other.minor:
                return True
            if self.minor > other.minor:
                return False
            if self.patch < other.patch:
                return True
            if self.patch > other.patch:
                return False
            return False
        except TypeError:
            return print("Can not commpare.")

    def __le__(self, other):
        """self <= other"""
        try:
            if self.major < other.major:
                return True
            if self.major > other.major:
                return False
            if self.minor < other.minor:
                return True
            if self.minor > other.minor:
                return False
            if self.patch < other.patch:
                return True
            if self.patch > other.patch:
                return False
            if self.major == other.major and self.minor == other.minor and\
                    self.patch == other.patch:
                return True
            return False
        except TypeError:
            return print("Can not commpare.")

    def __eq__(self, other):
        """self == other"""
        try:
            if self.major == other.major and self.minor == other.minor and\
                    self.patch == other.patch:
                return True
            return False
        except TypeError:
            return print("Can not commpare.")

    def __ne__(self, other):
        """self != other"""
        try:
            if self.major != other.major:
                return True
            if self.minor != other.minor:
                return True
            if self.patch != other.patch:
                return True
            return False
        except TypeError:
            return print("Can not commpare.")

    def __gt__(self, other):
        """self > other"""
        try:
            if self.major > other.major:
                return True
            if self.major < other.major:
                return False
            if self.minor > other.minor:
                return True
            if self.minor < other.minor:
                return False
            if self.patch > other.patch:
                return True
            if self.patch < other.patch:
                return False
            return False
        except TypeError:
            return print("Can not commpare.")

    def __ge__(self, other):
        """self >= other"""
        try:
            if self.major > other.major:
                return True
            if self.major < other.major:
                return False
            if self.minor > other.minor:
                return True
            if self.minor < other.minor:
                return False
            if self.patch > other.patch:
                return True
            if self.patch < other.patch:
                return False
            if self.major == other.major and self.minor == other.minor and\
                    self.patch == other.patch:
                return True
            return False
        except TypeError:
            return print("Can not commpare.")
