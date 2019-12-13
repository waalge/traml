import numpy as np
import obspy 
from sklearn.decomposition import PCA
import seaborn as sns

from sklearn import metrics
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
from sklearn.preprocessing import scale

from matplotlib.mlab import specgram
from obspy.signal.util import next_pow_2
from matplotlib import pyplot as plt 
from matplotlib import mlab


def stack_spec(total_st, events_st): 
    """
    Take streams return np array of spectra
    """
    winlen = 50
    stacked_specs = np.zeros((0,8193))
    maxs = []
    for ii in range(0,len(events_st)):
        specgram, freq, time = mlab.specgram(events_st[ii].data, Fs=100, NFFT=512,
                                             pad_to=next_pow_2(winlen*total_st[0].stats.sampling_rate)*2, noverlap=winlen*0.5)

        log_spectrogram = 10*np.log10(specgram)
        if np.max(log_spectrogram) < 0:
            plt.plot(freq,np.mean(log_spectrogram,axis=1))
            stacked_specs = np.vstack((stacked_specs,np.mean(log_spectrogram,axis=1)))
        else:
            print(np.max(log_spectrogram))

        maxs.append(np.max(log_spectrogram))
        #plt.draw()
    return maxs
    return stacked_specs


def pca(stacked_specs, n_components=2): 
    pca = PCA(n_components=n_components)
    pca.fit(stacked_specs)
    return pca.transform(stacked_specs) # doctest: +SKIP

def plot_k(point_cloud, n_clusters=6, n_init =10):
    kmeans = KMeans(init='k-means++', n_clusters=n_clusters, n_init=n_init)
    #kmeans = DBSCAN(eps=0.5, min_samples=5, metric='euclidean', metric_params=None, algorithm='auto', leaf_size=30, p=None, n_jobs=None)
    kmeans.fit(point_cloud)

    # Step size of the mesh. Decrease to increase the quality of the VQ.
    h = 1     # point in the mesh [x_min, x_max]x[y_min, y_max].

    x_min, x_max = point_cloud[:, 0].min() - 1, point_cloud[:, 0].max() + 1
    y_min, y_max = point_cloud[:, 1].min() - 1, point_cloud[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))

    # Obtain labels for each point in mesh. Use last trained model.
    Z = kmeans.predict(np.c_[xx.ravel(), yy.ravel()])

    # Put the result into a color plot
    Z = Z.reshape(xx.shape)


    plt.figure(figsize=(16,9))
    plt.clf()
    plt.imshow(Z, interpolation='nearest',
               extent=(xx.min(), xx.max(), yy.min(), yy.max()),
               cmap=plt.cm.Paired,
               aspect='auto', origin='lower')

    plt.plot(point_cloud[:, 0], point_cloud[:, 1], 'k.', markersize=2)
    #plt.plot(point_cloud[find_indi, 0], point_cloud[find_indi, 1], 'r.', markersize=5)
    # Plot the centroids as a white X
    centroids = kmeans.cluster_centers_
    plt.scatter(centroids[:, 0], centroids[:, 1],
                marker='x', s=169, linewidths=3,
                color='w', zorder=10)
    plt.title('K-means clustering on the digits dataset (PCA-reduced data)\n'
              'Centroids are marked with white cross')
    plt.xlim(x_min, x_max)
    plt.ylim(y_min, y_max)
    plt.xticks(())
    plt.yticks(())

    plt.show()


if __name__ == "__main__":
    ## FOR QUICK TESTING, 
    ## RUN FILE FROM ROOT DIR
    ## THIS EXPECTS THE SPECIFIC DATA FILE OF STREAM
    ## EXPECTS EVENTS FROM STREAM

    total_st = obspy.read('./data/AM_R10DB_EHZ_2019-12-02_23_59_57_alt.sac')
    events_st = obspy.read('./data/events/*')
    stacked = stack_spec(total_st, events_st)
    trans_stacked = pca(stacked) 
    plot_k(trans_stacked) 
