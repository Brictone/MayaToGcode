import maya.cmds as cmds
import subprocess

# export to cura as new scene
def returnFolder( fileFolder ):
    # if folder is empty create and use default user folder/MayaToGcode/
    folder = ''
    folderList = fileFolder.split( '/' )
    count = 0
    slash = ''
    for each in folderList[:-1]:
        if count != 0:
            slash = '/'
        folder = ( folder+slash+each )
        count += 1
    if len(folder) < 1:
        folder = os.environ.get( 'home' )
        folder = folder+'/maya/Projects/MayaToGcode'
        if not os.path.isdir( folder ):
            print 'creating folder: ', folder
            os.makedirs( folder )
    return folder+'/'
    
# get selection
originalObject = cmds.ls( selection = True ) 
print 'exporting object(s) as: ', originalObject[0]

# duplicate
object = cmds.duplicate( originalObject, name=originalObject[0], renameChildren=True )


objectGroup = cmds.group( object )

cmds.scale( 10,10,10, objectGroup )
cmds.delete( objectGroup,  constructionHistory = True )
cmds.makeIdentity( objectGroup, apply = True, t = True, r = True, s = True, n= False, pn = True )

# export selection as obj
fileFolder = cmds.file( query = True, location= True )
folder = returnFolder( fileFolder )
newFileFolder = ( folder+originalObject[0]+".obj" )
result = cmds.file( newFileFolder, force= True, typ="OBJexport", pr=True, es= True)
print result

# launch obj, opening with cura
subprocess.Popen( 'C:\Program Files\Ultimaker Cura 3.4\Cura.exe '+newFileFolder )
cmds.delete( objectGroup )
