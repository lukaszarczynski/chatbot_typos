def edit_distance(word1, word2, insertion_cost=1, deletion_cost=1, substitution_cost=1, transposition_cost=1):
    word1 = ' ' + word1
    word2 = ' ' + word2
    length1 = len(word1)
    length2 = len(word2)
    A = [[0] * length2 for i in range(length1)]
    for i in range(length1):
        A[i][0] = i * deletion_cost
    for j in range(length2):
        A[0][j] = j * insertion_cost
    for i in range(1, length1):
        for j in range(1, length2):
            if word1[i] == word2[j]:
                A[i][j] = A[i-1][j-1]
            else:
                A[i][j] = min(A[i-1][j] + deletion_cost,
                              A[i][j-1] + insertion_cost,
                              A[i-1][j-1] + substitution_cost,)
                if i > 1 and j > 1 and word1[i] == word2[j-1] and word1[i-1] == word2[j]:
                    A[i][j] = min(A[i][j],
                                  A[i-2][j-2] + transposition_cost)
    return A[length1-1][length2-1]

if __name__ == "__main__":
    print("qwerty", "qwretz", edit_distance("qwerty", "qwretz"))
    w1, w2 = input("> "), input("> ")
    print(edit_distance(w1, w2, 1, 1, 1, 1))