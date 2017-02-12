import logging
import time
import os
import sys


class Raster:
    """Instantiate a raster-object with necessary file-info. Validates input."""

    def __init__(self, fromPath, toDir,
                 toEpsg=25833,
                 fromEpsg=25833,
                 validExt='.tif',
                 indexName=None):

        # the file's old/existing metadata
        self.fromPath = self.unquote_text(fromPath)
        self.fromPathQuoted = self.quote_text(fromPath)
        self.fromEpsg = self.validate_epsg(fromEpsg)
        self.fromFilename, self.fromExt = self.get_basename_fileext(self.fromPath)

        # the file's new metadata
        self.toDir = self.unquote_text(toDir)
        self.toDirQuoted = self.quote_text(toDir)
        self.toFilename = self.fromFilename.lower()
        self.toExt = self.fromExt.lower()
        self.toPath = os.path.join(self.toDir, self.toFilename + self.toExt)
        self.toPathQuoted = self.quote_text(self.toPath)
        self.toEpsg = self.validate_epsg(toEpsg)
        self.validExt = self.validate_ext(validExt)

    def validate_epsg(self, epsg):
        try:
            epsg = int(epsg)
        except:
            sys.exit('Epsg:  %s  is not a valid int.' % epsg)
        return epsg

    def validate_ext(self, ext):
        if not ext.startswith('.'):
            ext = '.' + ext
        if len(ext) != 4:
            sys.exit('The file-extension %s must contain 3 characters.' \
                     ' "tif" or ".tif" is valid, "ti" or ".ti" is not.' % ext)
        return ext

    def unquote_text(self, text):
        if text.startswith(('"', "'")):
            text = text[1:]
        if text.endswith(('"', "'")):
            text = text[:-1]
        return text

    def quote_text(self, text):
        if text.startswith(('"', "'")):
            text = text[1:]
        if text.endswith(('"', "'")):
            text = text[:-1]
        commentedText = '"%s"' % text
        return commentedText

    def get_basename_fileext(self, filepath):
        basename = os.path.basename(filepath)
        filename, ext = os.path.splitext(basename)
        return filename, ext


class Gdals:
    """Gdal-functions, the inputs should only be objects from the Raster-class"""

    def translate(obj):
        print ('Working on %s' % obj)
        sys.stdout.flush()
        run = "gdal_translate %s %s" % (obj.fromPath, obj.toPath)
        # subprocess.call(run, shell=True)
        print (run)
        time.sleep(1)

    # def create_overviews(obj):

    # def translate_and_overviews(obj):

    # def warp(obj):

    # def warp_translate_overviews(obj):
        """Used for sjokart"""

    # def create_indexes(obj):

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
results = pool.map(Gdals.translate, objList)
