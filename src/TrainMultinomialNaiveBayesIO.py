import sys;
import numpy as np
from collections import Counter
import math


class TrainMultinomialNaiveBayes:
    
# |---------------------------------------------------------------|
# trainNaiveBayes
# |---------------------------------------------------------------|
    def trainNaiveBayes(self,classlist,uniqueTokenList,NoOfDocsInClass,totalDocs,totalTermsInAllClasses):
        """
        This method calculates prior probability of each class and conditional probability for each term for
        each class
        """
        priorProb=np.array([])
        #NoOfClasses indicates total number of classes
        NoOfClasses=len(classlist)
        #condProbList is the list which contains the conditional probability of each term for each class
        condProbList=[]
        
        '''for each class, prior probability is calculated first using equation Nc/N where Nc represents 
           number of documents in class c and N represents total number of documents of all classes all
           together '''  
        for classIndex,classk in enumerate(classlist):
            
            #Nc is the number of documents in class c
            Nc=NoOfDocsInClass[classIndex]
            priorProb=np.append(priorProb, (float(Nc)/float(totalDocs)))
            #myclassdict contains frequency of each term of classk
            myclassdict = Counter(classk)
            #classset is a set which contains unique terms of classk
            classset = set(classk)
            #totalTermsInClass indicates count of all terms included in classk
            totalTermsinClass=len(classk)
                        
            TotalOfThisTerm=np.array([])
            
            '''uniqueTokenList contains all unique tokens of all documents of a particular class
            TotalOfThisTerm is the counter of a particular term occuring in a particular class'''
            for term in uniqueTokenList:
                TotalOfThisTerm=np.append(TotalOfThisTerm,myclassdict[term])
            
            '''TermAndProbDict is a dictionary which contains the term and its corresponding conditional probability
               of current class''' 
            TermAndProbDict={}
            for termIndex,term in enumerate(uniqueTokenList):
                condProbability= (TotalOfThisTerm[termIndex]+1)/(totalTermsinClass+totalTermsInAllClasses)
                TermAndProbDict[term]=condProbability
            #for termIndex, term -ends
            condProbList.append(TermAndProbDict)
        #for classIndex,classk ends       
                
        return priorProb,condProbList,NoOfClasses;
#|--------------------------trainNaiveBayes -ends-----------------------------------|

# |---------------------------------------------------------------------------------|
# applyMultinomialNaiveBayes
# |---------------------------------------------------------------------------------|
    def applyMultinomialNaiveBayes(self, NoOfClasses,priorProb, condProbList, TestVocab):
        """
        This method takes TestVocab for a document and predicts the class in which it may belong to
        """
        #score is a numpy array which stores probability score of all classes
        score=np.array([])
        
        #for each class, prior probability is calculated and appended to score array.
        for classIndex in range(0,NoOfClasses):
            newscore=float(math.log(priorProb[classIndex]))
            
            classCondProbDict = condProbList[classIndex]
            '''for each term in test vocabulary, probability score of class is modified by adding conditional probability 
            of that term corresponding to a particular class'''
            for term in TestVocab:
                probVal = classCondProbDict.get(term, None)
                if (probVal!=None):
                    newscore=float(newscore)+float(math.log(probVal))
            #for ends
            score=np.append(score,newscore)
        #for ends 
        #predicted class determines classIndex of the class having highest probability score.
        predictedClass=np.argmax(score)
        
        return predictedClass
#|--------------------------applyMultinomialNaiveBayes -ends-------------------|
#|-----------------------------------------------------------------------------|
# classifyAllDocs
#|-----------------------------------------------------------------------------|
    def classifyAllDocs(self, fileTokenDict, classNameList, NoOfClasses,\
                                 priorProbArr, condProbList):
        """
        input:  fileTokenDict is a dict containing file name as key and 
                file token as value
                classNameList is a list containing names of all classes
        output: fileClassDict which is a dict containing file name as key and 
                file class as value
        
        given function is a wrapper function for applyMultinomialNaiveBayes(),
        and call it for all files in the testing dataset, and it matches the
        class number with classNameList and provides fileClassDict
        """
        fileClassDict = {}
        #for all file call applyMultinomialNaiveBayes()
        for key in fileTokenDict:
            testVocab = fileTokenDict[key]
            currentPredictedClassDig=self.applyMultinomialNaiveBayes(\
                                                NoOfClasses=NoOfClasses,\
                                                priorProb=priorProbArr,\
                                                condProbList=condProbList,\
                                                TestVocab=testVocab)
            #match currentPredictedClassDig with class name and store it in the
            #fileClassDict
            currentClassVal = classNameList[currentPredictedClassDig]
            fileClassDict[key]=currentClassVal
        #for key ends
        
        return fileClassDict
#|------------------------classifyAllDocs -ends--------------------------------|    
#|-----------------------------------------------------------------------------|
# findAccuracy
#|-----------------------------------------------------------------------------|
    def findAccuracy(self, filePredictedClassDict, fileActualClassDict):
        """
        input:  filePredictedCLassDict dict where key=fileName, 
                                                    value = predicted class name
                fileActualClassDict dict where key = fileName,
                                               value = actual class name
        output: accuracy
        given function matches predicted and actual class value for each file
        and based on that returns accuracy
        """
        #initializing variables
        correctPrediction = 0
        inCorrectPrediction = 0
        totalFiles = len(filePredictedClassDict)
        #compare each files from filePredictedClassDict with fileActualClassDict
        #and increment related counters
        for key in filePredictedClassDict:
            if(filePredictedClassDict[key]==fileActualClassDict[key]):
                correctPrediction+=1
            else:
                inCorrectPrediction+=1
            #if comparison ends
        #for key -ends
        
        #accuracy: (correctVal)/totalVal
        predictionAccuracy = float(correctPrediction)/float(totalFiles)
        
        return predictionAccuracy, correctPrediction, inCorrectPrediction
#|------------------------findAccuracy -ends-----------------------------------|    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
    
    trainingFolderPath="../dataset/Training"
    trainMultinomialNaiveBayes = TrainMultinomialNaiveBayes()
    classlist=[]
   
    classlist.append(['Chinese','Beijing','Chinese','Chinese', 'Chinese','Shanghai','Chinese','Macao'])
    classlist.append(['Tokyo', 'Japan', 'Chinese'])
    
    NoOfDocsInClass=[3,1]
    totalDocs=4
    TestVocab=['Chinese', 'Chinese', 'Chinese', 'Tokyo', 'Japan']
    
    priorProb,condProbList,NoOfClasses=trainMultinomialNaiveBayes.trainNaiveBayes(classlist,NoOfDocsInClass,totalDocs)
    
    #debug
    print("condProbList : {}".format(condProbList))
    #debug -ends
    
    predictedClass=trainMultinomialNaiveBayes.applyMultinomialNaiveBayes(NoOfClasses,priorProb,condProbList,TestVocab)
    
    
    