package game

import (
	"fmt"
	"HangmanGO/asciiart"
	"HangmanGO/words"
	"bufio"
	"os"
	"strings"
)

type Game struct {
	Word         string
	Guessed      map[rune]bool
	AttemptsLeft int
}

func NewGame() *Game {
	return &Game{
		Word:         words.RandomWord(),
		Guessed:      make(map[rune]bool),
		AttemptsLeft: asciiart.MaxStages() - 1,
	}
}

func (g *Game) Start() {
	for g.AttemptsLeft > 0 {
		g.Display()
		guess := g.PromptGuess()
		if !g.ProcessGuess(guess) {
			g.AttemptsLeft--
		}
		if g.Won() {
			fmt.Println("Congratulations! You won!")
			return
		}
	}
	asciiart.PrintStage(0)
	fmt.Printf("Game Over! The word was: %s\n", g.Word)
}

func (g *Game) Display() {
	asciiart.PrintStage(g.AttemptsLeft)
	for _, c := range g.Word {
		if g.Guessed[c] {
			fmt.Printf("%c ", c)
		} else {
			fmt.Print("_ ")
		}
	}
	fmt.Println()
}

func (g *Game) PromptGuess() rune {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Print("Enter a letter: ")
		input, _ := reader.ReadString('\n')
		input = strings.TrimSpace(input)
		if len(input) == 1 && input[0] >= 'a' && input[0] <= 'z' {
			return rune(input[0])
		}
		fmt.Println("Invalid input. Please enter a single lowercase letter.")
	}
}

func (g *Game) ProcessGuess(guess rune) bool {
	g.Guessed[guess] = true
	return strings.ContainsRune(g.Word, guess)
}

func (g *Game) Won() bool {
	for _, c := range g.Word {
		if !g.Guessed[c] {
			return false
		}
	}
	return true
}
