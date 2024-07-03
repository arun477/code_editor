class Solution:
    def mergeAlternately(self, word1: str, word2: str) -> str:
        merged_str = ''
        n1, n2 = len(word1), len(word2)
        i = 0
        for ch1, ch2 in zip(word1, word2):
            merged_str += ch1
            merged_str += ch2
            i += 1
        if n1-1 > i-1:
            merged_str += word1[i:]
        if n2-1 > i-1:
            merged_str += word2[i:]
        return merged_str