class Solution:
    def gcdOfStrings(self, str1: str, str2: str) -> str:
        m, n = len(str1), len(str2)
        if str1 + str2 != str2 + str1:
            return ''
        
        def gcd(a, b):
            while b:
                a, b = b, a%b
            return a

        return str1[:gcd(m, n)]