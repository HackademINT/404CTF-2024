import numpy as np

def encode_data(d):
	return list(d)+[sum([e for e in d])%2]

def encode_file(f):
	# Read a file and convert it to binary
	_bytes = np.fromfile(f, dtype = "uint8")
	bits = np.unpackbits(_bytes)
	output = []
	# Encode it for more data integrity safety ;)
	for i in range(0,len(bits),7):
		encoded = encode_data(bits[i:i+7])
		output += encoded.copy()
	return np.array(output,dtype="uint8")

def save_channel(data,channel):
	with open("channel_"+str(channel),"w+") as f:
		f.write(''.join(data.astype(str)))

def transmit(data):
	# Time to send it !
	# Separate each bits of each bytes 
	to_channel_1 = data[0::8] # Get the first bit of all bytes
	to_channel_2 = data[1::8] # Get the second bit of all bytes
	to_channel_3 = data[2::8] # ...
	to_channel_4 = data[3::8]
	to_channel_5 = data[4::8]
	to_channel_6 = data[5::8]
	to_channel_7 = data[6::8]
	to_channel_8 = data[7::8]
	# Send it to good channel (I hope)
	from_channel_1 = good_channel(to_channel_1)
	from_channel_2 = good_channel(to_channel_2)
	from_channel_3 = good_channel(to_channel_3)
	from_channel_4 = bad_channel(to_channel_4)  # Oups :/
	from_channel_5 = good_channel(to_channel_5)
	from_channel_6 = good_channel(to_channel_6)
	from_channel_7 = good_channel(to_channel_7)
	from_channel_8 = good_channel(to_channel_8)
	# It's up to you now ;)
	save_channel(from_channel_1,1)
	save_channel(from_channel_2,2)
	save_channel(from_channel_3,3)
	save_channel(from_channel_4,4)
	save_channel(from_channel_5,5)
	save_channel(from_channel_6,6)
	save_channel(from_channel_7,7)
	save_channel(from_channel_8,8)

def good_channel(data):
	return data
def bad_channel(data):
	return (data+np.random.randint(low=0,high=2,size=data.size,dtype='uint8'))%2

flag = encode_file("flag.png")
transmit(flag)