import time
import os
import logging
import sys


class Raster:
    """Instantiate a raster-object, with necessary file-info"""

    def __init__(self, currPath, toDir,
                 toEpsg=25833,
                 fromEpsg=25833,
                 validExt='.tif',
                 indexName=None):

        self.toEpsg = self.validate_epsg(toEpsg)
        self.fromEpsg = self.validate_epsg(fromEpsg)
        self.filename, self.ext = self.get_basename_fileext(currPath)
        self.currPath = self.quote_text(currPath)
        self.toDir = toDir
        self.toPath = self.quote_text(self.create_toPath(toDir, self.filename, self.ext))
        self.validExt = self.validate_ext(validExt)

    def validate_epsg(self, epsg):
        try:
            epsg = int(epsg)
        except:
            sys.exit('Epsg %s is not a valid int.' % epsg)
        return epsg

    def validate_ext(self, ext):
        if not ext.startswith('.'):
            ext = '.' + ext
        if len(ext) != 4:
            sys.exit('The file-extension %s must contain 3 characters.' \
                     ' "tif" is valid, "ti" is not.' % ext)
        return ext

    def quote_text(self, text):
        if text.startswith(('"', "'")):
            text = text[1:]
        if text.endswith(('"', "'")):
            text = text[:-1]
        commentedText = '"%s"' % text
        return commentedText

    def get_basename_fileext(self, currPath):
        basename = os.path.basename(currPath)
        filename, ext = os.path.splitext(basename)
        return filename, ext

    def create_toPath(self, toDir, basename, ext):
        toPath = os.path.join(toDir, basename.lower() + ext.lower())
        return toPath


class Gdals:
    """Gdal-functions, the inputs should only be objects from the Raster-class"""

    def translate(obj):
        print ('Working on %s' % obj)
        sys.stdout.flush()
        run = "gdal_translate %s %s" % (obj.currPath, obj.toPath)
        # subprocess.call(run, shell=True)
        print (run)
        time.sleep(3)

    # def create_overviews(obj):

    # def translate_and_overviews(obj):

    # def warp(obj):

    # def create_indexes(obj):




a = Raster('Test/rAster1.tif', 'teSt1')
b = Raster('test/rAster2.tif', 'test2')
c = Raster('test/rAster3.tif', 'test3')
d = Raster('test/rAster4.tif', 'test4')
objList = [a, b, c, d]

print (a.toPath)
print (a.currPath)
print (a.ext)
print (a.filename)

import multiprocessing


pool = multiprocessing.Pool(processes=4)
results = pool.map(Gdals.translate, objList)
