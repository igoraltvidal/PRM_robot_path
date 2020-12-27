#Probabilistic Road Maps - PRM
#Author: Igor Althoff Vidal
import pygame 
import random
import math
import numpy
import sys

try:
    # Get the desired maze
    if(sys.argv[1] == 'maze1'):
        path_maze = './fig/maze1.png'
    elif(sys.argv[1] == 'maze2'):
        path_maze = './fig/maze2.png'
    elif(sys.argv[1] == 'maze3'):
        path_maze = './fig/maze3.png'
    elif(sys.argv[1] == 'maze4'):
        path_maze = './fig/maze4.png'
    elif(sys.argv[1] == 'maze5'):
        path_maze = './fig/maze5.png'
    else:
        path_maze = './maze3.png'

    # Get the desired number of nodes
    if(int(sys.argv[2]) > 0):
        number_of_nodes_from_user = int(sys.argv[2])
    else:
        number_of_nodes_from_user = 500 #default
except:
    print("[ERROR] Please insert the correct arguments (e.g. maze3 500)")
    pygame.quit() 
    quit() 




pygame.init() 
  
# Window size 
X = 600
Y = 600
  
# Create the surface/screen
display_surface = pygame.display.set_mode((X, Y)) 
pygame.display.set_caption('Probabilistic Road Maps - PRM') 

class Setup():
    '''
    Define all the variables related to the process.
    '''
    def __init__(self):
        self.node_list = [] # All the nodes created
        self.final_optimun_path = []
        self.node_name = 0
        # Constants
        ## Variable constants 
        self.NUMBER_NODES = number_of_nodes_from_user
        self.WEIGHT_HEURISTIC_WALKED_NODES = 10000
        self.EDGES_NUMBER_PER_NODE = 10
        # Color constants 
        self.WHITE = (255, 255, 255) 
        self.BLACK = (0, 0, 0)
        self.RED = (255,99,71)
        self.GRAY_LIGHT = (200,200,200)

    def reset_image(self, option, maze, node_list, message = "# Path robot - PRM #"):
        '''
        Called each time something must change on the screen.
        Update all the nodes.
        Update all the edges if the option = 'WITH_EDGES_LIST'
        '''
        display_surface.fill(self.WHITE) 
        maze.draw(display_surface)

        if(option == 'WITH_EDGES_LIST'):
            for i in range(0,len(node_list)):
                for j in range(0,len(node_list[i].edge_list)):
                    node_list[i].edge_list[j].draw(display_surface)

        for i in range(0,len(node_list)):
            node_list[i].draw(display_surface)

        myfont = pygame.font.SysFont("Comic Sans MS", 30)
        label = myfont.render(message, 1, self.GRAY_LIGHT)
        display_surface.blit(label, (10, 500))
        pygame.display.update() 

    def set_nodes_matrix(self):
        '''
        UNUSED
        Create a matrix with all the nodes X0 and correlated nodes X1,X2,X3 with edges with that node X0
        '''
        nodes_matrix = numpy.empty(shape=(len(self.node_list),300), dtype=object)
        for i in range(0,len(self.node_list)):
            nodes_matrix[i][0] = self.node_list[i]
            for j in range(0,len(self.node_list[i].edge_list)):
                if(self.node_list[i].edge_list[j].node2 == self.node_list[i]):
                    nodes_matrix[i][j+1] = self.node_list[i].edge_list[j].node1
                else:
                    nodes_matrix[i][j+1] = self.node_list[i].edge_list[j].node2
            
        return nodes_matrix

    def inc_edges_from_other_nodes(self):
        '''
        Include edges that already exist, but are not recognized by the node.
        '''
        for i in range(0,len(self.node_list)):
            for j in range(0,len(self.node_list[i].edge_list)):
                if(self.node_list[i].edge_list[j] not in self.node_list[i].edge_list[j].node2.edge_list):
                    self.node_list[i].edge_list[j].node2.edge_list.append(self.node_list[i].edge_list[j])

    def print_names_nodes_matrix(self,nodes_matrix):
        '''
        UNUSED
        Print the nodes_matrix
        '''
        for i in range(len(nodes_matrix)):
            print("[", end =" ")
            for j in range(len(nodes_matrix[i])):
                try:
                    node_name = nodes_matrix[i][j].name
                    print(node_name, end =" ")
                except:
                    pass
            print("]")

    def set_all_edges_hide(self):
        '''
        Set all edges with line color white
        '''
        for i in range(0,len(self.node_list)):
            self.node_list[i].hide_all_node_edges()

    def set_all_edges_show(self):
        '''
        Set all edges with line color gray
        '''
        for i in range(0,len(self.node_list)):
            self.node_list[i].show_all_node_edges()


setup = Setup()

class Maze(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y        
        self.image = pygame.image.load(path_maze).convert_alpha()
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (self.x,self.y))   

    def draw(self, surface):
        '''
        Draw the maze
        '''
        surface.blit(self.image, (self.x, self.y))

maze = Maze(0, 0)
display_surface.fill(setup.WHITE) 
maze.draw(display_surface)

class Node(pygame.sprite.Sprite):
    def __init__(self, x, y,image= './fig/node_not_path.png', is_special_node = False):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y        
        self.image = pygame.image.load(image).convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect(topleft = (self.x,self.y)) #here rect is created
        self.edge_list = []
        self.name = "n" + str(self.x) + str(self.y)
        self.dist_to_goal = 0
        self.is_special_node = is_special_node

    def draw(self, surface):
        '''
        Draw the node
        '''
        self.rect.topleft = (round(self.x), round(self.y)) 
        surface.blit(self.image, (self.x, self.y))

    def change_image(self,path):
        '''
        Change the node image
        '''
        if(self.is_special_node==True):
            self.image = pygame.image.load('./fig/flag.png').convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x,self.y)) #here rect is created
        else:
            self.image = pygame.image.load(path).convert_alpha()
            self.mask = pygame.mask.from_surface(self.image)
            self.rect = self.image.get_rect(topleft = (self.x,self.y)) #here rect is created

    # def check_collision_maze(self, Maze):
    #     '''
    #     Check if an edge collide with Maze
    #     TODO: Change to edge Class
    #     '''
    #     return pygame.sprite.collide_mask(self, Maze)

    def create_edge_between_nodes(self, Maze, Node):
        '''
        Take two nodes and create an edge between,
        IF AND ONLY IF edge dont collide with maze
        '''
        new_edge = Edge(self,Node)
        if(new_edge.check_collision_maze(Maze) == None):
            new_edge.draw(display_surface)
            self.edge_list.append(new_edge)
            new_edge.append_edge_to_node2_edge_list()
        else:
            new_edge.draw(display_surface,setup.RED)

    def optimize_edges(self):
        '''
        Only keep the edges with the smallest distance
        '''
        if(len(self.edge_list)>=3):
            optimized_edge_list = [self.edge_list[0],self.edge_list[1],self.edge_list[2]]
            short_distance_1 = self.edge_list[0].distance
            short_distance_2 = self.edge_list[1].distance
            short_distance_3 = self.edge_list[2].distance
            for i in range(0,len(self.edge_list)):
                if(self.edge_list[i].distance < short_distance_1):
                    short_distance_3 = short_distance_2
                    short_distance_2 = short_distance_1
                    short_distance_1 = self.edge_list[i].distance
                    optimized_edge_list = [self.edge_list[i],optimized_edge_list[1],optimized_edge_list[2]]
                elif(self.edge_list[i].distance < short_distance_2):
                    short_distance_3 = short_distance_2
                    short_distance_2 = self.edge_list[i].distance
                    optimized_edge_list = [optimized_edge_list[0],self.edge_list[i],optimized_edge_list[1]]
                elif(self.edge_list[i].distance < short_distance_3):
                    short_distance_3 = self.edge_list[i].distance
                    optimized_edge_list = [optimized_edge_list[0],optimized_edge_list[1],self.edge_list[i]]

            self.edge_list = optimized_edge_list

    def calc_dist_to_goal(self, goal_node):
        self.dist_to_goal = math.sqrt((self.x - goal_node.x)**2 + (self.y - goal_node.y)**2)

    def calc_edge_dist(self, node2):
        return math.sqrt((self.x - node2.x)**2 + (self.y - node2.y)**2)

    def calc_heuristic(self,from_node, list_walked_nodes):
        '''
        The heuristic calculation looks like an A*
        but with an improvement.
        It is the 
        (distance to goal) + (distance to another node) + (how many times that node was reached)*constant
        '''
        times_walked_on_node = list_walked_nodes.count(self.name)
        heuristic = self.calc_edge_dist(from_node) * self.dist_to_goal + times_walked_on_node*setup.WEIGHT_HEURISTIC_WALKED_NODES
        return heuristic

    def show_all_node_edges(self):
        for i in range(0,len(self.edge_list)):
            self.edge_list[i].is_to_hide_edge = False

    def hide_all_node_edges(self):
        for i in range(0,len(self.edge_list)):
            self.edge_list[i].is_to_hide_edge = True

    def get_edge_from_nodes(self, another_node):
        for i in range(0,len(self.edge_list)):
            returned_node = self.edge_list[i].get_another_node(self)
            if(returned_node == another_node):
                return self.edge_list[i]
        self.create_edge_between_nodes(maze,another_node)
        self.get_edge_from_nodes(another_node)
        return None

class Edge(pygame.sprite.Sprite):
    def __init__(self, node1, node2):
        pygame.sprite.Sprite.__init__(self)
        self.x0 = node1.x
        self.y0 = node1.y
        self.x1 = node2.x
        self.y1 = node2.y
        self.node1 = node1
        self.node2 = node2
        self.rect = pygame.draw.line(display_surface, setup.GRAY_LIGHT, (self.x0, self.y0), (self.x1, self.y1), 1)
        self.surface = display_surface.subsurface(self.rect)
        self.mask = pygame.mask.from_surface(self.surface.convert_alpha())
        self.distance = math.sqrt((self.x1 - self.x0)**2 + (self.y1 - self.y0)**2)
        self.is_to_hide_edge = False

    def draw(self, surface, color=setup.GRAY_LIGHT):
        if(self.is_to_hide_edge == True):
            pygame.draw.line(display_surface, setup.WHITE, (self.x0, self.y0), (self.x1, self.y1), 1)
        else:
            pygame.draw.line(display_surface, color, (self.x0, self.y0), (self.x1, self.y1), 2)

    def check_collision_maze(self, Maze):
        return pygame.sprite.collide_mask(self, Maze)

    def append_edge_to_node2_edge_list(self):
        self.node2.edge_list.append(self)

    def get_another_node(self,actual_node):
        if(actual_node == self.node1):
            another_node = self.node2
        elif(actual_node == self.node2):
            another_node = self.node1
        else:
            another_node = None
        return another_node
 

#######################################
#   _____ _______ ______ _____    __  #
#  / ____|__   __|  ____|  __ \  /_ | #
# | (___    | |  | |__  | |__) |  | | #
#  \___ \   | |  |  __| |  ___/   | | #
#  ____) |  | |  | |____| |       | | #
# |_____/   |_|  |______|_|       |_| #
#######################################

while len(setup.node_list) < setup.NUMBER_NODES: 

    if(len(setup.node_list) < setup.NUMBER_NODES/9):
    #ROW 1
        node_x_rand = random.randint(0, int(maze.width/3))
        node_y_rand = random.randint(0, int(maze.height/3))
    elif(len(setup.node_list) < 2*(setup.NUMBER_NODES/9)):
        node_x_rand = random.randint(int(maze.width/3), int(2*maze.width/3))
        node_y_rand = random.randint(0, int(maze.height/3))
    elif(len(setup.node_list) < 3*(setup.NUMBER_NODES/9)):
        node_x_rand = random.randint(int(2*maze.width/3), int(3*maze.width/3))
        node_y_rand = random.randint(0, int(maze.height/3))
    elif(len(setup.node_list) < 4*(setup.NUMBER_NODES/9)):
    #ROW 2
        node_x_rand = random.randint(0, int(maze.width/3))
        node_y_rand = random.randint(int(maze.height/3), int(2*maze.height/3))
    elif(len(setup.node_list) < 5*(setup.NUMBER_NODES/9)):
        node_x_rand = random.randint(int(1*maze.width/3), int(2*maze.width/3))
        node_y_rand = random.randint(int(maze.height/3), int(2*maze.height/3))
    elif(len(setup.node_list) < 6*(setup.NUMBER_NODES/9)):
        node_x_rand = random.randint(int(2*maze.width/3), int(3*maze.width/3))
        node_y_rand = random.randint(int(maze.height/3), int(2*maze.height/3))
    elif(len(setup.node_list) < 7*(setup.NUMBER_NODES/9)):
    #ROW 3
        node_x_rand = random.randint(int(0*maze.width/3), int(1*maze.width/3))
        node_y_rand = random.randint(int(2*maze.height/3), int(3*maze.height/3))
    elif(len(setup.node_list) < 8*(setup.NUMBER_NODES/9)):
        node_x_rand = random.randint(int(1*maze.width/3), int(2*maze.width/3))
        node_y_rand = random.randint(int(2*maze.height/3), int(3*maze.height/3))
    else:
        node_x_rand = random.randint(int(2*maze.width/3), int(3*maze.width/3))
        node_y_rand = random.randint(int(2*maze.height/3), int(3*maze.height/3))

    new_node = Node(node_x_rand,node_y_rand)

    if(pygame.sprite.collide_mask(new_node, maze) == None):
        setup.node_list.append(new_node)
        new_node.draw(display_surface)

        pygame.display.update() 
         
#########################################
#   _____ _______ ______ _____    ___   #
#  / ____|__   __|  ____|  __ \  |__ \  #
# | (___    | |  | |__  | |__) |    ) | #
#  \___ \   | |  |  __| |  ___/    / /  #
#  ____) |  | |  | |____| |       / /_  #
# |_____/   |_|  |______|_|      |____| #
#########################################

for i in range(0,len(setup.node_list)):
    if(i > setup.NUMBER_NODES/18 and i + setup.NUMBER_NODES/18<setup.NUMBER_NODES):
        for j in range(int(i - setup.NUMBER_NODES/18), int(i + setup.NUMBER_NODES/18)):
            if(len(setup.node_list[i].edge_list) > setup.EDGES_NUMBER_PER_NODE):
                    break
            if(setup.node_list[i] != setup.node_list[j]):
                setup.node_list[i].create_edge_between_nodes(maze, setup.node_list[j])
            pass

    for j in range(0,len(setup.node_list)):
        if(len(setup.node_list[i].edge_list) > setup.EDGES_NUMBER_PER_NODE):
                break
        if(setup.node_list[i] != setup.node_list[j]):
            setup.node_list[i].create_edge_between_nodes(maze, setup.node_list[j])
        pass

    setup.reset_image('',maze,setup.node_list,"Finding edges: " + str(int(100*(i/setup.NUMBER_NODES))) + "%")

setup.reset_image('WITH_EDGES_LIST',maze,setup.node_list)

##########################################
#   _____ _______ ______ _____    ____   #
#  / ____|__   __|  ____|  __ \  |___ \  #
# | (___    | |  | |__  | |__) |   __) | #
#  \___ \   | |  |  __| |  ___/   |__ <  #
#  ____) |  | |  | |____| |       ___) | #
# |_____/   |_|  |______|_|      |____/  #
##########################################

pos_init = None
pos_goal = None

is_goal_pos_set = False
setup.reset_image('WITH_EDGES_LIST',maze,setup.node_list,"Click to save the init position")
pygame.event.clear()
while(is_goal_pos_set == False):
    ev = pygame.event.get()
    for event in ev:
     
        if event.type == pygame.MOUSEBUTTONUP:
            if(pos_init == None):
                pos_init = pygame.mouse.get_pos()
                setup.reset_image('WITH_EDGES_LIST',maze,setup.node_list,"Click to save the final position")
            else:
                pos_goal = pygame.mouse.get_pos()
                is_goal_pos_set = True

node_init = Node(pos_init[0],pos_init[1],'./fig/flag.png',is_special_node=True)
setup.node_list.append(node_init)
node_goal = Node(pos_goal[0],pos_goal[1],'./fig/flag.png',is_special_node=True)
setup.node_list.append(node_goal)

for i in range(0,len(setup.node_list)):
    if(setup.node_list[i] != node_init):
        node_init.create_edge_between_nodes(maze, setup.node_list[i])
    if(setup.node_list[i] != node_goal):
        node_goal.create_edge_between_nodes(maze, setup.node_list[i])

node_init.optimize_edges()
node_goal.optimize_edges()

setup.reset_image('WITH_EDGES_LIST',maze,setup.node_list)

setup.inc_edges_from_other_nodes()


###########################################
#   _____ _______ ______ _____    _  _    #
#  / ____|__   __|  ____|  __ \  | || |   #
# | (___    | |  | |__  | |__) | | || |_  #
#  \___ \   | |  |  __| |  ___/  |__   _| #
#  ____) |  | |  | |____| |         | |   #
# |_____/   |_|  |______|_|         |_|   #
###########################################

for i in range(0,len(setup.node_list)):
    setup.node_list[i].calc_dist_to_goal(node_goal)

actual_node = node_init
setup.set_all_edges_hide()
setup.reset_image(' ',maze,setup.node_list)

path_list_all_nodes_walked = [node_init]
path_list_all_nodes_walked_name = [node_init.name]
is_node_goal_found = False
while(is_node_goal_found == False):
    i_random = random.randint(0, len(actual_node.edge_list)-1)
    best_candidate_next_node = actual_node.edge_list[i_random].get_another_node(actual_node)
    best_candidate_next_node_heuristic = actual_node.edge_list[i_random].get_another_node(actual_node).calc_heuristic(actual_node, path_list_all_nodes_walked_name)
    for i in range(0,len(actual_node.edge_list)):
        node_in_test = actual_node.edge_list[i].get_another_node(actual_node)
        if(node_in_test == node_goal):
            is_node_goal_found = True
        if(node_in_test != None):
            heuristic = node_in_test.calc_heuristic(actual_node, path_list_all_nodes_walked_name)
            if(float(heuristic) < best_candidate_next_node_heuristic):
                best_candidate_next_node = node_in_test
                best_candidate_next_node_heuristic = heuristic

    if(best_candidate_next_node in setup.final_optimun_path and len(setup.final_optimun_path) > 2):
        while(setup.final_optimun_path[-1] != best_candidate_next_node):
            del(setup.final_optimun_path[-1])
    else:
        setup.final_optimun_path.append(best_candidate_next_node)

    path_list_all_nodes_walked.append(best_candidate_next_node)
    path_list_all_nodes_walked_name.append(best_candidate_next_node.name)
    actual_node = best_candidate_next_node
    actual_node.change_image('./fig/node_actual.png')
    actual_node.draw(display_surface)
    actual_node.show_all_node_edges()
    setup.reset_image('WITH_EDGES_LIST',maze,setup.node_list)
    actual_node.change_image('./fig/node_tmp.png')
    actual_node.draw(display_surface)
    actual_node.hide_all_node_edges()

setup.set_all_edges_hide()


setup.reset_image('',maze,setup.node_list)


for i in range(0,len(setup.final_optimun_path)):
    setup.final_optimun_path[i].change_image('./fig/node_path.png')
    setup.final_optimun_path[i].draw(display_surface)

for i in range(1,len(setup.final_optimun_path)):
    returned_edge = setup.final_optimun_path[i].get_edge_from_nodes(setup.final_optimun_path[i-1])
    if(returned_edge != None):
        returned_edge.is_to_hide_edge = False
        returned_edge.draw(display_surface)

pygame.display.update() 


while(1):
    for event in pygame.event.get() : 
        if event.type == pygame.QUIT : 
            pygame.quit() 
            quit() 
