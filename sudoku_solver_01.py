import numpy as np


class Sudoku_solver:

    def __init__(self,prob):
        self.print_once = True
        self.game_end = False
        self.error_sign = False
        self.hit_either_or = False
        self.wrong_game  =False
        self.wrong_game_check(prob)
        self.main(prob)

    def solving(self,prob):
        self.switch_to_expert_on = True
        self.cor=[]
        for i in range(9):
            for j in range(9):
                if prob[i,j] == 0:
                    number = self.find_only_number(i,j,prob)
                    if number == -1:
                        self.error_sign = True
                        break
                        #print(f'*******error is detected! **********')
                    if not self.error_sign:
                        prob[i,j] = number
                        if self.hit_either_or:
                            self.cor.append([i,j])
                    if number != 0:   #if it found answers, we don't need to hit either_or
                        self.switch_to_expert_on = False


        if 0 not in prob:
            self.game_end = True

        return prob

    def find_only_number(self,i,j,prob):
        tbt = self.threebythree(i,j,prob)
        answer = -1
        for num in range(1,10):
            flag = 0
            if answer != 0:
                if num in prob[i,:]:
                    flag = 1
                if num in prob[:,j]:
                    flag = 1
                if num in tbt:
                    flag = 1
                if flag == 0:
                    if answer == -1:
                        answer = num
                    else:
                        answer = 0
        return answer

    def either_or(self, prob):
        self.switch_to_expert_on = False
        self.hit_either_or = True
        for i in range(9):
            for j in range(9):
                if prob[i,j] == 0:
                    numbers = self.find_two_number(i,j,prob)
                    if len(numbers) == 2:
                        numbers.append([i,j])
                        return numbers

    def guessing(self, numbers, prob, path):
        i,j = numbers[2]
        prob_temp1 = prob.copy()
        prob_temp1[i,j] =numbers[0]
        ## Let's say it is left side of tree
        self.main(prob_temp1 , 'left', path)

        if not self.game_end:
            ## Error is from above. We need to try right side This is to go back to parent
            self.error_sign = False
            prob[i,j] =numbers[1]
            self.main(prob ,'right', path)

    def find_two_number(self, i, j, prob):
        tbt = self.threebythree(i,j,prob)
        over_two = False
        numbers = []
        for num in range(1,10):
            flag = 0
            if not over_two:
                if num in prob[i,:]:
                    flag = 1

                if num in prob[:,j]:
                    flag = 1

                if num in tbt:
                    flag = 1

                if flag == 0:
                    numbers.append(num)

                if len(numbers) > 2:
                    over_two = True
                    numbers.clear()
        return numbers

    def threebythree(self, i, j, prob):
        x = i//3*3
        y = j//3*3
        return prob[x:x+3,y:y+3]

    def main(self, prob , direction ='' , path = []):
        path.append(direction)
        while not self.game_end:
            prob = self.solving(prob)

            ## If there is -1, it meams error. Exit a loop and go back or end game.
            if self.error_sign:
                self.game_end = False
                break
            ## If solving function didn't find a answer, I will return self.switch_to_expert_on as True.
            ## It means we need to guess a answer between 2 candidates
            if self.switch_to_expert_on:
                numbers = self.either_or(prob)
                if numbers is None:
                    self.wrong_game = True
                    break
                self.guessing(numbers, prob , path)

        ## If there is no zero in prob, Solving returns self.game_end as True.
        if  (not self.game_end and not self.hit_either_or) or self.wrong_game:
            print("Wrong problem")
            return

        if self.game_end and self.print_once:
            print(prob)
            print('game done')
            self.print_once = False

    def wrong_game_check(self,prob):
        prob_copy = prob.copy()
        for i in range(9):
            for j in range(9):
                if prob_copy[i,j] != 0:
                    number = prob_copy[i,j]
                    prob_copy[i,j] = 0
                    if number in prob_copy[i,:]:
                        self.wrong_game = True
                        self.game_end = True
                        return
                    if number in prob_copy[:,j]:
                        self.wrong_game = True
                        self.game_end = True
                        return
                    tbt = self.threebythree(i,j,prob_copy)
                    if number in tbt:
                        self.wrong_game = True
                        self.game_end = True
                        return
