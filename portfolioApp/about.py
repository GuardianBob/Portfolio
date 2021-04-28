from django.shortcuts import render, redirect
# from loginApp.models import User
from django.http import JsonResponse, HttpResponseRedirect

# class AboutMe:
#     def __init__(self, firstName, lastName, gitHub="", linkedIn=""):
#         self.first_name = firstName
#         self.last_name = lastName
#         self.gitHub_link = gitHub
#         self.linkedIn_link = linkedIn
#         return self
        

#     def display_info(self):
#         print(f"Hi, I'm {self.first_name} {self.last_name}!" \
#             f"Github: {self.gitHub_link}" \
#             f"LinkedIn: {self.linkedIn_link}")
#         return self

import User

class AboutMe:
    def __init__(self):
        self.first_name = "Jesse"
        self.last_name = "Meyer"
        self.gitHub_link = "https://github.com/GuardianBob"
        self.linkedIn_link = "https://www.linkedin.com/in/meyerjg/"

    def display_info(self):
        print(f"Hi, I'm {self.first_name} {self.last_name}!", "\n" \
            f"Github: {self.gitHub_link}", "\n" f"LinkedIn: {self.linkedIn_link}", \
                "\n" "Hire me!")

jesse = AboutMe()
jesse.display_info()