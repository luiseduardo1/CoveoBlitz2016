import datetime
import re

class TeamMember:
    '''A team member
    
    Attributes:
        first_name (string): The first name of the team member
        last_name (string): The last name of the team member
        email (string): The email of the team member
        phone_number (string): The phone number of the team member
        educational_establishment (string): The name of the school of the team member
        study_program (string): The program in which the team member study
        date_program_end (int): The ending date of the study program
        in_charge (bool): Specifies if the team member is in charge of the team
    '''
    def __init__(self, 
                 first_name, 
                 last_name, 
                 email, 
                 phone_number, 
                 educational_establishment, 
                 study_program, 
                 date_program_end, 
                 in_charge=False):
        '''Constructor of the class

        Args:
            first_name (string): The first name of the team member
            last_name (string): The last name of the team member
            email (string): The email of the team member
            phone_number (string): The phone number of the team member
            educational_establishment (string): The name of the school of the team member
            study_program (string): The program in which the team member study
            date_program_end (datetime): The ending date of the study program
            in_charge (bool): Specifies if the team member is in charge of the team

        Raises:
            TypeError: If any of the arguments do not conform to their specified types
            ValueError: If the phone number is not in the right format
        '''
        if not isinstance(first_name, str):
            raise TypeError("The first name is not a string.")
        if not isinstance(last_name, str):
            raise TypeError("The last name is not a string.")
        if not isinstance(email, str):
            raise TypeError("The email is not a string.")
        if not isinstance(phone_number, str):
            raise TypeError("The phone number is not a string.")
        if not isinstance(educational_establishment, str):
            raise TypeError("The educational establishment is not a string.")
        if not isinstance(study_program, str):
            raise TypeError("The study program name is not a string.")
        if not isinstance(date_program_end, datetime.datetime):
            raise TypeError("The end date of the team member study program is not a datetime.")
        if not isinstance(in_charge, bool):
            raise TypeError("The in_charge variable is not a boolean.")
        if not re.match("^(1 )?\d{3}-\d{3}-\d{4}( x\d{1,5})?$", phone_number):
            raise ValueError("The phone number is not in a good format.")
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.phone_number = phone_number
        self.educational_establishment = educational_establishment
        self.study_program = study_program
        self.date_program_end = date_program_end
        self.in_charge = in_charge
