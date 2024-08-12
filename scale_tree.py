import nuke

def get_pivot(nodes):
    nodes = nuke.selectedNodes()
    all_xpos = []
    all_ypos = []
    for node in nodes:
        getx = node['xpos'].value()
        gety = node['ypos'].value()
        all_xpos.append(getx)
        all_ypos.append(gety)
    minx = min(all_xpos)
    miny = min(all_ypos)
    maxx = max(all_xpos)
    maxy = max(all_ypos)
    pivotx = (maxx + minx) / 2
    pivoty = (maxy + miny) / 2
    return pivotx, pivoty


def scale_tree(mx, my):
    nodes = nuke.selectedNodes()
    if len(nodes) > 1:
        px = get_pivot(nodes)[0]
        py = get_pivot(nodes)[1]
        multiplyX = mx
        multiplyY = my
        for n in nodes:
            # get screen width, height, Xpos, Ypos
            sw = n.screenWidth()
            sh = n.screenHeight()        
            x = n['xpos'].value() + sw/2
            y = n['ypos'].value() + sh/2
            # math
            sx = (px - ((px - x) * multiplyX)) - sw/2
            sy = (py - ((py - y) * multiplyY)) - sh/2
            # apply scaled values to the nodes
            n['xpos'].setValue(sx)
            n['ypos'].setValue(sy)
    else:
        nuke.message("Please Select 2 or more Nodes to scale")


def scaledown():
    scale_tree(0.5, 0.5)
    
def scaleup():
    scale_tree(2, 2)
    
def scaleupY():
    scale_tree(1, 2)

def scaledownY():
    scale_tree(1, .5)
    
def scaleupX():
    scale_tree(2, 1)

def scaledownX():
    scale_tree(.5, 1)