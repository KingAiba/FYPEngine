import xml.etree.ElementTree as ET
import os


# utility functions to read xml and get paths
def GetAttribute(path, t, att):
    myTree = os.path.abspath(path)
    myTree = ET.parse(myTree)
    myRoot = myTree.getroot()

    for i in myRoot:
        if i.tag == t:
            return i.attrib[att]
        else:
            for j in i:
                if j.tag == t:
                    return j.attrib[att]
                else:
                    pass


def GetRootAttribute(path, att):
    myTree = os.path.abspath(path)
    myTree = ET.parse(myTree)
    myRoot = myTree.getroot()
    return myRoot.attrib.get(att)


def PathToProject():
    return os.path.dirname(__file__) + "/../../"
# print(GetAttribute('../../res/Config/actor.xml', 'Sprite', 'Alpha'))
