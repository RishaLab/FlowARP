import sys
import random
import re

from flask import Flask, render_template, request, url_for
app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/generate', methods =['POST','GET'])
def generate():
    if request.method =='POST':
        code = request.form['nm']
        code2 = request.form['nm2']
        print(code + '\n\nint main(){\n\n' + code2 + '\nreturn 0;\n\n}')

        rres = code + '\n\nint main(){\n\n' + code2 + '\nreturn 0;\n\n}'

        
        # file = open('new_target.cpp','r').readlines()
        # file2 = open('new_target.cpp','r').read()

        file = rres.split('\n')
        file2 = rres
        # print(file)

        protocols = []
        flow = {}
        blocks = re.findall("\{([^}]*\n)*[^}]*\}", file2)



        def isFuncdef(line):
            if '){' in line:
                x = re.search("[A-Za-z_0-9]*\(", line)
                # print(x)
                # print(line)
                return x
            else:
                return ""


        block_num = 0


        for line in file:
            # print(line)
            # line = line.lower()
            if isFuncdef(line)!="":
                

                all_funcs = re.findall("[A-Za-z_0-9]*\([a-z0-9,]*\)", blocks[block_num])
                protocols.append(isFuncdef(line).group() + ')')
                # print(protocols[block_num])
                # print(all_funcs)
                # print(all_funcs)
                flow[protocols[block_num]] = all_funcs
                block_num = block_num+1
                # print('------------------------------------')



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

        def get_entity(pos, delay):
            # line = "        <a-box position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 6000; delay: "+str(delay)+";\" height = 0.20; width = 0.20; depth = 0.20; material=\'opacity: 0;\' color = \""+"green"+"\"></a-box>\n"
            line = "        <a-cylinder rotation='-80 0 0' position=\'"+str(pos)+"\' animation=\"property: material.opacity; to: 1.0; dur: 3000; delay: "+str(delay)+";\" height = 0.20; radius = 0.14 material='opacity: 0;' color = \"orange\"></a-cylinder>"
            return line

        def get_line(start, end, delay):
            # line = "        <a-box position=\'"+str(start)+"\' animation=\"property: position; to: "+ end +"; dur: 6000; delay: "+str(delay)+";\" height = 0.040; width = 0.040; depth = 0.040; material=\'opacity: 1;\' color = \""+"red"+"\"></a-box>\n"
            line = "        <a-box position=\'"+str(start)+"\' animation=\"property: position; to: "+ end +"; dur: 500; delay: "+str(delay)+"; loop: true;\" height = 0.040; width = 0.040; depth = 0.040; material='opacity: 1;' color = \"lightblue\"></a-box>"
            return line

        def get_text(text, pos, delay):
            line = "        <a-text rotation=\"0 0 0\"  animation=\"property: rotation; to: -90 0 0; dur:3000 ; delay: "+str(delay)+";\" material=\'opacity: 0;\' width=2 position = \""+ pos +"\" value=\""+ text +"\"></a-text>"
            return line

        f = open('templates/new_test2.html','w+')

        def get_pos(pos):
            pos_str = str(pos[0])+" "+str(pos[1])+" "+str(pos[2])
            return pos_str



        print(flow)
        print("========================")
        print(protocols)
        print("========================")

        positions = []


        def add_position(key, lev, prev):
            # print(key)
            # print(lev)
            pos = [0.0,0.0,0.0]
            pos[2] = lev/2.0
            pos[0] = prev

            wreck = 1
    
            for kl in positions:
                if kl[0] == key:
                    wreck = 0
                
            if wreck != 0:
                positions.append([key, pos, lev])
                
            lev = lev + 1
            queue = []
            try:
                # print(flow[key])
                for j in flow[key]:
                    # print(j)
                    queue.append([j,lev,prev])
                    prev = prev + 0.8
            except:
                pass

            # print("::", key)
            # print(queue)

            for j in queue:
                add_position(j[0], j[1], j[2])





        # Figure out parent array.
        # parent = []

        def add_nodes(postions, delay):
            
            prev_pos = positions[0][1]
            prev_delay = 0
            for kk,i in enumerate(positions[1:]):
                # print(i[1])
                print(i, kk)
                delay = 4000 * i[2]
                delay_line = delay - 1000
                pos_str = get_pos(i[1])
                text_pos = [i[1][0], i[1][1]+0.15, i[1][2]]
                text_str = get_pos(text_pos)
                # print(pos_str)
                f.write(get_entity(pos_str, delay) +'\n'+ get_text(i[0], text_str, delay) + '\n')


                for child in list(flow.keys()):
                    if i[0] in flow[child]:
                        _parent = child
                        f.write(get_line(get_pos(positions[parent_help[_parent]][1]), pos_str, delay_line) + '\n\n')
                

                
                prev_pos = i[1]
                prev_delay = delay
                
                
        add_position("main()", 0, 0)
        # print(positions)

        print(positions)



        f.write(header)

        k = positions[0]
        delay = 4000 * k[2]
        pos_str = get_pos(k[1])
        text_pos = [k[1][0], k[1][1]+0.15, k[1][2]]
        text_str = get_pos(text_pos)


        parent = [4,4,4,1,5,0]
        parent_help = {i[0]:num for num, i in enumerate(positions)}


        print("---------------------------------------")
        print(parent_help)
        print("---------------------------------------")



        # print(pos_str)
        f.write('\n\n'+get_entity(pos_str, delay) + '\n' + get_text(k[0], text_str, delay) + '\n\n')
        add_nodes(positions, 0)
        f.write(footer)
        f.close()
        #for i in protocols:
        #     pos = [0.0,0.0,0.0]
            
        #     choice = random.choice(['1','-1'])
        #         if choice == '1':
        #             pos[1] = random.random()
        #         else:
        #             pos[1] = -1 * random.random()
        #     print(choice)

        
        return render_template('new_test2.html', result = code)


if __name__ == '__main__':
    app.run(debug = True)