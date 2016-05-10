#!/usr/bin/python
# Copyright (C) 2012 Sibi <sibi@psibi.in>
#
# This file is part of pyuClassify.
#
# pyuClassify program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyuClassify program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# pyuClassify program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with pyuClassify.  If not, see <http://www.gnu.org/licenses/>.
#
# Author:   Sibi <sibi@psibi.in>

from xml.dom.minidom import Document
from time import gmtime, strftime
from uclassify_eh import uClassifyError
import xml.dom.minidom
import requests
import base64
import socket

def sendData(xmlSchema):
	HOST = 'localhost'    # The remote host
	PORT = 54441              # The same port as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, PORT))
	s.sendall(xmlSchema)
	s.shutdown(socket.SHUT_WR)
	data = s.recv(1000000)
	s.close()
	return data


class uclassify:
    def __init__(self):
        pass

    def _buildbasicXMLdoc(self):
        doc = Document()
        root_element = doc.createElementNS('http://api.uclassify.com/1/RequestSchema', 'uclassify')
        root_element.setAttribute("version", "1.01")
        root_element.setAttribute("xmlns", "http://api.uclassify.com/1/server/RequestSchema")
        doc.appendChild(root_element)
        return doc,root_element

    def _getText(self,nodelist):
        rc = []
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc.append(node.data)
        return ''.join(rc)

    def _getResponseCode(self,content):
        """Returns the status code from the content.
           :param content: (required) XML Response content
        """
        doc = xml.dom.minidom.parseString(content)
        node = doc.documentElement
        status = node.getElementsByTagName("status")
        success = status[0].getAttribute("success")
        status_code = status[0].getAttribute("statusCode")
        text = self._getText(status[0].childNodes)
        return success, status_code, text

    def create(self,classifierName):
        """Creates a new classifier.
           :param classifierName: (required) The Classifier Name you are going to create.
        """
        doc,root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        create = doc.createElement("create")
        cur_time = strftime("%Y%m%d%H%M", gmtime())
        create.setAttribute("id",cur_time + "create" + classifierName)
        root_element.appendChild(writecalls)
        writecalls.appendChild(create)
        success, status_code, text = self._getResponseCode(sendData(doc.toxml()))
        if success == "false":
            raise uClassifyError(text,status_code)

    def addClass(self,className,classifierName):
        """Adds class to an existing Classifier.
           :param className: (required) A List containing various classes that has to be added for the given Classifier.
           :param classifierName: (required) Classifier where the classes will be added to.
        """
        doc, root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(writecalls)
        for clas in className:
            addclass = doc.createElement("addClass")
            addclass.setAttribute("id","AddClass" + clas)
            addclass.setAttribute("className",clas)
            writecalls.appendChild(addclass)
        success, status_code, text = self._getResponseCode(sendData(doc.toxml()))
        if success == "false":
            raise uClassifyError(text,status_code)
    
    def removeClass(self,className,classifierName):
        """Removes class from an existing Classifier.
           :param className: (required) A List containing various classes that will be removed from the given Classifier.
           :param classifierName: (required) Classifier
        """
        doc, root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(writecalls)
        for clas in className:
            addclass = doc.createElement("removeClass")
            addclass.setAttribute("id","removeClass" + clas)
            addclass.setAttribute("className",clas)
            writecalls.appendChild(addclass)
        success, status_code, text = self._getResponseCode(sendData(doc.toxml()))
        if success == "false":
            raise uClassifyError(text,status_code)
    
    def train(self,texts,className,classifierName):
        """Performs training on a single classs.
           :param texts: (required) A List of text used up for training.
           :param className: (required) Name of the class that needs to be trained.
           :param classifierName: (required) Name of the Classifier
        """
        base64texts = []
        for text in texts:
            base64_text = base64.b64encode(text) #For Python version 3, need to change.
            base64texts.append(base64_text)
        doc,root_element = self._buildbasicXMLdoc()
        textstag = doc.createElement("texts")
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(textstag)
        root_element.appendChild(writecalls)
        counter = 1
        for text in base64texts:
            textbase64 = doc.createElement("textBase64")
            traintag = doc.createElement("train")
            textbase64.setAttribute("id",className + "Text" + str(counter))
            ptext = doc.createTextNode(text)
            textbase64.appendChild(ptext)
            textstag.appendChild(textbase64)
            traintag.setAttribute("id","Train"+className+ str(counter))
            traintag.setAttribute("className",className)
            traintag.setAttribute("textId",className + "Text" + str(counter))
            counter = counter + 1
            writecalls.appendChild(traintag)
        success, status_code, text = self._getResponseCode(sendData(doc.toxml()))
        if success == "false":
            raise uClassifyError(text,status_code)

    def untrain(self,texts,className,classifierName):
        """Performs untraining on text for a specific class.
           :param texts: (required) A List of text used up for training.
           :param className: (required) Name of the class.
           :param classifierName: (required) Name of the Classifier
        """
        base64texts = []
        for text in texts:
            base64_text = base64.b64encode(text) #For Python version 3, need to change.
            base64texts.append(base64_text)
        doc,root_element = self._buildbasicXMLdoc()
        textstag = doc.createElement("texts")
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        root_element.appendChild(textstag)
        root_element.appendChild(writecalls)
        counter = 1
        for text in base64texts:
            textbase64 = doc.createElement("textBase64")
            traintag = doc.createElement("untrain")
            textbase64.setAttribute("id",className + "Text" + str(counter))
            ptext = doc.createTextNode(text)
            textbase64.appendChild(ptext)
            textstag.appendChild(textbase64)
            traintag.setAttribute("id","Untrain"+className+ str(counter))
            traintag.setAttribute("className",className)
            traintag.setAttribute("textId",className + "Text" + str(counter))
            counter = counter + 1
            writecalls.appendChild(traintag)
        success, status_code, text = self._getResponseCode(sendData(doc.toxml()))
        if success == "false":
            raise uClassifyError(text,status_code)

    def classify(self,texts,classifierName,username = None):
        """Performs classification on texts.
           :param texts: (required) A List of texts that needs to be classified.
           :param classifierName: (required) Classifier Name
           :param username: (optional): Name of the user, under whom the classifier exists.
        """
        doc,root_element = self._buildbasicXMLdoc()
        textstag = doc.createElement("texts")
        readcalls = doc.createElement("readCalls")
        root_element.appendChild(textstag)
        root_element.appendChild(readcalls)
        base64texts = []
        for text in texts:
            base64_text = base64.b64encode(text) #For Python version 3, need to change.
            base64texts.append(base64_text)
        counter = 1
        for text in base64texts:
            textbase64 = doc.createElement("textBase64")
            classifytag = doc.createElement("classify")
            textbase64.setAttribute("id","Classifytext"+ str(counter))
            ptext = doc.createTextNode(text)
            textbase64.appendChild(ptext)
            classifytag.setAttribute("id","Classify"+ str(counter))
            classifytag.setAttribute("classifierName",classifierName)
            classifytag.setAttribute("textId","Classifytext"+str(counter))
            if username != None:
                classifytag.setAttribute("username",username)
            textstag.appendChild(textbase64)
            readcalls.appendChild(classifytag)
            counter = counter + 1
        content = sendData(doc.toxml())
        success, status_code, text = self._getResponseCode(content)
        if success == "false":
            raise uClassifyError(text,status_code)
        else:
            return self.parseClassifyResponse(content,texts)

    def parseClassifyResponse(self,content,texts):
        """Parses the Classifier response from the server.
           :param content: (required) XML Response from server.
        """
        counter = 0
        doc = xml.dom.minidom.parseString(content)
        node = doc.documentElement
        result = []
        classifytags = node.getElementsByTagName("classification")
        for classi in classifytags:
            text_coverage = classi.getAttribute("textCoverage")
            classtags = classi.getElementsByTagName("class")
            cresult = []
            for ctag in classtags:
                classname = ctag.getAttribute("className")
                cper = ctag.getAttribute("p")
                tup = (classname,cper)
                cresult.append(tup)
            result.append((texts[counter],text_coverage,cresult))
            counter = counter + 1
        return result
            
    def classifyKeywords(self,texts,classifierName,username = None):
        """Performs classification on texts.
           :param texts: (required) A List of texts that needs to be classified.
           :param classifierName: (required) Classifier Name
           :param username: (optional): Name of the user, under whom the classifier exists.
        """
        doc,root_element = self._buildbasicXMLdoc()
        textstag = doc.createElement("texts")
        readcalls = doc.createElement("readCalls")
        root_element.appendChild(textstag)
        root_element.appendChild(readcalls)
        base64texts = []
        for text in texts:
            base64_text = base64.b64encode(text) #For Python version 3, need to change.
            base64texts.append(base64_text)
        counter = 1
        for text in base64texts:
            textbase64 = doc.createElement("textBase64")
            classifytag = doc.createElement("classifyKeywords")
            textbase64.setAttribute("id","Classifytext"+ str(counter))
            ptext = doc.createTextNode(text)
            textbase64.appendChild(ptext)
            classifytag.setAttribute("id","Classify"+ str(counter))
            classifytag.setAttribute("classifierName",classifierName)
            classifytag.setAttribute("textId","Classifytext"+str(counter))
            if username != None:
                classifytag.setAttribute("username",username)
            textstag.appendChild(textbase64)
            readcalls.appendChild(classifytag)
            counter = counter + 1
        content = sendData(doc.toxml())
        success, status_code, text = self._getResponseCode(content)
        if success == "false":
            raise uClassifyError(text,status_code)
        else:
            return self.parseClassifyResponse(content,texts)
        
        def parseClassifyKeywordResponse(self,content,texts):
            """Parses the Classifier response from the server.
              :param content: (required) XML Response from server.
            """
            counter = 0
            doc = xml.dom.minidom.parseString(content)
            node = doc.documentElement
            result = []
            keyw = []
            classifytags = node.getElementsByTagName("classification")
            keywordstags = node.getElementsByTagName("keywords")
            for keyword in keywordstags:
                classtags = keyword.getElementsByTagName("class")
                for ctag in classtags:
                    kw = ctag.firstChild.data
                if kw != "":
                    keyw.append(kw)
            for classi in classifytags:
                text_coverage = classi.getAttribute("textCoverage")
                classtags = classi.getElementsByTagName("class")
                cresult = []
                for ctag in classtags:
                    classname = ctag.getAttribute("className")
                    cper = ctag.getAttribute("p")
                    tup = (classname,cper)
                    cresult.append(tup)
                result.append((texts[counter],text_coverage,cresult,keyw))
                counter = counter + 1
            return result
    
    def getInformation(self,classifierName):
        """Returns Information about the Classifier in a List.
           :param classifierName: (required) Classifier Name
        """
        doc,root_element = self._buildbasicXMLdoc()
        readcalls = doc.createElement("readCalls")
        root_element.appendChild(readcalls)
        getinfotag = doc.createElement("getInformation")
        getinfotag.setAttribute("id","GetInformation")
        getinfotag.setAttribute("classifierName",classifierName)
        readcalls.appendChild(getinfotag)
        content = sendData(doc.toxml())
        success, status_code, text = self._getResponseCode(content)
        if success == "false":
            raise uClassifyError(text,status_code)
        else:
            return self._parseClassifierInformation(content)
        
    def _parseClassifierInformation(self,content):
        doc = xml.dom.minidom.parseString(content)
        node = doc.documentElement
        classinfo = node.getElementsByTagName("classInformation")
        result = []
        for classes in classinfo:
            cname = classes.getAttribute("className")
            uf = classes.getElementsByTagName("uniqueFeatures")
            tc = classes.getElementsByTagName("totalCount")
            for uniquef in uf:
                uf_data = uniquef.firstChild.data
            for totalc in tc:
                tc_data = totalc.firstChild.data
            result.append((cname,uf_data,tc_data))
        return result

    def removeClassifier(self,classifierName):
        """Removes Classifier.
           :param classifierName(required): Classifier Name
        """
        doc,root_element = self._buildbasicXMLdoc()
        writecalls = doc.createElement("writeCalls")
        writecalls.setAttribute("classifierName",classifierName)
        removetag = doc.createElement("remove")
        removetag.setAttribute("id","Remove")
        root_element.appendChild(writecalls)
        writecalls.appendChild(removetag)
        content = sendData(doc.toxml())
        success, status_code, text = self._getResponseCode(content)
        if success == "false":
            raise uClassifyError(text,status_code)
