#!/usr/bin/env python

import urllib.request
import uuid
import os

class stringsDownloader():
    """Class to donwload the strings, validate the url, and so on"""

    '''
    Valid Urls
       https://translate.wordpress.org/projects/wp-themes/avenue/es/default
       https://translate.wordpress.org/projects/wp/dev/es/default
       https://translate.wordpress.org/projects/wp-plugins/user-role-editor/dev/es/default

    File Strings example
        https://translate.wordpress.org/projects/wp-themes/avenue/es/default/export-translations?format=json
    '''

    testURL = "https://translate.wordpress.org/projects/wp/dev/es/default"
    dirStringsDownloaded = '/tmp/stringsDownloaded/'

    def __init__(self, url = None):

        # Create the forlder to store the files
        try:
            os.makedirs(self.dirStringsDownloaded)
        except Exception as e:
            pass

        # condition_is_true if condition else condition_is_false
        # "fat" if is_fat else "not fat"
        self.url = url if url is not None else 'https://translate.wordpress.org/projects/wp/dev/es/default'
        
        # name of the file that will contain the strings
        self.uniqueFileName = str(uuid.uuid4()) + '.json'
        pass

    def validateURL(self):
        pass


    def donwloadStrings(self):
        '''
        Given the url download the strings and store it in a temporary file
        '''
        # To download with json format
        urlExport = self.url + '/export-translations?format=json'

        print('Downloading the file')
        print( urlExport )
        urllib.request.urlretrieve(urlExport, ( self.dirStringsDownloaded +
                                                '/'+self.uniqueFileName )
                                  )
        pass


if ( __name__ == "__main__" ):
    sDownload = stringsDownloader()
    sDownload.donwloadStrings()