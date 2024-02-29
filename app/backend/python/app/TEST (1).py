from iota.Api import *
from iota.Device import *
from iota.Hub import *
from iota.Schedule import *
from iota.Trigger import *
from iota.User import *
from iota import genRandomID


testApi1 = Api(genRandomID(16, prefix="API-"))
testApi2 = Api(genRandomID(16, prefix="API-"))
testApi3 = Api(genRandomID(16, prefix="API-"))

testDev1 = Device(genRandomID(16, prefix="DEV-"), "TestDevice1", api=testApi1)
testDev2 = Device(genRandomID(16, prefix="DEV-"), "TestDevice2", api=testApi2)
testDev3 = Device(genRandomID(16, prefix="DEV-"), "TestDevice3", api= testApi3)


#if the user enters "var." or "i.", as a parameter, warn them that this may cause issues var. 
#should be added when the user accesses a variable codeblock
testCode = [#Start number from 1, i was just being lazy and deleted the first entry
            FunctionCode(commandType="IF",          number=2,  params=["var.test", "==", ""]),#Variables that are not previously ini[tialised are set to ''
            FunctionCode(commandType="SET",         number=3,  params=["var.test2", "=", "3"]),
            FunctionCode(commandType="END",         number=4,  linkedCommands=[2]),
            FunctionCode(commandType="WHILE",       number=5,  params=["var.test2", "<=", "3"]),
            FunctionCode(commandType="SET",         number=6,  params=["var.test2", "=", "var.i5"]), #i5 is a variable created when WHILE (number 5) runs, as an iterator, i8 will also be made when the FOR loop (number 8) is run
            FunctionCode(commandType="END",         number=7,  linkedCommands=[5]),
            FunctionCode(commandType="FOR",         number=8,  params=[3]), #RunCode() will handle types other than strings in params, this would also work as ...params=['3'] (Will not work as ...params['c'], but the form can be limited to just number here)
            FunctionCode(commandType="END",         number=9,  linkedCommands=[8]),#You don't technically need code between the start and end. - I will make it so it skips these in the future
            FunctionCode(commandType="IF",          number=10, params=[1, "==", "2"]),#will return false but not because of types. Caring about types isn't needed with iota's intended function, but i will add later if there's time.
            FunctionCode(commandType="END",         number=11, linkedCommands=[10]),
            FunctionCode(commandType="OTHERWISE",   number=12, linkedCommands=[10], params=["1", ">", "2"]), #ELSE IF
            FunctionCode(commandType="END",         number=13, linkedCommands=[12]), 
            FunctionCode(commandType="OTHERWISE",   number=14, linkedCommands=[10, 12]), #ELSE thats connected to both the if and else if - you could technically just put the number of the last ELSE IF statement in linkedCommands
            FunctionCode(commandType="END",         number=15, linkedCommands=[14]), 
            ]

testSchedule = Schedule(genRandomID(16, prefix="SDU-"), "TestRun", code=testCode, debug=True)

testSchedule.runCode()

testTrigger = Trigger(genRandomID(16, prefix="TRG-"), schedule=testSchedule, data={testDev1:["value", "==", "1"]})

testHub = Hub(genRandomID(16, prefix="HUB-"), "TestHub", schedules=[testSchedule])

testUser = User(genRandomID(16, prefix="USR-"), "admin", "pass", "email", False, {testHub, 99})
