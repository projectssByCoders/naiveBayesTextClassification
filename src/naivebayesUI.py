import sys
import os
import numpy as np
from dataPreprocessing import DataPreprocessing

class NaiveBayesUI:
    
#|-----------------------------------------------------------------------------|
# naiveBayesTextClassification
#|-----------------------------------------------------------------------------|
    def naiveBayesTextClassification(self, trainingDirPath, testingDirPath):
        """
        given function performs naiveBayesTextClassification in which it performs
        I. data preprocessing
            1. reading all files
            2. tokenizing content of each files
        II.Naive Bayes 
            1. training data by 
                a. finding prior probability of each class
                b. finding conditional probability of each class based on terms
                c. apply naive Bayes
            2. find prediction class of testing data by 
                a. finding prediction probability score of each class, 
                b. assign clas with max probability score as predicted class
        """
        
        dataPreprocessing = DataPreprocessing()
        completeTokenList, uniqueTokenList, nDocsInClassArr = \
                            dataPreprocessing.preprocessData(trainingDirPath)
        
        #debug
        print ('tokenList = {} '.format(completeTokenList))
        print ('uniqueTokenList = {}'.format(uniqueTokenList))
        print ('nDocInClassArr = {}'.format(nDocsInClassArr))
        #debug -ends
#|------------------------naiveBayesTextClassification -ends-------------------|                   
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
if __name__ == '__main__':
        
        '''
        This function takes two command line arguments - 
        one is the path of the folder containing training data and 
        the other is the path of the folder containing testing data
        '''
        
        if len(sys.argv)>1:
            trainingDirPath = sys.argv[1]
            testingDirPath = sys.argv[2]
        else:
            trainingDirPath= '../dataset/5news-bydate-train'
            testingDirPath='../dataset/5news-bydate-test'
        
        naivebayesui = NaiveBayesUI()
        naivebayesui.naiveBayesTextClassification(trainingDirPath, testingDirPath)
        
        
        
    