import pymel.core as pm
import pymel.util as pmUtil
import pymel.core.datatypes as dt

from maya import cmds

from kraken.plugins.maya_plugin import logger as mayaLogger

logger = mayaLogger.getLogger("mayaLogger")


def lockObjXfo(dccSceneItem):
    """Locks the dccSceneItem's transform parameters.

    Arguments:
    dccSceneItem -- Object, DCC object to lock transform parameters on.

    Return:
    True if successful.

    """

    localXfoParams = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz', 'sx', 'sy', 'sz']
    for eachParam in localXfoParams:
        pm.setAttr(dccSceneItem.longName() + "." + eachParam, lock=True, keyable=False, channelBox=False)

    return True