class WordGame():
    def __init__(self,word):
        self.word = word.lower()
        self.lenght = len(word)
        self.attemps = 0
        self.max_attempts = 6
        self.over = False
        self.win = False
    def MakeGuess(self,guess):
        if self.over == True:
            return {"error":"Game is already over"}
        self.attemps += 1
        result = self.CheckLetters(guess.lower())
        if guess.lower() == self.word:
            self.win = True
            self.over = True
        elif self.attemps >= self.max_attempts:
            self.over = True
        
        response = {
            "result": result,
            "attemps":self.attemps,
            "remaining":self.max_attempts - self.attemps,
            "is_won": self.win,
            "is_over": self.over
        }

        if self.over and not self.win:
            response["answer"] = self.word

        return response
    def CheckLetters(self,guess):
        result = ["grey"] * len(guess)
        used_letters = [0]* len(self.word)
        word = self.word
        for i in range(len(guess)):
            if guess[i] == word[i]:
                result[i] = "green"
                used_letters[i] = 1
        for i in range(len(guess)):
            if result[i] != "green" and guess[i] in word:
                for j in range(len(guess)):
                    if word[j] == guess[i] and used_letters[j] == 0:
                        result[i] = "yellow" 
                        used_letters[j] =1
                        break    
        return result
