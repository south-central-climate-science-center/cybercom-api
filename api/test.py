__author__ = 'mstacy'


def merge_sort(seq):
    """Accepts a mutable sequence. Utilizes merge_sort to sort in place, return
    a sorted sequence"""
    if len(seq) == 1:
        return seq
    else:
        # recursion: break sequence down into chunks of 1
        mid = len(seq) / 2
        left = merge_sort(seq[:mid])
        right = merge_sort(seq[mid:])

        i, j, k = 0, 0, 0  #i= left counter, j= right counter, k= master counter

        #run until left or right is out
        while i < len(left) and j < len(right):
            #if current left val is < current right val; assign to master list
            if left[i] < right[j]:
                seq[k] = left[i]
                i += 1
                k += 1
            #else assign right to master
            else:
                seq[k] = right[j]
                j += 1
                k += 1
        #handle remaining items in remaining list
            if i < j:
                remaining = left
            else:
                remaining =right
            if remaining == left:
                r = i
            else:
                r= j
        while r < len(remaining):
            seq[k] = remaining[r]
            r += 1
            k += 1
        return seq