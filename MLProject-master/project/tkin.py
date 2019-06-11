import Tkinter as tkr
import tkSimpleDialog
import tkMessageBox
from functools import reduce

import pandas as pd
import pprint

class Classifier():
    data = None
    class_attr = None
    priori = {}
    cp = {}
    hypothesis = None


    def __init__(self,filename=None, class_attr=None ):
        self.data = pd.read_csv(filename, sep=',', header =(0))
        self.class_attr = class_attr

    '''
        probability(class) =    How many  times it appears in cloumn
                             __________________________________________
                                  count of all class attribute
    '''
    def calculate_priori(self):
        class_values = list(set(self.data[self.class_attr]))
        class_data =  list(self.data[self.class_attr])
        for i in class_values:
            self.priori[i]  = class_data.count(i)/float(len(class_data))
        print ("Priori Values: ", self.priori)

    '''
        Here we calculate the individual probabilites 
        P(outcome|evidence) =   P(Likelihood of Evidence) x Prior prob of outcome
                               ___________________________________________
                                                    P(Evidence)
    '''
    def get_cp(self, attr, attr_type, class_value):
        data_attr = list(self.data[attr])
        class_data = list(self.data[self.class_attr])
        total =1
        for i in range(0, len(data_attr)):
            if class_data[i] == class_value and data_attr[i] == attr_type:
                total+=1
        return total/float(class_data.count(class_value))

    '''
        Here we calculate Likelihood of Evidence and multiple all individual probabilities with priori
        (Outcome|Multiple Evidence) = P(Evidence1|Outcome) x P(Evidence2|outcome) x ... x P(EvidenceN|outcome) x P(Outcome)
        scaled by P(Multiple Evidence)
    '''
    def calculate_conditional_probabilities(self, hypothesis):
        for i in self.priori:
            self.cp[i] = {}
            for j in hypothesis:
                self.cp[i].update({ hypothesis[j]: self.get_cp(j, hypothesis[j], i)})
        print ("\nCalculated Conditional Probabilities: \n")
        pprint.pprint(self.cp)

    def classify(self):
        root =tkr.Tk()

        print ("Result: ")
        a=[]
        for i in self.cp:
            result=reduce(lambda x, y: x*y, self.cp[i].values())*self.priori[i]
            print (i, " ==> ", result)
            a.insert(i,result)
        l=max(a)
        d=a.index(l)
        w =tkr.Label(root,text=d+1)
        w.pack()
        button = tkr.Button(root, text="Predicted Rating ", command=self.classify) 
        button.pack()
        root.mainloop()

if __name__ == "__main__":
    root =tkr.Tk()

    tkMessageBox.showinfo("welcome","add your detail here")
    

    c = Classifier(filename="googleplaystore.csv", class_attr="Rating" )
    c.calculate_priori()
    category=tkSimpleDialog.askstring("category","Enter the Category(eg.BEAUTY):")
    content_rating=tkSimpleDialog.askstring("content_rating","Enter the content_rating(HINT:Who can use your APP):")
    Generes=tkSimpleDialog.askstring("Generes","Enter the Generes(eg.Beauty):")
    Type=tkSimpleDialog.askstring("Type","Enter the Type(HINT:Free or Paid):")
    Size=tkSimpleDialog.askstring("Size","Enter the Size(eg.58M):")

    c.hypothesis = {"Category":category, "Content Rating":content_rating, "Genres":Generes , "Type":Type , "Size":Size}

    c.calculate_conditional_probabilities(c.hypothesis)
    c.classify()

