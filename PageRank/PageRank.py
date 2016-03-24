import sys, math

dampingFactor = 0.85

class PageRank:
    def __init__(self, filename):
        self.__inLinks = {}
        self.__outLinks = {}
        self.__PR = {}
        self.__perplexityList = []
        self.__freader = open(filename)
        self.__processFile()
    
    def __processFile(self):
        """
        processes the inlinks file and stores the inlinks and outlinks 
        """
        line = self.__freader.readline()
        while line:
            pages = line.split()
            linesize = len(pages)
            if linesize == 0:
                break
            dstPage = pages[0]
            srcPages = pages[1:]
            self.__inLinks[dstPage] = srcPages
            self.__modifyOutLinks(dstPage, 0)
            #print self.__outLinks
            if len(srcPages) > 0:
                for srcPage in srcPages:
                    self.__modifyOutLinks(srcPage, 1)
            line = self.__freader.readline()
    
    def __modifyOutLinks(self, word, increment):
        """
        modifies the count of outlinks of a word
        """
        count = self.__outLinks.get(word)
        if count == None:
            self.__outLinks[word] = increment
        else:
            self.__outLinks[word] = count + increment

    def computePR(self):
        """
        Compute the pagerank value of all the pages
        """
        N = float(len(self.__outLinks))
        for page in self.__outLinks.keys():
            self.__PR[page] = 1.0/N
        PRTmp = {}
        while not self.__checkConvergence():
            sinkPR = 0.0
            for page,oLinks in self.__outLinks.items():
                if oLinks == 0:
                    sinkPR += self.__PR[page]
            for page,iLinks in self.__inLinks.items():
                newPR = (1.0 - dampingFactor)/N
                newPR = newPR + dampingFactor*sinkPR/N
                for link in iLinks:
                    newPR = newPR + dampingFactor*self.__PR[link]/float(self.__outLinks[link])
                PRTmp[page] = newPR
            self.__PR = PRTmp
            PRTmp = {}        

    def sortAndPrint(self, numPages):
        """
        Sort the documents by their PageRank and output the top <arg0> documents
        """
        sortedPR = sorted([(PR, pages) for (pages, PR) in self.__PR.items()], reverse=True)
        print "Top %d documents: " % numPages
        for n in range(numPages):
            print "{:15}".format(sortedPR[n][1]) + '   ' + \
                    '{0:.8f}'.format(sortedPR[n][0])

    def printPerplexities(self):
        """
        Prints the perplexities computed in every iteration
        """    
        size = len(self.__perplexityList)
        print "Perplexities:"
        for n in range(size):
            print '{:10}'.format('Round %d' %(n+1)) + '   '    + \
                    '{0:.4f}'.format(self.__perplexityList[n])

    def __checkConvergence(self):
        """
        check if the computation has reached convergence
        """
        perplexity = self.__computePerplexity()
        pInt = math.floor(perplexity)
        similarPerps = filter(lambda x: \
                                math.fabs(math.floor(perplexity)-x) <= 5, \
                                self.__perplexityList)
        if len(similarPerps) >= 2:
            return True
        else:
            self.__perplexityList.append(perplexity)
            return False

    def __computePerplexity(self):
        entropy = 0.0
        for page, PR in self.__PR.items():
            entropy = entropy - PR*math.log(PR, 2)
        perplexity = math.pow(2, entropy)
        return perplexity

def main():
    pr = PageRank("wt2g_inlinks.txt")
    pr.computePR()
    pr.printPerplexities()
    pr.sortAndPrint(20)
    
if __name__ == "__main__":
    main()
