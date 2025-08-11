package game

import (
	"bufio"
	"fmt"
	"os"
	"strconv"
	"strings"
	"HangmanGO/asciiart"
)

func Shop(balance int, inventory map[string]int) (int, map[string]int) {
	reader := bufio.NewReader(os.Stdin)
	for {
		fmt.Println(asciiart.MicrotransactionsBanner)
		fmt.Printf("jeffcoins: %d\n", balance)
		for idx, item := range ShopItems {
			fmt.Printf("%d. %s (%d) - %s\n", idx+1, item.Name, item.Cost, item.Desc)
		}
		fmt.Printf("%d. Exit\n", len(ShopItems)+1)
		fmt.Print("Buy # or exit: ")
		choice, _ := reader.ReadString('\n')
		choice = strings.TrimSpace(strings.ToLower(choice))
		if choice == strconv.Itoa(len(ShopItems)+1) || choice == "exit" || choice == "q" {
			break
		}
		idx, err := strconv.Atoi(choice)
		if err != nil || idx < 1 || idx > len(ShopItems) {
			fmt.Println("Invalid.")
			continue
		}
		item := ShopItems[idx-1]
		if balance >= item.Cost {
			balance -= item.Cost
			inventory[item.Name]++
			fmt.Printf("Bought %s. jeffcoins: %d\n", item.Name, balance)
		} else {
			fmt.Println("Not enough.")
		}
	}
	return balance, inventory
}
