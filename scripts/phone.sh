ABC=`ssh phone 'ls ../Android/data/com.taskwc2/files'`
scp ~/.task/*.pem phone:../Android/data/com.taskwc2/files/$ABC
scp ~/.taskrc phone:../Android/data/com.taskwc2/files/$ABC
