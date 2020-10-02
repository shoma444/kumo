# Written and developed by Shoma Yamanouchi
# Contact: syamanou@physics.utoronto.ca
# Website: https://sites.google.com/view/shoma-yamanouchi
# version 1.0.1
version = '1.0.1'
DEVELOPED_BY_SHOMA = 'RM Budddy was developed by Shoma Yamanouchi 2020 (c)'

import os, sys, wx
import wx.lib.scrolledpanel as scrolled

class MainMenu(wx.Frame):
    def __init__(self):
        super(MainMenu, self).__init__(parent=None, title='RM Buddy',size=(500,350))
        panel = wx.Panel(self)
        menu_sizer = wx.BoxSizer(wx.VERTICAL)
        self.text_ctrl = wx.TextCtrl(panel)
        Welcome = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
        Welcome.SetLabel('Main Menu\n\nEnter the directory you wish to clean up here, and hit Start.')
        menu_sizer.Add(Welcome, 0, wx.ALL | wx.CENTER, 20)
        menu_sizer.Add(self.text_ctrl, 0, wx.ALL | wx.EXPAND, 10)
        inputpath = self.text_ctrl.GetValue()
        start_button = wx.Button(panel, label='Start')
        start_button.Bind(wx.EVT_BUTTON, self.start_press)
        menu_sizer.Add(start_button, 0, wx.ALL | wx.CENTER, 0)
        quit_button = wx.Button(panel, label='Quit')
        quit_button.Bind(wx.EVT_BUTTON, self.QuitAll)
        menu_sizer.Add(quit_button, 0, wx.ALL | wx.CENTER, 5)
        menu_sizer.AddSpacer(25)
        shoma_icon = wx.StaticBitmap(panel, bitmap=wx.Bitmap('./images/RM_Buddy_logo.png'),size=(1,1),style = wx.ALIGN_CENTRE)
        menu_sizer.Add(shoma_icon,wx.ALL | wx.CENTER)
        menu_sizer.AddSpacer(5)
        shoma_statement = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
        shoma_statement_font = wx.Font(10, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        shoma_statement.SetFont(shoma_statement_font)
        shoma_statement.SetLabel('Version '+version)
        menu_sizer.Add(shoma_statement,0,wx.ALL | wx.CENTER,2)
        shoma_statement = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
        shoma_statement_font = wx.Font(12, wx.DECORATIVE, wx.NORMAL, wx.NORMAL)
        shoma_statement.SetFont(shoma_statement_font)
        shoma_statement.SetLabel(DEVELOPED_BY_SHOMA)
        menu_sizer.Add(shoma_statement,0,wx.ALL | wx.CENTER,2)
        menu_sizer.AddSpacer(3)
        panel.SetSizer(menu_sizer)
        self.Show()

    def start_press(self, event):
        inputpath = self.text_ctrl.GetValue()
        if not inputpath:
            WarningPopup('Error','Please enter the directory you wish to clean up.',(450, 110))
        else:
            MainWrapper(inputpath)
            
    def QuitAll(self, event):
        wx.Exit()
        

def WarningPopup(Title,Text,WindowSize):
    class WarningWindow(wx.Frame):
        def __init__(self):
            super(WarningWindow, self).__init__(parent=None, title=Title,size=WindowSize)#(450, 110)
            panel = wx.Panel(self)
            errorwindow_size = wx.BoxSizer(wx.VERTICAL)
            Warning = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Warning.SetLabel(Text)#e.g., 'Please enter the directory you wish to clean up.'
            errorwindow_size.Add(Warning, 0, wx.ALL | wx.CENTER, 15)
            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            errorwindow_size.Add(close_button, 0, wx.ALL | wx.CENTER, 0)
            panel.SetSizer(errorwindow_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
    WarningWindow()


def MainWrapper(path_argument):
    inputpath = path_argument
    if inputpath[-1] != '/':
        inputpath = inputpath + '/'
    # Check if given path is valid
    ValidPathFlag = os.path.isdir(inputpath)
    if not ValidPathFlag:
        WarningPopup('Error','Directory not found! Please enter a valid path.',(450, 110))
    else:
        Core(inputpath)

def Core(path_argument):
    inputpath = path_argument
    og,dub,ogdir,dubdir = mainfunc(inputpath) # Find duplicates here
    """
    ### For testing and debugging ###
    print 'Orignial files: ', og
    print '\nPossible duplicate files: ', dub
    print '\n\nOrignial directories: ', ogdir
    print '\nPossible duplicate directories: ', dubdir
    """
    files_to_del = []
    dirs_to_del = []
    # For window size estimate
    dflen = 120+10*len(dub)
    ddlen = 120+10*len(dubdir)
    size = min([800,400+dflen,400+ddlen,220+dflen+ddlen])
    class ResultFiles(wx.Frame):
        def __init__(self):
            super(ResultFiles, self).__init__(parent=None, title='Results',size=(600,size))
            panel = wx.Panel(self)
            result_sizer = wx.BoxSizer(wx.VERTICAL)
            resultprint = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
            resultprint.SetLabel('Given directory: '+inputpath+'\n')
            result_sizer.Add(resultprint, 0, wx.ALL | wx.EXPAND, 0)
            # GUI scroll bar obtained via scrolled.ScrolledPanel
            # Possible duplicate files
            resultprintfiles = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
            resultprintfiles.SetLabel('Possible duplicate files: '+'\n')
            result_sizer.Add(resultprintfiles, 0, wx.ALL | wx.RIGHT, 0)
            self.scrolling_panel_files = scrolled.ScrolledPanel(panel, -1)
            self.scrolling_panel_files.SetAutoLayout(1)
            self.scrolling_panel_files.SetupScrolling()
            self.scrollsizer = wx.BoxSizer(wx.VERTICAL)
            for i, dubs in enumerate(dub):
                self.cb = wx.CheckBox(self.scrolling_panel_files, label = dubs, pos = (10,100+20*i))
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                if i == 0:
                    self.scrollsizer.Add(self.cb, 0, wx.ALL | wx.RIGHT, 3)
                else:
                    self.scrollsizer.Add(self.cb, 0, wx.ALL | wx.RIGHT, 3)
            self.scrolling_panel_files.SetSizer(self.scrollsizer)
            self.scrolling_panel_files.Layout()
            result_sizer.Add(self.scrolling_panel_files, 1, wx.EXPAND)
            # Possible duplicate directories
            resultprintdirs = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
            resultprintdirs.SetLabel('\nPossible duplicate directories: '+'\n')
            result_sizer.Add(resultprintdirs, 0, wx.ALL | wx.RIGHT, 0)
            self.scrolling_panel_dirs = scrolled.ScrolledPanel(panel, -1)
            self.scrolling_panel_dirs.SetAutoLayout(1)
            self.scrolling_panel_dirs.SetupScrolling()
            self.scrollsizerdir = wx.BoxSizer(wx.VERTICAL)
            for i, dubdirs in enumerate(dubdir):
                self.cb2 = wx.CheckBox(self.scrolling_panel_dirs, label = dubdirs, pos = (10,100+20*i))
                self.Bind(wx.EVT_CHECKBOX,self.ifChecked_dirs)
                if i == 0:
                    self.scrollsizerdir.Add(self.cb2, 0, wx.ALL | wx.RIGHT, 3)
                else:
                    self.scrollsizerdir.Add(self.cb2, 0, wx.ALL | wx.RIGHT, 3)
            self.scrolling_panel_dirs.SetSizer(self.scrollsizerdir)
            #self.scrolling_panel_files.SetupScrolling()
            self.scrolling_panel_dirs.Layout()
            result_sizer.Add(self.scrolling_panel_dirs, 1, wx.EXPAND)
            del_all_button = wx.Button(panel, label='Delete selected')
            del_all_button.Bind(wx.EVT_BUTTON, self.Del_files)
            result_sizer.Add(del_all_button, 0, wx.ALL | wx.CENTER, 5)
            del_select_button = wx.Button(panel, label='Delete all')
            del_select_button.Bind(wx.EVT_BUTTON, self.Del_all_files)
            result_sizer.Add(del_select_button, 0, wx.ALL | wx.CENTER, 3)
            result_sizer.AddSpacer(6)
            panel.SetSizer(result_sizer)
            self.Show()

        def ToBottomTop(self, event):
            self.scroll.Scroll(600, 350+30*len(dub))
            
        def Bottom2Top(self, event):
            self.scroll.Scroll(1, 1)
        
        # Checkbox to select for deletion
        def ifChecked(self, event):
            cb = event.GetEventObject()
            #print cb.GetLabel(),' is clicked', cb.GetValue()
            if cb.GetValue() and cb.GetLabel() not in files_to_del:
                files_to_del.append(cb.GetLabel())
            elif cb.GetValue() and cb.GetLabel() in files_to_del:
                pass
            elif not cb.GetValue() and cb.GetLabel() not in files_to_del:
                pass
            elif not cb.GetValue() and cb.GetLabel() in files_to_del:
                while cb.GetLabel() in files_to_del: files_to_del.remove(cb.GetLabel())
                
        def ifChecked_dirs(self, event):
            cb = event.GetEventObject()
            #print cb.GetLabel(),' is clicked', cb.GetValue()
            if cb.GetValue() and cb.GetLabel() not in dirs_to_del:
                dirs_to_del.append(cb.GetLabel())
            elif cb.GetValue() and cb.GetLabel() in dirs_to_del:
                pass
            elif not cb.GetValue() and cb.GetLabel() not in dirs_to_del:
                pass
            elif not cb.GetValue() and cb.GetLabel() in dirs_to_del:
                while cb.GetLabel() in dirs_to_del: dirs_to_del.remove(cb.GetLabel())
            
        def Del_files(self, event):
            if not files_to_del and not dirs_to_del:
                WarningPopup('Error','Nothing was selected for deletion!\nPlease select at least one item you want to delete.',(450, 130))
            else:
                DeleteWarning(files_to_del,dirs_to_del)
        def Del_all_files(self, event):
            if not dub and not dubdir:
                WarningPopup('Error','Nothing was selected for deletion!\nPlease select at least one item you want to delete.',(450, 130))
            else:
                DeleteWarning(dub,dubdir)
                
    class NothingFound(wx.Frame):
        def __init__(self):
            super(NothingFound, self).__init__(parent=None, title='Results',size=(450,170))
            panel = wx.Panel(self)
            result_sizerNF = wx.BoxSizer(wx.VERTICAL)
            resultprint = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
            resultprint.SetLabel('RM Budddy could not find any files or directories\nthat appeared to be duplicates in:\n '+inputpath+'\n')
            result_sizerNF.Add(resultprint, 0, wx.ALL | wx.CENTER, 15)
            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            result_sizerNF.Add(close_button, 0, wx.ALL | wx.CENTER, 1)
            quit_button = wx.Button(panel, label='Quit ')
            quit_button.Bind(wx.EVT_BUTTON, self.quit)
            result_sizerNF.Add(quit_button, 0, wx.ALL | wx.CENTER, 4)
            result_sizerNF.AddSpacer(8)
            panel.SetSizer(result_sizerNF)
            self.Show()

        def quit(self, event):
            wx.Exit()
        def closepress(self, event):
            self.Close()
 

    if len(dub) == 0 and len(dubdir) == 0:
        NothingFound()
    else:
        ResultFiles()


def DeleteWarning(path,dirspath):
    class DelWarningWindow(wx.Frame):
        def __init__(self):
            super(DelWarningWindow, self).__init__(parent=None, title='Warning!',size=(450, 130))
            panel = wx.Panel(self)
            errorwindow_size = wx.BoxSizer(wx.VERTICAL)
            Warning = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            Warning.SetLabel('You are about to delete files. This CANNOT be undone.\nDo you wish to procede?')
            errorwindow_size.Add(Warning, 0, wx.ALL | wx.CENTER, 15)
            box = wx.BoxSizer(wx.HORIZONTAL)
            abort_button = wx.Button(panel, label='No, abort')
            abort_button.Bind(wx.EVT_BUTTON, self.closepress)
            box.Add(abort_button)
            procede_button = wx.Button(panel, label='Yes, procede')
            procede_button.Bind(wx.EVT_BUTTON, self.procede)
            box.Add(procede_button,wx.RIGHT|wx.BOTTOM)
            errorwindow_size.Add(box,flag=wx.ALIGN_CENTRE|wx.CENTRE)
            panel.SetSizer(errorwindow_size)
            self.Show()
            
        def closepress(self, event):
            self.Close()
        def procede(self, event):
            Delfunc(path,dirspath)
            self.Close()
    DelWarningWindow()

def mainfunc(path): # Main function
    if path[-1] != '/':
        path = path + '/'
    flist = os.listdir(path)
    flist = [ff for ff in flist if not ff.startswith('.')]# Ignore hidden files
    flist.sort() # Sort list of files
    dirs = [items for items in flist if os.path.isdir(path+items)]
    dirs.sort() # Sort list of directories
    # Initialize lists
    duplicates = []
    oglist = []
    duplicatesdirs = []
    oglistdirs = []
    possiblenames = []
    possiblenamesdir = []

    for x in flist: # Find possible 'original' names
        if x in dirs:
            pass
        else:
            orig = False
            orig2 = False
            orig = checkendcopy(x)
            orig2 = checkendnumber(x)
            if orig and orig2:
                if len(orig)>= len(orig2):
                    shortest = orig2
                elif len(orig2)>= len(orig):
                    shortest = orig
                possiblenames.append(shortest)
            elif orig and orig2 is False:
                possiblenames.append(orig)
            elif orig2 and orig is False:
                possiblenames.append(orig2)
            else:
                pass

    possiblenames = list(set(possiblenames))
    possiblenames.sort()

    for ognames in possiblenames: # Out of the possible names, find possible duplicates
        possible_duplicates = [dubs for dubs in flist if dubs.startswith(ognames)]
        possible_originals = min(possible_duplicates,key=len)
        # Find the extnsion of the original file
        ogbyext = []
        if len(possible_originals.split('.')) > 1:
            ext = possible_originals.split('.')[-1]
            if len(possible_originals.split('.')) > 2:
                argument = '.'.join(possible_originals.split('.')[:-1])
            else:
                argument = possible_originals.split('.')[0]
        else: ext = None
        if ext:
            different_ext = [x for x in possible_duplicates if x.startswith(ognames) and not x.endswith(ext)]
            for different_ext_item in different_ext:
                if len([x for x in different_ext if x.split('.')[-1] == different_ext_item.split('.')[-1]]) == 1:
                    oglist.append(path + different_ext_item)
                    ogbyext.append(different_ext_item)
                    different_ext_Flag = True
                else:
                    different_ext_Flag = False
                if not different_ext_Flag and different_ext_item == ognames + '.' + different_ext_item.split('.')[-1]:
                    oglist.append(path + different_ext_item)
                    ogbyext.append(different_ext_item)

        possible_duplicates_list = [dubs2 for dubs2 in possible_duplicates if dubs2 != possible_originals and dubs2 not in ogbyext]
            
        
        oglist.append(path + possible_originals)
        duplicates = duplicates + [path + x for x in possible_duplicates_list]
        
    for x2 in dirs: # Same treatment for sub-directories
        orig = False
        orig2 = False
        orig = checkendcopy(x2)
        orig2 = checkendnumber(x2)
        if orig and orig2:
            if len(orig)>= len(orig2):
                shortest = orig2
            elif len(orig2)>= len(orig):
                shortest = orig
            possiblenamesdir.append(shortest)
        elif orig and orig2 is False:
            possiblenamesdir.append(orig)
        elif orig2 and orig is False:
            possiblenamesdir.append(orig2)
        else:
            pass
    possiblenamesdir = list(set(possiblenamesdir))
    possiblenamesdir.sort()

    for ognamesdir in possiblenamesdir: # Same treatment for sub-directories
        possible_duplicates = [dubs for dubs in flist if dubs.startswith(ognamesdir)]
        possible_originals = min(possible_duplicates,key=len)
        possible_duplicates_list_dir = [dubs2 for dubs2 in possible_duplicates if dubs2 != possible_originals]
        oglistdirs.append(path + possible_originals + '/')
        duplicatesdirs = duplicatesdirs + [path + x + '/' for x in possible_duplicates_list_dir]

    subdircounter = 0 # Counter for sub-directories
    for x3 in dirs:
        subdircounter = submain(path+x3,subdircounter,duplicates,oglist,duplicatesdirs,oglistdirs) # Call a nearly identical function to this one

    #oglist.sort()
    #duplicates.sort()
    #oglistdirs.sort()
    #duplicatesdirs.sort()
    return oglist, duplicates, oglistdirs, duplicatesdirs



def submain(nextpath,counter,duplicatessub,oglistsub,duplicatesdirssub,oglistdirssub): # Function for sub-directories. Can call itself.
    counter = counter + 1
    # Here, the basic idea is repeated. This functionc can call itself to go multiple directories deep.
    if nextpath[-1] != '/':
        nextpath = nextpath + '/'
    flistsub = os.listdir(nextpath)
    flistsub = [ff for ff in flistsub if not ff.startswith('.')] # Ignore hidden files
    flistsub.sort()
    dirssub = [items for items in flistsub if os.path.isdir(nextpath+items)]
    dirssub.sort()

    possiblenames = []
    possiblenamesdir = []
    
    for x in flistsub:
        if x in dirssub:
            pass
        else:
            orig = False
            orig2 = False
            orig = checkendcopy(x)
            orig2 = checkendnumber(x)
            if orig and orig2:
                if len(orig)>= len(orig2):
                    shortest = orig2
                elif len(orig2)>= len(orig):
                    shortest = orig
                possiblenames.append(shortest)
            elif orig and orig2 is False:
                possiblenames.append(orig)
            elif orig2 and orig is False:
                possiblenames.append(orig2)
            else:
                pass

    possiblenames = list(set(possiblenames))
    possiblenames.sort()
        
    for ognames in possiblenames: # Out of the possible names, find possible duplicates
        possible_duplicates = [dubs for dubs in flistsub if dubs.startswith(ognames)]
        possible_originals = min(possible_duplicates,key=len)
        # Find the extnsion of the original file
        ogbyext = []
        if len(possible_originals.split('.')) > 1:
            ext = possible_originals.split('.')[-1]
            if len(possible_originals.split('.')) > 2:
                argument = '.'.join(possible_originals.split('.')[:-1])
            else:
                argument = possible_originals.split('.')[0]
        else: ext = None
        
        if ext:
            different_ext = [x for x in possible_duplicates if x.startswith(ognames) and not x.endswith(ext)]
            for different_ext_item in different_ext:
                if len([x for x in different_ext if x.split('.')[-1] == different_ext_item.split('.')[-1]]) == 1:
                    oglistsub.append(nextpath + different_ext_item)
                    ogbyext.append(different_ext_item)
                    different_ext_Flag = True
                else:
                    different_ext_Flag = False
                if not different_ext_Flag and different_ext_item == ognames + '.' + different_ext_item.split('.')[-1]:
                    oglistsub.append(nextpath + different_ext_item)
                    ogbyext.append(different_ext_item)
        
        oglistsub.append(nextpath + possible_originals)
        possible_duplicates_list = [dubs2 for dubs2 in possible_duplicates if dubs2 != possible_originals and dubs2 not in ogbyext]
        for x in possible_duplicates_list:
            duplicatessub.append(nextpath + x)

    for x2 in dirssub:
        orig = False
        orig2 = False
        orig = checkendcopy(x2)
        orig2 = checkendnumber(x2)
        if orig and orig2:
            if len(orig)>= len(orig2):
                shortest = orig2
            elif len(orig2)>= len(orig):
                shortest = orig
            possiblenamesdir.append(shortest)
        elif orig and orig2 is False:
            possiblenamesdir.append(orig)
        elif orig2 and orig is False:
            possiblenamesdir.append(orig2)
        else:
            pass
    possiblenamesdir = list(set(possiblenamesdir))
    possiblenamesdir.sort()

    for ognamesdir in possiblenamesdir:
        possible_duplicates = [dubs for dubs in flistsub if dubs.startswith(ognamesdir)]
        possible_originals = min(possible_duplicates,key=len)
        possible_duplicates_list_dir = [dubs2 for dubs2 in possible_duplicates if dubs2 != possible_originals]
        oglistdirssub.append(nextpath + possible_originals + '/')
        duplicatesdirssub = duplicatesdirssub + [nextpath + x + '/' for x in possible_duplicates_list_dir]
        
        for x4 in dirssub:
            if counter > 10: # The program will not go beyond 10 nested sub-directories
                pass
            else:
                counter = submain(nextpath+x4,counter,duplicatessub,oglistsub,duplicatesdirssub,oglistdirssub)
    
    return counter


def checkendnumber(file2): # Check end for words like 'copy' or numbers to indicate if previously copied
    # Check for parenthisized numbers at the end of the file name
    file = file2
    originalname = False
    if len(file.split('(')) > 1:
        numb = file.split('(')[-1].split(')')[0]
        if numb.isdigit():
            file3 = file2.split('(')
            temp = file3.pop()
            originalname = '('.join(file3)[:-1]
        else: pass
    return originalname

def checkendcopy(file): # Check end for words like 'copy' or numbers to indicate if previously copied
    #Check for 'copy'
    originalname = False
    if len(file.split('copy')) > 1:
        originalname = file.split('copy')[0][:-1]
    return originalname
    
def Delfunc(args,dirsargs):
    # For debugging
    """
    for x in args:
        print 'rm ', x
    for x in dirsargs:
        print 'rm -r ', x
    """
    errors = deldirs(args+dirsargs)
    deleteditems = len(args+dirsargs) - len(errors)
    if len(errors) == 0:
        WindowSize = (450, 130)
        SuccessFlag = True
    else:
        WindowSize = (450, min([450,150+10*len(errors)]))
        SuccessFlag = False
    class DeleteDone(wx.Frame):
        def __init__(self):
            if deleteditems == 1:
                super(DeleteDone, self).__init__(parent=None, title=str(deleteditems)+' item deleted',size=WindowSize)
            else:
                super(DeleteDone, self).__init__(parent=None, title=str(deleteditems)+' items deleted',size=WindowSize)
            panel = wx.Panel(self)
            DeleteDone_size = wx.BoxSizer(wx.VERTICAL)
            DoneMessage = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE)
            if SuccessFlag:
                if deleteditems == 1:
                    DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' item!' )
                else:
                    DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' items!' )
                DeleteDone_size.Add(DoneMessage, 0, wx.ALL | wx.CENTER, 15)
            else:
                if len(errors) == 1:
                    if deleteditems == 1:
                        DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' item but encountered \nan error for a file (see below).\nClick the bottom to quit.' )
                    else:
                        DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' items but encountered \nan error for a file (see below).\nClick the bottom to quit.' )
                else:
                    if deleteditems == 1:
                        DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' item but encountered \nerrors for some files (see below).\nClick the bottom to quit.' )
                    else:
                        DoneMessage.SetLabel('RM Buddy successfully deleted '+str(deleteditems)+' items but encountered \nerrors for some files (see below).\nClick the bottom to quit.' )
                DeleteDone_size.Add(DoneMessage, 0, wx.ALL | wx.CENTER, 15)
                resultprintfiles = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
                if len(errors) == 1:
                    resultprintfiles.SetLabel('Error with the following file: '+'\n')
                else:
                    resultprintfiles.SetLabel('Errors with the following files: '+'\n')
                DeleteDone_size.Add(resultprintfiles, 0, wx.ALL | wx.RIGHT, 0)
                self.scrolling_panel_files = scrolled.ScrolledPanel(panel, -1)
                self.scrolling_panel_files.SetAutoLayout(1)
                self.scrolling_panel_files.SetupScrolling()
                self.scrollsizer = wx.BoxSizer(wx.VERTICAL)
                print errors
                for i, dubs in enumerate(errors):
                    errorlist = wx.StaticText(self.scrolling_panel_files, -1, style = wx.ALIGN_CENTRE)
                    errorlist.SetLabel(dubs)
                    #self.cb = wx.CheckBox(self.scrolling_panel_files, label = dubs, pos = (10,100+20*i))
                    #self.Bind(wx.EVT_CHECKBOX,self.ifChecked)
                self.scrolling_panel_files.SetSizer(self.scrollsizer)
                self.scrolling_panel_files.Layout()
                DeleteDone_size.Add(self.scrolling_panel_files, 1, wx.EXPAND)
                resultprintfiles2 = wx.StaticText(panel, -1, style = wx.ALIGN_CENTRE | wx.ALIGN_TOP)
                resultprintfiles2.SetLabel('Make sure you have the necessary permissions to delete the files and directories you\'ve selected.')
                DeleteDone_size.Add(resultprintfiles2, 0, wx.ALL | wx.RIGHT, 0)
            close_button = wx.Button(panel, label='Close')
            close_button.Bind(wx.EVT_BUTTON, self.closepress)
            DeleteDone_size.Add(close_button, 0, wx.ALL | wx.CENTER, 4)
            
            quit_button = wx.Button(panel, label='Quit ')
            quit_button.Bind(wx.EVT_BUTTON, self.quit)
            DeleteDone_size.Add(quit_button, 0, wx.ALL | wx.CENTER, 3)
            panel.SetSizer(DeleteDone_size)
            self.Show()
            
        def quit(self, event):
            wx.Exit()
        def closepress(self, event):
            self.Close()
    DeleteDone()


def deldirs(pathdel): # Function to delete directories. Will recursively remove directories. Be careful!
    errors = [] # For debugging. List for tracking errors (possibly due to permission issues etc.)
    for todel in pathdel:
        try:
            todel = todel.split(' ')
            todel= '\ '.join(todel)
            todel = todel.replace('(', '\(')
            todel = todel.replace(')', '\)')
            x = os.system('rm -f '+todel)
            if x:
                errors(todel)
        except:
            errors.append(todel)
    return errors


def deldirs(pathdel): # Function to delete directories. Will recursively remove directories. Be careful!
    errors = [] # For debugging. List for tracking errors (possibly due to permission issues etc.)
    for todel in pathdel:
        try:
            todel = todel.split(' ')
            todel= '\ '.join(todel)
            todel = todel.replace('(', '\(')
            todel = todel.replace(')', '\)')
            x = os.system('rm -r -f '+todel)
            if x:
                errors(todel)
        except:
            errors.append(todel)
    return errors


if __name__ == '__main__':
    """
    if path[-1] != '/': # Add a '/' at the end if needed
        path = path + '/'
    og,dub,ogdir,dubdir = mainfunc(path) # Find duplicates here
    
    # If deleting
    if DelFlag:
        fileerror = delfiles(path,og,dub,ogdir,dubdir)
    """
    app = wx.App()
    frame = MainMenu()
    app.MainLoop()


    """
    if DelDirFlag:
        direrror = deldirs(path,og,dub,ogdir,dubdir)
    """
    # Directory deletion has been commented out to avoid unwanted deletion (as this requires the use of recursive deletion)
    """
    ### For testing and debugging ###
    print 'Orignial files: ', og
    print '\nPossible duplicate files: ', dub
    print '\n\nOrignial directories: ', ogdir
    print '\nPossible duplicate directories: ', dubdir
    print '\n',fileerror
    #print '\n',direrror
    """
