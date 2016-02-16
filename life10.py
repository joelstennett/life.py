# next generation
from random import randrange
from joelmodule import get_integer, is_integer, get_boolean, get_number
#from test04 import test 
from time import sleep
from os import listdir

##Because of space requirements, the mushrooms tend to grow in approximately a grid pattern.
#Each mushroom can have neighbors in any of the 8 locations surrounding it.
##Mushrooms with more than 3 neighbors will die off in the next generation due to lack of available nutrients in the environment.
##Mushrooms with fewer than 2 neighbors will die off in the next generation due to a lack of symbiotic nutrients created neighboring mushrooms.
##Mushrooms with 2 or 3 neighbors will continue to live in the next generation.
##Blank areas on the grid with exactly 3 living mushrooms as neighbors will produce new mushrooms in the next generation.

def main():
    fileName = ''
    command = ''
    generations = 0
    height = 50
    width = 125
    fillRate = 25
    ageString = ['.,+tccaaaaasssssoooooh']
    cellAge = 0
    liveCharacter = ageString[cellAge]
    deadCharacter = '@'
    instructions = 'helpMenu.txt'
    worldList, worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
    print(worldString)
    validCommands = 'rnfqmltjogdhvs?aw'
    prompt1 = '[R]andom [N]ext(generations) [F]illrate [Q]uit [H]elp torus [M]ore '
    prompt2 = '[L]ong L pattern change: [G]raphics, [D]imensions or [W]orld [T]est [J]ump ahead [S]ave [O]pen [V]iew library '
    speed = 9
    worldType = 'regular'
    cellDisplay = 'no change'
    oldCell = '&'
    youngCell = '@'
    while command != 'quit':
        #
        # print options for user, this is the prompt
        #
        command,parameter = get_command(prompt1,validCommands)
        if command == 'm': #more
            command == 'Pull up more options'
            print(command)
            command,parameter = get_command(prompt2,validCommands)
        if command in 'h?': #help
            command = 'Help Command'
            print(command)
            helpMenu = help_menu(instructions)
        if command == 'r': #random new world
            worldList, worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
            displayOfCells = get_boolean('Would you like the program to display cells differently based on whether they are old or young? ')
            if displayOfCells:
                cellDisplay = 'show old'
            else:
                cellDisplay = 'no change'
            command = 'created random new world'
            print(command)
        if command == 'n': #next world
            worldList,generationCounter,generations,sleepTime = next_world(parameter,worldList,height,width,liveCharacter,deadCharacter,fileName,command,speed)
            command = 'Ran '+str(generations)+' generations of the simulation'    
            print(command)
        elif command == 'a':
            speed = adjust_speed(speed)
            command = 'adjusted speed to: '+str(speed)
            print(command)
        elif command == 'f': #change fillrate
            worldString,fillRate = change_fillrate(parameter,height,width,fillRate,liveCharacter,deadCharacter)
            command = 'changed fillrate to: '+str(fillRate)
            print(command)
            worldList, worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
            print(worldString)
        elif command == 'j': #skip generations
            command = 'Jump ahead some generations'
            print(command)
            worldList = skip_generations(parameter,height,width,fillRate,worldList,liveCharacter,deadCharacter)
        elif command == 'l': #create l pattern world
            worldList = create_l_pattern_world(height,width)
            worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
            command = 'created l pattern world'
            print(command)
            print(worldString)
        elif command == 'g': #change graphics
            liveCharacter, deadCharacter = change_graphics(parameter, liveCharacter, deadCharacter)
            command = 'successfully changed live character to: '+str(liveCharacter)+' and changed dead character to '+str(deadCharacter)
            print(command)
            worldList,generationCounter,generations,sleepTime = next_world(parameter,worldList,height,width,liveCharacter,deadCharacter,fileName,command,speed)
        elif command == 'd': #change dimensions
            height,width = change_dimensions(parameter, height, width)
            command = 'changed dimensions to '+str(height)+' by '+str(width)
            print(command)
##            worldList, worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
##            worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
        elif command == 's': #save file
            fileName = save_file(parameter,worldList,height,width,parameter,liveCharacter,deadCharacter)
            command = 'saved file as '+str(fileName)
        elif command == 't': #run test suite
            command = 'run test suite'
            print(command)
            test()
        elif command == 'o': #open file
            worldList,height,width,fileName = open_file(parameter)
            command = 'opened: '+str(fileName)
            print(command)
        elif command == 'v': # view library
            command = 'open library'
            print(command)
            worldList = library(height,width)
            worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
            print(worldString)
        elif command == 'q': # quit
            command = 'quit'
            print(command)
        elif command == 'w': #change to torus world
            typeOfWorld = get_integer('Which kind of world do you want this to be? 1.torus 2.regular ')
            if typeOfWorld == 1:
                worldType = 'torus'
                change_torus(height,width,fillRate,liveCharacter,deadCharacter,worldList,row,column)
                command = 'Changed world to a torus world'
            elif typeOfWorld == 2:
                worldType = 'regular'
                worldList, worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
                command = 'Changed world to a regular world'
            else:
                print('Invalid.')
                typeOfWorld = get_integer('Which kind of world do you want this to be? 1.torus 2.regular ')
            print(command)
    else:
        cleanup()

def fill_corners(height,width,fillRate):
    worldList = create_world(height,width)
    fillRate = 0
    height = 10
    width = 10
    worldList[1][1] = 1
    worldList[1][width] = 1
    worldList[height][1] = 1
    worldList[height][width] = 1
    worldList = populate_world(worldList,height,width,fillRate)
    return worldList

def is_torus():
    isTorus = get_boolean('Would you like to change to a torus world? ')
    if not isTorus:
        world = regularWorld
    else:
        return isTorus
    
def change_torus(height,width,fillRate,liveCharacter,deadCharacter,worldList,row,column):
    """Change the world to a torus world"""
    isTorus = is_torus()
    if isTorus:
        worldList[0] = worldList[-2]
        worldList[-1] = worldList[1]
        for y in range(height):
            #
            # Moving from right to left
            #
            worldList[y][0] = worldList[y][-2]
            #
            # Moving from left to right
            #
            worldList[y][-1] = worldList[y][1]
    totalNeighbors = 0
    #
    # Go through 9 times in a 3x3 box of each cell and count neighbors
    # Then it counts 
    #
    for columnVariable in [-1,0,1]:
        for rowVariable in [-1,0,1,height+1]:
            if is_alive(worldList,row+rowVariable,column+columnVariable):
                totalNeighbors = totalNeighbors + 1
    if is_alive(worldList,row,column): 
        totalNeighbors = totalNeighbors - 1
    worldList,worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
    return worldList,worldString
    
        
def new_world(height,width,fillRate,liveCharacter,deadCharacter):
    worldList = create_world(height,width)
    worldList = populate_world(worldList,height,width,fillRate)
    worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
    return worldList, worldString

def create_world(height,width):
    '''Create a world'''
    worldList = []
    filler = 0
    #
    # Go through each row and add zeroes to the row and then add
    # the row to the world. Continue until column is run out
    #
    for rowCount in range(0,height+2): 
        row = []
        for cellCount in range(0,width+2):
            row.append(filler)
        worldList.append(row)
    return worldList

def populate_world(worldList,height,width, fillRate=25):
    """Populate the world with a certain amount of mushrooms based on fillRate"""
    liveCell = 1
    for row in range(1,height+1):
        for column in range(1,width+1):
            #
            # Pick a random number. If number is less than fill rate
            # the program will change it to a 1.
            # If number is greater than a one, nothing will be done
            #
            if randrange(0,100) <= fillRate:
                worldList[row][column] = liveCell
    return worldList

def display_world(worldList,height,width,liveCharacter,deadCharacter):
    """Display the world for the user"""
    displayString = ''
    for row in range(1,height+1):
        line = ''
        for column in range(1,width+1):
            #
            # Add live character to line if it is living, otherwise add deadCharacter
            #
            if worldList[row][column] == 1:
                line += liveCharacter 
            else:
                line += deadCharacter 
        #
        # add new line to the new world
        #
        displayString += line + '\n'
    print(displayString)
    return displayString

def skip_generations(skipNumber,height,width,fillRate,worldList,liveCharacter,deadCharacter):
    """Skip a user wanted number of generations"""
    if is_integer(skipNumber):
        skipNumber = int(skipNumber)
    else:
        skipNumber = get_integer("How many generations would you like to skip? ")
    for number in range(skipNumber):
        worldList,liveCount = next_generation(worldList,height,width)
    worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
    print(worldString)
    return worldList

def change_fillrate(parameter,height,width,fillRate,liveCharacter,deadCharacter):
    """Change the fill rate for a world"""
    if is_integer(parameter):
        fillRate = int(parameter)
    else:
        fillRate = get_integer('Please enter a new fill rate: ')
    worldString = new_world(height,width,fillRate,liveCharacter,deadCharacter)
    return worldString,fillRate

def next_world(parameter,worldList,height,width,liveCharacter,deadCharacter,fileName,command,speed,cellAge,ageString):
    """Compute the next generations"""
    if is_integer(parameter):
        generations = int(parameter)
    else:
        generations = 1
    generationCounter = 1
    speedList = [5,4,3,2,1,0.5,0.25,0.125,0.0675,0]
    sleepTime = speedList[int(speed)]
    for number in range(generations):
        print('Generation Number: '+str(generationCounter))
        worldList,liveCount,cellAge = next_generation(worldList,height,width)
        worldString = display_world(worldList,height,width,liveCharacter,deadCharacter)
        generationCounter = generationCounter + 1
##        speed = float(speed)
##        sleep(speed)
        statusLine = print_status_line(height,width,liveCount,generationCounter,fileName,command,sleepTime,worldType)
        sleep(sleepTime)
    return worldList,generationCounter,generations,sleepTime

def print_status_line(height,width,liveCount,generationCounter,fileName,command,sleepTime,worldType):
    """Print a status line for user at each generation"""
    areaOfWorld = (height)*(width)
    deadCount = (areaOfWorld-liveCount)
    livePercentage = round((liveCount/areaOfWorld)*(100),2)
    deadPercentage = round((deadCount/areaOfWorld)*(100),2)
    statusLine = 'generations: '+str(generationCounter)+' height: '+str(height)+' width: '+str(width)
    statusLine += ' livePercentage: '+str(livePercentage)+'% name: '+fileName+' lastCommand: '+command+'/n'
    statusLine += 'speed: '+str(sleepTime)+' worldType: '+str(worldType)
    print(statusLine)
    return statusLine
    
def get_command(prompt,validCommands):
    """Get command from user"""
    parameter = ''
    command = input(prompt)
    command.lower()
    if len(command) == 0:
        firstLetter = 'n'
        parameter = '1'
    else:
        while command[0].lower() not in validCommands:
            print('Invalid command')
            command = input(prompt)
            command[0].lower()
        firstLetter = command[0].lower()
        parameter = command[1:]
        command = firstLetter
        if parameter == '':
            parameter = ''
    return command,parameter
        
def count_neighbors(worldList,row,column):
    """Count the neighbors of each cell including the extra border"""
    totalNeighbors = 0
    #
    # Go through 9 times in a 3x3 box of each cell and count neighbors
    #
    for columnVariable in [-1,0,1]:
        for rowVariable in [-1,0,1]:
            if is_alive(worldList,row+rowVariable,column+columnVariable):
                totalNeighbors = totalNeighbors + 1
    if is_alive(worldList,row,column): 
        totalNeighbors = totalNeighbors - 1
    return totalNeighbors
                                     
def next_generation(worldList,height,width):
    """Create next generation of mushrooms"""
##    if isTorus:
##        worldList = create_torus_world(worldList,height,width)
    newWorld = create_world(height,width)
    liveCount = 0
    deadCount = 0
    #
    # This is to show different characters based on their age
    # 
    cellAge = 0
    if isTorus:
        worldList, worldString = change_torus(height,width,fillRate,liveCharacter,deadCharacter,worldList)
        for row in range(1,height+1): # dont have the range include the extra border we added
            for column in range(1,width+1):
                totalNeighbors = count_neighbors(worldList,row,column)
                livingCell = is_alive(worldList,row,column)
                #
                # Determine whether mushroom dies or lives
                #
                if livingCell and (totalNeighbors == 2 or totalNeighbors == 3):
                    newWorld[row][column] = 1
                    liveCount = liveCount + 1
                    cellAge = cellAge + 1
                if (not livingCell) and (totalNeighbors == 3):
                    newWorld[row][column] = 1
                    liveCount = liveCount + 1
                    cellAge = 1
    else:
        for row in range(1,height+1): # dont have the range include the extra border we added
            for column in range(1,width+1):
                totalNeighbors = count_neighbors(worldList,row,column)
                livingCell = is_alive(worldList,row,column)
                #
                # Determine whether mushroom dies or lives
                #
                if livingCell and (totalNeighbors == 2 or totalNeighbors == 3):
                    newWorld[row][column] = 1
                    liveCount = liveCount + 1
                    cellAge = cellAge + 1
                if (not livingCell) and (totalNeighbors == 3):
                    newWorld[row][column] = 1
                    liveCount = liveCount + 1
                    cellAge = 1
    return newWorld, liveCount, cellAge

def is_alive(worldList,row,column):
    """Determine whether mushrooms is alive or dead"""
    liveCharacter = 1
    deadCharacter = 0
    if worldList[row][column] == liveCharacter:
        alive = True
    else:
        alive = False
    return alive


def create_l_pattern_world(height,width):
    """Create l pattern world()"""                
    startingHeight = int(height/2-1) # middle of world
    startingWidth = int(width/2-1) #middle of world
    worldList = create_world(height,width)
    worldList[startingHeight+3][startingWidth] = 1
    worldList[startingHeight+3][startingWidth+1] = 1
    worldList[startingHeight+2][startingWidth] = 1
    worldList[startingHeight+1][startingWidth] = 1
    worldList[startingHeight][startingWidth] = 1
    return worldList


def save_file(parameter,worldList,height,width,fileName,liveCharacter,deadCharacter):
    """Save file to an external file"""
    while parameter or fileName == '':
        fileName = input(str("What do you want to save the file as? "))
    fileName = fix_filename_save(fileName)
    if fileName in listdir(path='./worlds/'):
        confirmation = input('A file named '+str(fileName)+' already exists. Do you wish to replace it? ')
        if confirmation in ['y','yes','yea','yep']:
            print('File replaced as '+str(fileName))
        else:
            fileName = input(str("What do you want to save the file as? "))
            fileName = fix_filename_save(fileName)
            fileName = saveFile(fileName,worldList,height,width,fileName,liveCharacter,deadCharacter)
    fileText = display_world(worldList,height,width,liveCharacter,deadCharacter)
    userFile = open(fileName,'w')
    userFile.write(fileText)
    userFile.close()
    print('Your world was saved as '+fileName)
    #
    # Add save file to list to keep track of
    #
    return fileName

def fix_filename_save(fileName):
    """Add worlds and life to file name to save correctly"""
    if fileName[-5:] != '.life':
        fileName = fileName + '.life'
        print('save file')
        print(fileName)
    #
    # add worlds to beginning so it saves to a folder
    #
    if fileName[0:9] != './worlds/':
        fileName = './worlds/' + fileName
    return fileName
   
    
def open_file(fileName):
    """Open a file that the user wants"""
    listOfFiles = listdir(path='./worlds/')
    filesString = 'Available files: '
    for file in listOfFiles:
        splitFile = file.split('.')
        if splitFile[1] == 'life':
            filesString += splitFile[0] + ', '
    if filesString == 'Available Files: ':
        print('no files are available ')
        fileName = ''
    else:
        print(filesString)
        fileName = fix_filename_open(fileName)   
        myFile = open(fileName,'r')
        worldFile = myFile.read()
        myFile.close()
        print('worldFile')
        print(worldFile)
        #
        # Split the world into separate lines by splitting them at new line
        #
        worldList = worldFile.split('\n')
        print('world as a list')
        height = len(worldList)
        print('height')
        print(height)
        width = len(worldList[0])
        worldList = create_world(height,width)
        liveCharacter = '@'
        deadCharacter = '*'
        for row in range(0,height):
            for column in range(0,width):
                if worldList[row][column] == liveCharacter:
                    worldList[row+1][column+1] = 1
        return worldList,height,width,fileName

def fix_filename_open(fileName):
    """Makes sure the filename has the right ending"""
    #
    # Find available files
    #
    while fileName == '':
        fileName = input('Please enter a file to open: ')
    files = listdir(path='./worlds/')
    filesString = 'Available files: '
    for file in files:
        splitFile = file.split('.')
        if len(splitFile) > 1 and splitFile[1] == 'life':
            filesString += splitFile[0] +', '
        if filesString == 'Available files: ':
            print('No files are available.')
            fileName = ''
        else:
            if fileName[-5:] != '.life':
                fileName =  fileName+'.life'
            if fileName[0:9] != './worlds/':
                fileName = './worlds/' + fileName
    return fileName
            
def change_graphics(parameter, liveCharacter, deadCharacter,oldCell,youngCell):
    """Change the charaters used to represent live and dead cells."""
    if parameter == '':
        liveCharacter = input('Which character should represent live cells [currently: "'+liveCharacter+'"]? ')
        while liveCharacter == '':
            liveCharacter = input('You have to enter something: ')
        deadCharacter = input('Which character should represent dead cells [currently: "'+deadCharacter+'"]? ')
        while deadCharacter == '':
            deadCharacter = input('You have to enter something: ')
    elif len(parameter) == 1:
        liveCharacter = parameter
        deadCharacter = deadCharacter
    else:
        liveCharacter = parameter[0]
        deadCharacter = parameter[-1]
    oldCharacter = input('Which character should represent old cells [currently: "'+oldCell+'"]? ')
    youngCharacter = input('Which character should represent young cells [currently: "'+youngCell+'"]? ')
    return liveCharacter, deadCharacter           

def change_dimensions(parameter, height, width):
    """Change the height and width of a world."""
    newHeight = 'x'
    newWidth = 'x'
    if parameter != 'noparametergiven':
        for splitChar in [' ',',','x']:
            parts = parameter.split(splitChar)
            if len(parts) == 2:
                newHeight = parts[0]
                newWidth = parts[1]
    if (is_integer(newHeight) and is_integer(newWidth)):
        height = abs(int(newHeight))
        width = abs(int(newWidth))
    else:
        height = get_integer('What should the new height be [currently: "'+str(height)+'"]? ')
        width = get_integer('What should the new width be [currently: "'+str(width)+'"]? ')   
    return height, width

def help_menu(instructions):
    """Print a help meny for the user"""
    helpMenu = open(instructions,'r')
    for line in helpMenu:
        print(line,end='')
    helpMenu.close
    

def library(height,width):
    """Display a library option of cool worlds to choose from"""
    isAllowed = False
    while isAllowed == False:
        library = 'library.txt'
        libraryFile = open(library,'r')
        for line in libraryFile:
            print(line,end='')
        whichWorld = get_number('Which world do you want to open? ')
        if whichWorld == 1:
            isAllowed = True
            worldList = create_l_pattern_world(height,width)
        else:
            print('There is nothing that is listed under that number. Try again.')
    return worldList

def adjust_speed(parameter,speed):
    """Allow the user to change the speed of the simulation"""
    if parameter == '' or not is_integer(parameter):
        speed = get_integer('Set velocity between 0 (slowest) and 10 (fastest) [currently: '+str(speed)+']? ')
    else:
        speed = int(parameter)
        if speed < 0:
            speed = 0
        if delay > 10:
            speed = 10
    return speed
        
# def make_torus_world():
# make into a donut shape
# has something to do with the extra border that we made
# copy the top line of world to bottom border


# run til static procedure
# x=0
# while (x<numberofgenerations) and notSTatic:
#   stuff
             
def cleanup():
    print('goodbye')


if __name__ == '__main__':
    main()
