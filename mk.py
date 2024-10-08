from random import choice

knb = ["scissors", "rock", "paper"]

user = input("введите scissors, rock, paper")

bot = choice(knb)

print(user, bot)

if bot == 'rock' and 'scissors':
    print("бот выиграл")