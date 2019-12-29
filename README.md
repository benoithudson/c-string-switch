# c-string-switch
Generate a switch statement on a string for C/C++

C# allows doing:
```
switch(a_string)
{
  case "a": // do something
  case "asdf": // something else
  case "bumblebee": // etc
  default: // yo
}
```

You can't do that in C or C++. Here's a python script that lets you do emulate it.

Run:
```
python c-string-switch.py
```

And type in the strings:
```
a
asdf
bumblebee
```

That spits out on stdout some C code (C++ compatible) that includes an enum and a function that parses a string and returns an enum value. The enum labels are the string, with a 'k' in front.
```
enum Values {
  kUnknown = 0,
  ka,
  kasdf,
  kbumblebee
}
```

This lets you write:
```
switch(convert(a_string))
{
  case ka: // do something
  case kasdf: // something else
  case kbumblebee: // etc
  default: // yo
}
```

Performance-wise the `convert` function does a single pass through the input string, which should make it notably faster than any hashing approach which at least needs to read twice (but I have no benchmarks to prove it).

## Command-line arguments

The script reads from stdin if there's no argument, and from the file named in the first argument if there is one.

There's no command-line arguments to control the name of the enum, the function, or how to generate the enum labels.
