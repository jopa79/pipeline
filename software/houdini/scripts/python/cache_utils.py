import os
import hou

def makeCachePath(mode, object):
    sceneName = hou.getenv('HIPNAME').rsplit('.v',1)[0]
    dataPath = hou.getenv('DATA')
    geoPath = dataPath + "/geo"
    scenePath = geoPath + "/" + sceneName
    nodePath = scenePath + "/" + object.name()
    startVersion = 0
    
    #mode 0 - get cache info
    if mode == 0:
        cachesList = []
        if os.path.exists(nodePath):
            for n in sorted(os.listdir(nodePath)):
                cachesList.append(nodePath + '/' + n)
            return cachesList
        
    if mode == 2:
        versionPath = ''
        #mkdir cache for current scene
        if not os.path.exists(scenePath): os.mkdir(scenePath)
        #mkdir cache for current node
        if not os.path.exists(nodePath): os.mkdir(nodePath)
        
        if not os.listdir(nodePath):
            versionPath = nodePath + "/" + str(startVersion).zfill(4)
            os.mkdir(versionPath)
        else:
            currentVersion = int(max(os.listdir(nodePath)))
            if os.path.exists(nodePath + "/" + str(startVersion).zfill(4)):
                versionPath = nodePath + "/" + str(currentVersion + 1).zfill(4)
                os.mkdir(versionPath)
        return versionPath


def abcCacheWrite(startFrame, endFrame, subFrame):

    selectedNodes = hou.selectedNodes()
    parent = selectedNodes[0].parent()
    ropnet = hou.node(parent.path()).createNode("ropnet")

    message = ''
    for n in selectedNodes:
        cachePath = makeCachePath(2, n)       
        message += 'NODE' + ' - ' + n.path() + ' > ' + 'CACHE - $DATA/geo/' + cachePath.split('geo/')[1] + '/' + n.name() + '.abc' + '\n'
        alembic = hou.node(ropnet.path()).createNode("alembic")
        alembic.setName(n.name()+"_alembic")
    
        hou.node(alembic.path()).parm("trange").set(1)
        hou.node(alembic.path()).parm("f1").set(startFrame)
        hou.node(alembic.path()).parm("f2").set(endFrame)
        hou.node(alembic.path()).parm("f3").set(1.0/subFrame)
        hou.node(alembic.path()).parm("filename").set(cachePath + "/" + n.name() + ".abc")
        hou.node(alembic.path()).parm("objects").set(n.path())

        submitButton = alembic.parm("execute")
        hou.Parm.pressButton(submitButton)

    hou.ui.displayMessage(message)
    ropnet.destroy()