#http://notestoself.posterous.com/using-google-apps-python-provi
from os import remove
from time import strftime
import gdata.apps.service
import gdata.docs.service
import gdata.spreadsheet.service
#import xlwt
#import xlrd

#authenticate credentials and login to Google Apps
class GoogleApi():
    def __init__(self, mail, password):
        self.address = mail
        self.URL = self.address.split('@')[-1] # takes your domain out of your email address
        self.key = password
        
        self.P_service = gdata.apps.service.AppsService(email = self.address, domain = self.URL, password = self.key)
        self.S_service = gdata.spreadsheet.service.SpreadsheetsService(self.address, self.key) 
        self.D_service = gdata.docs.service.DocsService(self.address, self.key)
        
        self.P_service.ProgrammaticLogin()
        self.S_service.ProgrammaticLogin()
        self.D_service.ProgrammaticLogin()
 
    ################ READ Data
    
    def printFeed(self, feed, printer):
        '''
        Prints out the contents of a feed to the console and puts items into a python list [].
        Takes Gdata XML feed as first argument, and 'printer' as second argument.
    
  
        If printer = True, the function will print results to the console. Straight from Google documentation.
        '''
        if(len(feed.entry) == 0):
            print 'No entries in feed.\n'
        
        feedItems = []
        for i, entry in enumerate(feed.entry):
            if printer == True:
                print '%s %s' % (i+1, entry.title.text.encode('UTF-8'))
            else:
                pass
            feedItems.append(entry.title.text.encode('UTF-8'))
        
        return feedItems
    
    def getAllUsers(self, printer = False):
        '''
        Prints list of user accounts and places their names in a python list via printFeed().
        printer = False as default.
        '''
        userFeed = self.P_service.RetrieveAllUsers()
        items = self.printFeed(userFeed, printer)
        userDict = {'Users':items}
        return userDict
        
    def getAllGroups(self, printer = False):
        '''
        Prints list of Groups and places names in a python list via printFeed().
        printer = False as default.
        '''
        groupFeed = self.P_service.RetrieveAllEmailLists()
        groups = self.printFeed(groupFeed, printer)
        return groups
#Esta clase getAllGroupsPermissions es mia
    def getAllGroupsPermissions(self):
        retorno=""
        ggroups=gdata.apps.service.GroupsService(domain=self.URL)
        ggroups.ClientLogin(username=self.address, password=self.key, source="G4Btools")
        list=ggroups.RetrieveAllGroups()
        for group in list:
            retorno=retorno+group["groupId"]+ " -> "+ group["emailPermission"]  +"<br>"
        return retorno
    
    def getGroupMembers(self, groupName, printer = False):
        '''Returns a python dictionary of a given group's members --> {groupName:[members]}. printer = False as default.'''
        recipientFeed = self.P_service.RetrieveAllRecipients(groupName)
        items = self.printFeed(recipientFeed, printer)
        groupDict = {groupName:items}
        return groupDict
        
    def getAllDocs(self, printer = False):
        '''Prints list of documents in your account and places titles in a python list via printFeed(). printer = False as default.'''
        docFeed = self.D_service.GetDocumentListFeed()
        docs = self.printFeed(docFeed, printer)
        return docs
        
    def makeGroupDict(self, printer = False): #includes domain users
        '''Create a dictionary of Group:MemberList for use with spreadsheet api. printer = False as default.'''
        groups = self.getAllGroups(printer)
        users = self.getAllUsers(printer)
        groupsDict = {}
        for group in groups:
            groupsDict.update(self.getGroupMembers(group, printer))
        groupsDict.update(users)
        return groupsDict
    
    def writeXLS(self):
        '''Use xlwt and xlrd to write data to an excel file which can be uploaded to Google Docs.'''
        print 'Getting data from Google Apps...'
        groupData = self.makeGroupDict()
        groupNames = sorted([name for name in groupData.iterkeys()])
        timestamp = strftime('%a_%b_%d_%I_%M_%p')
        path = '/The/Path/To/Your/File/'
        target = 'GroupLists%s.xls' % timestamp
        
        wt = xlwt.Workbook()
        
        #Add sheets with xlwt
        print 'Building spreadsheet...'
        sum_sheet = wt.add_sheet('Group Summary')
        sum_sheet.col(0).width = 4000
        for names in groupNames:
            sh = wt.add_sheet(names)
            sh.col(0).width = 8000
            
        print 'Creating temp file...'
        wt.save('tempGroups.xls')
        
        #create dictionary of sheet positions
        rd = xlrd.open_workbook('tempGroups.xls')
        sheetIndex = [rd.sheet_by_name(group).number for group in groupNames]
        sheetConfig = dict(zip(groupNames, sheetIndex))
        
        #write data to appropriate sheets
        print 'Writing Group data...'
        for sheet in sheetConfig:
            for name in groupData[sheet]:
                wt.get_sheet(sheetConfig[sheet]).write(groupData[sheet].index(name), 0, name)
        
        #create summary sheet, list of groups, # of members
        print 'Writing Summary data...'
        heading_xf = xlwt.easyxf('font: bold on; align: wrap on, vert centre, horiz center')
        
        sum_sheet.write(0,0,'Groups', heading_xf)
        sum_sheet.write(0,1,'Size', heading_xf)
        
        for index, name in enumerate(groupNames):
            sum_sheet.write(index+1, 0, name)
            sum_sheet.write(index+1, 1, len(groupData[name]))
        
        sum_sheet.write(len(groupNames)+3, 0, '* add users to general email list to get full length of list') # this accounts for domain users and external users
        
        print 'Saving file...'
        wt.save(path+target)
        
        print 'Removing temp file...'
        remove('tempGroups.xls')
        return path+target
        
    #upload to Google Docs
     
    def uploadDoc(self, filepath):
        '''Upload spreadsheet to Google Apps account.'''
        print 'Uploading document to Google Apps...'
        ms = gdata.MediaSource(file_path = filepath, content_type = 'application/vnd.ms-excel')
        filename = filepath.split('/')[-1]
        entry = self.D_service.UploadSpreadsheet(ms,filename)
        print 'Spreadsheet Link:', entry.GetAlternateLink().href
    
    
#def main():
#    filepath = writeXLS()
#    uploadDoc(filepath)
    
    

# enable as script 
#if (__name__ == '__main__'):
#    main()
