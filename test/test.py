import sys
from pysyncobj import SyncObj
from pysyncobj.batteries import ReplCounter, ReplDict

a1 = sys.argv[1]
p1 = sys.argv[2]
a2 = sys.argv[3]
p2 = sys.argv[4]
a3 = sys.argv[5]
p3 = sys.argv[6]

counter1 = ReplCounter()
counter2 = ReplCounter()
dict1 = ReplDict()
syncObj = SyncObj(a1 + ':' + p1, [a2 + ':' + p2, a3 + ':' + p3], consumers=[counter1, counter2, dict1])

dict1.set('abc', 'def', sync=True)

if p1 == '3333':
	counter1.set(42, sync=True) # set initial value to 42, 'sync' means that operation is blocking
	counter1.add(10, sync=True) # add 10 to counter value
	counter2.inc(sync=True) # increment counter value by one
	dict1.set('testKey1', 'testValue1', sync=True)
	dict1['testKey2'] = 'testValue2' # this is basically the same as previous, but asynchronous (non-blocking)
	print(counter1, counter2, dict1['testKey1'], dict1.get('testKey2'))
