#!/bin/env python3
#Author: Saurabh Pathak
'''edit distance metric'''
def edit_dist(s, i):
            r'''computes word based edit distance

                also provides a minimal sequence of operations insert (i), delete (d), and substitute (s) needed to convert the source string s into input string i.
                m stands for a matched word.

                >>> edit_dist('फिर भी बहुत से राज्य और शहर खुद इस दिशा में आगे बढ़ रहे हैं .', 'न्यू यॉर्क शहर भी इस दिशा में आगे बढ़ रहा है .')
                (9, 'ddddssmsmmmmmssm')
                >>> edit_dist('दीपावली को देखते हुए मिठाई की मांग बढ़ जाती है .', 'इसे देखते हुए घटिया व नकली मावे की बिक्री बढ़ जाती है .')
                (7, 'dsmmiiismsmmmm')
                >>> edit_dist('उन्होंने क्या किया है .', 'हमने क्या किया है .')
                (1, 'smmmm')

            '''
            s, i, ops = s.split(), i.split(), ''
            i_len, s_len = len(i), len(s)
            dp = [[(0,'') for k in range(i_len+1)] for j in range(s_len+1)]
            for j in range(1, s_len+1): dp[j][0] = (j, 'd'*j)
            for j in range(1, i_len+1): dp[0][j] = (j, 'i'*j)
            for j in range(1, s_len+1):
                for k in range(1, i_len+1):
                    if s[j-1] == i[k-1]: dp[j][k] = dp[j-1][k-1][0], dp[j-1][k-1][1] + 'm'
                    elif dp[j][k-1][0] < dp[j-1][k][0]:
                        if dp[j][k-1][0] < dp[j-1][k-1][0]: dp[j][k] = dp[j][k-1][0] + 1, dp[j][k-1][1] + 'i'
                        else: dp[j][k] = dp[j-1][k-1][0] + 1, dp[j-1][k-1][1] + 's'
                    elif dp[j-1][k][0] < dp[j-1][k-1][0]: dp[j][k] = dp[j-1][k][0] + 1, dp[j-1][k][1] + 'd'
                    else: dp[j][k] = dp[j-1][k-1][0] + 1, dp[j-1][k-1][1] + 's'
            return dp[s_len][i_len]

if __name__ == '__main__':
    import doctest
    doctest.run_docstring_examples(edit_dist, globals(), verbose=True)
