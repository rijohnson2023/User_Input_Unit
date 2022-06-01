# Key take-Aways from PseudoCode2:

## Technical knowledge required

1. Ability to construct menus
- Menu 1
- Menu 2
- Menu 3
2. Ability to construct and edit dictionaries
1. Ability to work with sets
- eliminate subset from set
 - ability to add set to set



## Menu1: List[str:] UI

**Information trying to gather:** String from the dictionary keys, or it will be a new key

**Input:** Integer related to an option

***SubInput:*** String from the dictionary keys, or it will be a new key

**Data:** Most popular data - dict[str:int]

**Output:** a list of strings

    print(Please choose all %s inputs)
    Menu1: # Please select a %s
        1. No additional %s inputs 
        2. First most popular
        3. Second most popular
        4. Third most popular
        5. Other

    UI_%s_Section % (UI_Variable) = input(list:str)

## Menu2: String UI

**Information trying to gather:** String from the dictionary keys, or it will be a new key

**Input:** Integer related to an option

***SubInput:*** String from the dictionary keys, or it will be a new key

**Data:** Most popular data - dict[str:int]

**Output:** Returns the string

    Menu2: # Please select a %s
        1. Most Popular 
        2. Second most popular
        3. Third most popular
        4. Other

    UI_Basis_Set_Name = input(str:)

## Menu3: Decision Node

**Information trying to gather:** This is a decision node, trying to decide the protocol to proceed with

**Input:** Integer related to an option

**Data:** None

**Output:** Returns the Integer related to the option

    Menu3:
        1. Apply single basis set to all atoms in the files
        2. Apply basis set to each atom
        3. Apply basis sets to subsets of atoms

    Menu3Input = input(int:)

## Technical Solution to 2: Sort,Filter Dict[str:int]

    import random

    def findKthLargest(nums: list[int], k: int) -> int:
        """
        Quick Select: Returns the value kth largest value in an unsorted array
        """
        # choosing a random number in the origional array to begin sorting the data into 3 arrays
        pivot = random.choice(nums)
        # Left right and mid are all arrays
        left = [x for x in nums if x > pivot]
        mid = [x for x in nums if x == pivot]
        right = [x for x in nums if x < pivot]

        # Counting the number of elements in the left and mid array
        L,M = len(left), len(mid)

        if k <= L:   # if k, the kth largest int, is less than the length of the left array, then K is in the left array 
            return findKthLargest(left,k)
        elif k > (L+M): # if k, the kth largest int is greater than the length of the left and middle array, then k must be in the right array
            return findKthLargest(right, k-(L+M))
        else: # if K is not in the left or right array, then it in the middle array, and the middle array only contains the pivot number
            return mid[0]

    def kLargestElems(data: dict[str:int], k: int) -> dict :
        """
        Return a filtered dictionary that keeps the elements whose values are greater than the value of the kth element.
        """
        # Sort the dictionary in descending order
        sorted_dict = dict(sorted(data.items(),key=lambda elem: elem[1],reverse=True))
        # Identify the fourth highest value in the dict
        value = findKthLargest(list(data.values()),4)
        # Create a new dict by filter the arg dict for the top k elements based on their value
        newDict = dict(filter(lambda elem: elem[1] >= value,sorted_dict.items()))
        return newDict

    Example = {'why': 12, 'this': 11, 'at': 9, 'here': 5, 'is': 2, 'were' :14, 'Boo Ya Baby': 20, "Riley's coding skills": 50 +10, "Curtis's Python Skills": 100, "Dr. Patterson's skills" : 100}

    # If the value is the amount of times a user uses that keyword for the program, I want the 5 most used keywords
    k = 5
    print(kLargestElems(Example,k))
    print(kLargestElems(Example,k).keys())

Ensuring Valid User Input
1. User cannot repeat a keyword -> collect sets, not lists
   1. Don't want to use sets if don't have to, order could help/might matter later
2. 