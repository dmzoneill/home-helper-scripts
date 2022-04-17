#!/usr/bin/python
import os
import sys
import subprocess

todo = []
delete = []

def query_yes_no(question, default="yes"):
    """Ask a yes/no question via raw_input() and return their answer.

    "question" is a string that is presented to the user.
    "default" is the presumed answer if the user just hits <Enter>.
        It must be "yes" (the default), "no" or None (meaning
        an answer is required of the user).

    The "answer" return value is True for "yes" or False for "no".
    """
    valid = {"yes": True, "y": True, "ye": True,
             "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' "
                             "(or 'y' or 'n').\n")


def transcode_video(filename):

    #for i in *.divx;   do name=`echo $i | cut -d'.' -f1`;   echo $name;   ffmpeg -i "$i" -c:v libx264 -preset fast "${name}.mkv"; done
    
    #print("Transcoding " + filename)
    file_name = os.path.splitext(filename)[0]
    command = ['/usr/bin/ffmpeg', '-i', '"' + filename + '"', '-c:v', 'libx264', '-preset', 'fast', '"' + file_name + '.mkv"']
    #print(' '.join(command))
    p1 = subprocess.Popen(' '.join(command), shell=True, stdout=subprocess.PIPE) 
    p1.wait()

    if p1.returncode == 0 and os.path.isfile(file_name + '.mkv'):
        #os.remove(filename)
        delete.append(filename)
        return True

    return False

def transcode_folder(folder):
    for dirpath, dirnames, filenames in os.walk(folder):
        for filename in filenames:
            file_extension = os.path.splitext(filename)[1]
            fullpath = os.path.join(dirpath, filename)
            allowed_exts = ['.mp4','.avi','.mkv','.srt','.smi']

            if file_extension not in allowed_exts:
                print("Selected " + fullpath)
                todo.append(fullpath)
    
    if query_yes_no("Transcode?"):
        for filename in todo:
            transcode_video(filename)

def main(argv):
    for filename in argv[1:]:
        if os.path.isdir(filename):
            transcode_folder(filename)
        else:
            transcode_video(filename)

    for filename in delete:
        print("rm \"" + filename + "\"")

if __name__ == '__main__':
    sys.exit(main(sys.argv))
