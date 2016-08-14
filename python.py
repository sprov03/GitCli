from subprocess import call
from subprocess import Popen, PIPE
import os
import sys

#
#	Commands
#	

# Displays status of each repo with your current branch
def gitStatus():
	shell('clear')
	for repo in repos:
		# if hasBranch(current_branch) is False:
		# 	continue
		cd(repo)
		print repoLabels[repo]
		shell('git status -sb')
		print
		print
		print

# Push each active repo to the current branch
def pushBranches():
	print "Pushing " + current_branch

	if current_branch == 'master':
		print "NEVER PUSH TO MASTER!!!!!!!"
		return

	for repo in repos:
		cd(repo)
		if current_branch != currentBranch():
			continue

		print "Pushing " + repoLabels[repo]
		shell('git push')
	gitStatus()

# Commit each repo with the commit message that has your current branch
def commitBranches():
	if current_branch == 'master':
		print "You Should never commit something to master!!!"
		return

	gitStatus()
	print 'COMMITING ==> ' + current_branch
	message = raw_input("What is the commit message: ")
	print "........"

	for repo in repos:
		cd(repo)
		if current_branch != currentBranch():
			continue
		print 'Commiting ' + repoLabels[repo]
		commit(message)
	gitStatus()

# Pulls master to each repo with your current branch
def pullMaster():
	print 'Pulling master onto ' + current_branch

	for repo in repos:
		cd(repo)
		if current_branch != currentBranch():
			continue

		print 'Pulling master onto ' + repoLabels[repo]
		shell('git pull origin master')

		if repo == API and current_branch != 'master':
			shell('gulp')
			shell('git add public/js/admin.js public/js/index.js')
			shell('git add public/js/admin.js.map public/js/index.js.map')

	gitStatus()

# Checks out a branch from each repo that has that branch
def checkoutBranches():
	runBranchRevertCommands()
	shell('git branch')
	branch = raw_input("What is the name of the branch that you want to checkout: ")

	for repo in repos:
		cd(repo)
		if hasBranch(branch) is False:
			continue

		shell('git checkout ' + branch)
	gitStatus()

# Creates New Branches in each repo that you decide
def checkoutNewBranches():
	gitStatus()
	runBranchRevertCommands()
	count = 1
	print "REPOS"

	for repo in repos:
		print str(count) + ': ' + repoLabels[repo]
		count += 1

	workingRepos = raw_input("What repos do you want to use: ").strip().split(' ')
	for repo in workingRepos:
		cd(repos[int(repo) - 1])
		print repoLabels[repos[int(repo) - 1]]

	newBranch = raw_input("What is the name of the new branch: ").strip()
	for repo in workingRepos:
		cd(repos[int(repo) - 1])
		shell('git checkout master')
		shell('git pull')
		shell('git checkout -b ' + newBranch)
		shell('git push --set-upstream origin ' + newBranch)

	gitStatus()

# Deletes the branch from each repo that has it
def deleteBranches():
	current_repo = noShell('git branch')
	gitStatus()
	print current_repo
	branch = raw_input("Branch to delete: ")
	if branch == 'master':
		print "Why and the Fuck are you trying to delete master!!!"
		return

	for repo in repos:
		cd(repo)
		if hasBranch(branch) is False:
			continue
		shell('git checkout master')
		shell('git push --delete origin ' + branch)
		shell('git branch -D ' + branch)
	gitStatus()

#
#	Helper Functions
#

# ssh into scotchbox and run php artisan migrate in the leadpropeller repo
def migrate():
	call(['ssh', 'vagrant@192.168.33.10', 'php /var/www/leadpropeller.dev/artisan migrate']);

# ssh into scotchbox and run php artisan migrate:rollback in the leadpropeller repo
def rollback():
	call(['ssh', 'vagrant@192.168.33.10', 'php /var/www/leadpropeller.dev/artisan migrate:rollback']);

# Returns the current working branch of the present repo
def currentBranch():
	branches = noShell('git branch').strip().split('\n')
	return [s for s in branches if '*' in s][0].replace("* ", "", 1)

# Checks to see if a repo has a branch
def hasBranch(branch):
	branches = noShell('git branch').strip().split('\n')
	for i in xrange(len(branches)):
		branches[i] = branches[i].strip().replace("* ", "", 1)

	if any(branch == string for string in branches):
		return True
	return False

# Run shell command and return the result
def shell(string):
	call(string.split(' '))
	process = Popen(string.split(' '), stdout=PIPE)
	(output, err) = process.communicate()
	return output

# Run shell command and return the result while suppressing the output
def noShell(string):
	process = Popen(string.split(' '), stdout=PIPE)
	(output, err) = process.communicate()
	return output

# Runs 'git commit -m {message}' in the shell
def commit(message):
	call(['git', 'commit', '-am', message])

# Change working directory to the repo's base directory
def cd(repo):
	os.chdir(os.path.dirname(repo))

def clearCommandFile():
	open(commandFile,'w').close()

def runBranchRevertCommands():
	response = raw_input("Do you want to run the revert commands: ")
	if response == 'no' or response == 'n':
		return
		
	file = open(commandFile, 'r')
	commands = file.read().strip().split('\n')
	for command in commands:
		globals()[command]()
	file.close()
	clearCommandFile()

def addRevertCommand(command):
	file = open(commandFile, 'a')
	file.write(command + '\n')
	file.close()

def testing():
	print 'testing was called'
	runBranchRevertCommands()
	# addRevertCommand('migrate')

baseDir = '/Users/shawnpivonka/Sites/'
scriptDir = baseDir + 'pytonGitCli.py/'

API  = baseDir + 'api.leadpropeller.dev/'
LEADPROPELLER = baseDir + 'leadpropeller.dev/'
PLUGIN = baseDir + 'api.leadpropeller.dev/storage/app/misc/wordpress/lp-admin-theme/'

repos = [API, LEADPROPELLER, PLUGIN]
repoLabels = {API: 'API LEADPROPELLER', LEADPROPELLER: 'LEADPROPELLER', PLUGIN: 'WORDPRESS PLUGIN'}

commandFile = scriptDir + 'commandFile'
current_branch = currentBranch()

locals()[sys.argv[1]]()



