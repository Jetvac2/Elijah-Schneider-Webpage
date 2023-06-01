import os

class PageManeger:

    def __init__(self):
        ''''
        temp_folder = "templates"
        for path in os.listdir(temp_folder):
            print(path)
            if os.path.isfile(os.path.join(temp_folder, path)) and path != "index.html":
                self.allPages.append(open("templates/" + path, "r+"))
                '''
                #Save the pages with a id in the datbase, 
                #have a thing with flask that will return a list of all the pages
                #              

    def createPage(self, name):
        try:
          page = open("templates/" + name + ".html", "x")
        except FileExistsError:
            pass

    def editPage(self, name):
        self.allPages[0].write("<h1> TEST </h1>")