#!/usr/bin/env python3
import random
from pypinyin import lazy_pinyin, Style
from enum import Enum

with open('idioms.txt', 'r') as f:
    idioms = [x.strip() for x in f.readlines()]

assert all(len(idiom) == 4 for idiom in idioms)


MAX_LEVEL = 512


class status(Enum):
    OK = 0
    MISS = 1
    WRONG = 2


def get_pinyin(guess):
    initials = lazy_pinyin(guess, style=Style.INITIALS, strict=False)
    finals_and_tones = lazy_pinyin(guess, style=Style.FINALS_TONE3, strict=False, neutral_tone_with_five=True)
    finals = [x[:-1] for x in finals_and_tones]
    tones = [x[-1].strip('5') for x in finals_and_tones]
    return initials, finals, tones


def validate(guess):
    if len(guess) != 4:
        return False
    if len(lazy_pinyin(guess, errors='ignore')) != 4:
        return False
    return True


def wrap_color(text, stat):
    CYAN = '\033[0;36m'
    BROWN = '\033[0;33m'
    NC = '\033[0m'
    if text:
        if stat == status.OK:
            return f'{CYAN}{text}{NC}'
        elif stat == status.MISS:
            return f'{BROWN}{text}{NC}'
    return text


def check_part(guess, answer):
    answer_chars = []
    for i in range(4):
        if guess[i] != answer[i]:
            answer_chars.append(answer[i])
    result = []
    for i in range(4):
        if guess[i] == answer[i]:
            result.append(status.OK)
        elif guess[i] in answer_chars:
            result.append(status.MISS)
            answer_chars.remove(guess[i])
        else:
            result.append(status.WRONG)
    return result


def check(guess, answer):
    guesspy = get_pinyin(guess)
    answerpy = get_pinyin(answer)
    py_results = [check_part(guesspy[i], answerpy[i]) for i in range(3)]
    for i in range(4):
        for j in range(3):
            print(wrap_color(guesspy[j][i], py_results[j][i]), end='')
        print(' ', end='')
    print()
    results = check_part(guess, answer)
    for i in range(4):
        print(wrap_color(guess[i], results[i]), end='')
    print()
    return guess == answer


def game(limit):
    for round in range(MAX_LEVEL):
        answer = random.choice(idioms)
        print(f'Round {1+round}')
        correct = False
        for _ in range(limit):
            while True:
                guess = input('> ')
                if validate(guess):
                    break
                print('Invalid guess')
            correct = check(guess, answer)
            if correct:
                break
        else:
            print('You failed...')
            return False

    return True


if __name__ == '__main__':
    print('Welcome to the "Handle" Game!')
    print('The game is the Chinese version of "Wordle".')
    print('You should guess a four-word idiom.')
    print('The rules are based on https://handle.antfu.me/')
    print()
    print('For whom feeling hard to solve wordle@TQLCTF in 4 rounds, try this version!')
    print()
    if game(4):
        print('Congratulations!')
        flag = open('flag').read()
        print(flag)
    else:
        print('Try harder next time!')
