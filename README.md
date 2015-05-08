# setgame

A Python implementation of the card game Set

## Dependencies

This depends on **pygame**

In Linux environments, you can install pygame by typing:
```
sudo apt-get install python-pygame
```

For other operating systems, consult the pygame documentation.

## Features

### Homescreen

The game includes four buttons on the homescreen that allow selecting the game mode.  This can be either a timed game (easy, medium, or hard), or a non-timed game.  In a timed game, the user has a limited amount of time to find each set, indicated by the screen slowly filling with a different color.

It also has a button which will display statistics about game time, including number of games played, average time per game, and the best time per game.

### Game Play

During the game, you can click up to three cards to select a set.  If the clicked cards form a set, then they are replaced by three new cards from the deck, and your set counter increases.  If they are wrong, they are "unclicked" and an invisible incorrect set counter is updated.  At the end of the game, each incorrect set adds three seconds to the recorded time score.

The game does not automatically add three new cards to the board if there are no sets present, to emulate a real game.  There is a plus-three button and when clicked, it will check if there are sets on the board.  If there are none, it will add three new cards.  If a set exists, it will do nothing, but there is no penalty to the player.

The hint button will give the user a hint to finding the set by clicking one of the cards in the set.  Therefore, clicking the hint button three times will find an entire set for you.  If no sets exist, clicking the hint button will add three cards to the board for the player.  By default the program allows five hints per game.  

One "feature" is that the hint button disregards cards that have already been clicked by the user.  If there exists two sets on the board and the player has already clicked one or two cards in one of them, and then clicks the hint button, it is not guaranteed to select a card from the same set.  Additionally, if the player has already clicked a card that is not in a set, clicking the hint button will begin to select correct cards, but it will form an incorrect set in combination with the previously clicked cards.

The game displays how many cards are left in the deck, so that the player can use the hint button to their advantage.  For example, if they are nearly done with the deck and have all their hints remaining, it might be beneficial to use up the hints to improve their score.

There is also a pause button that will pause the game, hiding all cards so that the player cannot use the pause button to study the cards without using up time.  The game presents three options upon pausing: resume the game, restart a new game, or return to the home screen.

The game ends in a win if the player uses up the deck and finds all sets.  In a timed game, the player can also lose, when time runs out.  Upon a win condition, the game will display statistics, showing the time taken, number of incorrect sets, and an adjusted time score based on ading three seconds per incorrect set.  It also displays the best time as a comparison.  On a win or lose condition, the game displays the same three buttons as the pause screen.  Here, the resume button and the restart button both serve the same purpose to start a new game.

## Planned Future Features

- It would be cool to include in statistics the average or median time it takes the player to find a set
- Include a settings screen where the player can adjust values such as number of hints available or time deduction from wrong sets
- Write scores to a file saved locally so that the high score does not reset itself when the program is closed
- Perhaps create an online leaderboard where the best scores are automatically uploaded to a webserver
