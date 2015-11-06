#!../bin/env python

import datetime
import json
import re

class TeamMember:
    '''A team member according to the Coveo Blitz specifications
    
    Attributes:
        firstName (string): The first name of the team member
        lastName (string): The last name of the team member
        email (string): The email of the team member
        phoneNumber (string): The phone number of the team member
        educationalEstablishment (string): The name of the school of the team member
        studyProgram (string): The program in which the team member study
        dateProgramEnd (float): The ending date of the study program
        inCharge (bool): Specifies if the team member is in charge of the team
    '''
    def __init__(self, 
                 firstName, 
                 lastName, 
                 email, 
                 phoneNumber, 
                 educationalEstablishment, 
                 studyProgram, 
                 dateProgramEnd, 
                 inCharge=False):
        '''Constructor 

        Args:
            firstName (string): The first name of the team member
            lastName (string): The last name of the team member
            email (string): The email of the team member
            phoneNumber (string): The phone number of the team member
            educationalEstablishment (string): The name of the school of the team member
            studyProgram (string): The program in which the team member study
            dateProgramEnd (datetime): The ending date of the study program
            inCharge (bool) (default: False): Specifies if the team member is in charge of the team 

        Raises:
            TypeError: If any of the arguments do not conform to their specified types
            ValueError: If the phone number or the email is not in the right format
        '''
        if not isinstance(firstName, str):
            raise TypeError("The first name is not a string.")
        if not isinstance(lastName, str):
            raise TypeError("The last name is not a string.")
        if not isinstance(email, str):
            raise TypeError("The email is not a string.")
        if not isinstance(phoneNumber, str):
            raise TypeError("The phone number is not a string.")
        if not isinstance(educationalEstablishment, str):
            raise TypeError("The educational establishment is not a string.")
        if not isinstance(studyProgram, str):
            raise TypeError("The study program name is not a string.")
        if not isinstance(dateProgramEnd, datetime.datetime):
            raise TypeError("The end date of the team member study program is not a datetime.")
        if not isinstance(inCharge, bool):
            raise TypeError("The inCharge variable is not a boolean.")
        if not re.match("^(1 )?\d{3}-\d{3}-\d{4}( x\d{1,5})?$", phoneNumber):
            raise ValueError("The phone number is not in a good format.")
        if not re.match("^(\w+(\.|\-)?)+(\d+)?@\w+\.\w+$", email):
            raise ValueError("The email is not in a good format.")
        self.firstName = firstName
        self.lastName = lastName
        self.email = email
        self.phoneNumber = phoneNumber
        self.educationalEstablishment = educationalEstablishment
        self.studyProgram = studyProgram
        self.dateProgramEnd = dateProgramEnd.timestamp()
        self.inCharge = inCharge

class Team:
    '''A team according to the Coveo Blitz specification

    Attributes:
        teamName (string): The name of the team
        teamMembers (list<TeamMember>): A list of the team members
    '''
    def __init__(self,
                 teamName,
                 teamMembers=[]):
        '''Constructor

        Args:
            teamName (string): The name of the team
            teamMembers (list<TeamMember> or TeamMember) (default: []): The team member(s)

        Raises:
            TypeError: If the arguments do not respect their specified types
        '''
        if not isinstance(teamName, str):
            raise TypeError("The team name is not a string.")
        #if not isinstance(teamMembers, list) or not isinstance(teamMembers, TeamMember):
        #    raise TypeError("The team member(s) is not a list or a TeamMember.")
        self.teamName = teamName
        self.teamMembers = teamMembers

    def serializableRepresentation(self):
        '''Get a serializable representation of the instance

        Returns:
            A dictionary with the name of the attributes of the class as the keys and their values.
        '''
        return {
                "teamName" : self.teamName,
                "teamMembers" : [teamMember.__dict__ for teamMember in self.teamMembers]
               }

class ResponseWriter:
    '''The response of the server in a JSON format for the Coveo Blitz competition entry

    Attributes:
        team (Team): The team that wants to enter the competition
        matchedParagraphs (list<int>): The paragraphs that contain the specified string
    '''
    def __init__(self, team):
        '''Constructor

        Args:
            team (Team): The team that wants to enter the competition
        
        Raises:
            TypeError: If the team argument is not a Team.
        '''
        if not isinstance(team, Team):
            raise TypeError("The team is not a Team object.")
        self.team = team
        self.matchedParagraphs = []

    def parseRequest(self, request):
        '''Parses the request and gets the matched paragraphs indexes

        Args:
            request (dict<str, str>): A dictionary with the string to match 
                                        and the paragraphs in which to search 
                                        for the string

        Raises:
            TypeError: If request is not a dictionary.
        '''
        if not isinstance(request, dict):
            raise TypeError("The request is not a dictionary.")
        matchingString = request['q'].lower()
        paragraphs = request['paragraphs']
        
        for index, paragraph in paragraphs.items():
            if matchingString in paragraph.lower():
                self.matchedParagraphs.append(int(index))

    def __serializableRepresentation(self):
        '''Get a serializable representation of the instance

        Returns:
            A representation that is serializable
        '''
        representation = self.team.serializableRepresentation()
        representation['matchedParagraphs'] = self.matchedParagraphs
        return representation

    def serializeJSON(self):
        '''Serialize the instance as JSON

        Returns:
            The serialized instance
        '''
        return (self.__serializableRepresentation())

def createResponseWriter(JSONFile="/home/luiseduardo1/mysite/teamMember.json"):
    '''Create a ResponseWriter instance by reading a JSON file

    Args:
        JSONFile (string): The JSON file in which the program will read the team members

    Returns:
        The newly created ResponseWriter instance
    '''
    team = Team("Beautiful Brown")
    with open(JSONFile, 'r' ) as membersFile:
        teamMembers = json.load(membersFile)
        for member in teamMembers:
            endDate = member['dateProgramEnd']
            endDate = endDate.split('/')
            teamMember = TeamMember(member['firstName'],
                                    member['lastName'],
                                    member['email'],
                                    member['phoneNumber'],
                                    member['educationalEstablishment'],
                                    member['studyProgram'],
                                    datetime.datetime(int(endDate[2]),
                                                      int(endDate[1]),
                                                      int(endDate[0])),
                                    member['inCharge'])
            team.teamMembers.append(teamMember)
    return ResponseWriter(team)

