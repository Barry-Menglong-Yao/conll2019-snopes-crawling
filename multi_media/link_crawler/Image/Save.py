import urllib.request
import os.path
import re 


class Save:
    def __init__(self, file_name,saving_name, path=''):
        """
        SaveFile Constructor
        :param file_name:
        :param path
        :rtype: object
        """
        self.file_name = file_name
        self.base_name=saving_name
        

        self.path = path

    def save(self) -> object:
        """
        Download from web and save it to local folder
        :rtype: object
        """
        try:
            if len(self.path) > 0:
                full_file_path = self.path + '/' + self.base_name
            else:
                full_file_path = self.base_name
            urllib.request.urlretrieve(self.file_name, full_file_path) 
        except Exception as e:
            print(str(e))
        
