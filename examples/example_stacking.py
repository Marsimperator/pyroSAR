##############################################################
# demonstration script for resampling, stacking, mosaicking and subsetting SAR images
# John Truckenbrodt 2017
##############################################################
import os
import re
from time import mktime, strptime

from pyroSAR.ancillary import finder
from pyroSAR.spatial import stack, Vector

# function to extract time stamp from file name.
# Images processed with pyroSAR functionalities via module snap or gamma will contain this information.
def seconds(name): return mktime(strptime(re.findall('[0-9T]{15}', name)[0], '%Y%m%dT%H%M%S'))


def groupbyTime(images, function, time):
    """
    function to group images by their acquisition time difference

    :param images: a list of image names
    :param function: a function to derive the time from the image names
    :param time: a time difference in seconds by which to group the images
    :return: a list of sub-lists containing the grouped images
    """
    # sort images by time stamp
    srcfiles = sorted(images, key=function)

    groups = []
    temp = []
    for item in srcfiles:
        if len(temp) == 0:
            temp.append(item)
        else:
            if 0 < abs(seconds(item)-seconds(temp[-1])) < time:
                temp.append(item)
            else:
                groups.append(temp) if len(temp) > 1 else groups.append(temp[0])
                temp = [item]
    return groups


def main():
    # define input directory containing file sto be stacked
    dir_in = '/...'

    # define output file name
    dstfile = '/.../x'

    # shapefile (for stack boundaries)
    shp = '/../x.shp'

    # store results in separate files or one single stack file? If separate then dstfile is used as a directory.
    sep = True

    # define
    srcfiles = finder(dir_in, ['S1*_VV_*norm_db.tif'])

    if os.path.isfile(dstfile):
        raise IOError('dstfile already exists')

    site = Vector(shp)

    # create groups of similar time stamps for mosaicking. All images with a time stamp of less than 30s difference will be mosaicked
    groups = groupbyTime(srcfiles, seconds, 30)

    # final function call
    stack(srcfiles=groups, dstfile=dstfile, resampling='bilinear',
          targetres=[20, 20], srcnodata=-99, dstnodata=-99,
          shapefile=site, sortfun=seconds, separate=sep, overwrite=False)

if __name__ == '__main__':
    main()
