import strawberry

# @strawberry.type
# class TestOutput():
#     message:str


class TestQuery():
    @staticmethod
    def testQuery():
        return "This is working fine" 