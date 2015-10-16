#clusterdata.py

#Description: This subtle programming aims to re-represent each sample (one flow/packet payload)in a sequence of bytes (encoded with hex )
#		by means of max-pooling technique of word embedding

#sys.argv[1] : vectorfile -> http_merge_64_1000_byteEmbedding.txt
#sys.argv[2] : inputfile -> sample hex file e.g. http_merge_64_1000.hex 
#sys.argv[3] : outputfile -> http_merge_64_1000_sampleEmbedding.txt 

import sys
import fileinput
import string

def getPayloadEmbeddingByConcatenation(vectorfile, inputfile, outputfile, numbytes):
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
			tar = []
			payload = line.split(" ")
			dimension = numbytes * v_width
			for j in range(0, dimension):
				tar.append(0.0)

			k = 0  # index for payload embedding
			for i in range(0, payload.__len__()):
				if payload[i] in vdict.keys():
					j = 0 
					for j in range(0, v_width):
						tar[k] = vdict[payload[i]][j]
						k += 1
			j = 0
			k -= 1

			#out.write(str(index_s))
			#out.write(",")
			#index_s += 1
			for j in range(0, dimension): 
				out.write(str(tar[j]))
				if j != dimension - 1:
					out.write(",")
				else:
					out.write("\n")
			
	out.close()
		


def getPayloadEmbeddingByAverage(vectorfile, inputfile, outputfile):
	vector = open(vectorfile)
	vectors = vector.readlines()
	vdict = {}
	v_width = 0   # The dimension of byte embedding
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
			c = 0 # Count the number of payload sample
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
	getPayloadEmbeddingByConcatenation(sys.argv[1], sys.argv[2], sys.argv[3], 64)
