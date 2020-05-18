import numpy
import glm
from Source.Renderer.BatchRenderer import BatchRenderer

# from OpenGL.GL import *
# x = GL_TRUE
# if not x:
#     print(x)
# else:
#     print("Not working")
# import os
# from xml.dom import minidom
#
# FILEPATH = os.path.dirname(__file__) + "/../../res/Config/SystemConfig.xml"
#
# myFile = minidom.parse(FILEPATH)
#
# options = myFile.getElementsByTagName('Graphics')
# print(options[0].getAttribute('maxFps'))
# # options.item(0).attributes['name'].value
#
# --------------------------------------------------------------
# foo = 1
# twod_list = []
# for i in range (0, 10):
#     new = []
#     for j in range (0, 10):
#         new.append(foo)
#         foo=foo+1
#     twod_list.append(new)
# print(twod_list)

# list = ["a", "b", "c", "d", "e","f"]
# Last = 2;
# amount = len(list)
# for x in range(Last, amount):
#     if list[x] == "h":
#         print("End")
#         break
#     print(list[x])

# from PIL import Image
# NumOfRows = 1
# NumOfCols = 6
#
# CurrRow = 1
# CurrCol = 3
#
# xOffset = CurrCol/NumOfCols
# yOffset = CurrRow/NumOfRows
#
# ImageSource = Image.open("../../res/Textures/GraveRobber_attack1.png")
# if not ImageSource:
#     print("ERROR: IMAGE NOT FOUND")
# ImageArray = ImageSource.tobytes()
# ImgX, ImgY = ImageSource.size
# newX = ImgX/NumOfCols
# newY = ImgY/NumOfRows
# print("Img Coords: X :" + str(ImgX) + " Y: " + str(ImgY))
# print("xOffset :" + str(xOffset) + " yOffset : " + str(yOffset))
# print("new: X :" + str(newX) + " Y: " + str(newY))
# print("Curr X :" + str(newX+(newX*xOffset)) + " Y: " + str(newY+(newY*yOffset)))
# a = numpy.array([1, 2, 3, 4, 5,
#                          6, 7, 8, 9, 10,
#                          1, 1, 1, 1, 1,
#
#                          1, 1, 1, 1, 1,
#                          1, 1, 1, 1, 1,
#                          1, 1, 1, 1, 1], dtype="f")
# b = numpy.array([2, 2, 2, 2, 2,
#                          2, 2, 2, 2, 2,
#                          0.0, 0.0, 0.0, 0.0, 3,
#
#                          0.0, 1.0, 0.0, 1.0, 3,
#                          1.0, 1.0, 1.0, 1.0, 3,
#                          1.0, 0.0, 1.0, 0.0, 3], dtype="f")
# verticies = numpy.array([0.0, 1.0, 0.0, 1.0,
#                                  1.0, 0.0, 1.0, 0.0,
#                                  0.0, 0.0, 0.0, 0.0,
#
#                                  0.0, 1.0, 0.0, 1.0,
#                                  1.0, 1.0, 1.0, 1.0,
#                                  1.0, 0.0, 1.0, 0.0], dtype="f")
# a = numpy.append(a ,b)
# print(a)
#
#
# a = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
# while a:
#     print (a);
#     del a[:3]
# import xml.etree.ElementTree as ET
# import os
#
#
# def find_attrib(path, t, att):
#     myTree = os.path.abspath(path)
#     myTree = ET.parse(myTree)
#     myRoot = myTree.getroot()
#
#     for i in myRoot:
#         if (i.tag == t):
#             return i.attrib[att]
#         else:
#             for j in i:
#                 if (j.tag == t):
#                     return j.attrib[att]
#                 else:
#                     pass
#
#
# print(find_attrib('../../res/Config/actor.xml', 'Sprite', 'Alpha'))
#
# -> SceneManager
# # -> Input Manager
# # -> System Class -> initialize all system -> load shader and taxtures
#
# system -> I/O
#        -> render
#         -> Level/Scene Manager
#                             ->init
#                             ->free
#                             ->update
#                           ->render

# LevelManager  -> init()
#               ->free()
#                 -> add() -> list of object in leverl
#               -> Update()
#               -> Render()
# Super class
# Level Manager in system class
# Initialize game system in system class
# Change level functions
#
# gameObject class -> attributes, check collision not part
# -> check -> engine
#
#
# arr = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
# count = 0
# for item in arr:
#     print(item)
#     del arr[count]
#     print(arr)
#     count += 1
#
arr = []
print(arr)
arr.append(1)
print(arr)
arr.append(2)
print(arr)
