"""
CreativeContextTest.py

Tests
"""
from CreativeWand.Framework.CreativeContext.BaseCapability import BaseCapability
from CreativeWand.Framework.CreativeContext.BaseCreativeContext import BaseCreativeContext, ContextQuery


class TestCreativeContext(BaseCreativeContext):

    def get_generated_content(self) -> object:
        return []

    def execute_query(self, query: ContextQuery) -> object:
        return None


class TestCapability(BaseCapability):

    def __call__(self, x1, x2):
        return x1 + x2


if __name__ == '__main__':
    a = TestCreativeContext()

    a.register_capabilities(
        name="test",
        cap_object=TestCapability(a)
    )

    b = a.call_capabilities(name="test", x1=2, x2=3)

    print(b)
