#clusterdata.py

#Description: This subtle programming aims to re-represent each sample (one flow/packet payload)in a sequence of bytes (encoded with hex )
#		by means of max-pooling technique of word embedding

#sys.argv[1] : vectorfile -> wordEmbedding.txt
#sys.argv[2] : inputfile -> sample hex file e.g. smtp_merge_128_hex.post 
#		(the suffix '.post' means that this file is obtained by preprocess of smtp_merge_128_hex.log)
#sys.argv[3] : outputfile -> sampleEmbedding.txt 

import sys
import fileinput
import string

def getData(vectorfile, inputfile, outputfile):
	vector = open(vectorfile)
	vectors = vector.readlines()
	vdict = {}
	v_width = 0
	for i in range(1, vectors.__len__()):
		line = vectors[i]
		line = line.strip()
		if line:
			words = line.split("\t")
			key = words[0]
			nums = words[1].split(" ")
			v_width = nums.__len__()
			conts = []
			for j in range(0, nums.__len__()):
				conts.append(float(nums[j]))
			vdict[key] = conts
	vector.close()

	index_s = 0

	out = open(outputfile, "w")

	for line in fileinput.input(inputfile):
		line = line.strip()
		if line:
			c = 0
			tar = []
			for j in range(0, v_width):
				tar.append(0.0)
			"""
			for i in range(0, line.__len__()):
				if line[i] in vdict.keys():
					c += 1
					j = 0
					for j in range(0, v_width):
						tar[j] += vdict[line[i]][j]
			"""
			payload = line.split(" ")
			for i in range(0, payload.__len__()):
				if payload[i] in vdict.keys():
					c += 1
					j = 0
					for j in range(0, v_width):
						tar[j] += vdict[payload[i]][j]
			j = 0

			if c != 0:
				out.write(str(index_s))
				out.write(",")
				index_s += 1
				for j in range(0, v_width):
					tar[j] /= c
					out.write(str(tar[j]))
					if j != v_width - 1:
						out.write(",")
					else:
						out.write("\n")
			
	out.close()

if "__main__" == __name__:
	getData(sys.argv[1], sys.argv[2], sys.argv[3])
