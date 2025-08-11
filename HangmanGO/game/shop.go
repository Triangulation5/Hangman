package game

var ShopItems = []struct {
	Name  string
	Desc  string
	Cost  int
}{
	{"Shield", "Protects you from one wrong guess.", 30},
	{"Hint", "Buy an extra hint.", 20},
	{"Obvious Hint", "A very obvious hint.", 40},
	{"Super Juice", "Removes five letters that cannot be in the word.", 50},
	{"Peace Treaty", "Improves foreign relations.", 25},
	{"Rizz Juice", "Increases Mr. Hangman's rizz and cures depression.", 25},
}
