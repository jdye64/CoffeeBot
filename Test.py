import subprocess
p = subprocess.Popen(['hdfs', 'dfs', '-ls', '/user/matacker/aam_logs/*.gz'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = p.communicate()

lines = out.split("\n")

for line in lines:
    file_parts = line.split(" ")
    hdfs_path = file_parts[len(file_parts) - 1]
    print "HDFS Path: " + str(hdfs_path)
    hdfs_parts = hdfs_path.split("/")
    filename_with_ext = hdfs_parts[len(hdfs_parts) - 1]
    print "Filename with Ext: " + str(filename_with_ext)
    filename = filename_with_ext.split(".")[0]
    print "Filename no Ext: " + str(filename)
    file_parts = filename.split("_")

    year = file_parts[1]
    day = file_parts[2]
    month = file_parts[3]

    print "Year: " + str(year) + " Month: " + str(month) + " Day: " + str(day)
    # Do whatever you want to do here??