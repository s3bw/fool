"""
Read comments in order of objects:
D -> A -> B -> C
"""


class A:

    def this(self):
        print("A")
        # If inherited call 'this' method on next object
        # from the left. (B.this())
        super().this()


class B:

    def this(self):
        print("B")
        # Calls 'this' on (C.this())
        super().this()


class C:

    def this(self):
        print("C")
        # If this class contained 'super' an error will raise
        # since there are no more classes in inheritance.
        # super().this()


class D(A, B, C):

    def this(self):
        # Call an inherited 'this' method on 1st inheritance
        # from the left. (A.this())
        super().this()


if __name__ == '__main__':
    d = D()
    d.this()
