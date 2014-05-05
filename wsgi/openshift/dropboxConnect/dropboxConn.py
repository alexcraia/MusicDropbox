from django.conf import settings
from dropboxConnect.models import Client
APP_KEY = settings.DROPBOX_CONSUMER_KEY
APP_SECRET = settings.DROPBOX_CONSUMER_SECRET

from dropbox.client import DropboxOAuth2Flow, DropboxClient
from django.contrib.sites.models import Site


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
    def __init__(self, access_key=None,access_secret=None,user=None):
        """Constructor"""
        if access_key == None:
            self.client = None
        else:
            cl = user.client
            sess = dropbox.session.DropboxSession(APP_KEY, APP_SECRET, 
                                                  'dropbox')
            sess.set_token(cl.key_token, cl.secret_token)
            self.client = dropbox.client.DropboxClient(sess)
        
 
    #----------------------------------------------------------------------
    def get_url_connect(self, user):
        client = Client.objects.get(user=user)
        app_key = APP_KEY
        app_secret = APP_SECRET
        access_type = "dropbox"
        session = dropbox.session.DropboxSession(app_key,
                                                 app_secret,
                                                 access_type)
        site = Site.objects.get(pk=1)
        dom = site.domain + "/first_connect/"
        req = session.obtain_request_token()
        self.request_token = req
        self.url = session.build_authorize_url(req, oauth_callback=dom)
        cl = user.client
        cl.request_key = req.key
        cl.request_secret = req.secret
        cl.save()
        return self.url

    def request_token2(self, key, secret):
        self.key = key
        self.secret = secret


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
        client = user.client
        req = self.request_token2(client.request_key,client.request_secret)
        session.set_request_token(client.request_key, client.request_secret)
        access_token = session.obtain_access_token()
        client.key_token = access_token.key
        client.secret_token = access_token.secret
        client.save()
        
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

    #---------------------------------------------------------------------
    def view_all_mp3(self):
        list_mp3 = self.client.search('/', '.mp3')

        sounds = {}
        sound = {}
        k = 0
        patht = [list_mp3[0]['path'].split('/')[1], ]
        sounds[list_mp3[0]['path'].split('/')[1]] = []
        for m in list_mp3:
            path = m['path'].split('/')[1]
            if path in patht:
                sound = {}
                sound['path'] = m['path'].split('/')[1:-1],
                sound['name'] = m['path'].split('/')[-1]
                sound['index'] = k
                sounds[path].append(sound)
            else:
                sounds[path] = []
                patht.append(path)
                sound = {}
                sound['path'] = m['path'].split('/')[1:-1],
                sound['name'] = m['path'].split('/')[-1]
                sound['index'] = k
                sounds[path].append(sound)
            k += 1
        return sounds
        #return list_mp3
if __name__ == "__main__":
    drop = DropObj("somefile.txt")
