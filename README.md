# SneakyMath

SneakyMath is a Python game using [pygame](https://github.com/pygame/pygame).
It's a game of mental arithmetic with inspiration from the classic Snake.

## Installation

Get the executable on the [itch.io page](https://lysquid.itch.io/sneakymath) (Windows & Linux).
Alternatively, you can run the code after installing the librairies specified in the [requirements](requirements.txt).

## How to play

You control the snake and you can eat the blocks on the grid. But here is the twist : your snake growth is based on the number written on the block you eat. Additionally, there are two operation modes, addition and substraction, which is determined by the last operation block you ate. Depending of the operation mode you're in, your snake size will increase or decrease.

## Goal

Unlike the classic Snake, your goal is not to grow the biggest, but reached the exact size indicated as the goal on the top right of the screen. When you do so, parts of your snake turn to yellow to indicate they are full, and a new goal is generated, usually harder to reach ! All of this, while, of course, avoiding to get into the tail of your snake. At the end, your score is given by number of yellow parts your snake has.

## Context

This game was created for the [Prix Bernard Novelli 2020](http://www.tropheestangente.com/PBN.php) and received [acknowledgement](http://www.tropheestangente.com/palmares_2020.php).
