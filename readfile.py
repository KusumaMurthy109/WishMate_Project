class ReadFile: #reads into a file, such as .txt
    def read(self, file):
        file = open(file, 'r')
        list1 = []
        for line in file:
            list1 = line.strip().split(',')
        
        return list1

