package game

import (
	"bufio"
	"fmt"
	"os"
	"strings"
	"HangmanGO/profiles"
	"HangmanGO/asciiart"
)

func MainMenu() {
	profile := authenticateOrCreateProfile()
	balance := profile.Balance
	inventory := profile.Inventory
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println(asciiart.Banner)
		fmt.Printf("Profile: %s\n", profile.Name)
		fmt.Printf("jeffcoins: %d\n", balance)
		fmt.Println("1. Hangman")
		fmt.Println("2. Slots")
		fmt.Println("3. Shop")
		fmt.Println("4. Inventory")
		fmt.Println("5. Profile")
		fmt.Println("6. Exit")
		fmt.Print("Option: ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(strings.ToLower(choice))
		switch choice {
		case "6", "exit", "q":
			profile.Balance = balance
			profile.Inventory = inventory
			profiles.SaveProfile(profile)
			fmt.Println("Bye!")
			os.Exit(0)
		case "1":
			balance, inventory = PlayHangman(balance, inventory)
		case "2":
			fmt.Println(asciiart.SlotBanner)
			// TODO: Implement slot machine
			fmt.Println("Slot machine not implemented yet.")
		case "3":
			balance, inventory = Shop(balance, inventory)
		case "4":
			ShowInventory(inventory)
		case "5":
			profile.Balance = balance
			profile.Inventory = inventory
			profiles.SaveProfile(profile)
			profile = ProfileMenu(profile)
			balance = profile.Balance
			inventory = profile.Inventory
		default:
			fmt.Println("Invalid.")
		}
	}
}