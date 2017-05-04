"""Global Variables for describing automata and transducers"""
#pylint: disable=C0103
####################################################################
#   THE NEXT SECTION CONTAINS LOTS OF GLOBAL VARIABLES FOR
#   DESCRIBING AUTOMATA AND TRANSDUCERS
####################################################################

#
#
##  Input altering transducers for var length codes
strpx = '@Transducer 1 * 0\n\
         0 a a 0 \n\
         0 b b 0 \n\
         0 a @epsilon 1 \n\
         0 b @epsilon 1 \n\
         1 a @epsilon 1 \n\
         1 b @epsilon 1 \n'
#tpx = fio.readOneFromString(strpx)
strsx = '@Transducer 1 * 0 \n\
         0 a @epsilon 0 \n\
         0 b @epsilon 0 \n\
         0 a @epsilon 1 \n\
         0 b @epsilon 1 \n\
         1 a a 1 \n\
         1 b b 1 \n'
#tsx = fio.readOneFromString(strsx)
strix = '@Transducer 2 3 4 \n\
         1 a @epsilon 2 \n\
         1 b @epsilon 2 \n\
         1 a a 5 \n\
         1 b b 5 \n\
         2 a @epsilon 2 \n\
         2 b @epsilon 2 \n\
         2 a a 3 \n\
         2 b b 3 \n\
         3 a a 3 \n\
         3 b b 3 \n\
         3 a @epsilon 4 \n\
         3 b @epsilon 4 \n\
         4 a @epsilon 4 \n\
         4 b @epsilon 4 \n\
         5 a a 5 \n\
         5 b b 5 \n\
         5 a @epsilon 4 \n\
         5 b @epsilon 4 \n'

# Input altering transducers
str1sd = '@Transducer 1 * 0 \n\
          0 a a 0 \n\
          0 b b 0 \n\
          0 a b 1 \n\
          1 a a 1 \n\
          1 b b 1 \n'
#t1sd = fio.readOneFromString(str1sd)
str2sd = '@Transducer 1 2 * 0 \n\
          0 a a 0 \n\
          0 b b 0 \n\
          0 a b 1 \n\
          1 a a 1 \n\
          1 b b 1 \n\
          1 a b 2 \n\
          1 b a 2 \n\
          2 a a 2 \n\
          2 b b 2 \n'
#t2sd = fio.readOneFromString(str2sd)
#
str1id = '@Transducer 1 * 0 \n\
          0 a a 0 \n\
          0 b b 0 \n\
          0 a @epsilon 1 \n\
          0 b @epsilon 1 \n\
          1 a a 1 \n\
          1 b b 1 \n'
#t1id = fio.readOneFromString(str1id)
str2id = '@Transducer 1 2 * 0 3 6 \n\
          0 a a 0 \n\
          0 b b 0 \n\
          0 a @epsilon 1 \n\
          0 b @epsilon 1 \n\
          1 a a 1 \n\
          1 b b 1 \n\
          1 a @epsilon 2 \n\
          1 b @epsilon 2 \n\
          2 a a 2 \n\
          2 b b 2 \n\
          3 a a 3 \n\
          3 b b 3 \n\
          3 a @epsilon 4 \n\
          4 b b 5 \n\
          5 a a 5 \n\
          5 b b 5 \n\
          4 @epsilon b 2 \n\
          5 @epsilon a 2 \n\
          5 @epsilon b 2 \n\
          6 a a 6 \n\
          6 b b 6 \n\
          6 @epsilon b 7 \n\
          7 a a 8 \n\
          8 a a 8 \n\
          8 b b 8 \n\
          7 a @epsilon 2 \n\
          8 a @epsilon 2 \n\
          8 b @epsilon 2 \n'
#t2id = fio.readOneFromString(str2id)
#
#
##  Input preserving transducers for error-detection
#
# Up to 1 substitution (IP transducer)
s1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 substitutions (IP transducer)
s2ts = '@Transducer 0 1 2 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 b a 1\n'\
        '0 a b 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'\
        '1 b a 2\n'\
        '1 a b 2\n'\
        '2 a a 2\n'\
        '2 b b 2\n'

# Up to 1 insertion and deletion (IP transducer)
id1ts = '@Transducer 0 1 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 @epsilon a 1\n'\
        '0 @epsilon b 1\n'\
        '0 a @epsilon 1\n'\
        '0 b @epsilon 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'

# Up to 2 insertions and deletions (IP transducer)
id2ts = '@Transducer 0 1 2 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 @epsilon a 1\n'\
        '0 @epsilon b 1\n'\
        '0 a @epsilon 1\n'\
        '0 b @epsilon 1\n'\
        '1 a a 1\n'\
        '1 b b 1\n'\
        '1 @epsilon a 2\n'\
        '1 @epsilon b 2\n'\
        '1 a @epsilon 2\n'\
        '1 b @epsilon 2\n'\
        '2 a a 2\n'\
        '2 b b 2\n'

# Up to 1 transposition error
t1ts = '@Transducer 0 3 * 0\n'\
        '0 a a 0\n'\
        '0 b b 0\n'\
        '0 a b 1\n'\
        '1 b a 3\n'\
        '0 b a 2\n'\
        '2 a b 3\n'\
        '3 a a 3\n'\
        '3 b b 3\n'

# Up to 1 transposition error over {0, 1}
t1t01s = '@Transducer 0 3 * 0\n'\
        '0 0 0 0\n'\
        '0 1 1 0\n'\
        '0 0 1 1\n'\
        '1 1 0 3\n'\
        '0 1 0 2\n'\
        '2 0 1 3\n'\
        '3 0 0 3\n'\
        '3 1 1 3\n'

#
# odd parity code of length 5
op5as = '@NFA 9 * 0\n'\
        '0 a 2\n'\
        '0 b 1\n'\
        '2 a 4\n'\
        '2 b 3\n'\
        '4 a 6\n'\
        '4 b 5\n'\
        '6 a 8\n'\
        '6 b 7\n'\
        '8 b 9\n'\
        '1 a 3\n'\
        '1 b 4\n'\
        '3 a 5\n'\
        '3 b 6\n'\
        '5 a 7\n'\
        '5 b 8\n'\
        '7 a 9\n'

a_bstar_a = '@NFA 2 * 0\n'\
        '0 a 1\n'\
        '1 b 1\n'\
        '1 a 2\n'\

a_bb_star = '@NFA 0 * 0\n'\
        '0 a 0\n'\
        '0 b 1\n'\
        '1 b 0\n'\

a_ab_bb = '@NFA 1 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 b 3\n'\
        '2 b 3\n'\

a_ab_ba = '@NFA 1 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 b 3\n'\
        '2 a 3\n'\

aa_ab_bb = '@NFA 3 * 0\n'\
        '0 a 1\n'\
        '0 b 2\n'\
        '1 a 3\n'\
        '1 b 3\n'\
        '2 b 3\n'\

strb5 = '@NFA 5 * 0 \n\
         0 a 1 \n\
         0 b 1 \n\
         1 a 2 \n\
         1 b 2 \n\
         2 a 3 \n\
         2 b 3 \n\
         3 a 4 \n\
         3 b 4 \n\
         4 a 5 \n\
         4 b 5 \n'
#ab5 = fio.readOneFromString(strb5)
strb6 = '@NFA 6 * 0 \n\
         0 a 1 \n\
         0 b 1 \n\
         1 a 2 \n\
         1 b 2 \n\
         2 a 3 \n\
         2 b 3 \n\
         3 a 4 \n\
         3 b 4 \n\
         4 a 5 \n\
         4 b 5 \n\
         5 a 6 \n\
         5 b 6 \n'
#ab6 = fio.readOneFromString(strb6)
strb7 = '@NFA 7 * 0 \n\
         0 a 1 \n\
         0 b 1 \n\
         1 a 2 \n\
         1 b 2 \n\
         2 a 3 \n\
         2 b 3 \n\
         3 a 4 \n\
         3 b 4 \n\
         4 a 5 \n\
         4 b 5 \n\
         5 a 6 \n\
         5 b 6 \n\
         6 a 7 \n\
         6 b 7 \n'
#ab7 = fio.readOneFromString(strb7)
