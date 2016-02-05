*** Settings ***
Library           criotdm.py
Library           ciotdm.py
Library           Collections

*** Variables ***
${httphost}       ${CONTROLLER}
${httpuser}       admin
${httppass}       admin
${rt_ae}          2
${rt_container}    3
${rt_contentInstance}    4

*** Test Cases ***
Set Suite Variable
    ${iserver} =    Connect To Iotdm    ${httphost}    ${httpuser}    ${httppass}    http
    Set Suite Variable    ${iserver}
    #==================================================
    #    ResultContent(rcn) Test
    #==================================================


Create the tree
    Connect And Create The Tree


*** Keywords ***
Connect And Create The Tree
    [Documentation]    Create a tree that contain AE/ container / contentInstance in different layers
    ${iserver} =    Connect To Iotdm    ${httphost}    ${httpuser}    ${httppass}    http
    ${attr} =    Set Variable    "api":"jb","apn":"jb2","or":"http://hey/you","rr":true
    Create Resource    ${iserver}    InCSE1    ${rt_ae}    ${attr}    AE1
    Create Resource    ${iserver}    InCSE1    ${rt_ae}    ${attr}    AE2
    Create Resource    ${iserver}    InCSE1    ${rt_ae}    ${attr}    AE3
    ${attr} =    Set Variable
    Create Resource    ${iserver}    InCSE1/AE1    ${rt_container}    ${attr}    Container1
    Create Resource    ${iserver}    InCSE1/AE1    ${rt_container}    ${attr}    Container2
    ${attr} =    Set Variable    "cr":null,"mni":5,"mbs":150,"or":"http://hey/you","lbl":["underCSE"]
    Create Resource    ${iserver}    InCSE1    ${rt_container}    ${attr}    Container3
    Create Resource    ${iserver}    InCSE1    ${rt_container}    ${attr}    Container4
    Create Resource    ${iserver}    InCSE1    ${rt_container}    ${attr}    Container5
    ${attr} =    Set Variable    "cr":null,"mni":5,"mbs":150,"or":"http://hey/you","lbl":["underAEContainer"]
    Create Resource    ${iserver}    InCSE1/AE1/Container1    ${rt_container}    ${attr}    Container6
    ${attr} =    Set Variable    "cr":null,"mni":5,"mbs":150,"or":"http://hey/you","lbl":["underCSEContainer"]
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_container}    ${attr}    Container7
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_container}    ${attr}    Container8
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_container}    ${attr}    Container9
    ${attr} =    Set Variable    "cnf": "1","or": "http://hey/you","con":"102","lbl":["contentInstanceUnderAEContainer"]
    Create Resource    ${iserver}    InCSE1/AE1/Container1    ${rt_contentInstance}    ${attr}    conIn1
    Create Resource    ${iserver}    InCSE1/AE1/Container1    ${rt_contentInstance}    ${attr}    conIn2
    ${attr} =    Set Variable    "cnf": "1","or": "http://hey/you","con":"102","lbl":["contentInstanceUnderContainerContainer"]
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_contentInstance}    ${attr}    conIn3
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_contentInstance}    ${attr}    conIn4
    Create Resource    ${iserver}    InCSE1/Container3    ${rt_contentInstance}    ${attr}    conIn5
    ${attr} =    Set Variable    "cnf": "1","or": "http://hey/you","con":"102","lbl":["contentInstanceUnderContainer"]
    Create Resource    ${iserver}    InCSE1/Container4    ${rt_contentInstance}    ${attr}    conIn6
    Create Resource    ${iserver}    InCSE1/Container4    ${rt_contentInstance}    ${attr}    conIn7
    Create Resource    ${iserver}    InCSE1/Container4    ${rt_contentInstance}    ${attr}    conIn8
