# Import flask dependencies
from flask import Blueprint, render_template, request, redirect, url_for

from .models import Process, ComplexTask, SimpleTask
from app import app

from app.products.models import Product
from app.shopfloor.models import Function

# Define the blueprint: 'process', set its url prefix: app.url/process
mod_process = Blueprint('process', __name__, url_prefix='/process')

#welcome page of the processes. Display the list and a button from which add a new process(new page), 
#remove a process(post request with id), view in detail a process(new page) from which modify it (new page)
@mod_process.route('/', methods=['GET'])
def hello():
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#remove a process
@mod_process.route('/', methods=['POST'])
def remove():
    data = request.json
    procId = data[0]
    app.session.query(Process).filter_by(id=procId).delete()
        
    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#add a new process to the db. welcome page and request (post) after the user data input
@mod_process.route('/newProc/', methods=['GET'])
def new():
    prod = app.session.query(Product).all()
    f = app.session.query(Function).all()
    return render_template("processes/newProc.html", products=prod, functions=f)

@mod_process.route('/newProc/', methods=['POST'])
def newP():
    data = request.json
    # Add a new process
    name = data[0]['name']
    pId = data[0]['product']
    p = app.session.query(Product).filter_by(id=pId).first()

    tasks = data[0]['tasks']
    cT, sT = addTask(tasks)

    process = Process(name=name, product=p, complex_tasks=cT, simple_tasks=sT)

    app.session.add(process)
    app.session.commit()

    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)

#AUXILIARY FUNCTIONS to define the complex tasks objects
# and associate all to the process
def addTask(tasks):
    complexs = []
    simples = []
    for i in range(len(tasks)):
        #take the values
        name = tasks[i]['name']
        ttype = tasks[i]['type']
        #If the task it's at the higher level, simply add it to the list
        if(ttype == 'complex'):
            c = ComplexTask(name=name)
            complexs.append(c)
            subT = tasks[i]['list']
            #then iterate on its subtasks, but iff it's a complex one
            tmpC, tmpS = addTaskAux(c, subT, [], [])
            complexs.extend(tmpC)
            simples.extend(tmpS)
        elif(ttype == 'simple'):
            mode = tasks[i]['modality']
            f1id = tasks[i]['f1']
            f2id = tasks[i]['f2']
            f1 = app.session.query(Function).filter_by(id=f1id).first()
            f2 = app.session.query(Function).filter_by(id=f2id).first()
            s = SimpleTask(name=name, modality=mode, f1=f1, f2=f2)
            simples.append(s)
    
    return complexs, simples
            
def addTaskAux(parent, subT, resC, resS):
    if(not subT):
        return [], []
    for i in range(len(subT)):
        name = subT[i]['name']
        ttype = subT[i]['type']
        if(ttype == 'complex'):
            c = ComplexTask(name=name, parent=parent)
            resC.append(c)
            tmpC, tmpS = addTaskAux(c, subT[i]['list'], [], [])
            if (tmpC):
                resC.extend(tmpC)

            if (tmpS):
                resS.extend(tmpS)
        elif(ttype == 'simple'):
            mode = subT[i]['modality']
            f1id = tasks[i]['f1']
            f2id = tasks[i]['f2']
            f1 = app.session.query(Function).filter_by(id=f1id).first()
            f2 = app.session.query(Function).filter_by(id=f2id).first()
            s = SimpleTask(name=name, modality=mode, parent=parent, f1=f1, f2=f2)
            resS.append(s)
    return resC, resS



#edit a process in the db. welcome page to view it and request (post) after the user data input
@mod_process.route('/viewProc/<procId>', methods=['GET'])
def mod(procId):
    proc = app.session.query(Process).filter_by(id=procId).first()
    prod = app.session.query(Product).all()
    return render_template("processes/detailProc.html", process=proc, products=prod)

@mod_process.route('/viewProc/<procId>', methods=['POST'])
def modP(procId):
    #get the data from user input
    data = request.json
    # Get the new values
    name = data[1]['name']
    pId = data[1]['processProduct']
    processId = data[0]

    #get the database values and update them
    proc = app.session.query(Process).filter_by(id=processId).first()
    proc.name = name
    p = app.session.query(Product).filter_by(id=pId).first()
    proc.product = p

    app.session.commit()
    proc = app.session.query(Process).all()
    return render_template("processes/indexProc.html", processes = proc)