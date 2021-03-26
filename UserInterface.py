from datetime import date
from datetime import datetime
from Note import Note
import os.path
from django.core.serializers.json import DjangoJSONEncoder
from collections import namedtuple
import json

class UserInterface:
    notes = []  # initializing empty list
    idCounter = 1  # initialize id

    def __init__(self):
        pass

    def Menu(self):
        while True:  # Infinite loop for the menu

            print("***** Menu *****")

            print("1. Add new Note")
            print("2. Display Note information")
            print("3. Update a Note")
            print("4. Delete a Note")
            print("5. Exit the Program")
            print("6. Total count of notes")
            print("7. Percent of notes that are incomplete")
            print("8. Update completion date for a note")
            print("9. Number of days for completion of a note")
            print("10. Save the Note")

            print("11. Load notes from file")

            print("****************")

            choice = input("Please select a menu item: ")

            if choice == "1":
                self.createNote()                                      # Adding new note
            elif choice == "2":
                noteId = input("Enter the note ID to be displayed: ")
                self.readNote(noteId)                                  # reading note by ID to display the notes
                input("Click to continue...")
            elif choice == "3":
                noteId = input("Enter the note ID to be updated: ")    # Entering  note ID to Update
                self.updateNote(noteId)
            elif choice == "4":
                noteId = input("Please enter the ID to be deleted: ")  # Enter Note ID to be deleted
                self.deleteNote(noteId)
                input("Click to continue...")
            elif choice == "5":
                break                                                  # Exit the program
            elif choice == "6":
                print("Total number of notes created = " + str(len(self.notes)))   # Showing how many notes that been created
                input("Click to continue...")
            elif choice == "7":
                if len(self.notes) > 0:
                    percentIncomplete = (sum(note.isCompleted == False for note in self.notes) / len(self.notes)) * 100
                    print("Percent of incomplete notes = " + str(percentIncomplete) + "%")  # Showing how many percent of Not that still not completed
                    input("Click to continue...")
                else:
                    print("Note not found")
            elif choice == "8":
                while True:
                    noteId = input("Please enter the note id to mark complete: ")  # Adding date manually when the note was completed
                    note = self.searchNote(noteId)
                    if note:
                        self.updateCompletion(note)
                        input("Please Click to continue...")
                        break
                    else:
                        print("Note not found")
            elif choice == "9":
                noteId = input("Please enter the ID to calculate days for completion: ")
                self.calculateDaysForCompletion(noteId) # checking the number of days, for the note to be completed
                input("Click to continue...")
            elif choice == "10":
                self.save_to_jsonfile()
            elif choice == "11":
                    self.notes = []
                    self.load_from_jsonfile()


    def searchNote(self, noteId):                                    # searching for a note  in the list
        for note in self.notes:                                      # Looping through list of notes
            if str(note.id) == noteId:
                return note

    def calculateDaysForCompletion(self, noteId):                    # method to calculate the days for completion
        note = self.searchNote(noteId)
        if note:
            print(note.calculateDays())
        else:
            print("Note not found")


    def createNote(self):
        if len(self.notes) > 0:
            self.idCounter = self.notes[len(self.notes)-1].id + 1;             # self.idCounter = self.idCounter + 1
        note = Note(self.idCounter, date.today(), "", "", False, "")
        note.title = input("please enter the titile of note: ")             # Entering Title field
        note.text = input("Please enter the text: ")                        # Entering the text field
        self.askIfCompleted(note)                                           # Ask if the note is completed or not
        self.notes.append(note)                                             # Adding new note to the list


    def askIfCompleted(self, note):                                         # method to ask if note is completed
        completed = input("is the note completed?(Y/N): ")
        if completed.upper() == "Y":
            note.isCompleted = True
            note.completionDate = date.today()
        else:
            note.isCompleted = False
            note.completionDate = ""


    def readNote(self, noteId):                                              # method to display note in the list
        note = self.searchNote(noteId)
        if note:
            note.display()                                                   # Returning found note
        else:
            print("Note not found")

    def updateNote(self, noteId):                                            # method to update note
        note = self.searchNote(noteId)
        if note:
            while True:
                print("***** Editable fields *****")                         # Updating note fields
                print("1. Title")
                print("2. Text")
                print("3. Exit from update menu")
                choice = input("Please select the field to edit: ")

                if choice == "1":
                    note.title = input("Enter the new title: ")
                    self.askIfCompleted(note)
                    print("UPDATED: Title of NoteId - " + noteId)
                elif choice == "2":
                    note.text = input("Enter the new text: ")
                    self.askIfCompleted(note)
                    print("UPDATED: Text of NoteId - " + noteId)
                elif choice == "3":
                    break
        else:
            print("Note not found")

    def updateCompletion(self, note):                                        # method to update the completion date
        date_string = input("Please enter the date of completion in YYYY-MM-DD format: ")
        isDate = self.validate_date_format(note, date_string)
        if isDate == True:
            note.isCompleted = True
            note.completionDate = datetime.strptime(date_string, '%Y-%m-%d').date()


    def deleteNote(self, noteId):                                             # method to delete note
        note = self.searchNote(noteId)
        if note:
            self.notes.remove(note)  # deleting note from list
            print("DELETED: Note Id - " + noteId)
        else:
            print("Note not found")


    def validate_date_format(self, note, date_string):            # method to validating the date format from the user
        try:
            datetime.strptime(date_string, '%Y-%m-%d')
            if datetime.strptime(date_string, '%Y-%m-%d').date() < note.creationDate:
                print("completion date cannot be less than creation date")
                return False
            else:
                return True
        except ValueError:
            print("Not a valid date")
            return False

    def save_to_jsonfile(self):                                   # save the notes in a json format in .txt file
        with open("notes.txt", "w") as file:
            x = json.dumps(
                [ob.__dict__ for ob in self.notes],
                indent=1,
                cls=DjangoJSONEncoder
            ).replace('\\n', '\n')
            file.write(x)

    def load_from_jsonfile(self):                                # method to load the txt file
        if os.path.isfile('notes.txt') == False:
            return None
        with open("notes.txt", "r") as file:
            jsonContent = file.read()
            existing_notes = json.loads(jsonContent)
            for existing_note in existing_notes:
                x = namedtuple("Note", existing_note.keys())(*existing_note.values())
                note = Note(x.id, x.creationDate, x.title, x.text, x.isCompleted, x.completionDate)
                self.notes.append(note)