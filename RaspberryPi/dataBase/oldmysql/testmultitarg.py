
def test(*args):
    if len(args) == 2:
        print "le premier argument est : " + str(args[0])
        print "le second arguement est : " + str(args[1])

    elif len(args) == 3:
        print "le premier argument est : " + str(args[0])
        print "le second arguement est : " + str(args[1])
        print "le second arguement est : " + str(args[2])

    else:
        print "bad parameter"

#programme


arg1 = "toto"
arg2 = "titi"
arg3 = "tata"
arg4 = "rien"

print "debit des test"
print "test 1"
test()

print "test 2"
test(arg1)

print "test 3"
test(arg1,arg2)

print "test 4"
test(arg1,arg2,arg3)

print "test 5"
test(arg1,arg2,arg3,arg4)