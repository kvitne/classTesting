import time
import os
import logger
import sys


class Validate:

    def validate_epsg(self, epsg):
        try:
            epsg = int(epsg)
        except:
            sys.exit('Epsg %s is not valid.' % epsg)
        return epsg

    def lower(self, text):
        return text.lower()

    def quote_text(self, text):
        if text.startswith('"', "'"):
            text = text[1:]
        if text.endswith('"', "'"):
            text = text[:1]
        commentedText = '"%s"' % text
        return commentedText

    def get_basename_fileext(self, currPath):
        _, ext = os.path.splitext(currPath)
        basename = os.path.basename(currPath)
        return basename, ext,k

    def create_toPath(self, toDir, basename, ext):
        toPath = os.path.join(toDir, basename.lower(), ext.lower())
        return toPath


class Gdals(Validate):

    def __init__(self,
                currPath,
                toDir,
                toEpsg=25833,
                fromEpsg=25833):
        self.toEpsg = self.validate_epsg(toEpsg)
        self.fromEpsg = self.validate_epsg(fromEpsg)
        self.basename, self.ext = self.get_basename_fileext(currPath)
        self.currPath = self.quote_text(currPath)
        self.toDir = toDir
        self.toPath = self.quote_text(self.create_toPath(toDir, basename, ext))

    def translate(self):
        run = "gdal_translate %s %s" % (self.currPath, self.toPath)
        subprocess.call(run, shell=True)

    def create_overviews(self):

    def translate_and_overviews(self):

    def warp(self):
    def create_indexes(self, indexName, validExt):




