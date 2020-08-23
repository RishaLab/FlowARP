import sys
import random
import re

from flask import Flask, render_template, request, url_for
app = Flask(__name__)

import re
import sys
import random

def isFuncdef(line):
    if '){' in line:
        x = re.search("[A-Za-z_0-9]*\(", line)
        # print(x)
        # print(line)
        return x
    else:
        return ""

def get_type_togethorness(lines):
    stack = 0
    states = []
    statement_blocks = []

    type_ = 'norm'
    type_state = ""

    for i in lines:
        # print(i)
        if '{' in i or '}' in i:
            if type_state != "":
                states.insert(0, type_state)
            statement_blocks.append((type_, states))
            if 'if(' in i or 'if ' in i:
                type_ = 'if'
                type_state = i
            elif 'while(' in i or 'while ' in i:
                type_ = 'while'
                type_state = i
            elif 'for(' in i or 'for ' in i:
                type_ = 'for'
                type_state = i
            elif 'else{' in i or 'else ' in i:
                type_ = 'else'
                type_state = i
            elif 'int ' in i or 'void ' in i or 'float ' in i or 'char ' in i or 'bool ' in i:
                func_name = isFuncdef(i)[0][:-1]
                type_ = 'def:'+func_name 
                type_state = i

                if func_name == 'main':
                    type_ = 'main'
                    
            if '}' in i:
                statement_blocks.append('close')
                type_ = 'norm'
                type_state = ""

            
                
            states = []
        else:
            states.append(i)

    return statement_blocks

            
def get_stacks(data):
    print(data, '\n\n\n')
    prev_if = []
    index = 0
    open_ = [0]
    parent = 0
    blocks = []

    for i in data:
        if i == 'close':
            parent = open_[-1]
            open_ = open_[:-1]
        if len(i) == 2:
            if i[1] != [] and 'def' not in i[0]:
                    
                if i[0] == 'if':
                    parent = open_[-1]
                    blocks.append([[], 'if' ,parent])
                    for line in i[1]:
                        blocks[index][0].append(line)
                    prev_if.append(index)
                    open_ = open_[:-1]
                    open_.append(index)
                    open_.append(index)
                    index+=1   
                elif i[0] == 'else':
                    # print('\n',i,'\n')
                    blocks.append([[], 'else' ,prev_if[-1]])
                    prev_if = prev_if[:-1]
                    for line in i[1]:
                        # print(line)
                        # print(index)
                        blocks[index][0].append(line)
                    open_ = open_[:-1]
                    open_.append(index)
                    open_.append(index)
                    index += 1

                elif i[0] == 'norm':
                    # print('\n',i,'\n')
                    parent = open_[-1]
                    blocks.append([[], 'norm' , parent])
                    
                    for line in i[1]:
                        # print(line)
                        # print(index)
                        blocks[index][0].append(line)
                    open_ = open_[:-1]
                    open_.append(index)
                    open_.append(index)
                    index += 1

                else:
                    # if index-1 >= 0 and blocks[index-1][1] == 'else':
                    #     parent = [index-1, blocks[index-1][2]]
                    # else:
                    parent = open_[-1]
                    blocks.append([[], i[0], parent])
                    parent = index-1
                    # print(index)
                    for line in i[1]:
                        blocks[index][0].append(line)
                    open_ = open_[:-1]
                    open_.append(index)
                    open_.append(index)
                    index+=1    
                         

      

    return blocks        

def retrieve_lines():
    file_lines = open('new_target.cpp','r').readlines()
    file_lines = [i.strip() for i in file_lines if i.strip()!='']
    return file_lines

header = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    <title>Document</title>

</head>

    <!-- x z y -->
    <script src="https://aframe.io/releases/1.0.3/aframe.min.js"></script>
    <!-- include ar.js for A-Frame -->
    <script src="https://jeromeetienne.github.io/AR.js/aframe/build/aframe-ar.js"></script>

<body>

<div>
    
    <a-scene { display: block; width: 50%; }>
'''

footer = '''
    <a-marker-camera preset='custom' type='pattern' url='/static/arjs_marker.patt'></a-marker-camera>
    </a-scene>

</div>
    </body>
</html>
'''


def get_entity(pos, hei):
    line = "        <a-box position=\'"+str(pos)+"\' height=0.30; width=0.50; depth="+hei+"; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    line2 = "        <a-box position=\'"+str(pos)+"\' height=0.001; width=0.525; depth="+hei+"8; material=\'opacity: 1;\' color = \""+"white"+"\"></a-box>\n"
    line = line + line2
    # line = "        <a-box position=\'"+str(pos)+"\' height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    # line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
    return line


def get_entity_red(pos, hei):
    line = "        <a-box position=\'"+str(pos)+"\' height=0.25; width=0.50; depth="+hei+"; material=\'opacity: 1;\' color = \""+"red"+"\"></a-box>\n"
    line2 = "        <a-box position=\'"+str(pos)+"\' height=0.0015; width=0.525; depth="+hei+"8; material=\'opacity: 1;\' color = \""+"white"+"\"></a-box>\n"
    line = line + line2
    # line = "        <a-box position=\'"+str(pos)+"\' height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    # line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
    return line



def get_entity_violet(pos, hei):
    line = "        <a-box position=\'"+str(pos)+"\' animation=\"property: material.opacity; from: 0.4; to: 1; dur: 1000; loop: true\" height=0.25; width=0.50; depth="+hei+"; color = \""+"#6a0dad"+"\"></a-box>\n"
    line2 = "        <a-box position=\'"+str(pos)+"\' height=0.0015; width=0.525; depth="+hei+"8; material=\'opacity: 1;\' color = \""+"white"+"\"></a-box>\n"
    line = line + line2
    # line = "        <a-box position=\'"+str(pos)+"\' height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    # line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
    return line

def get_entity_green(pos, hei):
    line = "        <a-box position=\'"+str(pos)+"\' height=0.25; width=0.50; depth="+hei+"; material=\'opacity: 1;\' color = \""+"green"+"\"></a-box>\n"
    line2 = "        <a-box position=\'"+str(pos)+"\' height=0.0015; width=0.525; depth="+hei+"8; material=\'opacity: 1;\' color = \""+"white"+"\"></a-box>\n"
    line = line + line2
    # line = "        <a-box position=\'"+str(pos)+"\' height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    # line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
    return line

def get_entity_yellow(pos, hei):
    line = "        <a-box position=\'"+str(pos)+"\' animation=\"property: material.opacity; from: 0.4; to: 1; dur: 1000; loop: true\" height=0.15; width=0.40; depth="+hei+"; color = \""+"#9b870c"+"\"></a-box>\n"
    line2 = "        <a-box position=\'"+str(pos)+"\' height=0.001; width=0.45; depth="+hei+"8; material=\'opacity: 1;\' color = \""+"white"+"\"></a-box>\n" 
    # line = "        <a-box position=\'"+str(pos)+"\' height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"blue"+"\"></a-box>\n"
    # line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
    line = line + line2
    return line


def get_line(start, end, delay):
            # line = "        <a-box position=\'"+str(start)+"\' animation=\"property: position; to: "+ end +"; dur: 6000; delay: "+str(delay)+";\" height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"red"+"\"></a-box>\n"
            line = "        <a-box position=\'"+str(end)+"\' animation=\"property: position; to: "+ start +"; dur: 500; delay: "+str(delay)+"; loop: true;\" height = 0.080; width = 0.080; depth = 0.080; material='opacity: 1;' color = \"lightblue\"></a-box>"
            return line


# def get_line(start, end):
#     line = "        <a-entity line=\"start: "+str(start)+"; end: "+str(end)+"; color: white\"></a-entity>\n"
#     return line

def get_text(text, pos, thick):
    line = "        <a-text rotation=\"-90 0 0\" material=\'opacity: 1;\' width="+str(thick/1.8)+" position = \""+ str(pos) +"\" value=\""+ text +"\"></a-text>\n"
    return line



def get_pos(pos):
    pos_str = str(pos[0])+" "+str(pos[1])+" "+str(pos[2])
    return pos_str


def get_positions(blocks):
    hor_level = [0 for i in range(100)]

    prev_pos = [0, 0, 0]

    const_x = -2

    f = open('templates/index_test.html','w+')

    f.write(header)

    pos_parent = {}

    pos_parent[0] = prev_pos

    hei = len(blocks[0][0]) * 0.20

    

    f.write(get_entity(get_pos(prev_pos), str(hei)))
    text_pos = [prev_pos[0] + 0.2, prev_pos[1] + 0.15, prev_pos[2]]
    text = "\n".join(blocks[0][0])
    f.write(get_text(text,get_pos(text_pos), 5))



    for num, i in enumerate(blocks[1:]):
        print(num, i)
        vert = i[2] + 1

        hei = len(i[0]) * 0.20

        text = "\n".join(i[0])

        print(text)

        hor_level[vert] += 1.75

        br = random.uniform(-0.3,0.3)

        lr = random.uniform(-0.3,0.3)
        
        pos = [hor_level[vert]*1-lr + const_x, br, vert * 0.85]

        text_pos = [pos[0] + 0.2, pos[1] + 0.15, pos[2]]

        delay = 10000 + 4000 * num
        delay_line = delay - 1000
        
        type_ = i[1]

        if type_ == 'if':
            f.write(get_entity_green(get_pos(pos), str(hei)))
        elif type_ == 'else':
            f.write(get_entity_red(get_pos(pos), str(hei)))
        elif type_ == 'for':
            f.write(get_entity_yellow(get_pos(pos), str(hei)))
        elif type_ == 'while':
            f.write(get_entity_violet(get_pos(pos), str(hei)))
        elif type_ == 'norm':
            f.write(get_entity(get_pos(pos), str(hei)))
        

        # f.write(get_entity(get_pos(pos)))
        f.write(get_line(get_pos(pos), get_pos(pos_parent[i[2]]), delay_line))
        f.write(get_text(text,get_pos(text_pos), 5))

        pos_parent[num+1] = pos
        # prev_pos = pos
        print(pos)

    f.write(footer)
    f.close()


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods =['POST','GET'])
def generate():
    if request.method =='POST':
        code = request.form['nm2']
        file_lines = code.split('\n')
        file_lines = [i.strip() for i in file_lines if i.strip()!='']
        file_lines.append('}')
        print(file_lines)

        data = get_type_togethorness(file_lines)

        data_blocks = get_stacks(data)

        get_positions(data_blocks)

        return render_template('index_test.html')
        


if __name__ == '__main__':
    app.run(debug = True)