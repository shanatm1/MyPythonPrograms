from datetime import date

class Note:
     def __init__(self, id, creationDate, title, text, isCompleted, completionDate): # Note Constructor
         self.id = id
         self.creationDate = creationDate
         self.title = title
         self.text = text
         self.isCompleted = isCompleted
         self.completionDate = completionDate

     def display(self):                                 #display note fields
         print("id:", self.id,", creationDate:",self.creationDate,", title:",self.title,", text:",self.text,", isCompleted:", self.isCompleted,", completionDate:", self.completionDate)

     def calculateDays(self):                           # calculating number of days since completion
         if self.isCompleted == True:
             return "Days for completion = " + str((self.completionDate - self.creationDate).days)+" days."
         else:
             return "Note is not completed yet"