import math
from copy import deepcopy
from random import uniform


class Tree:
    def __init__(self, startStep):
        self.firstStep = TreeNode(startStep)
        self.currentStep = self.firstStep

    def GetNextStep(self):
        """
        calculate all neigbours of this step then find step with minimum score. 
        if minimum score is lesser than currentStep then return new step with flag true,
         otherwise return current step with flag false.
        """
        flag = False
        minimumScore = self.currentStep.score
        neigbureSteps = self.currentStep.CreateNeighbours()
        for step in neigbureSteps:
            if step.score < minimumScore:
                flag = True
                minimumScore = step.score
                self.currentStep = step
        return self.currentStep, flag


class TreeNode:
    def __init__(self, groups):
        self.groups = groups
        self.score = self.CalculateScore()

    def CalculateScore(self):
        """
        calculate average of each group then calculate their variance as score.
        """
        averages = []
        for group in self.groups:
            sum = 0
            for number in group:
                sum += number
            averages.append(sum / len(group))
        sum = 0
        minAvg = min(averages)
        for avg in averages:
            sum += math.pow(avg - minAvg, 2)
        variance = sum / (len(averages) - 1)
        return variance

    def CreateNeighbours(self):
        """
        neigboure is a node that by swiping "one number" from a group with "another number" in diffrent group we can creat it using current node. 
        """
        neigbours = []
        for groupIndex in range(len(self.groups)):
            for numberIndex in range(len(self.groups[groupIndex])):
                for targetGroupIndex in range(groupIndex + 1, len(self.groups)):
                    for targetNumberIndex in range(len(self.groups[targetGroupIndex])):
                        neigbours.append(
                            TreeNode(
                                self.SwipeNumbers(
                                    deepcopy(self.groups),
                                    numberIndex,
                                    groupIndex,
                                    targetNumberIndex,
                                    targetGroupIndex,
                                )
                            )
                        )
        return neigbours

    def SwipeNumbers(
        self,
        groups,
        firstNumberIndex,
        firstGroupIndex,
        secondNumberIndex,
        secondGroupIndex,
    ):
        """
        swipe number in firstNumberIndex of firstGroupIndex to number in secondNumberIndex of secondGroupIndex.
        """
        temp = groups[firstGroupIndex][firstNumberIndex]
        groups[firstGroupIndex][firstNumberIndex] = groups[secondGroupIndex][
            secondNumberIndex
        ]
        groups[secondGroupIndex][secondNumberIndex] = temp
        return groups

    def PrintNode(self):
        """
        Print a group in each line.
        """
        for group in self.groups:
            print(group)


def CreateGroups(groupsCount, numbers):
    """
    Divide the "numbers" between "groupsCount" groupes.
    """
    numbers = ChangeOrder(numbers)
    groups = []
    for i in range(groupsCount):
        groups.append(numbers[0 : int(len(numbers) / (groupsCount - i))])
        numbers = numbers[int(len(numbers) / (groupsCount - i)) :]
    return groups


def ChangeOrder(itemsList=[]):
    """
    get a list and change order of its items randomly.
    """
    for i in range(len(itemsList)):
        itemsList.append(itemsList.pop(int(uniform(0, len(itemsList)))))
    return itemsList


if __name__ == "__main__":
    numbersCount = int(input("How many Numbers?"))
    groupsCount = int(input("How many Groups?"))
    numbers = list()
    inputNumbers = input("input Numbers and devide them with a ' '( space ). ").split(
        " "
    )
    for i in range(numbersCount):
        numbers.append(int(inputNumbers[i]))
    for i in range(max([numbersCount / 10, 5])):
        groups = CreateGroups(groupsCount, numbers)
        tree = Tree(groups)
        bestResult = tree.currentStep
        while True:
            step, flag = tree.GetNextStep()
            if not flag:
                if step.score < bestResult.score:
                    bestResult = step
                break
    bestResult.PrintNode()
