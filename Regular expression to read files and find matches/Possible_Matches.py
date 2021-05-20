#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
# Name: Parvez Golam
# Date: 05/03/2021
# Reading files of Iris marriages records and finding possible matches
#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------

import re

class FileParser:
    '''
    Class for parsing file extracting information
    based on regular expression setup
    '''
    def __init__(self):
        # Constants
        self.NAME = "name"
        self.AREA = "area"
        self.YEAR = "year"
        self.QUARTER = "quarter"
        self.VOLUME = "volume"
        self.PAGE = "page"

        # regular expression setup to collect 
        # Name, district and returns year/quarter/volume/page
        self.__reg_dict = {
            self.NAME: re.compile(r"Marriage of(?P<name>.+)\n"),
            self.AREA: re.compile(r"SR District/Reg Area\t(?P<area>.*)\n"), 
            self.YEAR: re.compile(r"Returns Year\t(?P<year>\d+)\n"),
            self.QUARTER: re.compile(r"Returns Quarter\t(?P<quarter>\d)\n"),
            self.VOLUME: re.compile(r"Returns Volume No\t(?P<volume>\d+)\n"),
            self.PAGE: re.compile(r"Returns Page No\t(?P<page>\d+)\n"),
        }

    def parse_line(self,line):
        '''
        Method that finds and returns the match object from 'line'
        by using Regular expression setup
        '''

        for key, rx in self.__reg_dict.items():
            match = rx.search(line)
            if match:
                return key, match
    
        return None, None

    def parse_file(self,file_name):
        '''
        Method that takes text file in 'file_name' and returns 
        all the possible matches from  Regular expression setup 
        '''
        data = []
        row = {}

        textfile = open(file_name, "r")
        line = textfile.readline()

        # get the file data in below format
        # [{Name: 'name_value' , 
        #   District: 'Dist_value', 
        #   Year: 'year_value',
        #   Quarter: 'quarter_value', 
        #   Volume: 'volume_number',
        #   Page: ' 'page_number'},....]
        while line:
            key, match = self.parse_line(line)
            if key == self.NAME or key == self.AREA or\
                key ==self.YEAR or key ==self.QUARTER or\
                key == self.VOLUME or key == self.PAGE :

                row[key] = match.group(key)

            if key == self.PAGE:
                data.append(row)
                row = {}

            line = textfile.readline()

        textfile.close()
        return data
        

def find_matches(nfile, mrfile):
    # Func that takes text files 'nfile' and 'mrfile' and prints
    # the possible couple matches from them.

    parse_obj = FileParser()

    # Data extraction for Nicholas 
    n_data = parse_obj.parse_file(nfile)

    # Data extraction for Mary Roche
    mr_data = parse_obj.parse_file(mrfile)

    # identifing Couples based on district and 
    # returns year/quarter/volume/page
    for n in n_data:
        for mr in mr_data:
            if n[parse_obj.AREA] == mr[parse_obj.AREA] and \
                n[parse_obj.YEAR] == mr[parse_obj.YEAR] and\
                n[parse_obj.QUARTER] == mr[parse_obj.QUARTER] and \
                n[parse_obj.VOLUME] == mr[parse_obj.VOLUME] and\
                n[parse_obj.PAGE] == mr[parse_obj.PAGE]:

                print("\n Possible match!")
                print("%s and %s in %s in %s" 
                    % (n[parse_obj.NAME], mr[parse_obj.NAME],\
                        n[parse_obj.AREA], n[parse_obj.YEAR]))
                print(" Quarter = %s, Volume = %s, Page = %s" 
                    % (n[parse_obj.QUARTER], n[parse_obj.VOLUME],\
                    n[parse_obj.PAGE]))


if __name__ == "__main__":

    # Find Couples from the files
    find_matches("nicholas.txt", "mary_roche.txt")