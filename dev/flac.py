# -*- coding: utf-8 -*-
# vim: ts=4 expandtab si 

import os

from config import *
from shell import shell
from time import time
import subprocess as sp

#This class is called by every other conversion function, to return a "decode" object
class flacdecode:
    def __init__(self,infile,pipefile):
        self.infile = infile
        self.shell = shell
        self.pipe = pipefile
    def __call__(self):
#        fd = sp.Popen([flacpath + "flac", '-d', '-s', '-o',self.pipe, "%s" % self.infile],stdout=sp.PIPE,stderr=sp.PIPE,bufsize=8192)
        fd = sp.Popen([flacpath + "flac", '-d', '-s','-f', '-o',self.pipe, "%s" % self.infile],stderr=sp.PIPE)
        return (None,fd.stderr)

#Class that deals with FLAC

class flac:
    def __init__(self,flacopts=""):
        self.opts = flacopts
        self.shell = shell()
        self.qEscape = lambda x: self.shell.parseEscapechars(x,True)

    def flacConvert(self, infile, outfile,logq):
        #TODO: see about tag copying across as well
        startTime=time()
        #Seems newer versions of flac actually support flac -> flac 
        #recompression natively. Which is nice. This is now very 
        #simple to implement, hence removed the old code
        startTime = time()
        if opts['overwrite'] == True:
            self.opts += " -f "

        rc = os.system("%sflac %s -s -o '%s.flac' '%s'" %
            (
            flacpath,
            self.opts,
            outfile,
            infile
            )
        )
        if (rc == 0):
            logq.put([infile,outfile,"flac","SUCCESS",rc, time() - startTime])
        else:
            logq.put([infile,outfile,"flac","ERROR:flac ",rc, time() - startTime])


    def getflacmeta(self,flacfile):
        #flacdata = os.popen("%smetaflac --list --block-type VORBIS_COMMENT  \"%s\"" %
        flacdata = sp.check_output([
            "%smetaflac" % metaflacpath,
            "--list",
            "--block-type","VORBIS_COMMENT",
            flacfile
            ]
        )

        datalist = [] #init a list for storing all the data in this block

        #this dictionary (note different brackets) will store only the comments
        #for the music file
        commentlist = {}

        for data in flacdata.split('\n'):
            #get rid of any whitespace from the left to the right
            data = data.strip()

            #check if the tag is a comment field (shown by the first 7 chars
            #spelling out "comment")
            if(data[:8] == "comment["):
                datalist.append( data.split(':') )

        for data in datalist:
            #split according to [NAME]=[VALUE] structure
            comment = data[1].split('=')
            comment[0] = comment[0].strip()
            comment[1] = comment[1].strip()

            #convert to upper case
            #we want the key values to always be the same case, we decided on
            #uppercase (whether the string is upper or lowercase, is dependent
            # on the tagger used)
            comment[0] = comment[0].upper()

            #assign key:value pair, comment[0] will be the key, and comment[1]
            #the value
            commentlist[comment[0]] = comment[1]
        return commentlist

    def flactest(self, infile, outfile,logq):
        test = os.popen("%sflac -s -t \"%s\"" % (flacpath,self.qEscape(infile)),'r')
        results = test.read()

        #filepath = generateoutdir(file,outfile) + "results.log"

    #if (os.path.exists(filepath)):
    #   os.remove(filepath)

                #os.mknod(filepath,0775)
                #out = os.popen(filepath,'w')

                #results = ""

                #for line in test.readlines():
#                       print "++++++++++++" + line
#                       results = line

#               out.write(results)

#       print "==============" + results
#       test.flush()
        test.close()

#       out.flush()
#       out.close()



