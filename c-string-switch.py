#! /usr/bin/python

from __future__ import division, print_function
import sys

# Input: list of unique strings. They should be valid C identifiers but we
#       don't check.
# Output:
# 1. enum Values whose labels are based on the strings.
# 2. C function that takes const char* and outputs an enum value.
#       That function implements a trie.

def get_keys(f):
    """
    Parse a file (or stdin) with keys in it.

    Return a list of key values.
    """
    return [x.strip() for x in f]

def make_key_constant(key):
    """
    Convert a key into an C enum value constant label.
    """
    return 'k' + str(key)

def print_enum(keys):
    """
    Print the enum as C code.
    """
    print("enum Values {");
    print("  kUnknown = 0,");
    for key in keys:
        print("  {},".format(make_key_constant(key)))
    print("};");

def print_case(keys, index, indent = '  '):
    """
    Recursive function that builds the giant switch statement for the trie.

    The switch statement is in a function with signature:
        enum Values convert(const char *query);

    Base case: if there's one key and we're past the end of it
    (including the nul), return the enum value.

    Recursive case: compute the set of characters at the given index. Emit a
    switch statment on query[index]. For each character in the set, recursively
    print_case over the relevant sub-array.
    """
    def char(key):
        if index == len(key):
            return '\\0'
        else:
            return key[index]

    if len(keys) == 1 and index > len(keys[0]):
        # we get here in the context that we checked even the nul: we're done!
        print('{}return k{};'.format(indent, keys[0]))
        return

    # this line could be much faster if we knew the keys were sorted, but
    # if we cared we wouldn't be using python.
    chars = list(sorted(set([char(k) for k in keys if index <= len(k)])))

    if len(chars) == 1:
        # only one choice is valid; early return if it's not that.
        print("{}if(query[{}] != '{}') {{ return kUnknown; }}".format(
                    indent, index, chars[0]))
        print_case([k for k in keys if char(k) == chars[0]], index + 1, indent)
    else:
        # multiple choices are valid; do a switch statement over the cases.
        print('{}switch(query[{}]) {{'.format(indent, index))
        for c in sorted(chars):
            print("{}  case '{}':".format(indent, c))
            print_case([k for k in keys if char(k) == c], index + 1, indent + '    ')
        print('{}  default:'.format(indent))
        print('{}    return kUnknown;'.format(indent))
        print('{}}}'.format(indent))

if __name__ == '__main__':
    if len(sys.argv) == 1:
        keys = get_keys(sys.stdin)
    else:
        keys = get_keys(sys.argv[1])
    print_enum(keys)
    print("enum Values convert(const char *query) {");
    print_case(keys, 0)
    print("}");
