import numpy as np
from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.datasets import load_iris
from sklearn.neighbors import kneighbors_graph
from sklearn.cluster import SpectralClustering

import os

def groupByAssignment(estimator, filename, protocol):
	
	baseDir = "../related_files/" + protocol + "/ClusterResult_" + str(estimator.n_clusters)

	os.mkdir(baseDir)

	for i in xrange(estimator.n_clusters):
		os.mknod(baseDir + "/cluster_" + str(i) + ".txt");

	predict_labels = estimator.labels_


	fsrc = open(filename, "r")
	for i in xrange(predict_labels.size):
		fdst = open(baseDir + "/cluster_" + str(predict_labels[i]) + ".txt", "a")
		fdst.write(fsrc.readline());
		fdst.close()
	fsrc.close()


def flush(predict_labels, filename):
	"""
	@description: Flush data the disk.
	@filename   : Filename of output data.
	"""
	foutput = open(filename, "w")
	res = {}
	for i in xrange(predict_labels.size):
		foutput.write(str(predict_labels[i]))
		foutput.write("\n")
	print("Flush Done.")
	foutput.close()

if __name__ == '__main__':

	
	X = np.loadtxt("../related_files/pop3/pop3_pkt_64_2921_payloadEmbedding.txt", dtype=np.float, delimiter=",")

	#iris = load_iris()
	#data = iris.data
	#X = data

	n_samples, n_features = X.shape
	K = 10 

	print "n_samples: %d" % n_samples
	print "n_features: %d" % n_features

	# Kmeans
	estimator_1 = KMeans(init="k-means++", n_clusters=K, n_init=10).fit(X)
	# Spectral Clustering
	connectivity = kneighbors_graph(X, n_neighbors=10)
	affinity_matrix = 0.5 * (connectivity + connectivity.T)

	estimator_2 = SpectralClustering(n_clusters=K, 
				affinity="precomputed", 
				assign_labels="kmeans").fit(affinity_matrix)

	score_kmeans = metrics.silhouette_score(X, estimator_1.labels_, metric="euclidean")
	score_sc = metrics.silhouette_score(X, estimator_2.labels_, metric="euclidean")

	flush(estimator_2.labels_, "../related_files/pop3/pop3_pkt_64_2921_assignment.txt")


	print "silhouette score(kmeans): %f" % score_kmeans
	print "silhouette score(spectral clustering): %f" % score_sc

	groupByAssignment(estimator_1, "../related_files/pop3/pop3_pkt_64_2921.hex", "pop3")

	
	
