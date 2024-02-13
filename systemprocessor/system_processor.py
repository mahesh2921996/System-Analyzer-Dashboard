import pstats
import pandas as pd
import re
from util.helper import Helper


class SystemProcessor:
    """This class is used to help process on data."""

    def __init__(self):
        self.helper = Helper()

        self.method = []
        self.rest_url = []
        self.endpoint = []
        self.time = []
        self.date = []
        
        self.lis_ncalls = []
        self.lis_tottime = []
        self.lis_percall = []
        self.lis_cumtime = []
        self.lis_file_path = []
        self.lis_line = []
        self.lis_function = []


    def create_df_from_prof_folder(self, all_files):
        # method = []
        # rest_url = []
        # endpoint = []
        # time = []
        # date = []
        for i in all_files:
            self.method.append(i.split(".")[0])
            ur = i.split(".")[1:-3]
            self.rest_url.append("\\".join(ur))
            self.endpoint.append(i.split(".")[-6])
            self.time.append(int(i.split(".")[-3][:-2])/1000)
            self.date.append(self.helper.convert_timestamp_datetime(i.split(".")[-2]))

        prof_data = dict(date=self.date, rest_url=self.rest_url, server_function = self.endpoint, method=self.method, time=self.time)
        prof_df = pd.DataFrame(prof_data)

        return prof_df
    
    def create_df_from_prof_files(self, path, selected_files):
        
        file_path = path + "\\system_info\\" + selected_files

        # Create a Stats object, passing in the path to the .prof file as an argument.
        stats = pstats.Stats(file_path)
        
        # get data
        stat_dic = stats.stats
        
        # lis_ncalls = []
        # lis_tottime = []
        # lis_percall = []
        # lis_cumtime = []
        # lis_file_path = []
        # lis_line = []
        # lis_function = []
        lk =[]
        for i in stat_dic.keys():
            self.lis_ncalls.append(stat_dic[i][0])
            self.lis_tottime.append(stat_dic[i][1])
            self.lis_percall.append(stat_dic[i][2])
            self.lis_cumtime.append(stat_dic[i][3])

            lis_sing_line = []
            path = ""
            function = ""
            for k in stat_dic[i][4].keys():
                path = path + " " + k[0]
                lis_sing_line.append(k[1])
                function = function + " " + k[2]

            self.lis_file_path.append(path)
            self.lis_line.append(lis_sing_line)
            self.lis_function.append(function)
            
        stat_data = dict(ncalls=self.lis_ncalls, tottime=self.lis_tottime, percall=self.lis_percall, cumtime=self.lis_cumtime, filepath=self.lis_file_path, line=self.lis_line, function=self.lis_function)
        
        df = pd.DataFrame(stat_data)
        
        # df["short_path"] = df["filepath"].apply(lambda x: x.split("site-packages\\")[-1] if x.find("site-packages") != -1 else x.split("Python")[-1])

        
        df["short_path"] = df["filepath"].apply(lambda x: x.split(f"{path.split('//')[-1]}"+"\\")[-1] if x.find(path.split("\\")[-1]) != -1 else x.split("site-packages\\")[-1] if x.find("site-packages") != -1 else x.split("Python")[-1])
        df["short_path"] = df["short_path"].apply(lambda x: x.split("site-packages\\")[-1] if x.find("site-packages") != -1 else x.split(f"{path.split('//')[-1]}\\")[-1] if x.find(path.split("\\")[-1]) != -1 else x.split("Python")[-1])

        # df["directory"] = df["filepath"].apply(lambda x: "virtual" if x.find("site-packages") != -1 else "base" if x.find("Python\\") != -1 else "main")
        df["directory"] = df["filepath"].apply(lambda x: "virtual" if x.find("site-packages") != -1 else "base" if x.find("Python\\") != -1 else "main")

        def find_drive(string):    
            lis_drive = ["A:","B:","C:","D:","E:","F:","G:","H:","J:","K:","L:","M:","N:","O:", "P:", "Q:", "R:", "S:", "T:", 
                        "U:", "V:", "W:", "X:", "Y:", "Z:"]

            for dri in lis_drive:
                result = re.findall(dri, string)
                if len(result) != 0:
                    return result[0][0]
        
        df["drive"] = df["filepath"].apply(find_drive)
        
        return df
        