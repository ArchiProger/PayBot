import sqlite3
import datetime


class DataBase:

    def __init__(self, dataBaseFile):
        self.connection = sqlite3.connect(dataBaseFile)
        self.cursor = self.connection.cursor()

    def userExists(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `users` WHERE `user_id` = ?", (user_id,)).fetchall()
            return(bool(len(result)))

    def getAllUsers(self):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `user_id` FROM `users`").fetchall()
            return result

    def addUser(self, user_id, date):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `users` (`user_id`, `date`) VALUES (?, ?)", (user_id, date,))

    def userDate(self, user_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT `date` FROM `users` WHERE `user_id` = ?", (user_id,)).fetchmany(1)

            dateArray = result[0][0].split('-')
            date = datetime.date(int(dateArray[0]), int(
                dateArray[1]), int(dateArray[2]))

            return date

    def setNewDate(self, user_id, date):
        with self.connection:
            result = self.cursor.execute(
                "UPDATE `users` SET `date` = ? WHERE `user_id` = ?", (date, user_id,))

    def deleteUser(self, user_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM `users` WHERE `user_id` = ?", (user_id,))

    def addCheck(self, user_id, bill_id):
        with self.connection:
            self.cursor.execute(
                "INSERT INTO `check` (`user_id`, `bill_id`) VALUES (?, ?)", (user_id, bill_id,))

    def getCheck(self, bill_id):
        with self.connection:
            result = self.cursor.execute(
                "SELECT * FROM `check` WHERE `bill_id` = ?", (bill_id,)).fetchmany(1)

            if not bool(len(result)):
                return False

            return result[0]

    def deleteCheck(self, bill_id):
        with self.connection:
            return self.cursor.execute(
                "DELETE FROM `check` WHERE `bill_id` = ?", (bill_id,))
