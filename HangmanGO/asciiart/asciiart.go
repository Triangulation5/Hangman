package asciiart

import "fmt"

var stages = []string{
	`  +---+
  |   |
      |
      |
      |
      |
=========`,
	`  +---+
  |   |
  O   |
      |
      |
      |
=========`,
	`  +---+
  |   |
  O   |
  |   |
      |
      |
=========`,
	`  +---+
  |   |
  O   |
 /|   |
      |
      |
=========`,
	`  +---+
  |   |
  O   |
 /|\  |
      |
      |
=========`,
	`  +---+
  |   |
  O   |
 /|\  |
 /    |
      |
=========`,
	`  +---+
  |   |
  O   |
 /|\  |
 / \  |
      |
=========`,
}

func PrintStage(stage int) {
	if stage < 0 || stage >= len(stages) {
		stage = len(stages) - 1
	}
	fmt.Println(stages[len(stages)-1-stage])
}

func MaxStages() int {
	return len(stages)
}