package main

import (
	"fmt"
	"os"
	"HangmanGO/game"
)

func main() {
	fmt.Println("Welcome to Hangman!")
		game.MainMenu()
	os.Exit(0)
}
