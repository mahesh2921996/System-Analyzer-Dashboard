import pstats
import pandas as pd
import re


def make_df_from_prof(path, selected_files):
    
    file_path = path + "\\system_info\\" + selected_files

    # Create a Stats object, passing in the path to the .prof file as an argument.
    stats = pstats.Stats(file_path)
    
    # get data
    stat_dic = stats.stats
    
    lis_ncalls = []
    lis_tottime = []
    lis_percall = []
    lis_cumtime = []
    lis_file_path = []
    lis_line = []
    lis_function = []
    lk =[]
    for i in stat_dic.keys():
        lis_ncalls.append(stat_dic[i][0])
        lis_tottime.append(stat_dic[i][1])
        lis_percall.append(stat_dic[i][2])
        lis_cumtime.append(stat_dic[i][3])

        lis_sing_line = []
        path = ""
        function = ""
        for k in stat_dic[i][4].keys():
            path = path + " " + k[0]
            lis_sing_line.append(k[1])
            function = function + " " + k[2]

        lis_file_path.append(path)
        lis_line.append(lis_sing_line)
        lis_function.append(function)
        
    stat_data = dict(ncalls=lis_ncalls, tottime=lis_tottime, percall=lis_percall, cumtime=lis_cumtime, filepath=lis_file_path, line=lis_line, function=lis_function)
    
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