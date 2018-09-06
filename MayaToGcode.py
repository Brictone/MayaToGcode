import maya.cmds as cmds
import subprocess

# export to cura as new scene
def returnFolder( fileFolder ):
    folder = ''
    folderList = fileFolder.split( '/' )
    count = 0
    slash = ''
    for each in folderList[:-1]:
        if count != 0:
            slash = '/'
        folder = ( folder+slash+each )
        count += 1
    return folder+'/'
    
# get selection
originalObject = cmds.ls( selection = True ) 
print originalObject
# duplicate
object = cmds.duplicate( originalObject, name=originalObject[0], renameChildren=True )
print object
newObjectString = ''
try:
    newObject = cmds.parent( object, world=True)
    newObject = cmds.rename( newObject, originalObject )
    newObjectString = newObject
except Exception as e:
    print e
    newObjectString = object[0]
    
# scale up 10x
objectGroup = cmds.group( newObjectString, name = newObjectString+'_' )
print objectGroup
cmds.scale( 10,10,10, objectGroup )
cmds.delete( objectGroup,  constructionHistory = True )
cmds.makeIdentity( objectGroup, apply = True, t = True, r = True, s = True, n= False, pn = True )

# export selection as obj
fileFolder = cmds.file( query = True, location= True )
print fileFolder
folder = returnFolder( fileFolder )
print folder
newFileFolder = (folder+objectGroup+".obj")
print newFileFolder
result = cmds.file( newFileFolder, force= True, typ="OBJexport",pr=True, es= True)
print result

# launch obj, opening with cura
subprocess.Popen( 'C:\Program Files\Ultimaker Cura 3.4\Cura.exe '+newFileFolder )
cmds.delete( objectGroup )
