# 2223-Groupe2-Snake

Tim DAFFNER - Charles DEZONS

## 1. Objectives
- Programming a video game that resembles the popular single player game "Snake" with pygame
- Implementing a two players version
- Implementing an AI for the user to play against
- Taking further inspiration from the game "Tron"

## 2. Features
- Snakes
  - are able to grow
  - moving over the screen on a grid
  - User steers them with buttons
  - Buttons for first and second user
- Apples (or other items) for the snakes to eat and grow
- Scoreboard
  - time or eaten items/length
- Start-screen:
  - Two or one player?
  - User names?
  - Highscore (single player)
- End-screen:
  - Highscore
  - Current score (single player)
  - Winner
- AI
  - choice of difficulty?
  - random?

## 3. Structure
### 3.1 Components
- screen
- snake(s)
- apples
- scoreboard
- Startscreen
- Endscreen

### 3.2 Schedule
1. Snake moving on the screen
  1. User steering snake
  2. Border rules
  3. Apples
2. Scoreboard
3. Start-screen
4. End-screen
5. Second snake
  1. Second user steering the snake
  2. Adapting scoreboard for two users
  3. Adapting start + end-screen if not done before
6. AI
  1. Implementing random AI
  2. Adapting startscreen for AI choice
  3. ??? smart AI with different levels
