import logging
import os
import sys
import time


logging.basicConfig(level=logging.INFO)


def validate_epsg(epsg):
    try:
        epsg = int(epsg)
    except:
        sys.exit('ERROR: Epsg:  %s  is not a valid int.' % epsg)
    return epsg


def validate_ext(ext):
    if not ext.startswith('.'):
        ext = '.' + ext
    if len(ext) != 4:
        sys.exit('ERROR: The file-extension must contain 3 characters.'
                 ' "tif" or ".tif" is valid, "ti" or ".ti" is not.'
                 ' The extension which threw the error was: %s ' % ext)
    return ext


def unquote_text(text):
    if text.startswith(('"', "'")):
        text = text[1:]
    if text.endswith(('"', "'")):
        text = text[:-1]
    return text


def quote_text(text):
    if text.startswith(('"', "'")):
        text = text[1:]
    if text.endswith(('"', "'")):
        text = text[:-1]
    commentedText = '"%s"' % text
    return commentedText


def get_filename_ext(filepath):
    basename = os.path.basename(filepath)
    filename, ext = os.path.splitext(basename)
    return filename, ext


class Raster:
    """Instantiate a raster-object with necessary file-info. Validates input.
    Contains gdal-methods to work on the raster-objects.
    """

    def __init__(self, fromPath, toDir,
                 toEpsg=25833,
                 fromEpsg=25833,
                 srcNoData=9999,
                 dstNoData=9999):

        logging.debug('Beginning to create object %s' % self)
        # the file's old/existing metadata
        self.fromPath = unquote_text(fromPath)
        self.fromPathQuoted = quote_text(fromPath)
        self.fromEpsg = validate_epsg(fromEpsg)
        self.fromFilename, self.fromExt = get_filename_ext(fromPath)
        self.srcNoData = srcNoData

        # the file's new metadata
        self.toDir = unquote_text(toDir)
        self.toDirQuoted = quote_text(toDir)
        self.toFilename = self.fromFilename.lower()
        self.toExt = self.fromExt.lower()
        self.toPath = os.path.join(self.toDir, self.toFilename + self.toExt)
        self.toPathQuoted = quote_text(self.toPath)
        self.toEpsg = validate_epsg(toEpsg)
        self.dstNoData = dstNoData
        logging.debug('Created object %s with the following properties: %s' %
                      (self, vars(self)))

    def translate(self):
        logging.info('Running gdal_translate on %s' % self.fromPathQuoted)
        run = "gdal_translate %s %s" % (self.fromPathQuoted, self.toPathQuoted)
        logging.debug('Running process: %s' % run)
        # subprocess.call(run, shell=True)
        # time.sleep(1)

    def create_overviews(self):
        logging.info('Running create_overviews on %s' % self.toPathQuoted)
        run = ("gdal_overviews %s" % self.toPathQuoted)
        logging.debug('Running process: %s' % run)

    def warp(self):
        logging.info('Running gdalwarp on %s' % self.fromPathQuoted)
        if self.srcNoData == 9999 or self.dstNoData == 9999:
            logging.warning('Found 9999 in the srcnodata- or dstnodata-values.'
                            ' 9999 is considered the default "skip"-value. '
                            'Skipping assigning nodata in gdalwarp. ')
            noData = ''
        else:
            noData = '-srcnodata %s -dstnodata %s' % (self.srcNoData, self.dstNoData)
        run = ("gdalwarp %s %s" % (noData, self.fromPathQuoted))
        logging.debug('Running process: %s' % run)

    """These "combined" methods exists to make it easier to run multiprocessing on
    the rasterfiles. If we were to f.ex. first run translate and then create_overviews
    in two different multiprocessing-operations there would be a significant timelag
    between the time the file is available externally and
    when the overviews would be created.
    """
    def translate_and_overviews(self):
        logging.debug('Running translate_and_overviews on object: %s' % self)
        self.translate()
        self.create_overviews()

    def warp_translate_overviews(self):
        """Used for sjokart"""
        logging.debug('Running warp_translate_overviews on object: %s' % self)
        self.warp()
        self.translate()
        self.create_overviews()


class Tileindex:

    def __init__(self, scanInDir, pathToCreateIndexnameFrom, validExt='.tif'):
        self.scanInDir = unquote_text(scanInDir)
        self.scanInDirQuoted = quote_text(scanInDir)
        self.validExt = validate_ext(validExt).lower()
        self.path = unquote_text(pathToCreateIndexnameFrom)

    def create_indexname(self):
        pass

    def create_tileindex(self):
        pass


a = Raster('Test/rAster1.tif', 'tja/hmm')
b = Raster('test/rAster2.tif', 'test2')
c = Raster('test/rAster3.tif', 'test3')
d = Raster('test/rAster4.tif', 'test4')
objList = [a, b, c, d]

print (a.toPath)
print (a.fromPath)
print (a.fromExt)
print (a.fromFilename)

import multiprocessing


pool = multiprocessing.Pool(processes=4)
results = pool.map(Raster.warp_translate_overviews, objList)
