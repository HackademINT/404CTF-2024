def decode_file():
	channel_states = []

	for i in range(1,9):
		with open("channel_"+str(i),"r") as file:
			data = file.read()
		channel_states.append(list(map(int,list(data))))
	decoded = []
	print([len(c) for c in channel_states])
	for i in range(len(channel_states[0])):
		s = 0
		for j in range(7):
			s+=channel_states[j][i]
			decoded.append(channel_states[j][i])
		if s%2 != channel_states[7][i]:
			decoded[i*7+3] = (decoded[i*7+3]+1)%2
			print("Error discovered")
	decoded = np.array(decoded,dtype="uint8")
	recovered_bytes = bytes(list(np.packbits(decoded)))
	
	with open("recovered.png", "w+b") as f:
		f.write(recovered_bytes)

decode_file()