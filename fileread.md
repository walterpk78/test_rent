CODE REVIEW OF FILE fileread.py

1) It is no necessary to create a class, It can be done with a def.
2)It has no sense to accept *args, **kwargs when the variables are fixed only 3 plus row variable
3) the import normally is done at the top of the program so any program can use it and listed in order.
4) the read and _read are so small than it can be only one def
5)the performance is bad when you call a def inside a for loop, opening files that can be very big is worst,
every call to e def has a cost instead of doing directly. It use not only once but twice a for loop with a def inside.
One for read and another for __mangle.
6) the log inside _read is repetitive filling a disk with every record it reads, it would be better to use it in the exception, where it is more important to trace what happened, not only do not use a log but instead a print! and with irrelevant information, not variables printed.
7)Another interesting thing is that a implicit "private"  _  is calling to a non declared private example: _read() call __mangle and __mangle call get_mangled_row.
the algorithm not only mangle the file but also the code for fun.
