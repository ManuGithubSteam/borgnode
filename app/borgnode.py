# app/routes.py

from flask import Flask, render_template, url_for, request, flash, redirect
import subprocess
import sys, re
from pprint import pprint
from pathlib import Path
from app import app

global_archives = []

@app.route('/')
@app.route('/index')
def index():
#    return "Hello, World!"
    file_backup_running = 'backup-running'
    path = Path(file_backup_running)
    if path.is_file():
        print(f'The file {file_backup_running } exists')
        backuprunning=True
    else:
        backuprunning=False
        print(f'The file {file_backup_running} does not exist, starting backup')
    return render_template("borgnode.html", html_backup_running=backuprunning)

@app.route('/hddlist',methods=['POST', 'GET'])
def hddlist():

    file_backup_running = 'backup-running'
    path = Path(file_backup_running)
    if path.is_file():
        print(f'The file {file_backup_running } exists')
        backuprunning=True
        flash('Backup/Restore is running - do nothing.')
        return render_template('borgnode.html', html_backup_running=backuprunning)
    else:
        backuprunning=False
        print(f'The file {file_backup_running } exists hddlist')

        listresult = subprocess.run(["./borgbackup.sh","list"], capture_output=True)
        errcmdoutput = listresult.stderr
        # remove Listing Archives and stuff in front of it
        archives = str(listresult.stdout).split('Listing archives', 1)[1]
        # remove backup id and control char cleanup
        #archives = re.sub("[\(\[].*?[\)\]]", "", archives)
        #archives = re.sub(r"[\[](.*?)[\)\]]", "", archives)
        #archives = re.sub("[\(\[].*?[\)\]]", "", archives)
        #archives = archives.replace("\\n","")
        #archives = archives.replace("'","")
        # Split archives up into lines
        archives = archives.split(']')
        # Remove n
        archives = [w.replace('\\n', '') for w in archives]
        # Remove '
        archives = [w.replace("'", "") for w in archives]
        # Remove Borg ID
        archives = [w.split("[", 1)[0] for w in archives]
        # Split into name and Date 
        archivetime = [w.split(" ", 1)[1:] for w in archives]
        archives = [w.split(" ", 1)[0] for w in archives]
        # Remove last dummy emelemt
        archives.pop()
        archivetime.pop()
        # Reverse Lists so latest is on top
        archives.reverse()
        archivetime.reverse()
        # save in globalarchives
        print(f'{archives} ')

        global_archives.append(archives)
        print(f'{global_archives} ')

        # Draw some stuff
        return render_template('borgnode.html',html_archives =enumerate(
                           archives),html_archivetime =
        archivetime,html_backup_running=backuprunning, html_archives_raw=archives )

@app.route('/backup',methods=['POST', 'GET'])
def startbackup():

    file_backup_running = 'backup-running'
    path = Path(file_backup_running)
    if path.is_file():
        print(f'The file {file_backup_running } exists')
        backuprunning=True
        flash('Backup/Restore is running - do nothing.')
        return render_template('borgnode.html', html_backup_running=backuprunning )
    else:
        backuprunning=True
        print(f'The file {file_backup_running} does not exist, starting backup')
        render_template('borgnode.html', html_backup_running=backuprunning )
        backupresult = subprocess.Popen(["./borgbackup.sh","backup"])
        flash('Sucess! Backup started in the background..')
        return render_template('borgnode.html', html_backup_running=backuprunning )

@app.route('/extract',methods=['POST', 'GET'])
def restorebackup():
    flash('Backup started ...')
    backupresult = subprocess.run(["./borgbackup.sh","extract"], capture_output=True)
    errcmdoutput = backupresult.stderr

    return render_template('borgnode.html' )

@app.route('/recover',methods=['POST', 'GET'])
def recover():
    text = request.form['text']
    print(f'entered into submission field:  {text} {global_archives[0]} ')
    if text in global_archives[0]:
       # flash('Backup {text} is present in the list')
        backupresult = subprocess.Popen(["./borgbackup.sh","extract", str(text)])
       # flash('Backup {text} gets restored in the background.')
    else:
        flash('Backup {text} is NOT present in the list')

    return render_template('borgnode.html' )
