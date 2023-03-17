"""

Tag.py

A simple decorator that adds a "tag" to a class for future retrieval.

"""


def tag(tags):
    """
    Returns a wrapper that gives a class a "tag" class variable.
    Use it like this:

    @tag(["tag1","tag2","..."])

    ...

    print(obj.tag) #["tag1","tag2","..."]

    :param tags: tags to apply to the class.
    :return: class wrapper.
    """

    class Tag:
        def __init__(self, cls):
            self.cls = cls

        def __call__(self, *args, **kwargs):
            other = self.cls(*args, **kwargs)
            other.tag = tags
            return other

    return Tag

# Test code
# @tag(["test"])
# class a(): pass
#
#
# if __name__ == '__main__':
#     obj = a()
#     print(hasattr(obj,"tag"))
#     print("test" in obj.tag)
