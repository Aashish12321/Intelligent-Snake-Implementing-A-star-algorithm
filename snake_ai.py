import heapq

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Node(object):
    def __init__(self, board, coords, nodeID, parent, f, g, head, direction):
        self.board = board
        self.coords = coords
        self.f = f
        self.g = g
        self.head = head
        self.info = {'id': nodeID, 'parent': parent, 'direction': direction}

    def __lt__(self, other):
        if self.f == other.f:
            return self.g > other.g
        else:
            return self.f < other.f

    def __eq__(self, other):
        if not other:
            return False
        if not isinstance(other, Node):
            return False
        return self.f == other.f


# A* Algorithm Applied AI
class SnakeAI(object):
    def __init__(self, direction):
        self.coords = []                                            # Snake body data
        self.path = None
        self.nodeID = 0
        self.direction = self.getDirection(direction)               # Snake movement direction data
        self.board = self.getBoard()                                # Absolute coordinates

    # pixel function to convert coordinates to absolute coordinates
    def getBoard(self):
        board = [[0 for x in range(27)] for y in range(27)]
        for i in range(27):
            board[0][i] = board[26][i] = board[i][0] = board[i][26] = 2
        return board

    def getXY(self, coord):
        x = (coord[0] - 10) // 20 + 1
        y = (coord[1] - 90) // 20 + 1
        return x, y

    # Function for snake movement direction data
    def getDirection(self, direction):
        move = [UP, DOWN, LEFT, RIGHT]
        return move.index(direction)

    # Function to initialize board
    def clearBoard(self):
        for x in range(1, len(self.board) - 1, 1):
            for y in range(1, len(self.board[0]) - 1, 1):
                self.board[y][x] = 0

    # Display snake coordinates and food absolute coordinates on the board
    def denoteXY(self, coords, coord):
        self.coords.clear()
        x, y = self.getXY(coord)
        self.goal = x, y
        self.board[y][x] = 1
        self.head = self.getXY(coords[0])

        for coord in coords:
            x, y = self.getXY(coord)
            self.coords.append((x, y))
            self.board[y][x] = 2

    # Function to request movement direction data
    def getNextDirection(self, coords, coord):
        if not self.path:
            self.findPath(coords, coord)
        if self.path:
            return self.path.pop()
        else:
            return -1

    # Node function to copy coords data required for creation
    def copyCoords(self, coords):
        coordies = []

        for coord in coords:
            coordies.append(coord)

        return coordies

    # Node function to copy board data required for creation
    def copyBoard(self, coords):
        board = self.getBoard()

        for coord in coords:
            x, y = coord
            board[y][x] = 2
        x, y = self.goal
        board[y][x] = 1

        return board

    # Function to calculate distance between the snake head node and the food node
    def getHeuristic(self, x, y):
        x1, y1 = self.goal
        return (abs(x - x1) + abs(y - y1))

    # Function to trace a path
    def findPath(self, coords, coord):
        self.clearBoard()
        self.denoteXY(coords, coord)
        self.path = self.aStar()

    # A* Algorithm implementation function
    """
    Create and expand nodes using snake head coordinates and body coordinates. Insert the expanded nodes into an open 
    heap queue (automatically sorted in ascending order). Retrieve each node and check if it has reached the food node. 
    If it has not reached the food node, insert it into the close list for path tracing and expand the node.
    """
    def aStar(self):
        # h (Estimated weight from the confirmed weight to the goal) g (Confirmed assumption from the start node)
        h = self.getHeuristic(self.head[0], self.head[1])
        g = 0
        node = Node(self.board, self.coords, 0, 0, h, g, self.coords[0], self.direction)
        open = []
        close = []
        self.expandNode(open, node)

        while open:
            node = heapq.heappop(open)

            # Handling the case where the food position is obscured by the snake body
            if g < node.g:
                g = node.g
            if g - node.g > 1:
                continue

            if node.head == self.goal:
                return self.makePath(close, node.info)

            close.append(node.info)
            self.expandNode(open, node)

        if close:
            path = [close[0]['direction']]
            return path

        return

    # Path tracing function in case the snake body is bent and there is space.
    # (If there is a space of more than 2 cells, it is possible to enter and exit, so it can be visited).
    def isHole(self, x, y, direction, board):
        if y - 1 >= 0 and direction > 1:
            if x == 25 and board[y - 1][x] == 2:
                return 10

        if y + 1 < 27 and direction > 1:
            if board[y + 1][x] == 2 and x == 1:
                return 10

        if y + 1 < 27 and y - 1 >= 0 and direction > 1:
            if board[y + 1][x] == 2 and board[y - 1][x] == 2:
                return 10
            if (board[y + 1][x] == 2 or board[y - 1][x] == 2):
                return 0

        if x - 1 >= 0 and direction < 2:
            if y == 25 and board[y][x - 1] == 2:
                return 10

        if x + 1 < 27 and direction < 2:
            if board[y][x + 1] == 2 and y == 1:
                return 10

        if x + 1 < 27 and x - 1 >= 0 and direction < 2:
            if board[y][x + 1] == 2 and board[y][x - 1] == 2:
                return 10
            if (board[y][x + 1] == 2 or board[y][x - 1] == 2):
                return 0

        return 3

    # Node expansion function
    def expandNode(self, open, nodes):
        moves = [UP, DOWN, LEFT, RIGHT]
        x, y = nodes.head

        for i in range(4):
            dx, dy = moves[i]
            x1 = x + dx
            y1 = y + dy
            if nodes.board[y1][x1] < 2:
                coords = self.copyCoords(nodes.coords)
                head = (x1, y1)
                coords.insert(0, head)
                coords.pop()
                board = self.copyBoard(coords)
                h = self.getHeuristic(x1, y1)
                if h > 0:
                    h1 = self.isHole(x1, y1, i, board)
                    h += h1
                g = nodes.g + 1
                self.nodeID += 1
                id = self.nodeID
                parent = nodes.info['id']
                node = Node(board, coords, id, parent, g + h, g, head, i)
                heapq.heappush(open, node)



    # Path tracing function when the food node is reached
    def makePath(self, closed, information):
        path = [information['direction']]

        while closed:
            info = closed.pop()
            if info['id'] == information['parent']:
                path.append(info['direction'])
                information = info

        return path

