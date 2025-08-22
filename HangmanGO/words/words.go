package words

import (
	"math/rand"
	"time"
)

var wordList = []string{
	"gopher", "hangman", "python", "developer", "interface", "variable", "function", "package", "slice", "channel",
}

func RandomWord() string {
	rand.Seed(time.Now().UnixNano())
	return wordList[rand.Intn(len(wordList))]
}