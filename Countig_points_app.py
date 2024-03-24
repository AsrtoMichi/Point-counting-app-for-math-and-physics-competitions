#!/usr/bin/env python3
# -*- coding: utf-8 -*-


import tkinter as tk


class App(tk.Tk):

    def __init__(self, solutions, n_concurrens, vantage, derive):

        # starting main windows

        super().__init__()
        self.title("Competitors")
        self.geometry("800x300")

        # creations list solutions

        self.solutions = []
        for x in range(len(solutions)):
            partial = solutions[x]
            self.solutions.append([partial[0], partial[1], 0, 0, vantage])
        self.number_of_questions = len(self.solutions)

        # starting clock values

        self.timer_seconds = 7200
        self.timer_status = 0

        # creations list points squadre

        self.n_concurrens = n_concurrens
        self.derive = derive

        self.base_points = 220
        self.svantage = 10

        self.list_point = []
        for _ in range(self.n_concurrens):
            team_points = []
            for _ in range(self.number_of_questions):
                team_points.append([0, 0, 1])
            self.list_point.append(team_points)

        self.create_widgets()

        self.arbiter_window()

    def arbiter_window(self):

        # starting artiter's window
        self.arbiter_GUI = tk.Toplevel(self)
        self.arbiter_GUI.title("Arbiter")
        self.arbiter_GUI.geometry("500x200")
        self.arbiter_GUI.resizable(False, False)

        # craatition entry for data

        squadre_label = tk.Label(
            self.arbiter_GUI, text="Team number:")
        squadre_label.pack()
        self.squadre_entry = tk.Entry(self.arbiter_GUI)
        self.squadre_entry.pack()

        question_label = tk.Label(
            self.arbiter_GUI, text="Question number:")
        question_label.pack()
        self.question_entry = tk.Entry(self.arbiter_GUI)
        self.question_entry.pack()

        value_label = tk.Label(self.arbiter_GUI, text="Insert an answer:")
        value_label.pack()
        self.answer_entry = tk.Entry(self.arbiter_GUI)
        self.answer_entry.pack()

        tk.Button(self.arbiter_GUI, text="Submit",
                  command=self.submit_answer).pack()

        self.jolly_window()

        self.arbiter_GUI.mainloop()

    def jolly_window(self):

        # starting jolly window
        self.jolly_GUI = tk.Toplevel(self)
        self.jolly_GUI.title("Jolly")
        self.jolly_GUI.geometry("500x200")
        self.jolly_GUI.register(False, False)

        # craatition entry for data

        squadre_label = tk.Label(
            self.jolly_GUI, text="Team numbe:")
        squadre_label.pack()
        self.squadre_entry_jolly = tk.Entry(self.jolly_GUI)
        self.squadre_entry_jolly.pack()

        question_label = tk.Label(self.jolly_GUI, text="Question number:")
        question_label.pack()
        self.question_entry_jolly = tk.Entry(self.jolly_GUI)
        self.question_entry_jolly.pack()

        tk.Button(self.jolly_GUI, text="Submit",
                  command=self.submit_jolly).pack()

        self.jolly_GUI.mainloop()

    def submit_answer(self):

        try:
            # get values
            selected_team = int(self.squadre_entry.get())
            entered_question = int(self.question_entry.get())
            entered_answer = float(self.answer_entry.get())

            #clear entry

            self.squadre_entry.delete(0, tk.END)
            self.question_entry.delete(0, tk.END)
            self.answer_entry.delete(0, tk.END)

            # get specif n_error and golly staus

            point_team = self.list_point[selected_team-1]
            errors, status, jolly = point_team[entered_question-1]

            # gestion error for fisic competions

            xm, er, correct, incorrect, points = self.solutions[entered_question - 1]
            ea = (er)/100*xm
            ma, mi = xm + ea, xm-ea

            # gestion gived solutiions

            if self.timer_status == 1:

                # if correct

                if mi <= entered_answer <= ma:
                    correct += 1
                    status = 1

                # if wrong

                elif entered_answer <= mi or entered_answer >= ma:
                    if entered_answer is not None:
                        if status == 0:
                            errors += 1
                            incorrect += 1

            # inboxing solutions
            self.solutions[entered_question -
                           1] = [xm, er, correct, incorrect, points]

            # inboxig points
            point_team[entered_question-1] = [errors, status, jolly]
            self.list_point[selected_team-1] = point_team
            self.update_entry()

        except ValueError:
            self.squadre_entry.delete(0, tk.END)
            self.question_entry.delete(0, tk.END)
            self.answer_entry.delete(0, tk.END)

    def submit_jolly(self):

        try:
            # get values

            selected_team = int(self.squadre_entry_jolly.get())
            entered_question = int(self.question_entry_jolly.get())

            # clear entry

            self.squadre_entry_jolly.delete(0, tk.END)
            self.question_entry_jolly.delete(0, tk.END)

            # check timer staus

            if self.timer_status == 1 and self.timer_seconds > (6600):

                # check if other jolly are been given
                if sum(sotto_lista[2] for sotto_lista in self.list_point[selected_team-1]) == self.number_of_questions:
                    # adding jolly

                    squadre_points = self.list_point[selected_team-1]
                    answer_squadre_points = squadre_points[entered_question]
                    answer_squadre_points[2] = 2
                    squadre_points[entered_question] = answer_squadre_points
                    self.list_point[selected_team-1] = squadre_points
        except ValueError:
            self.squadre_entry_jolly.delete(0, tk.END)
            self.question_entry_jolly.delete(0, tk.END)

    def point_answer(self, question):
        if question < self.number_of_questions:
            answer_data = self.solutions[question]
            answer_data[4]+answer_data[1]*2

            return answer_data[4]+answer_data[3]*2

    def get_point_answer(self, squadre, question):
        if question < self.number_of_questions and squadre <= self.n_concurrens:
            points_squadre = self.list_point[squadre-1]
            answer_point = points_squadre[question]

            return (answer_point[1]*self.point_answer(question)-answer_point[0]*self.svantage)*answer_point[2]

    def get_total_points(self, squadre):
        if squadre <= self.n_concurrens:
            partial = []
            for x in range(self.number_of_questions):
                partial.append(self.get_point_answer(squadre, x))
            return sum(partial)+self.base_points

    def create_widgets(self):

        # cratin timer
        self.timer_label = tk.Label(self, text=f"Tempo rimasto: {self.timer_seconds // 3600:02}:{(
            self.timer_seconds % 3600) // 60:02}:{self.timer_seconds % 60:02}", font=("Helvetica", 18, "bold"))
        self.timer_label.pack()

        # cration start buttun
        self.start_button = tk.Button(
            self, text="Start", command=self.start_clock)
        self.start_button.pack()

        # creation point label

        self.points_label = tk.Frame(self)
        self.points_label.pack(pady=20)

        # creations row, coluns

        for x in range(self.n_concurrens+1):
            self.points_label.rowconfigure(x+1, weight=1)
            for y in range(self.number_of_questions):
                self.points_label.rowconfigure(y*2+2, weight=1)

        # creation label points value

        for x in range(self.n_concurrens+1):
            if x == 0:

                # value qustion

                for z in range(self.number_of_questions*2+2):
                    if z % 2 == 1 and z > 2:
                        value_label = tk.Entry(self.points_label, width=5)
                        value_label.insert(0, str(self.point_answer((z-2)//2)))
                        value_label.grid(column=z, row=0, sticky=tk.W)

            else:
                for y in range(self.number_of_questions*2+2):

                    # write Total
                    if y == 0:
                        tk.Label(self.points_label, text=f"Total {x}:", width=7).grid(
                            column=0, row=x, sticky=tk.W)

                    # write total points of a squadre
                    elif y == 1:
                        total_num = tk.Entry(self.points_label, width=5)
                        total_num.insert(
                            0, str(self.get_total_points(x)))
                        total_num.grid(column=1, row=x, sticky=tk.W)

                    else:
                        # write number of question
                        if y % 2 == 0:
                            tk.Label(self.points_label, text=f"{y//2}", width=5).grid(
                                column=y, row=x, sticky=tk.W)
                        else:
                            point = self.get_point_answer(x, (y-2)//2)
                            total_num = tk.Entry(self.points_label, width=5)
                            total_num.insert(0, str(point))
                            if point < 0:
                                total_num.configure(background="red")
                            elif point > 0:
                                total_num.configure(background="green")
                            else:
                                total_num.configure(background="white")
                            total_num.grid(column=y, row=x, sticky=tk.W)

    def update_entry(self):
        self.timer_label.destroy()
        self.start_button.destroy()
        self.points_label.destroy()
        self.create_widgets()

    def update_timer(self):
        self.timer_seconds -= 1
        self.timer_label.config(text=f"Tempo rimasto: {self.timer_seconds // 3600:02}:{
                                (self.timer_seconds % 3600) // 60:02}:{self.timer_seconds % 60:02}")

        if self.timer_seconds > 0:
            self.after(1000, self.update_timer)

            if self.timer_seconds % 5 == 0:
                self.update_entry()

            if self.timer_seconds % 5 == 0:
                for x in range(self.number_of_questions):
                    answer = self.solutions[x]
                    if answer[2] < self.derive:
                        answer[4] += 2
                    self.solutions[x] = answer

        else:
            self.timer_status = 0

    def start_clock(self):
        self.update_timer()
        self.timer_status = 1


if __name__ == "__main__":
    solutions = ((2, 1), (2, 1))
    squadre = 2
    vantage = 40
    derive = 3
    app = App(solutions, squadre, vantage, derive)

    app.mainloop()
