package game

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"math/rand"
	"time"
	"HangmanGO/asciiart"
	"HangmanGO/words"
)

type Difficulty struct {
	Name     string
	Hints    int
	Excluded int
}

var Difficulties = []Difficulty{
	{"easy", 4, 5},
	{"medium", 2, 3},
	{"hard", 1, 2},
	{"super hard", 0, 1},
	{"mental", 0, 0},
}

func PlayHangman(balance int, inventory map[string]int) (int, map[string]int) {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println("Select difficulty: easy, medium, hard, super hard, mental")
		fmt.Print("Enter difficulty: ")
		difficultyInput, _ := reader.ReadString('\n')
		difficultyInput = strings.TrimSpace(strings.ToLower(difficultyInput))
		var settings *Difficulty
		for _, d := range Difficulties {
			if d.Name == difficultyInput {
				settings = &d
				break
			}
		}
		if settings == nil {
			fmt.Println("Invalid difficulty.")
			continue
		}
		fmt.Print("Enter '1' to input your own word, '2' for a random word: ")
		mode, _ := reader.ReadString('\n')
		mode = strings.TrimSpace(mode)
		var secretWord string
		if mode == "1" {
			fmt.Print("Enter your word: ")
			secretWord, _ = reader.ReadString('\n')
			secretWord = strings.TrimSpace(strings.ToLower(secretWord))
		} else {
			secretWord = words.RandomWord()
		}
		missed := make(map[rune]bool)
		correct := make(map[rune]bool)
		gameDone := false
		hintsLeft := settings.Hints
		hintsUsed := 0
		shieldActive := false
		alphabet := "abcdefghijklmnopqrstuvwxyz"
		lettersInWord := make(map[rune]bool)
		for _, c := range secretWord {
			lettersInWord[c] = true
		}
		var excludedLetters []rune
		if settings.Excluded > 0 {
			var notInWord []rune
			for _, c := range alphabet {
				if !lettersInWord[c] {
					notInWord = append(notInWord, c)
				}
			}
			rand.Seed(time.Now().UnixNano())
			perm := rand.Perm(len(notInWord))
			for i := 0; i < settings.Excluded && i < len(notInWord); i++ {
				excludedLetters = append(excludedLetters, notInWord[perm[i]])
			}
		}
		fmt.Printf("Excluded Letters: %s\n", string(excludedLetters))
		for {
			displayBoard(len(missed), missed, correct, secretWord)
			fmt.Printf("Hints left: %d\n", hintsLeft)
			fmt.Printf("Excluded Letters: %s\n", string(excludedLetters))
			fmt.Print("Enter a letter, 'hint', or 'inv': ")
			guess, _ := reader.ReadString('\n')
			guess = strings.TrimSpace(strings.ToLower(guess))
			if guess == "inv" {
				ShowInventory(inventory)
				continue
			}
			if guess == "hint" {
				if hintsLeft > 0 {
					var unrevealed []rune
					for c := range lettersInWord {
						if !correct[c] {
							unrevealed = append(unrevealed, c)
						}
					}
					if len(unrevealed) > 0 {
						hint := unrevealed[rand.Intn(len(unrevealed))]
						fmt.Printf("Hint: The word contains '%c'\n", hint)
						correct[hint] = true
						hintsLeft--
						hintsUsed++
						if allRevealed(lettersInWord, correct) {
							fmt.Printf("Yes! The secret word is '%s'! You win!\n", secretWord)
							fmt.Println("You earned jeffcoins!")
							balance += 10
							gameDone = true
						}
					} else {
						fmt.Println("No more letters to reveal!")
					}
				} else {
					fmt.Println("No hints left!")
				}
				continue
			}
			if len(guess) != 1 || guess[0] < 'a' || guess[0] > 'z' {
				fmt.Println("Please enter a single letter (a-z).")
				continue
			}
			c := rune(guess[0])
			if containsRune(excludedLetters, c) {
				fmt.Printf("The letter '%c' is excluded.\n", c)
				continue
			}
			if missed[c] || correct[c] {
				fmt.Println("Already guessed.")
				continue
			}
			if lettersInWord[c] {
				correct[c] = true
				if allRevealed(lettersInWord, correct) {
					fmt.Printf("Yes! The secret word is '%s'! You win!\n", secretWord)
					fmt.Println("You earned jeffcoins!")
					balance += 10
					gameDone = true
				}
			} else {
				missed[c] = true
				if len(missed) == asciiart.MaxStages()-1 {
					displayBoard(len(missed), missed, correct, secretWord)
					fmt.Printf("You have run out of guesses! The word was '%s'.\n", secretWord)
					gameDone = true
				}
			}
			if gameDone {
				fmt.Print("Play again? (y/n): ")
				again, _ := reader.ReadString('\n')
				again = strings.TrimSpace(strings.ToLower(again))
				if again == "y" {
					break
				} else {
					return balance, inventory
				}
			}
		}
	}
}

func displayBoard(missedCount int, missed, correct map[rune]bool, secretWord string) {
	asciiart.PrintStage(asciiart.MaxStages()-1-missedCount)
	fmt.Print("Missed letters: ")
	for c := range missed {
		fmt.Printf("%c ", c)
	}
	fmt.Println()
	for _, c := range secretWord {
		if correct[c] {
			fmt.Printf("%c ", c)
		} else {
			fmt.Print("_ ")
		}
	}
	fmt.Println()
}

func allRevealed(lettersInWord, correct map[rune]bool) bool {
	for c := range lettersInWord {
		if !correct[c] {
			return false
		}
	}
	return true
}

func containsRune(slice []rune, r rune) bool {
	for _, c := range slice {
		if c == r {
			return true
		}
	}
	return false
}
