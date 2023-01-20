import os
from termcolor import colored


class Node:
    def __init__(self, key):
        self.key = key
        self.red = True
        self.left = None
        self.right = None
        self.parent = None
        self.size = 1

    def print_node(self):
        if self.red:
            print("{0}|{1}".format(colored(self.key, 'red'), self.size))
        else:
            print("{0}|{1}".format(self.key, self.size))

    def fix(self):
        if self.right != None and self.left != None:
            self.size = self.right.size + self.left.size + 1
        elif self.right == None and self.left != None:
            self.size = self.left.size + 1
        elif self.right != None and self.left == None:
            self.size = self.right.size + 1


class RBTree:
    def __init__(self):
        self.root = None

    def fix_size(self, node):
        while node != self.root:
            node.fix()
            node = node.parent
            self.fix_size(node)
        else:
            node.fix()

    def print_root(self):
        print(self.root.key, self.root.size, self.root.red)

    def left_rotate(self, node):
        print("LEFT ROTATE ", node.key)
        y = node.right
        node.right = y.left
        if y.left != None:
            y.left.parent = node
        p = node.parent
        y.parent = p
        if node == self.root:
            self.root = y
            print("New root >> {0}".format(y.key))
        elif node == p.left:
            p.left = y
        elif node == p.right:
            p.right = y

        y.left = node
        node.parent = y
        # size
        y.size = node.size
        if node.right != None and node.left != None:
            node.size = node.right.size + node.left.size + 1
        elif node.right == None and node.left != None:
            node.size = node.left.size + 1
        elif node.right != None and node.left == None:
            node.size = node.right.size + 1
        else:
            node.size = 1

    def right_rotate(self, node):
        print("RIGHT ROTATE ", node.key)
        y = node.left
        node.left = y.right
        if y.right != None:
            y.right.parent = node
        p = node.parent
        y.parent = p
        if node == self.root:
            self.root = y
            print("New root >> {0}".format(y.key))
        elif node == p.left:
            p.left = y
        elif node == p.right:
            p.right = y

        y.right = node
        node.parent = y
        # size
        y.size = node.size
        if node.right != None and node.left != None:
            node.size = node.right.size + node.left.size + 1
        elif node.right == None and node.left != None:
            node.size = node.left.size + 1
        elif node.right != None and node.left == None:
            node.size = node.right.size + 1
        else:
            node.size = 1

    def search(self, key):
        current_node = self.root
        while current_node is not None and key != current_node.key:
            if key < current_node.key:
                current_node = current_node.left
            else:
                current_node = current_node.right
        # print('Parent {} is {}'.format(current_node.key, current_node.parent.key))
        #print(colored(current_node.key, 'red'))
        return current_node

    def insert(self, key):
        node = Node(key)
        # Base Case - Nothing in the tree
        if self.root is None:
            node.red = False
            self.root = node
            print('ROOT IS - {0}'.format(self.root.key))
            return
        last_node = self.root
        while last_node is not None:
            potential_parent = last_node
            if node.key < last_node.key:
                last_node = last_node.left
            else:
                last_node = last_node.right
        # Assign parents and siblings to the new node
        node.parent = potential_parent
        print('NODE KEY- {0} NODE PARENT - {1} '.format(node.key,
                                                      node.parent.key))
        if node.key < node.parent.key:
            node.parent.left = node
            print('GO LEFT < NODE PARENT PARENT LEFT KEY - ',
                  node.parent.key)
        else:
            node.parent.right = node
            print('GO RIGHT > NODE PARENT PARENT RIGHT KEY - ',
                  node.parent.key)
        node.left = None
        node.right = None
        f = node.parent
        self.fix_size(f)
        self.fix_tree(node)

    def fix_tree(self, node):
        print('NODE PARENT RED - {}'.format(node.parent.red))
        try:
            while node is not self.root and node.parent.red is True:
                print('FIX>> NODE KEY - {} '
                      'NODE PARENT KEY - {} '.format(node.key, node.parent.key))
                if node.parent == node.parent.parent.left: # если отец является левым сыном
                   try:
                       uncle = node.parent.parent.right  # то дядя - правый сын деда
                       print('[LEFT] UNCLE RED - {} '
                             'UNCLE KEY - {} PARENT PARENT KEY - {}'.format(uncle.red, uncle.key, node.parent.parent.key))
                       if uncle.red:  # case 1 красный дядя
                           node.parent.red = False
                           uncle.red = False
                           node.parent.parent.red = True
                           node = node.parent.parent
                           if node != self.root:
                               print('NODE RED - {} UNCLE RED - {} PARENT RED - '
                                     '{}'.format(
                                   colored(node.red, 'red',
                                           attrs=['reverse', 'blink']),
                                   colored(uncle.red, 'yellow',
                                           attrs=['reverse', 'blink']),
                                   colored(node.parent.red, 'yellow',
                                           attrs=['reverse', 'blink'])))
                           else:
                               print('NODE IS ROOT')
                       else:
                           if node == node.parent.right:
                               # This is Case 2
                               print('in TEST>>>>', node.key)
                               node = node.parent
                               print('AFTER TEST>>>>', node.key)
                               self.left_rotate(node)
                           # This is Case 3
                           node.parent.red = False
                           node.parent.parent.red = True
                           self.right_rotate(node.parent.parent)

                   except AttributeError:
                       print("No uncle")
                       if node == node.parent.right:
                           # This is Case 2
                           print('in TEST>>>>', node.key)
                           node = node.parent
                           print('AFTER TEST>>>>', node.key)
                           self.left_rotate(node)
                       # This is Case 3
                       node.parent.red = False
                       node.parent.parent.red = True
                       self.right_rotate(node.parent.parent)
                       continue

                else:
                    try:
                        uncle = node.parent.parent.left
                        print('[RIGHT] UNCLE RED - {} '
                              'UNCLE KEY - {}'.format(uncle.red, uncle.key))
                        if uncle.red:
                            #  Case 1
                            node.parent.red = False
                            uncle.red = False
                            node.parent.parent.red = True
                            node = node.parent.parent
                            if node != self.root:
                                print('NODE RED - {} UNCLE RED - {} PARENT RED - '
                                      '{}'.format(
                                    colored(node.red, 'red',
                                            attrs=['reverse', 'blink']),
                                    colored(uncle.red, 'yellow',
                                            attrs=['reverse', 'blink']),
                                    colored(node.parent.red, 'yellow',
                                            attrs=['reverse', 'blink'])))
                            else:
                                print('NODE IS ROOT')
                        else:
                            if node == node.parent.left:
                                # This is Case 2
                                print('in TEST>>>>', node.key)
                                node = node.parent
                                print('AFTER TEST>>>>', node.key)
                                self.right_rotate(node)
                            # This is Case 3
                            node.parent.red = False
                            node.parent.parent.red = True
                            self.left_rotate(node.parent.parent)

                    except AttributeError:
                        print("No Uncle")
                        if node == node.parent.left:
                            # This is Case 2
                            print('in TEST>>>>', node.key)
                            node = node.parent
                            print('AFTER TEST>>>>', node.key)
                            self.right_rotate(node)
                        # This is Case 3
                        node.parent.red = False
                        node.parent.parent.red = True
                        self.left_rotate(node.parent.parent)
                        continue

            #self.root.red = False
        except AttributeError:
            print("\n\nTree BUILT")
        self.root.red = False

    def os_select(self, root, i):
        try:
            if root.left != None:
                r = root.left.size + 1
            else:
                r = 1
            if i == r:
                return root.key
            elif i < r:
                return self.os_select(root.left, i)
            else:
                return self.os_select(root.right, i - r)
        except AttributeError:
            print("ERROR! OUT OF RANGE!")

    def os_rank(self, tree, x):
        node = tree.search(x)
        if node.left != None:
            r = node.left.size + 1
        else:
            r = 1
        y = node
        while y != tree.root:
            if y == y.parent.right and y.parent.left != None:
                r = r + y.parent.left.size + 1
            elif y == y.parent.right and y.parent.left == None:
                r = r + 1
            y = y.parent
        return r

    # def real_delete_node(self, key): #trash
    #     current_node = self.search(key)
    #     if current_node is None:
    #         return
    #     if current_node.parent is None:
    #         if current_node == self.root:
    #             self.root = None
    #         return
    #     if current_node.parent.left == current_node:
    #         current_node.parent = None
    #     else:
    #         current_node.parent = None


def test_lr():
    first_tree = RBTree()
    first_tree.insert(11)
    first_tree.insert(2)
    first_tree.insert(14)
    first_tree.insert(15)
    first_tree.insert(1)
    first_tree.insert(7)
    first_tree.insert(5)
    first_tree.insert(8)
    first_tree.insert(4)

    first_tree.print_root()
    first_tree.root.left.print_node()
    first_tree.root.right.print_node()
    first_tree.search(2).right.print_node()
    first_tree.search(2).left.print_node()
    first_tree.search(14).right.print_node()
    first_tree.search(11).right.print_node()
    first_tree.search(11).left.print_node()
    first_tree.search(5).left.print_node()

def test_rr():
    first_tree = RBTree()
    first_tree.insert(11)
    first_tree.insert(2)
    first_tree.insert(20)
    first_tree.insert(1)
    first_tree.insert(16)
    first_tree.insert(22)
    first_tree.insert(15)
    first_tree.insert(17)
    first_tree.insert(18)

    first_tree.print_root()
    first_tree.root.left.print_node()
    first_tree.root.right.print_node()
    first_tree.search(11).right.print_node()
    first_tree.search(11).left.print_node()
    first_tree.search(20).right.print_node()
    first_tree.search(20).left.print_node()
    first_tree.search(2).left.print_node()
    first_tree.search(17).right.print_node()

def test_rot():
    first_tree = RBTree()
    first_tree.insert(16)
    #first_tree.insert(17)
    #first_tree.search(17).red = False
    first_tree.insert(11)
    first_tree.insert(8)
    #first_tree.insert(8)

    first_tree.print_root()
    first_tree.root.left.print_node()
    first_tree.root.right.print_node()

def test_rr_size():
    first_tree = RBTree()
    first_tree.insert(11)
    first_tree.insert(2)
    first_tree.insert(20)
    first_tree.insert(1)
    first_tree.insert(16)
    first_tree.insert(22)
    first_tree.insert(15)
    first_tree.insert(17)
    first_tree.insert(18)

    print("We FIND >> ", first_tree.os_select(first_tree.root, 6))

def test_rr_size2():
    first_tree = RBTree()
    first_tree.insert(11)
    first_tree.insert(2)
    first_tree.insert(20)
    first_tree.insert(1)
    first_tree.insert(16)
    first_tree.insert(22)
    first_tree.insert(15)
    first_tree.insert(17)
    first_tree.insert(18)

    print("We FIND >> ", first_tree.os_rank(first_tree, 17))

#test_rr_size2()

def main():
    first_tree = RBTree()
    print("Menu:")
    print("1. Insert")
    print("2. Search by index (i)")
    print("3. Search by key")
    print("4. Exit")
    print("------------------------------")
    while True:
        i = int(input("Select action: "))
        if i == 1:
            key = int(input("Enter a key: "))
            first_tree.insert(key)
        elif i == 2:
            index = int(input("Enter searching index: "))
            print("Key >> ", first_tree.os_select(first_tree.root, index))
        elif i == 3:
            value = int(input("Enter searching key: "))
            print("Index >> ", first_tree.os_rank(first_tree, value))
        elif i == 4:
            os.abort()
        else:
            print("ERROR! Wrong value.")

main()
