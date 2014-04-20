from django.conf import settings
from dropboxConnect.models import Client
APP_KEY = settings.DROPBOX_CONSUMER_KEY
APP_SECRET = settings.DROPBOX_CONSUMER_SECRET

from dropbox.client import DropboxOAuth2Flow, DropboxClient

import dropbox
import os
import sys
import webbrowser

 
########################################################################
class DropObj(object):
    """
    Dropbox object that can access your dropbox folder,
    as well as download and upload files to dropbox
    """
 
    #----------------------------------------------------------------------
    def __init__(self, filename=None, path='/'):
        """Constructor"""
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.filename = filename
        self.path = path
        self.client = None
        
        config_path = os.path.join(self.base_path, "config.ini")
 
 
    #----------------------------------------------------------------------
    def get_url_connect(self, user):
        client = Client.objects.get(user=user)
        app_key = APP_KEY
        app_secret = APP_SECRET
        access_type = "dropbox"
        session = dropbox.session.DropboxSession(app_key,
                                                 app_secret,
                                                 access_type)
        req = self.request_token(client.key_token, client.secret_token)
        url = session.build_authorize_url(req,callback="http://google.ro")
        return url

    def connect(self):
        """
        Connect and authenticate with dropbox
        """
        app_key = APP_KEY
        app_secret = APP_SECRET
 
        access_type = "dropbox"
        session = dropbox.session.DropboxSession(app_key,
                                                 app_secret,
                                                 access_type)
 
        request_token = session.obtain_request_token()
 
        url = session.build_authorize_url(request_token)
        msg = "Opening %s. Please make sure this application is allowed before continuing."
        print msg % url
        webbrowser.open(url)
        raw_input("Press enter to continue")
        access_token = session.obtain_access_token(request_token)
 
        self.client = dropbox.client.DropboxClient(session)
 
   #----------------------------------------------------------------------
    
    def save_credentials(self, user):
        access_type = 'dropbox'
        session = dropbox.session.DropboxSession(APP_KEY,
                                                 APP_SECRET,
                                                 access_type)
        request_token = session.obtain_request_token()
        Client.objects.get_or_create(user=user)
        client = Client.objects.get(user=user)
        client.key_token = request_token.key
        client.secret_token = request_token.secret
        client.save()

        
    def request_token(self,key, secret):
        self.key = key
        self.secret = secret
    def download_file(self, filename=None, outDir=None):
        """
        Download either the file passed to the class or the file passed
        to the method
        """
 
        if filename:
            fname = filename
            f, metadata = self.client.get_file_and_metadata("/" + fname)
        else:
            fname = self.filename
            f, metadata = self.client.get_file_and_metadata("/" + fname)
 
        if outDir:
            dst = os.path.join(outDir, fname)
        else:
            dst = fname
 
        with open(fname, "w") as fh:
            fh.write(f.read())
 
        return dst, metadata
 
    #----------------------------------------------------------------------
    def get_account_info(self):
        """
        Returns the account information, such as user's display name,
        quota, email address, etc
        """
        return self.client.account_info()
 
    #----------------------------------------------------------------------
    def list_folder(self, folder=None):
        """
        Return a dictionary of information about a folder
        """
        if folder:
            folder_metadata = self.client.metadata(folder)
        else:
            folder_metadata = self.client.metadata("/")
        return folder_metadata
 
    #----------------------------------------------------------------------
    def upload_file(self):
        """
        Upload a file to dropbox, returns file info dict
        """
        try:
            with open(self.filename) as fh:
                path = os.path.join(self.path, self.filename)
                res = self.client.put_file(path, fh)
                print "uploaded: ", res
        except Exception, e:
            print "ERROR: ", e
 
        return res
 
if __name__ == "__main__":
    drop = DropObj("somefile.txt")
