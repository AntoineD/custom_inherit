import pytest
from six import add_metaclass

from custom_inherit import DocInheritMeta


@pytest.mark.parametrize("style", ["numpy_with_merge", "numpy_napoleon_with_merge"])
def test_inheritance_numpy_with_merge_styles(style):
    @add_metaclass(DocInheritMeta(style=style))
    class Parent(object):
        """Parent.

        Notes
        -----
        Blah
        """

        def meth(self, x, y=None):
            """
            Raises
            ------
            NotImplementedError"""
            raise NotImplementedError

    class Child1(Parent):
        """Child1.

        Methods
        -------
        meth: does something
        """

        def meth(self, x, y=None):
            """Method description.

            Parameters
            ----------
            x: int
            y: float"""
            return 0

    class Child2(Parent):
        """Child 2.

        Methods
        -------
        blah : does not much
        """

        def blah(self):
            """Method blah2."""
            pass

    class GrandChild(Child1, Child2):
        """Grand Child."""

        def meth(self, x, y=None):
            """
            Parameters
            ----------
            x: int
            y: float"""
            return 0

        pass

    """
    Grand Child.
    
    Methods
    -------
    blah : does not much
    meth: does something
    
    Notes
    -----
    Blah"""
    assert (
        GrandChild.__doc__
        == "Grand Child.\n\nMethods\n-------\nblah : does not much\nmeth: does something\n\nNotes\n-----\nBlah"
    )

    """
    Method description.
    
    Parameters
    ----------
    x: int
    y: float
    
    Raises
    ------
    NotImplementedError"""
    assert (
        GrandChild.meth.__doc__
        == "Method description.\n\nParameters\n----------\nx: int\ny: float\n\nRaises\n------\nNotImplementedError"
    )


def test_inheritance_google_with_merge_style():
    @add_metaclass(DocInheritMeta(style="google_with_merge"))
    class A(object):
        """Testing A.

        Attributes:
            a :
                parameter a.
            b :
                parameter b.
            **c :
                parameter c.

        Returns:
            None

        Note:
            Hello
        """

        pass

    class B(A):
        """Testing B.

        Attributes:
            d :
                parameter d.
            e :
                parameter e.
            *f :
                parameter f.

        Return:
            None
        """

        pass

    class C(B):
        """Testing C.

        Attributes:
            a :
                priority description
                of a
            g :
                parameter g.
            h :
                parameter h.
            i :
                parameter i.

        Note:
            None
        """

        pass

    assert (
        C.__doc__
        == "Testing C.\n\nAttributes:\n    a :\n        priority description\n        of a\n    b :\n        parameter b.\n    d :\n        parameter d.\n    e :\n        parameter e.\n    g :\n        parameter g.\n    h :\n        parameter h.\n    i :\n        parameter i.\n    *f :\n        parameter f.\n    **c :\n        parameter c.\n\nReturns:\n    None\n\nNotes:\n    None"
    )
