# -*- coding: utf-8 -*-

import json
import os
import pprint
import urllib.request
import uuid


class strings_downloader():
    '''
    Class to donwload the strings

    Valid Urls
       https://translate.wordpress.org/projects/wp-themes/avenue/es/default
       https://translate.wordpress.org/projects/wp/dev/es/default
       https://translate.wordpress.org/projects/wp-plugins/user-role-editor/dev/es/default

    File Strings example
        https://translate.wordpress.org/projects/wp-themes/avenue/es/default/export-translations?format=json
    '''

    testURL = "https://translate.wordpress.org/projects/wp/dev/es/default"
    dirStringsDownloaded = os.path.join('/tmp', 'stringsDownloaded')

    def __init__(self, url=None):

        # Create the forlder to store the files
        try:
            os.makedirs(self.dirStringsDownloaded)
        except Exception:
            pass

        # condition_is_true if condition else condition_is_false
        # "fat" if is_fat else "not fat"
        self.url = url if url is not None else self.testURL

        # name of the file that will contain the strings, something unique
        self.uniqueFileName = str(uuid.uuid4()) + '.json'

        # Contains the absolute path pointing to the file
        self.abosultePath = os.path.join(self.dirStringsDownloaded,
                                         self.uniqueFileName)

        # To store the donwloaded strings
        self.strings = dict()

    def donwload_strings(self):
        '''
        Given the url download the strings and store it in a temporary file
        '''
        # To download with json format
        urlExport = self.url + '/export-translations?format=json'
        urllib.request.urlretrieve(urlExport, self.abosultePath)

    def print_strings_downloaded(self):
        pprint.pprint(self.strings)

    def load_donwloaded_strings(self):
        f = open(self.abosultePath, 'r')
        self.strings = json.loads(f.read(),
                                       encoding='UTF-8')

    def delete_file(self):
        '''
        Delete the file downloaded
        '''
        os.remove(self.dirStringsDownloaded+"/"+self.uniqueFileName)

    def get_strings(self):
        return self.strings

if (__name__ == "__main__"):
    sDownload = strings_downloader()

    print('Donwloading the file in json format using of the project',
          sDownload.url)

    sDownload.donwload_strings()

    print('Strings Donwloaded at the dir:', sDownload.dirStringsDownloaded,
          'on the file:', sDownload.uniqueFileName)
    print('Full path:', sDownload.abosultePath)
    print('-----------------------')
    print('Showing the downloaded file')

    sDownload.load_donwloaded_strings()
    sDownload.print_strings_downloaded()

    print('-----------------------')
    print('Deleting the file...')

    sDownload.delete_file()

    print('File deleted')
